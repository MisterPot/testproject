from subprocess import Popen, PIPE
from eshopcron.env import ENV
from etest.config import ticks, tick_time
from time import sleep
from signal import SIGTERM
from etest.utils import analyze_output


def test_parser(external_parser_data):
    ex_id, path = external_parser_data
    curr_time = 0
    max_time = tick_time * ticks

    if any(i in path for i in ('metaldetectors', 'stabs', 'elektropatron', 'bikes',
                               'agregators', 'boats', 'google_sheets', 'prom', 'siteparser',
                               'stabs_ru')):
        run_path = ENV.ECRON_TASKS("parsers/{}").format(path)
    else:
        run_path = ENV.SHOP3(path)
    proc = Popen(['/usr/bin/python2.7', run_path], stdout=PIPE, stderr=PIPE)

    for i in range(ticks):

        if curr_time == max_time:
            proc.send_signal(SIGTERM)
            proc.wait()
            print('Parser time outed.')
            assert 1 == 0

        if proc.returncode is not None:
            break

        sleep(tick_time)
        curr_time += tick_time

    if proc.returncode >= 1:
        print(proc.stderr.read())
    else:
        out = proc.stdout.read()
        analyze_output(out)
        print(out)
    assert proc.returncode == 0
