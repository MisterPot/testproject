from re import compile
from csv import DictWriter

fields = [
    '', 'ParserId', '',
    '', 'Path', '',
    '', 'WorkStatus', '',
    '', 'Errors (if bad status)', ''
]

clear_fields = map(lambda item: item, fields)


def create_csv(filename):
    with open(filename, 'w') as f:
        writer = DictWriter(f, fieldnames=fields, delimiter=';')
        writer.writeheader()


def write_row(filename, row):
    with open(filename, 'a') as f:
        writer = DictWriter(f, fieldnames=fields, delimiter=';')
        writer.writerow(row)


def analyze_output(stdout):
    analyze_rows = stdout.split('\n')[-8:]

    if len(analyze_rows) < 8:
        raise ValueError('Invalid parser output')

    pattern = compile(r'\d+')
    validProductCount = int(pattern.findall(analyze_rows[2])[0]),
    allProductCount = int(pattern.findall(analyze_rows[6])[0])

    if not validProductCount or not allProductCount:
        raise ValueError('Very small products count or count is 0')
