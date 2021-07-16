# *_*coding:utf-8 *_*

import fasttext
import jieba
from toolkit.profileSpider import text_toolkit
import os


class Model:
    def __init__(self, gen_train_data=False):
        self.gen_train_data = gen_train_data
        basedir = os.path.dirname(os.path.abspath(__file__))
        self.classifier = fasttext.supervised(basedir + r"/train_data.txt", basedir + r"/model_file",
                                              label_prefix='__label__',
                                              epoch=100, dim=50, lr=0.1, loss="softmax")

    def single_predict(self, string, stopwords=None):
        if not stopwords:
            stopwords = ['年', '为', '于', '月', '日']
        texts = []
        segments = jieba.lcut(string)
        segments = filter(lambda x: x not in stopwords and x != ' ', segments)
        segments = filter(lambda x: x not in text_toolkit.match_symbol(x) and x not in text_toolkit.match_digit(x),
                          segments)
        texts.append(" ".join(segments))
        res = self.classifier.predict_proba(texts)
        pre, prob = list(res[0][0])[0], list(res[0][0])[1]
        if self.gen_train_data:
            self.gen_train_model_data(string, "__label__" + pre)
        # if '__label__' in pre[0][0]:
        #     label = pre[0][0][pre[0][0].index('__label__') + len('__label__'):]
        #     return label, float(prob)
        return pre, float(prob)

    def gen_train_model_data(self, string, label, stopwords=None):
        if not stopwords:
            stopwords = ['年', '为', '于', '月', '日']

        segments = jieba.lcut(string.strip('\n'))
        # segments = filter(lambda x: len(x) > 1, segments)
        segments = filter(lambda x: x not in stopwords, segments)
        segments = filter(lambda x: x not in text_toolkit.match_digit(x), segments)
        segments = filter(lambda x: x not in text_toolkit.match_date(x), segments)
        segments = filter(lambda x: x not in text_toolkit.match_symbol(x) and x != ' ', segments)
        basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dn = basedir + r"/output/"
        os.makedirs(dn, exist_ok=True)
        with open(dn + "for_train_archive.txt", "a+", encoding='utf-8') as f:
            f.write(label + " " + " ".join(segments) + '\n')

    def get_labels(self):
        return self.classifier.get_labels()
