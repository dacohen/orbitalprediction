import datetime
import unittest
import utils

class TestUtils(unittest.TestCase):

	def test_datetime_from_epoch(self):
		result = utils.datetime_from_epoch("19209.53234192")
		# Ignore microseconds
		result = result.replace(microsecond=0)
		self.assertEqual(datetime.datetime(2019, 7, 28, 12, 46, 34), result)