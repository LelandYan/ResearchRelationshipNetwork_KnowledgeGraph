# *_*coding:utf-8 *_*
from django.shortcuts import render
from toolkit.initialization import neo_con
from web.data4page import trans_search_ls2json
import os
import json
import re
import wordninja
import re
from collections import Counter
import wordninja


def words(text):
    return re.findall(r'\w+', text.lower())


Words = Counter(
    words(open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r"\toolkit\embedding\big.txt", 'r',
               encoding="utf8").read()))


def P(word, N=sum(Words.values())):
    return Words[word] / N


def correction(word):
    return max(candidates(word), key=P)


def candidates(word):
    return (known([word]) or known(editsl(word)) or known(editsl2(word)) or [word])


def known(words):
    return set(w for w in words if w in Words)


def editsl(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def editsl2(word):
    return (e2 for e1 in editsl(word) for e2 in editsl(e1))


pinyinLib = ['a', 'o', 'e', 'ai', 'ei', 'ao', 'ou', 'an', 'en', 'vn', 'van', 'ang', 'eng',
             'ba', 'bo', 'bi', 'bu', 'bai', 'bei', 'bao', 'bie', 'biao', 'ban', 'ben', 'bin', 'bian', 'bang', 'beng',
             'bing',
             'pa', 'po', 'pi', 'pu', 'pai', 'pei', 'pao', 'pou', 'pie', 'piao', 'pan', 'pen', 'pin', 'pian', 'pang',
             'peng', 'ping',
             'ma', 'mo', 'me', 'mi', 'mu', 'mai', 'mei', 'mao', 'mou', 'mie', 'miao', 'miu', 'man', 'men', 'min',
             'mian', 'mang', 'meng', 'ming',
             'fa', 'fo', 'fu', 'fei', 'nao', 'fou', 'fan', 'fen', 'fang', 'feng',
             'da', 'de', 'di', 'du', 'dai', 'dao', 'dou', 'dia', 'die', 'duo', 'diao', 'diu', 'dui', 'dan', 'den',
             'din', 'dian', 'duan', 'dun', 'dang', 'deng', 'ding', 'dong',
             'ta', 'te', 'ti', 'tu', 'tai', 'tao', 'tou', 'tie', 'tuo', 'tiao', 'tui', 'tan', 'tin', 'tian', 'tuan',
             'tun', 'tang', 'teng', 'ting', 'tong',
             'na', 'ne', 'ni', 'nu', 'nai', 'nei', 'nao', 'nou', 'nie', 'nuo', 'nve', 'niao', 'niu', 'nan', 'nen',
             'nin', 'nian', 'nuan', 'nun', 'nang', 'neng', 'ning', 'nong', 'niang',
             'la', 'le', 'li', 'lu', 'lai', 'lei', 'lao', 'lou', 'lie', 'luo', 'lve', 'liao', 'liu', 'lan', 'len',
             'lin', 'lian', 'luan', 'lun', 'lang', 'leng', 'ling', 'long', 'liang',
             'ga', 'ge', 'gu', 'gai', 'gei', 'gao', 'gou', 'gua', 'guo', 'guai', 'gui', 'gan', 'gen', 'guan', 'gun',
             'gang', 'geng', 'gong', 'guang',
             'ka', 'ke', 'ku', 'kai', 'kei', 'kao', 'kou', 'kua', 'kuo', 'kuai', 'kui', 'kan', 'ken', 'kuan', 'kun',
             'kang', 'keng', 'kong', 'kuang',
             'ha', 'he', 'hu', 'hai', 'hei', 'hao', 'hou', 'hua', 'huo', 'huai', 'hui', 'han', 'hen', 'huan', 'hun',
             'hang', 'heng', 'hong', 'huang',
             'ju', 'jiao', 'jiu', 'jian', 'juan', 'jun', 'jing', 'jiang', 'jiong', 'jia',
             'qi', 'qu', 'qia', 'qie', 'qiao', 'qiu', 'qin', 'qian', 'quan', 'qun', 'qing', 'qiang', 'qiong',
             'xi', 'xu', 'xia', 'xie', 'xiao', 'xiu', 'xin', 'xian', 'xuan', 'xun', 'xing', 'xiang', 'xiong',
             'zha', 'zhe', 'zhi', 'zhu', 'zhai', 'zhao', 'zhou', 'zhua', 'zhuo', 'zhuai', 'zhui', 'zhan', 'zhen',
             'zhuan', 'zhun', 'zhang', 'zheng', 'zhong', 'zhuang',
             'cha', 'che', 'chi', 'chu', 'chai', 'chao', 'chou', 'chuo', 'chuai', 'chui', 'chan', 'chen', 'chuan',
             'chun', 'chang', 'cheng', 'chong', 'chuang',
             'sha', 'she', 'shi', 'shu', 'shai', 'shao', 'shou', 'shua', 'shuo', 'shuai', 'shui', 'shan', 'shen',
             'shuan', 'shun', 'shang', 'sheng', 'shong', 'shuang',
             're', 'ri', 'ru', 'rao', 'rou', 'ruo', 'rui', 'ran', 'ren', 'ruan', 'run', 'rang', 'reng', 'rong',
             'za', 'ze', 'zi', 'zu', 'zai', 'zei', 'zao', 'zou', 'zuo', 'zui', 'zan', 'zen', 'zuan', 'zun', 'zang',
             'zeng', 'zong',
             'ca', 'ce', 'ci', 'cu', 'cai', 'cao', 'cou', 'cuo', 'cui', 'can', 'cen', 'cuan', 'cun', 'cang', 'ceng',
             'cong',
             'sa', 'se', 'si', 'su', 'sai', 'sao', 'sou', 'suo', 'sui', 'san', 'sen', 'suan', 'sun', 'sang', 'seng',
             'song',
             'ya', 'yo', 'ye', 'yi', 'yu', 'yao', 'you', 'yan', 'yin', 'yuan', 'yun', 'yang', 'ying', 'yong',
             'wo', 'wu', 'wai', 'wei', 'wan', 'wen', 'wang', 'weng', 'yong', 'er']


def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


def exact_Match(phrase, findword):
    b = r'(\s|^|$)'
    res = re.match(b + findword + b, phrase, flags=re.IGNORECASE)
    return bool(res)


def isAuthor(findword):
    if is_all_chinese(findword): return True
    file = open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r"\toolkit\fasttextModel\author.txt", 'r',
                encoding="utf8")
    for line in file:
        line = line.replace("\n", "")
        if exact_Match(line, findword) and len(line) == len(findword):
            file.close()
            return True
    file.close()
    return False


