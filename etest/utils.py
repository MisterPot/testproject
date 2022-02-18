import re


def analyze_output(stdout):
    analyze_rows = stdout.split('\n')[-8:]

    if len(analyze_rows) < 8:
        raise ValueError('Invalid parser output')

    pattern = re.compile(r'\d+')
    validProductCount = int(pattern.findall(analyze_rows[2])[0]),
    allProductCount = int(pattern.findall(analyze_rows[6])[0])

    if not validProductCount or not allProductCount:
        raise ValueError('Very small products count or count is 0')