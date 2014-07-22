import random
import unittest
import uuid

from uuid import UUID

from timeuuid import TimeUUID
from timeuuid import timeuuid_from_time
from timeuuid import UUIDType

def py_cmp(tu1, tu2):
  return cmp((tu1.time, tu1.bytes), (tu2.time, tu2.bytes))

def get_str_uuids(n):
  for _ in xrange(n):
    yield str(uuid.uuid4())

class TestTimeUUID(unittest.TestCase):
  def test_time(self):
    for uuid_str in get_str_uuids(10000):
      uu = UUID(uuid_str)
      tuu = TimeUUID(uuid_str)
      self.assertEqual(uu.time, tuu.time)

  def test_bytes(self):
    for _id in get_str_uuids(10000):
      uu = UUID(_id)
      tuu = TimeUUID(_id)
      self.assertEqual(uu.bytes, tuu.bytes)

  def test_cmp(self):
    uuids = map(lambda s: TimeUUID(s), get_str_uuids(10000))
    random.shuffle(uuids)
    for _ in xrange(10000):
      a, b = random.choice(uuids), random.choice(uuids)
      self.assertEqual(cmp(a, b), py_cmp(a, b))

    for _ in xrange(1000):
      i = random.randint(1, 9999)
      self.assertTrue(uuids[i] == uuids[i])
      self.assertTrue(uuids[i] >= uuids[i])
      self.assertTrue(uuids[i] <= uuids[i])
      self.assertFalse(uuids[i] != uuids[i])
      self.assertFalse(uuids[i - 1] == uuids[i])
      self.assertTrue(uuids[i - 1] != uuids[i])

  def test_descending(self):
    uuid_strs = list(get_str_uuids(10000))
    uuids = sorted(map(lambda s: TimeUUID(s), uuid_strs))
    descending_uuids = sorted(map(lambda s: TimeUUID(s, descending=True),
                                  uuid_strs))
    self.assertEqual(uuids, descending_uuids[::-1])

    for uu, duu in zip(uuids, descending_uuids[::-1]):
      self.assertTrue(uu == duu)
      self.assertTrue(uu <= duu)
      self.assertTrue(uu >= duu)
      self.assertFalse(uu != duu)

  def test_str(self):
    for uuid_str in get_str_uuids(20000):
      tuu = TimeUUID(uuid_str)
      self.assertEqual(uuid_str, str(tuu))
      self.assertEqual('TimeUUID(%s)' % uuid_str, repr(tuu))

  def test_bytes_init(self):
    for uuid_str in get_str_uuids(10000):
      uu = UUID(uuid_str)
      tuu1 = TimeUUID(str(uu))
      tuu2 = TimeUUID(bytes=uu.bytes)
      self.assertEqual(tuu1, tuu2)

  def test_timeuuid_from_time(self):
    for uuid_str in get_str_uuids(10000):
      uu = UUID(uuid_str)
      for t in (UUIDType.LOWEST, UUIDType.HIGHEST, UUIDType.RANDOM):
        tuu = timeuuid_from_time(uu.time, type=t)
        self.assertEqual(uu.time, tuu.time)

  def test_timeuuid_low_high(self):
    for uuid_str in get_str_uuids(100):
      uu = UUID(uuid_str)
      low = timeuuid_from_time(uu.time, UUIDType.LOWEST)
      high = timeuuid_from_time(uu.time, UUIDType.HIGHEST)
      self.assertTrue(low < high)
      for i in xrange(5000):
        rand = timeuuid_from_time(uu.time, UUIDType.RANDOM)
        self.assertTrue(low < rand)
        self.assertTrue(high > rand)
