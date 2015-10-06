import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'taas.server.test_settings'
test_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))
sys.path.insert(0, test_dir)

import django
from django.conf import settings
from django.test.utils import get_runner


def run_tests():
    django.setup()
    test_runner_class = get_runner(settings)
    test_runner = test_runner_class(verbosity=1, interactive=True)
    failures = test_runner.run_tests([])
    sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests()
