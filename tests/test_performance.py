import random
import time

from contextlib import contextmanager
from uuid import UUID
from uuid import uuid4

from timeuuid import TimeUUID

def create(cls, n):
  return [cls(str(uuid4())) for _ in xrange(n)]

def compare(uuids, n):
  for _ in xrange(n):
    cmp(random.choice(uuids), random.choice(uuids))

@contextmanager
def timeit(name):
  start = time.time()
  yield
  print '>', name, 'took', '%ss' % (time.time() - start)

def test_create():
  print
  for cls in [UUID, TimeUUID]:
    with timeit(cls.__name__):
      create(cls, 250000)

def test_cmp():
  print
  for cls in [UUID, TimeUUID]:
    uuids = create(cls, 100000)
    with timeit(cls.__name__):
      compare(uuids, 500000)
