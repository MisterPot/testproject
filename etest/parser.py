from argparse import ArgumentParser
import sys
import etest
import os

consts = {
    'all': 1,
    'active_vendors': 1,
}


def parse():
    parser = ArgumentParser()
    parser.add_argument('--ids', type=str, nargs='*', help='Input the ids in view "--ids 12 13 14 15" or'
                        ' may use file "--ids file:~/ids/ids.txt". File must been write in view'
                        ' (d=delimiter) "12d13d14d15" (d in [" ", ",", ";", "\\n"])')
    args = {key: value for key, value in parser.parse_args().__dict__.items()}

    ids = args.get('ids')
    if ids:

        if 'file' in ids[0]:
            filename = ids[0].split(':')[1]
            with open(filename) as file:
                ids = file.read()\
                    .replace(';', ' ')\
                    .replace(',', ' ')\
                    .replace('\n', ' ')\
                    .split(' ')

        with open(etest.args_file, 'w') as file:
            file.write('\n'.join([id_ for id_ in ids if id_]))

        os.system('sudo python2 ' + etest.parser_test)
        sys.exit(0)

    print('No ids to parse, use "etest -help" for more information')