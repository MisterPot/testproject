from os.path import join, normpath

root = __path__[0]
args_file = join(root, 'data.txt')
parser_test = join(root, normpath('/tests/test_parsers.py'))