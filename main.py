import argparse
import os.path

import MeCab
from openpyxl import load_workbook

ANONYMIZED_TAG = '[ANON]'

anonymization_count = {
    'Person': 0,
    'Location': 0,
    'Organization': 0,
    'Other': 0,
}
tagger = MeCab.Tagger()
# tagger = MeCab.Tagger('-d /opt/homebrew/lib/mecab/dic/ipadic')
# tagger = MeCab.Tagger('-r /dev/null -d /opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd')

force_anonymize_columns = []
force_anonymize_tokens = []
stop_words = []
out_dir = None


def process_file(file):
    filename = os.path.split(file)[1]
    f = load_workbook(file)
    for sheet in f.worksheets:
        for column in sheet.iter_cols():
            if column[0].value in force_anonymize_columns:
                for cell in column[1:]:
                    cell.value = force_deidentify(str(cell.value))
                continue
            for cell in column[1:]:
                if isinstance(cell.value, str):
                    print(cell)
                    cell.value = deidentify(cell.value)

    out = os.path.join(out_dir, filename)
    if os.path.exists(out):
        out = out.replace(".xlsx", "_anon.xlsx")
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
    elif token[0] in force_anonymize_tokens:
        anonymization_count["Special tokens"] += 1
        return True
    return False


def get_mecab_parsing(text):
    return [[chunk.split('\t')[0], tuple(chunk.split('\t')[1].split(','))] for chunk in
            tagger.parse(text).splitlines()[:-1]]


def deidentify(text: str):
    """
    Method that performs the actual anonymization of texts. Can be called directly from other scripts in order to
    execute the anonymization logic in a single string.

    :param text: The text to be anonymized.
    :return: The anonymized text.
    """
    parsed = get_mecab_parsing(text)

    # Debug print
    for token in parsed:
        print(token)

    anonymized_text = list()
    for i, token in enumerate(parsed):
        if should_deidentify(token):
            anonymized_text.append(ANONYMIZED_TAG)
        elif token[0] in stop_words:
            anonymized_text[-1] = ANONYMIZED_TAG
            anonymized_text.append(token[0])
        else:
            anonymized_text.append(token[0])
    return "".join(anonymized_text)


def force_deidentify(text):
    for _ in text.split(" "):
        anonymization_count["Forced anonymization"] += 1
    return " ".join([ANONYMIZED_TAG for _ in text.split(" ")])


def process_directory(directory):
    files = os.listdir(directory)
    filtered = filter(lambda x: x.endswith(".xlsx") and not x.startswith("."), files)
    return [os.path.join(directory, f) for f in filtered]


def main(input: str, output: str, force_anonymize_columns: list = None, force_anonymize_tokens: list = None,
         stop_words: list = None):
    """
    Main function for anonymizing Excel files, called when executing this script directly.

    :param input: The input file(s) or directory(ies)
    :param output: The output directory
    :param force_anonymize_columns: Columns to be forcibly anonymized, regardless of the content type
    :param force_anonymize_tokens: Special tokens that should always be anonymized
    :param stop_words: Special words that implicate the previous word should be anonymized, e.g. "病院" or "クリニック"
    :return:
    """
    global out_dir
    globals()['force_anonymize_columns'] = force_anonymize_columns
    globals()['force_anonymize_tokens'] = force_anonymize_tokens
    globals()['stop_words'] = stop_words
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
            process_file(file)
        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue

    return anonymization_count, len(files)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Excel file anonymizer tool')
    parser.add_argument('--input', type=str, nargs='+', required=True,
                        help='Input file(s) or directory(ies) path')
    parser.add_argument('--output', type=str, required=True, help='Anonymized output folder')
    parser.add_argument('--force_anonymize_columns', type=str, nargs='+',
                        help='Columns to be forcibly anonymized, regardless of the content type')
    parser.add_argument('--force_anonymize_tokens', type=str, nargs='+',
                        help='Special tokens that should always be anonymized')
    parser.add_argument('--stop_words', type=str, nargs='+',
                        help='Special words that implicate the previous word should be anonymized, e.g. "病院" or "クリニック"')

    args = parser.parse_args()

    main(args.input, args.output, args.force_anonymize_columns, args.force_anonymize_tokens, args.stop_words)
