import re


def remove_tags(text):
    regex = re.compile('\r\n|<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    return re.sub(regex, '', text)


def remove_unnecessary_symbols(text):
    regex = re.compile('[ ,:()•\\[\\]-]')
    return re.sub(regex, '', text)


def remove_ws(text):
    elements = str(text).split(';')
    for elem in elements:
        if elem != '':
            if elem[0] == ' ':
                elem = elem[1:]
    return ';'.join(elements)

