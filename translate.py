# Задача №1
# Необходимо расширить функцию переводчика так, чтобы она принимала следующие параметры:
#
# Путь к файлу с текстом;
# Путь к файлу с результатом;
# Язык с которого перевести;
# Язык на который перевести (по-умолчанию русский).
# У вас есть 3 файла (DE.txt, ES.txt, FR.txt) с новостями на 3 языках: французском, испанском, немецком.
# Функция должна взять каждый файл с текстом, перевести его на русский и сохранить результат в новом файле.


# TODO RULE:
#  1) input file in folder "source"
#  2) input file name "LN.txt" (LN - abbreviated language accord as
#       https://yandex.ru/dev/translate/doc/dg/concepts/api-overview-docpage/#api-overview__languages)
#  3) result file in folder "output"
#  4) use Yandex.Translate and accord design-requirements-docpage
#       (https://yandex.ru/dev/translate/doc/dg/concepts/design-requirements-docpage/)

import requests
import os


URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
KEY_API = 'trnsl.1.1.20190704T182934Z.17f33d8db55385c6.e6d41260c9ccabfba9197455fd6d6679fec9bf38'
LNG_OUT = 'RU'
LEGAL = f'\n{"=" * 67}\nПереведено сервисом «Яндекс.Переводчик» http://translate.yandex.ru/\n'

def make_output_dir():
    """
    check folder name "output". if no -> create.
    :return:
    """
    if 'output' not in os.listdir():
        os.mkdir('output')

def translate(text, lang):
    '''
    translation input text
    https://translate.yandex.net/api/v1.5/tr.json/translate
     ? [key=<API-ключ>]
     & [text=<переводимый текст>]
     & [lang=<направление перевода>]
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    :return:
    translated text
    '''
    params = {
        'key': KEY_API,
        'text': text,
        'lang': '{}-{}'.format(lang, LNG_OUT).lower(),
    }
    response = requests.get(URL, params=params)
    return ''.join(response.json()['text'])

def open_file_as_str(filename):
    """
    open file 'filename'

    :param filename:
    :return:
    all content file as a one string
    """
    string_ = str()
    with open(filename, encoding='utf-8') as file:
        for string in file:
            if string.strip() == '':
                string_ += '. '
            else:
                string_ += string.strip()
        return string_

def open_file_as_lst(filename):
    """
    open file 'filename'

    :param filename:
    :return:
    all content file as list
    """
    lst = list()
    with open(filename, encoding='utf-8') as file:
        for string in file:
            string = string.strip()
            if string.strip() == '':
                continue
            elif '<p>' in string:
                string_ = string.split('<p>')
                for string in string_:
                    lst.append(string)
            else:
                lst.append(string)
        return lst

def get_langs():
    """
    get list file name in folder source
    :return:
    abbreviated languages as list
    """
    langs = []
    for lang in os.listdir('source'):
        if '.txt' in lang:
            langs.append(lang.replace('.txt', ''))
        else:
            continue
    return langs

def write_translate(text, lang, mode='wt'):
    """
    Record translate text to file

    :param text:
    :param lang:
    :param mode:
    :return:
    """
    out_file = os.path.join('output', f'{lang.upper()}_to_{LNG_OUT}.txt')
    with open(out_file, mode=mode, encoding='utf-8') as file:
        file.write(text)

def output_result():
    """
    main function for write translated text from input file to output file
    :return:
    """
    for lang in get_langs():
        text = open_file_as_lst(f'source/{lang}.txt')
        for txt in text:
            write_translate(translate(txt, lang), lang, 'at')
            write_translate('\n\n', lang, 'at')
            print(translate(txt, lang))
        write_translate(LEGAL, lang, 'at')
        print(LEGAL)


if __name__ == '__main__':
    make_output_dir()
    output_result()
