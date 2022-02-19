from subprocess import Popen, PIPE
from eshopcron.env import ENV
from etest.config import parser_timeout
from etest.utils import analyze_output, create_csv, write_row
from threading import Timer
from colorama import init, Fore
import etest
from os.path import exists

init()

reporting = False

with open(etest.csv_file) as f:
    filename = f.read()
    if filename:
        reporting = True
        create_csv(filename)


def write_up_report(report, status, error=None):
    report['WorkStatus'] = str(status)
    report['Errors (if bad status)'] = str(error)
    write_row(filename, report)


def colored(text, color='YELLOW'):
    return getattr(Fore, color.upper()) + text


def kill(proc, parser_report):
    try:
        proc.kill()

    except OSError:
        pass

    finally:
        print(colored('Parser time outed'))
        write_up_report(parser_report, proc.returncode, error='Parser time outed')
        assert 1 == 0


def test_parser(external_parser_data):
    ex_id, path = external_parser_data

    parser_report = {
        'ParserId': str(ex_id),
        'Path': path
    }

    if any(i in path for i in ('metaldetectors', 'stabs', 'elektropatron', 'bikes',
                               'agregators', 'boats', 'google_sheets', 'prom', 'siteparser',
                               'stabs_ru')):
        run_path = ENV.ECRON_TASKS("parsers/{}").format(path)
    else:
        run_path = ENV.SHOP3(path)

    if not exists(run_path):
        print(colored('Path to parser not found'))
        write_up_report(parser_report, 1, error='Path to parser not found')
        assert 1 == 0

    proc = Popen(['/usr/bin/python2.7', run_path], stdout=PIPE, stderr=PIPE)
    timer = Timer(parser_timeout, kill, [proc, parser_report])

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
            write_up_report(parser_report, proc.returncode, error=e.message)
            assert 1 == 0

        print(colored(out, color='green'))
    assert proc.returncode == 0

