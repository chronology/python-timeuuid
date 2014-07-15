import random
import time

from contextlib import contextmanager
from uuid import UUID
from uuid import uuid4

from timeuuid import TimeUUID

def create(cls, n, hex_or_bytes='hex'):
  if hex_or_bytes == 'hex':
    return [cls(str(uuid4())) for _ in xrange(n)]
  elif hex_or_bytes == 'bytes':
    return [cls(bytes=uuid4().bytes) for _ in xrange(n)]
  raise ValueError(hex_or_bytes)

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
  print '* Using hex constructor:'
  for cls in [UUID, TimeUUID]:
    with timeit(cls.__name__):
      create(cls, 100000)
  print '* Using bytes constructor:'
  for cls in [UUID, TimeUUID]:
    with timeit(cls.__name__):
      create(cls, 100000, hex_or_bytes='bytes')
    
def test_cmp():
  print
  for cls in [UUID, TimeUUID]:
    uuids = create(cls, 100000)
    with timeit(cls.__name__):
      compare(uuids, 500000)
