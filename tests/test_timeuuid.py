import random
import unittest
import uuid

from uuid import UUID

from timeuuid import TimeUUID

def py_cmp(tu1, tu2):
  return cmp((tu1.time, tu1.bytes), (tu2.time, tu2.bytes))

def get_str_uuids(n):
  for _ in xrange(n):
    yield str(uuid.uuid4())

class TestTimeUUID(unittest.TestCase):
  def test_time(self):
    for _id in get_str_uuids(5000):
      uu = UUID(_id)
      tuu = TimeUUID(_id)
      self.assertEqual(uu.time, tuu.time)

  def test_bytes(self):
    for _id in get_str_uuids(5000):
      uu = UUID(_id)
      tuu = TimeUUID(_id)
      self.assertEqual(uu.bytes, tuu.bytes)

  def test_cmp(self):
    uuids = map(lambda s: TimeUUID(s), get_str_uuids(5000))
    random.shuffle(uuids)
    for _ in xrange(5000):
      a, b = random.choice(uuids), random.choice(uuids)
      self.assertEqual(cmp(a, b), py_cmp(a, b))

    for _ in xrange(100):
      i = random.randint(1, 4999)
      self.assertTrue(uuids[i] == uuids[i])
      self.assertTrue(uuids[i] >= uuids[i])
      self.assertTrue(uuids[i] <= uuids[i])
      self.assertFalse(uuids[i] != uuids[i])
      self.assertFalse(uuids[i - 1] == uuids[i])
      self.assertTrue(uuids[i - 1] != uuids[i])

  def test_reverse(self):
    uuid_strs = list(get_str_uuids(100))
    uuids = sorted(map(lambda s: TimeUUID(s), uuid_strs))
    reverse_uuids = sorted(map(lambda s: TimeUUID(s, reverse=True), uuid_strs))
    self.assertEqual(uuids, reverse_uuids[::-1])

    for uu, ruu in zip(uuids, reverse_uuids[::-1]):
      self.assertTrue(uu == ruu)
      self.assertTrue(uu <= ruu)
      self.assertTrue(uu >= ruu)
      self.assertFalse(uu != ruu)

  def test_str(self):
    for uuid_str in get_str_uuids(1000):
      tuu = TimeUUID(uuid_str)
      self.assertEqual(uuid_str, str(tuu))
      self.assertEqual('TimeUUID(%s)' % uuid_str, repr(tuu))
