import argparse
import glob
import os.path
import re

import MeCab
from openpyxl import load_workbook
from unidic import unidic

ANONYMIZED_TAG = '[ANON]'

anonymization_count = {
    'Person': 0,
    'Location': 0,
    'Organization': 0,
    'Other': 0,
}
tagger = MeCab.Tagger()
# tagger = MeCab.Tagger('-d "{}"'.format(unidic.DICDIR))
force_anonymize = []
special_tokens = []
out_dir = None

def process(file):
    filename = os.path.split(file)[1]
    f = load_workbook(file)
    for sheet in f.worksheets:
        for column in sheet.iter_cols():
            if column[0].value in force_anonymize:
                for cell in column[1:]:
                    cell.value = force_deidentify(str(cell.value))
                continue
            for cell in column[1:]:
                if isinstance(cell.value, str):
                    cell.value = deidentify(cell.value)

    out = os.path.join(out_dir, filename)
    if os.path.exists(out):
        out.replace(".xlsx", "_2.xlsx")
    f.save(out)


def should_deidentify(token):
    # Remove all proper nouns
    if (token[1][0] == '名詞' and token[1][1] == '固有名詞'):
        # Person name
        if token[1][2] == '人名':
            anonymization_count['Person'] += 1
        # Location
        elif token[1][2] == '地名':
            anonymization_count['Location'] += 1
        # Organization
        elif token[1][2] == '一般' or token[1][3] == '一般' or token[1][2] == "地域":
            anonymization_count['Organization'] += 1
        else:
            anonymization_count["Other"] += 1
        return True
    elif token[0] in special_tokens:
        anonymization_count["Special tokens"] += 1
        return True
    return False


def get_mecab_parsing(text):
    return [[chunk.split('\t')[0], tuple(chunk.split('\t')[1].split(','))] for chunk in
            tagger.parse(text).splitlines()[:-1]]


def deidentify(text):
    parsed = get_mecab_parsing(text)
    for i, token in enumerate(parsed):
        if should_deidentify(token):
            text = text.replace(token[0], ANONYMIZED_TAG)
        if token[0] in ["病院", "クリニック"]:
            text = text.replace(parsed[i - 1][0], ANONYMIZED_TAG)
    return text


def force_deidentify(text):
    for _ in text.split(" "):
        anonymization_count["Forced anonymization"] += 1
    return " ".join([ANONYMIZED_TAG for _ in text.split(" ")])


def process_directory(directory):
    files = os.listdir(directory)
    filtered = filter(lambda x: x.endswith(".xlsx") and not x.startswith("."), files)
    return [os.path.join(directory, f) for f in filtered]


def main(input, output, anonymize_columns=[], tokens=[]):
    global force_anonymize
    global special_tokens
    global out_dir
    if anonymize_columns != None:
        force_anonymize = anonymize_columns
    if tokens != None:
        special_tokens = tokens
    out_dir = output

    # Parse file list
    files = []
    for path in input:
        if os.path.isfile(path) and path.endswith(".xlsx"):
            files.append(path)
        elif os.path.isdir(path):
            files.extend(process_directory(path))
        else:
            print(f"Invalid file: {path}")

    os.makedirs(out_dir, exist_ok=True)

    for file in files:
        try:
            process(file)
        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue


    # print(deidentify("田中と申します。大阪にすんでいます。"))
    return anonymization_count, len(files)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Excel file anonymizer tool')
    parser.add_argument('--input', type=str, nargs='+', required=True,
                        help='Input file(s) or directory(ies) path')
    parser.add_argument('--output', type=str, required=True, help='Anonymized output folder')
    parser.add_argument('--force_anonymize', type=str, nargs='+',
                        help='Columns to be forcibly anonymized, regardless of the content type')
    parser.add_argument('--special_tokens', type=str, nargs='+',
                        help='Special tokens that should always be anonymized')
    parser.add_argument('--special_tokens', type=str, nargs='+',
                        help='Special tokens that should always be anonymized')
    # parser.add_argument('--replace_file_name', type=srt, help='Replace the file name with the given string')

    args = parser.parse_args()

    main(args.input, args.output, args.force_anonymize, args.special_tokens)
