import random
import unittest
import uuid

from uuid import UUID

from timeuuid import TimeUUID

def py_cmp(tu1, tu2):
  return cmp((tu1.time, tu1.bytes), (tu2.time, tu2.bytes))

def get_uuids(n=1, version=1):
  if version == 1:
    u = lambda: uuid.uuid1(random.randint(0, 2**48 - 1))
  elif version == 4:
    u = lambda: uuid.uuid4()
  else:
    raise ValueError
  for _ in xrange(n):
    yield str(u())

class TestTimeUUID(unittest.TestCase):
  def test_time(self):
    for _id in get_uuids(n=5000):
      uu = UUID(_id)
      tuu = TimeUUID(_id)
      self.assertEqual(uu.time, tuu.time)

  def test_bytes(self):
    for _id in get_uuids(n=5000, version=4):
      uu = UUID(_id)
      tuu = TimeUUID(_id)
      self.assertEqual(uu.bytes, tuu.bytes)

  def test_cmp(self):
    uuids = map(lambda s: TimeUUID(s), get_uuids(n=5000))
    random.shuffle(uuids)
    for _ in xrange(5000):
      a, b = random.choice(uuids), random.choice(uuids)
      self.assertEqual(cmp(a, b), py_cmp(a, b))
