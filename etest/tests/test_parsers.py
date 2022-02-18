from subprocess import Popen, PIPE
from eshopcron.env import ENV
from etest.config import parser_timeout
from etest.utils import analyze_output
from threading import Timer
from colorama import init, Fore

init()


def colored(text, color='YELLOW'):
    return getattr(Fore, color.upper()) + text


def kill(proc):
    try:
        proc.kill()

    except OSError:
        pass

    finally:
        print(colored('Parser time outed'))
        assert 1 == 0


def test_parser(external_parser_data):
    ex_id, path = external_parser_data

    if any(i in path for i in ('metaldetectors', 'stabs', 'elektropatron', 'bikes',
                               'agregators', 'boats', 'google_sheets', 'prom', 'siteparser',
                               'stabs_ru')):
        run_path = ENV.ECRON_TASKS("parsers/{}").format(path)
    else:
        run_path = ENV.SHOP3(path)

    proc = Popen(['/usr/bin/python2.7', run_path], stdout=PIPE, stderr=PIPE)
    timer = Timer(parser_timeout, kill, [proc])

    timer.start()
    proc.wait()
    timer.cancel()

    if proc.returncode >= 1:
        print(colored(proc.stderr.read(), color='magenta'))
    else:
        out = proc.stdout.read()
        try:
            analyze_output(out)
        except Exception as e:
            print(colored(e.message))
            assert 1 == 0

        print(colored(out, color='green'))
    assert proc.returncode == 0
