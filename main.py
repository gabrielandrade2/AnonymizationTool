import argparse

import ipadic as ipadic
import unidic

import MeCab
from openpyxl import load_workbook

ANONYMIZED_TAG = '[ANON]'

anonymization_count = {
    'Person': 0,
    'Location': 0,
    'Organization': 0,
}
tagger = MeCab.Tagger(ipadic.MECAB_ARGS)
# tagger = MeCab.Tagger(unidic.DICDIR)


def should_deidentify(token):
    # Remove all proper nouns
    if (token[1][0] == '名詞' and token[1][1] == '固有名詞'):
        # Person name
        if token[1][2] == '人名':
            anonymization_count['Person'] += 1
        # Location
        if token[1][2] == '地名':
            anonymization_count['Location'] += 1
        # Organization
        if token[1][2] == '一般':
            anonymization_count['Organization'] += 1
        return True

    return False

def get_mecab_parsing(text):
    return [[chunk.split('\t')[0], tuple(chunk.split('\t')[1].split(','))] for chunk in
              tagger.parse(text).splitlines()[:-1]]

def deidentify(text):
    parsed = get_mecab_parsing(text)
    for token in parsed:
        if should_deidentify(token):
            text = text.replace(token[0], ANONYMIZED_TAG)
    return text

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Anonymize Nagoya University Hospital records')
    # parser.add_argument('--input', type=str, help='Input file path')
    # parser.add_argument('--output', type=str, help='Anonymized output file path')
    # args = parser.parse_args()
    #
    # f = load_workbook(args.input)
    # for sheet in f.worksheets:
    #     for row in sheet.iter_rows():
    #         for cell in row:
    #             if isinstance(cell.value, str):
    #                 cell.value = deidentify(cell.value)
    #
    # f.save(args.output)
    print(deidentify("えいさいかいレイディスクリニック"))
    print(deidentify("担当高原Dr."))

    print(anonymization_count)

    # Special rules/exceptions:
    # 病院　クリニック
    # Dr
    # ちゃん