def isConcept(findword):
    file = open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r"\toolkit\fasttextModel\concept.txt",
                'r',
                encoding="utf8")
    for line in file:
        line = line.replace("\n", "")
        if exact_Match(line, findword) and len(line) == len(findword):
            file.close()
            return True
    file.close()
    return False


def is_pinyin(string):
    '''
    judge a string is a pinyin or a english word.
    pinyin_Lib comes from a txt file.
    '''
    string = string.lower()
    stringlen = len(string)
    max_len = 6
    result = []
    n = 0
    while n < stringlen:
        matched = 0
        temp_result = []
        for i in range(max_len, 0, -1):
            s = string[0:i]
            if s in pinyinLib:
                temp_result.append(string[:i])
                matched = i
                break
            if i == 1 and len(temp_result) == 0:
                return False
        result.extend(temp_result)
        string = string[matched:]
        n += matched
    return True


def search_list(request):
    nothing = {}
    if request.GET:
        entity = request.GET['user_text'].strip()
        search_flag = request.GET['search_flag'].strip()
        db = neo_con
        # 针对作者的搜索功能，这里实现的关于作者英文和拼音无空格分词的识别、中文作者名字的识别
        if search_flag == "author":
            print("This search is author")
            if is_pinyin(entity) and not is_all_chinese(entity):
                if " " not in entity:
                    res_tmp = wordninja.split(entity)
                    if len(res_tmp) > 2:
                        res = res_tmp[0] + res_tmp[1] + " " + res_tmp[2]
                    else:
                        res = res_tmp[0] + " " + res_tmp[1]
                    entity = res
            print(entity)
            tmp = db.get_search_ls_by_name(entity)

        elif search_flag == "studyfields":
            print("This search is study filed")
            if " " not in entity:
                res_tmp = wordninja.split(entity)
                if len(res_tmp) > 1:
                    res = correction(res_tmp[0])
                    for i in range(len(res_tmp)):
                        if i == 0:
                            continue
                        else:
                            res += (" " + correction(res_tmp[i]))
                else:
                    res = correction(res_tmp[0])
                entity = res
            else:
                entity = correction(entity)
            print(entity)
            tmp = db.get_search_ls_by_concept(entity)
        else:
            print("This search is key words")
            entity = correction(entity)
            res_tmp = wordninja.split(entity)
            print(res_tmp)
            if len(res_tmp) > 1:
                res = correction(res_tmp[0])
                for i in range(len(res_tmp)):
                    if i == 0:
                        continue
                    else:
                        res += (" " + correction(res_tmp[i]))
            else:
                res = correction(res_tmp[0])
            entity = res
            print(entity)
            tmp = db.get_search_ls_by_keys(entity)
        # print(tmp)
        entity_relation = json.loads(json.dumps(tmp, ensure_ascii=False))
        if len(entity_relation) == 0:
            nothing = {'title': '<h1>Sorry, Not Found in Database</h1>'}
            return render(request, 'searchList.html', {'nothing': json.dumps(nothing, ensure_ascii=False)})
        else:
            return render(request, 'searchList.html', trans_search_ls2json(entity_relation))
    return render(request, "searchList.html", {'nothing': nothing})
