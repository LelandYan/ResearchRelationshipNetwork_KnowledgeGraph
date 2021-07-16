# *_*coding:utf-8 *_*

import os
import nltk

'''
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
'''


def section_NRE(text):
    with open('text_tmp.txt', 'w+') as f:
        f.write(text)
    cmd = 'java -Xmx512m -jar toolkit/Ollie/ollie-app-latest.jar ' \
          '--malt-model toolkit/Ollie/engmalt.linear-1.7.mco -s text_tmp.txt'
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


def text2kg_api(text, confidence, max_entity_len, fine_grain=True, tags=None):
    if tags is None:
        tags = ['NNP', 'NNPS']
    entity_rel = section_NRE(text)
    data4api = {}
    triple_id = 0

    # 4 entity->entity
    for _key in entity_rel:
        # print('---------------------------------')
        # print(_key)
        candidate_words = []
        for item in nltk.pos_tag(nltk.word_tokenize(_key)):
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
                if not flag:
                    break
            else:
                words = triple[0].split()
                words2 = triple[2].split()
                flag = False
                for w in words:
                    if w in candidate_words:
                        flag = True
                if not flag:
                    break
                flag = False
                for w in words2:
                    if w in candidate_words:
                        flag = True
                if not flag:
                    break

            if len(triple) == 3:
                if len(triple[0].split()) <= max_entity_len and len(triple[2].split()) <= max_entity_len:
                    tri = {'source': triple[0], 'target': triple[2], 'rela': triple[1],
                           'confidence': item['confidence'],
                           'ext_info': {'type': 'entity2entity'}}
                    data4api[str(triple_id)] = tri
                    triple_id += 1
    return data4api


if __name__ == '__main__':
    print(text2kg_api(text="AceMap is based on MAG.", confidence=0.1, max_entity_len=4, fine_grain=True))
