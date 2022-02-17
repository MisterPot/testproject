from subprocess import Popen, PIPE
from eshopcron.env import ENV


def test_parser(external_parser_data):
    ex_id, path = external_parser_data
    if any(i in path for i in ('metaldetectors', 'stabs', 'elektropatron', 'bikes')):
        run_path = ENV.ECRON_TASKS("parsers/{}").format(path)
    else:
        run_path = ENV.SHOP3(path)
    proc = Popen(['/usr/bin/python2.7', run_path], stdout=PIPE, stderr=PIPE)
    proc.wait()
    if proc.returncode == 1:
        print(proc.stdout)
    assert proc.returncode == 0