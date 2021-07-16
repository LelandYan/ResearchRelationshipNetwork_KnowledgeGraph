import re


def match_digit(text):
    """
    :param text: str
    :return: list
    """
    return re.findall(r"\d+", text)


def match_symbol(text):
    """
        :param text: str
        :return: list
    """
    return re.findall(r'[^\w\s]', text)


def match_email(text):
    """
    :param text: str
    :return: list
    """
    return re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)


# Bugs
def match_date(text):
    """
    :param text: str
    :return: list
    """
    r1 = re.findall(r"(\d{4}[-/._年]\d{1,2}[-/._月]\d{1,2}[日]*)", text)
    if not r1:
        r1 = re.findall(r"(\d{4}[-/._年]\d{1,2})", text)
        if not r1:
            r1 = re.findall(r"(\d{4})", text)
    return r1


def match_single_year(text):
    """
    :param text: string
    :return: string
    """
    ls = re.findall(r"(?:19|20)\d{2}", text)
    if len(ls) > 0:
        return ls[0]
    else:
        return ''


def match_url(text):
    """
    :param text: str
    :return: list
    """
    urls = re.findall(r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)|([a-zA-Z]+.\w+\.+[a-zA-Z0-9\/_]+)",text)
    urls = list(sum(urls, ()))
    return [x for x in urls if x != '' and '@' not in x and ' ' not in x]


def match_gender(text):
    """
    :param text: string
    :return: string
    """
    text = text.lower()
    if 'female' in text or '女' in text:
        return 'female'
    if 'male' in text or '男' in text:
        return 'male'
    return ''


def remove_bracket(text):
    """
    :param text: string
    :return: string
    """
    return re.sub(r"（.*?）|{.*?}|\[.*?\]|【.*?】|\(.*?\)", "", text)


if __name__ == '__main__':
    print(match_single_year('vfdsdas23r43202932frefre32chnsjkad'))

