from argparse import ArgumentParser
import sys
import etest
from subprocess import Popen
from eshopadmin.db import db_sql_get_recordset_ex


def all_ids():
    query = db_sql_get_recordset_ex('SELECT "ExternalShopId" FROM prod."ExternalShopsParsers"', ())
    return map(lambda item: item['ExternalShopId'], query)


def active_vendors():
    query = db_sql_get_recordset_ex('SELECT "ExternalShopsIds" FROM prod."Suppliers" '
                                    'WHERE 32 = any("ShopIds") or 71 = any("ShopIds");', ())
    result = []
    for ids in filter( lambda item: item['ExternalShopsIds'] is not None, query):
        result.extend(ids)

    return result


consts = {
    'all': all_ids,
    'active_vendors': active_vendors,
}

const_help = {
    'all': "All parsers ids",
    'active_vendors': 'Parser ids only for active vendors ("ExternalShopsIds != NULL")'
}


def parse():
    parser = ArgumentParser()
    parser.add_argument('--ids', type=str, nargs='*', help='Input the ids in view "--ids 12 13 14 15" or'
                        ' may use file "--ids file:~/ids/ids.txt". File must been write in view'
                        ' (d=delimiter) "12d13d14d15" (d in [" ", ",", ";", "\\n"])')
    parser.add_argument('--consts', type=bool, default=False, help="Print available constants")
    args = {key: value for key, value in parser.parse_args().__dict__.items()}

    ids = args.get('ids')

    if args.get('consts'):
        print('\n'.join(['{}: \t\t {}'.format(key, value) for key, value in const_help.items()]))
        sys.exit(0)

    if ids:

        if 'file' in ids[0]:
            filename = ids[0].split(':')[1]
            with open(filename) as file:
                ids = file.read()\
                    .replace(';', ' ')\
                    .replace(',', ' ')\
                    .replace('\n', ' ')\
                    .split(' ')

        elif 'const' in ids[0]:
            func = consts.get(ids[0].split(':')[1])

            if not ids:
                print('Bad constant, see available constants "etest --consts"')
                sys.exit(0)

            ids = func()

        with open(etest.args_file, 'w') as file:
            file.write('\n'.join([id_ for id_ in ids if id_]))

        proc = Popen(['sudo', 'python2', '-m', 'pytest', etest.parser_test])
        proc.wait()
        sys.exit(0)

    print('No ids to parse, use "etest -help" for more information')