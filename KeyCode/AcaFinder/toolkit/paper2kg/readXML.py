# *_*coding:utf-8 *_*

from xml.dom.minidom import parse
from toolkit.paper2kg.toolkit.pdf_parser import Parser
import os
import time
import nltk
import re

'''
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
'''


class PaperXML:
    def __init__(self, file_path, base_dir):
        """
        :param file_path: XML file path rather than PDF
        """
        self.base_dir = base_dir
        self.dom = parse(file_path)
        self.data = self.dom.documentElement
        self.paper_title = self.get_paper_title()
        self.section_dict = self.get_secs()

        self.ref_dict = self.get_rf()
        self.paper_aff_dict = self.get_affiliation()
        self.paper_year = self.get_paper_year()
        self.author_dict = self.get_author()

    def get_paper_title(self):
        try:
            if self.paper_title:
                return self.paper_title
        except AttributeError:
            return self.data.getElementsByTagName('article-title')[0].childNodes[0].nodeValue

    def get_paper_year(self):
        try:
            if self.paper_year:
                return self.paper_year
        except AttributeError:
            try:
                return self.data.getElementsByTagName('article-meta')[0].getElementsByTagName('year')[0].childNodes[
                    0].nodeValue
            except IndexError as e:
                return '0000'

    def get_affiliation(self):
        try:
            if self.paper_aff_dict:
                return self.paper_aff_dict
        except AttributeError:
            data_range = self.data.getElementsByTagName('article-meta')[0].getElementsByTagName('contrib-group')[0]
            aff_ls = data_range.getElementsByTagName('aff')
            aff_dict = {}
            for item in aff_ls:
                aff_id = item.getElementsByTagName('label')[0].childNodes[0].nodeValue
                aff_name = item.getElementsByTagName('institution')[0].childNodes[0].nodeValue
                aff_dict[aff_id] = {'affiliationName': aff_name}
                if item.getElementsByTagName('addr-line'):
                    address = item.getElementsByTagName('addr-line')[0].childNodes[0].nodeValue
                    aff_dict[aff_id]['address'] = address
                if item.getElementsByTagName('country'):
                    country = item.getElementsByTagName('country')[0].childNodes[0].nodeValue
                    aff_dict[aff_id]['country'] = country
            return aff_dict

    def get_author(self):
        try:
            if self.author_dict:
                return self.author_dict
        except AttributeError:
            data_range = self.data.getElementsByTagName('article-meta')[0].getElementsByTagName('contrib-group')[0]
            author_ls = data_range.getElementsByTagName('contrib')
            author_dict = {}
            author_rank = 0
            for item in author_ls:
                author_name = item.getElementsByTagName('string-name')[0].childNodes[0].nodeValue
                if item.getElementsByTagName('email'):
                    email = item.getElementsByTagName('email')[0].childNodes[0].nodeValue
                    author_dict[str(author_rank)] = {'authorName': author_name, 'email': email}
                else:
                    author_dict[str(author_rank)] = {'authorName': author_name}
                affiliation = []
                xref_ls = item.getElementsByTagName('xref')
                for xref_item in xref_ls:
                    xref_val = xref_item.getAttribute('ref-type')
                    if xref_val == 'aff':
                        affiliation.append(xref_item.childNodes[0].nodeValue)
                author_dict[str(author_rank)]['affiliation'] = affiliation
                author_rank += 1
            return author_dict

    def get_rf(self):
        try:
            if self.ref_dict:
                return self.ref_dict
        except AttributeError:
            ref_ls = self.data.getElementsByTagName('ref')
            rf_rank = 0
            ref_dict = {}
            for item in ref_ls:
                try:
                    article_title = item.getElementsByTagName('mixed-citation')[0]. \
                        getElementsByTagName('article-title')[0].childNodes[0].nodeValue
                    article_year = item.getElementsByTagName('year')[0].childNodes[0].nodeValue
                    ref_dict[str(rf_rank)] = {'paperName': article_title, 'year': article_year}
                    rf_rank += 1
                except IndexError as e:
                    print('PaperXML.get_rf Error:', e)
            return ref_dict

    def get_secs(self):
        try:
            if self.section_dict:
                return self.section_dict
        except AttributeError:
            secs = self.data.getElementsByTagName('sec')
            section_dict = {}
            all_sec_text = ''
            sec_rank = 0
            for item in secs:
                sec_title = item.getElementsByTagName('title')[0].childNodes[0].nodeValue
                p_ls = item.getElementsByTagName('p')
                p_text = ''
                for p in p_ls:
                    p_val = str(p.childNodes[0].nodeValue).replace('\n', ' ').strip()
                    p_val = re.findall('[a-zA-Z0-9\s+\t\.\!\/_,$%^*(+\"\'\-]+', p_val, re.S)
                    p_val = "".join(p_val)
                    all_sec_text += p_val + '\n'
                    p_text += p_val + ' '
                if sec_title == '-':
                    sec_title = 'abstract'
                section_dict[str(sec_rank)] = {'sec_title': sec_title}
                section_dict[str(sec_rank)]['text'] = p_text
                sec_rank += 1
            with open(self.base_dir + r'/all_sec_text.txt', 'w+',encoding="utf8") as f:
                f.write(all_sec_text)
            return section_dict

    def get_sec_id4NRE(self, string):
        res = ''
        for key in self.section_dict:
            if string in self.section_dict[key]['text']:
                res = key
        return res

    def section_NRE(self):
        cmd = 'java -Xmx512m -jar toolkit/Ollie/ollie-app-latest.jar ' \
              '--malt-model toolkit/Ollie/engmalt.linear-1.7.mco -s all_sec_text.txt'
        res = os.popen(cmd)
        info = res.readlines()
        sentence = ''
        entity_rel = {}
        for line in info:
            line = line.strip('\r\n')
            if len(line) > 2 and ': (' not in line:
                sentence = line
                entity_rel[sentence] = []
            elif ': (' in line:
                confidence, triple = line.split(': ')
                if sentence != '':
                    entity_rel[sentence].append({'confidence': confidence, 'triple': triple})
            elif len(line) == 0:
                sentence = ''
        return entity_rel

    def paper2kg_d3js_basicInfo(self):
        d3js_data = []
        tri = {'source': self.paper_title, 'target': self.paper_year, 'rela': 'year', 'type': 'resolved'}
        d3js_data.append(tri)
        for key in self.ref_dict:
            tri = {'source': self.paper_title, 'target': self.ref_dict[key]['paperName'],
                   'rela': 'cites', 'type': 'resolved'}
            d3js_data.append(tri)
        for key in self.author_dict:
            tri = {'source': self.paper_title, 'target': self.author_dict[key]['authorName'],
                   'rela': 'belong to', 'type': 'resolved'}
            d3js_data.append(tri)
            if 'affiliation' in self.author_dict[key]:
                for aff_id in self.author_dict[key]['affiliation']:
                    tri = {'source': self.author_dict[key]['authorName'],
                           'target': self.paper_aff_dict[aff_id]['affiliationName'],
                           'rela': 'work in', 'type': 'resolved'}
                    d3js_data.append(tri)
                    if 'address' in self.paper_aff_dict[aff_id]:
                        tri = {'source': self.paper_aff_dict[aff_id]['affiliationName'],
                               'target': self.paper_aff_dict[aff_id]['address'],
                               'rela': 'is located in', 'type': 'resolved'}
                        d3js_data.append(tri)
                    if 'country' in self.paper_aff_dict[aff_id]:
                        tri = {'source': self.paper_aff_dict[aff_id]['affiliationName'],
                               'target': self.paper_aff_dict[aff_id]['country'],
                               'rela': 'belong to', 'type': 'resolved'}
                        d3js_data.append(tri)
        for key in self.section_dict:
            tri = {'source': self.paper_title, 'target': self.section_dict[key]['sec_title'],
                   'rela': 'has', 'type': 'resolved'}
            d3js_data.append(tri)
        with open(self.base_dir + r'/paper_d3js_data.txt', 'w+',encoding="utf8") as f:
            f.write(str(d3js_data))

    def paper2kg_d3js(self, confidence, max_entity_len, fine_grain=True, tags=None):
        if tags is None:
            tags = ['NNP', 'NNPS']
        entity_rel = self.section_NRE()
        d3js_data = []

        # 4 paper->section
        for key in self.section_dict:
            tri = {'source': self.paper_title, 'target': self.section_dict[key]['sec_title'],
                   'rela': 'has', 'type': 'resolved'}
            d3js_data.append(tri)

        # 4 section->entity and entity->entity
        for _key in entity_rel:
            # print('---------------------------------')
            # print(_key)

            candidate_words = []
            for item in nltk.pos_tag(nltk.word_tokenize(_key)):
                if item[1] in tags:
                    candidate_words.append(item[0])
            # print(candidate_words)

            # print(self.get_sec_id4NRE(_key))
            # print(entity_rel[_key])
            for item in entity_rel[_key]:
                if float(item['confidence']) < confidence:
                    continue
                triple = item['triple'].strip('(').strip(')').split('; ')

                if fine_grain:
                    words = triple[0].split()
                    words.extend(triple[2].split())
                    flag = False
                    for w in words:
                        if w in candidate_words:
                            flag = True
                            break
                    if not flag:
                        break
                else:
                    words = triple[0].split()
                    words2 = triple[2].split()
                    flag = False
                    for w in words:
                        if w in candidate_words:
                            flag = True
                            break
                    if not flag:
                        break
                    flag = False
                    for w in words2:
                        if w in candidate_words:
                            flag = True
                            break
                    if not flag:
                        break

                if len(triple) == 3:
                    if len(triple[0].split()) <= max_entity_len and len(triple[2].split()) <= max_entity_len:
                        section_id = str(self.get_sec_id4NRE(_key))
                        tri = {'source': triple[0], 'target': triple[2], 'rela': triple[1], 'type': 'resolved'}
                        d3js_data.append(tri)
                        try:
                            tri = {'source': triple[0], 'target': self.section_dict[section_id]['sec_title'],
                                   'rela': 'exists in', 'type': 'resolved'}
                            d3js_data.append(tri)
                            tri = {'source': triple[2], 'target': self.section_dict[section_id]['sec_title'],
                                   'rela': 'exists in', 'type': 'resolved'}
                            d3js_data.append(tri)
                        except KeyError as e:
                            print(e, triple[0], triple[2])

        with open(self.base_dir + r'/section_d3js_data.txt', 'w+') as f:
            f.write(str(d3js_data))

    def paper2kg_api(self, confidence, max_entity_len, fine_grain=True, tags=None):
        if tags is None:
            tags = ['NNP', 'NNPS', 'NNS']
        entity_rel = self.section_NRE()
        data4api = {}
        triple_id = 0

        # 4 paper->section
        for key in self.section_dict:
            tri = {'source': self.paper_title, 'target': self.section_dict[key]['sec_title'], 'rela': 'has',
                   'confidence': '1.0',
                   'ext_info': {'type': 'paper2section', 'section_id': key}}
            data4api[str(triple_id)] = tri
            triple_id += 1

        # 4 section->entity and entity->entity
        for _key in entity_rel:
            # print('---------------------------------')
            # print(_key)
            candidate_words = []
            for item in nltk.pos_tag(nltk.word_tokenize(_key)):
                # print(item)
                if item[1] in tags:
                    candidate_words.append(item[0])
            # print(self.get_sec_id4NER(_key))
            # print(entity_rel[_key])
            for item in entity_rel[_key]:
                if float(item['confidence']) < confidence:
                    continue
                triple = item['triple'].strip('(').strip(')').split('; ')

                if fine_grain:
                    words = triple[0].split()
                    words.extend(triple[2].split())
                    flag = False
                    for w in words:
                        if w in candidate_words:
                            flag = True
                            break
                    if not flag:
                        break
                else:
                    words = triple[0].split()
                    words2 = triple[2].split()
                    flag = False
                    for w in words:
                        if w in candidate_words:
                            flag = True
                            break
                    if not flag:
                        break
                    flag = False
                    for w in words2:
                        if w in candidate_words:
                            flag = True
                            break
                    if not flag:
                        break

                if len(triple) == 3:
                    if len(triple[0].split()) <= max_entity_len and len(triple[2].split()) <= max_entity_len and len(
                            triple[0].split()[0]) >= 2:
                        # print(triple)
                        section_id = str(self.get_sec_id4NRE(_key))
                        tri = {'source': triple[0], 'target': triple[2], 'rela': triple[1],
                               'confidence': item['confidence'],
                               'ext_info': {'type': 'entity2entity', 'section_id': section_id}}
                        data4api[str(triple_id)] = tri
                        triple_id += 1
                        try:
                            tri = {'source': triple[0], 'target': self.section_dict[section_id]['sec_title'],
                                   'rela': 'exists in',
                                   'confidence': '1.0',
                                   'ext_info': {'type': 'section2entity', 'section_id': section_id}}
                            data4api[str(triple_id)] = tri
                            triple_id += 1

                            tri = {'source': triple[2], 'target': self.section_dict[section_id]['sec_title'],
                                   'rela': 'exists in',
                                   'confidence': '1.0',
                                   'ext_info': {'type': 'section2entity', 'section_id': section_id}}
                            data4api[str(triple_id)] = tri
                            triple_id += 1
                        except KeyError as e:
                            pass
                            # print(e, triple[0], triple[2])

        return data4api


# if __name__ == '__main__':
#     start = time.time()
#     parser = Parser('cermine')
#     parser.parse('text', 'ELG.pdf', 'output', 0)
#     paper = PaperXML('output/ELG.cermine.xml')
#     paper.paper2kg_d3js(confidence=0.6, max_entity_len=4, fine_grain=False)
#     print(time.time() - start)
