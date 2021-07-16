import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
import chardet


def has_style(tag):
    return tag.has_attr('style')


def has_class(tag):
    return tag.has_attr('class')


def has_id(tag):
    return tag.has_attr('id')


def has_colspan(tag):
    return tag.has_attr('colspan')


def has_width(tag):
    return tag.has_attr('width')


def has_valign(tag):
    return tag.has_attr('valign')


def clean(soup):
    if soup.name == 'br' or soup.name == 'img' or soup.name == 'p' or soup.name == 'div':
        return
    try:
        ll = 0
        for j in soup.strings:
            ll += len(j.replace('\n', ''))
        if ll == 0:
            soup.decompose()
        else:
            for child in soup.children:
                clean(child)
    except Exception as e:
        pass


def dfs(soup, v):
    if soup.name == 'a' or soup.name == 'br':
        return
    try:
        lt = len(soup.get_text())
        ls = len(str(soup))
        a = soup.find_all('a')
        at = 0
        for j in a:
            at += len(j.get_text())
        lvt = lt - at
        v.append((soup, lt / ls * lvt))
        for child in soup.children:
            dfs(child, v)
    except Exception as e:
        pass


def extract(url, text_only=True, remove_img=True, save=False):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    for img in soup.findAll('img'):
        img['src'] = urljoin(url, img['src'])
    filt = ['script', 'noscript', 'style', 'embed', 'label', 'form', 'input', 'iframe', 'head', 'meta', 'link',
            'object', 'aside', 'channel']
    if remove_img:
        filt.append('img')
    for ff in filt:
        for i in soup.find_all(ff):
            i.decompose()
    for tag in soup.find_all(has_style):
        del tag['style']
    for tag in soup.find_all(has_class):
        del tag['class']
    for tag in soup.find_all(has_id):
        del tag['id']
    for tag in soup.find_all(has_width):
        del tag['width']
    for tag in soup.find_all(has_valign):
        del tag['valign']
    for tag in soup.find_all(has_colspan):
        del tag['colspan']
    clean(soup)
    LVT = len(soup.get_text())
    for i in soup.find_all('a'):
        LVT -= len(i.get_text())
    v = []
    dfs(soup, v)
    mij = 0
    for i in range(len(v)):
        if v[i][1] > v[mij][1]:
            mij = i
    if text_only:
        res = v[mij][0].get_text()
    else:
        res = str(v[mij][0])

    if save:
        basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dn = basedir + r"/output/"
        os.makedirs(dn, exist_ok=True)
        if text_only:
            with open(dn + '_out.txt', 'w', encoding='utf-8') as f:
                f.write(res)
        else:
            with open(dn + '_out.html', 'w', encoding='utf-8') as f:
                f.write(res)
    try:
        return res, v[mij][1] / LVT
    except ZeroDivisionError as e:
        return res, -1


# category extractor

def extract_category(url, save=False, title_on=True, text_on=True, href_on=True, img_on=True):
    try:
        par = urlparse(url)
        default_header = {'X-Requested-With': 'XMLHttpRequest', 'Referer': par[0] + '://' + par[1],
                          'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
                          'Host': par[1]}
        r = requests.get(url, headers=default_header, timeout=10).content
        encoding = chardet.detect(r)['encoding']
        if encoding in ['GB2312', 'GBK']:
            encoding = 'gb18030'
        soup = BeautifulSoup(r, 'html.parser', from_encoding=encoding)
        for ff in ['script', 'noscript', 'style']:
            for i in soup.find_all(ff):
                i.decompose()
        a = soup.find_all("a")
        img = soup.find_all("img")

        title = soup.title.string
        text = soup.get_text("")
        hrefs = []
        imgs = []
        for i in a:
            try:
                hrefs.append(i['href'])
            except Exception as e:
                pass
        for i in img:
            try:
                imgs.append(i['src'])
            except Exception as e:
                pass
        if save:
            save_cat(title, a, img, text)

        result = []
        if title_on:
            result.append(title)
        if text_on:
            result.append(text)
        if href_on:
            result.append(hrefs)
        if img_on:
            result.append(imgs)
        return result

    except Exception as e:
        print(e)
        return []


def save_cat(title, a, img, text):
    try:
        basedir = os.path.dirname(os.path.abspath(__file__))
        dn = basedir + r"/output/"
        os.makedirs(dn, exist_ok=True)
        with open(dn + "href.txt", "w", encoding='utf-8') as f:
            for i in a:
                try:
                    f.write(i['href']+'\n')
                except Exception as e:
                    pass
        with open(dn + "img.txt", "w", encoding='utf-8') as f:
            for i in img:
                try:
                    f.write(i['src']+'\n')
                except Exception as e:
                    pass
        with open(dn + "title.txt", "w", encoding='utf-8') as f:
            f.write(title)
        with open(dn + "text.txt", "w", encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        print(e)
