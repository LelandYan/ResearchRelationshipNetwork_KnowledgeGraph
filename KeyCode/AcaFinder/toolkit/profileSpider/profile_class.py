from toolkit.profileSpider import html_extract as he
from toolkit.profileSpider import text_toolkit
from toolkit.profileSpider.ff_classifier import classifier as cf
import re


class Profile:
    def __init__(self, url, threshold=0.2, save=True, see=False, stopwords=None, pattern=None):
        self.url = url
        self.title = None
        self.text = None
        self.href = None
        self.img = None
        self.save = save
        self.threshold = threshold
        self.stopwords = stopwords
        self.see = see
        if not pattern:
            self.pattern = r'；|;|。|\[\d+\]|\|'
        else:
            self.pattern = pattern

        self.edu_dict = {}
        self.honor_dict = {}
        self.pub_dict = {}
        self.year_dict = {}
        self.confirmed_text_ls = []
        self.del_ls = []
        self.except_ls = []

    def get_pattern(self):
        return self.pattern

    def get_email(self):
        if self.text:
            try:
                return text_toolkit.match_email(self.text)[0]
            except IndexError:
                return ''
        else:
            print('[Class Profile]', 'Error')
            return 'Error'

    def get_homepage(self):
        if self.text:
            try:
                return text_toolkit.match_url(self.text)[0]
            except IndexError:
                return ''
        else:
            print('[Class Profile]', 'Error')
            return 'Error'

    def get_gender(self):
        if self.text:
            try:
                return text_toolkit.match_gender(self.text)[0]
            except IndexError:
                return ''
        else:
            print('[Class Profile]', 'Error')
            return 'Error'

    def get_edu_dict(self):
        if self.text:
            return self.edu_dict
        else:
            print('[Class Profile]', 'Error')
            return 'Error'

    def get_honor_dict(self):
        if self.text:
            return self.honor_dict
        else:
            print('[Class Profile]', 'Error')
            return 'Error'

    def get_pub_dict(self):
        if self.text:
            return self.pub_dict
        else:
            print('[Class Profile]', 'Error')
            return 'Error'

    def get_year_dict(self):
        if self.text:
            return self.year_dict
        else:
            print('[Class Profile]', 'Error')
            return 'Error'

    def get_confirmed_ls(self):
        if self.text:
            return self.confirmed_text_ls
        else:
            print('[Class Profile]', 'Error')
            return 'Error'

    def get_del_ls(self):
        if self.text:
            return self.del_ls
        else:
            print('[Class Profile]', 'Error')
            return 'Error'

    def get_except_ls(self):
        if self.text:
            return self.except_ls
        else:
            print('[Class Profile]', 'Error')
            return 'Error'

    def identify(self):
        try:
            self.title, self.text, self.href, self.img = he.extract_category(self.url, save=self.save)
            raw_text_ls = [re.split(self.pattern, i) for i in self.text.split('\n') if len(i) > 1]
            text_ls = []
            for ls in raw_text_ls:
                text_ls += [i.strip() for i in ls if len(i.strip()) > 1]

            text_len_ls = [len(i) for i in text_ls]
            ave_text_len = sum(text_len_ls) / len(text_len_ls)
            min_text_len = min(text_len_ls)
            max_text_len = max(text_len_ls)
            classifier = cf.Model(gen_train_data=self.save)
            for string in text_ls:
                if not (min(max_text_len, 5 * int(ave_text_len)) > len(string) > max(min_text_len,
                                                                                     int(ave_text_len / 5))):
                    self.del_ls.append(string)
                else:
                    self.confirmed_text_ls.append(string)

            pa = r'\d\.|，|、'
            for string in self.del_ls:
                if len(string) >= max(min_text_len, int(ave_text_len / 5)):
                    self.confirmed_text_ls += map(str.strip, re.split(pa, text_toolkit.remove_bracket(string)))
                    self.except_ls.append(string)
            for string in self.confirmed_text_ls:
                label, prob = classifier.single_predict(string, stopwords=self.stopwords)
                if prob > self.threshold:
                    year = text_toolkit.match_single_year(string)
                    if self.see:
                        print(label, prob, year, string)
                    if label == 'edu':
                        self.edu_dict[string] = {'prob': prob, 'year': year}
                        if year not in self.year_dict:
                            self.year_dict[year] = []
                            self.year_dict[year].append({'class': 'education', 'prob': prob, 'item': string})
                        else:
                            self.year_dict[year].append({'class': 'education', 'prob': prob, 'item': string})
                    elif label == 'honor':
                        self.honor_dict[string] = {'prob': prob, 'year': year}
                        if year not in self.year_dict:
                            self.year_dict[year] = []
                            self.year_dict[year].append({'class': 'honor', 'prob': prob, 'item': string})
                        else:
                            self.year_dict[year].append({'class': 'honor', 'prob': prob, 'item': string})
                    elif label == 'publication':
                        self.pub_dict[string] = {'prob': prob, 'year': year}
                        if year not in self.year_dict:
                            self.year_dict[year] = []
                            self.year_dict[year].append({'class': 'publication', 'prob': prob, 'item': string})
                        else:
                            self.year_dict[year].append({'class': 'publication', 'prob': prob, 'item': string})
                else:
                    self.del_ls.append(string)
            return True

        except Exception as e:
            print('[Class Profile]', e)
            return False
