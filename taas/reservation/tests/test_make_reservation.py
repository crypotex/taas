from django.test import TestCase
from datetime import datetime
from freezegun import freeze_time

@freeze_time("2015-11-11 17:00:00")
class test_make_reservation(TestCase):
    def test_freezegun_datetime_now(self):
        self.assertEqual(datetime.now(), datetime.strptime("2015-11-11 17:00:00", '%Y-%m-%d %H:%M:%S'),
                         'freeze_time package might be not installed. datetime.now() should return 2015-11-11 17:00:00')



