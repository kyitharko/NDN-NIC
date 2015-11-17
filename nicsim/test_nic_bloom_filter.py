import unittest as ut
from nic_bloom_filter import NicBloomFilter

class NicBloomFilterTestCase(ut.TestCase):
	"""
	Test for NicBloomFilter
	"""

	def setup(self):
		self.NBF = NicBloomFilter(100)

	def test_add_query_true(self):
		"""
		Add ("/ndn/test","PIT) into NicBloomFilter
		and make a query of "/ndn/test"
		"""

		NBF = NicBloomFilter(100)
		NBF.add("/ndn/test","PIT")
		result = NBF.query("/ndn/test")
		self.assertTrue(result, "Query result is invalid")

	def test_add_query_false(self):
		"""
		Add ("/ndn/test","PIT) into NicBloomFilter
		and make a query of "/ndn/test1"
		"""

		NBF = NicBloomFilter(100)
		NBF.add("/ndn/test","PIT")
		result = NBF.query("/ndn/test1")
		self.assertFalse(result, "Query result is invalid")

	def test_add_query_FP(self):
		"""
		Add multiple keys into NicBloomFilter to achieve FP
		and make a query of diffent key with FP
		"""

		NBF = NicBloomFilter(100)
		for i in range(200):
			NBF.add(str(i),"PIT")
		result = NBF.query("300")
		self.assertEqual(result,"FP", "Query result is invalid")


if __name__ == '__main__':
    ut.main(verbosity=2)