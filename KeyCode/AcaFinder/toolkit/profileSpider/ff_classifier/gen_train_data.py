# *_*coding:utf-8 *_*

import jieba
import io
import text_toolkit

stopwords = ['安徽', '安徽省', '年', '为', '于', '月', '日']


def pre_text():
    edu_len_ls = []
    honor_len_ls = []
    pub_len_ls = []
    sentences = []
    with open("raw_data.txt", "r") as f:
        for line in f.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            label = line[line.index('__label__'): line.index(' ')]
            raw_string = line[line.index(' ') + 1:]
            segments = jieba.lcut(raw_string)
            # segments = filter(lambda x: len(x) > 1, segments)
            segments = filter(lambda x: x not in stopwords, segments)
            segments = filter(lambda x: x not in text_toolkit.match_digit(x), segments)
            segments = filter(lambda x: x not in text_toolkit.match_date(x), segments)
            segments = filter(lambda x: x not in text_toolkit.match_symbol(x) and x != ' ', segments)
            sentences.append(label + " " + " ".join(segments))
            print(sentences[-1])
            if label == '__label__honor':
                honor_len_ls.append(len(sentences[-1]) - len('__label__honor '))
            elif label == '__label__publication':
                pub_len_ls.append(len(sentences[-1]) - len('__label__publication '))
            elif label == '__label__edu':
                edu_len_ls.append(len(sentences[-1]) - len('__label__edu '))

    # with open("train_data2.txt", "a+") as f:
    #     for item in sentences:
    #        f.write(item + '\n')
    #return sentences
    print(honor_len_ls)
    print(min(edu_len_ls), max(edu_len_ls), sum(edu_len_ls)/len(edu_len_ls))
    print(min(honor_len_ls), max(honor_len_ls), sum(honor_len_ls)/len(honor_len_ls))
    print(min(pub_len_ls), max(pub_len_ls), sum(pub_len_ls)/len(pub_len_ls))


if __name__ == '__main__':
    pre_text()
