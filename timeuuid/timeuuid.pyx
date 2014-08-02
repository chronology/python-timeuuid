# Learn more about the following directives at:
# http://docs.cython.org/src/reference/compilation.html#compiler-directives
#
# cython: boundscheck=False, wraparound=False, embedsignature=True

from cpython cimport bool
from cpython.object cimport Py_EQ, Py_GE, Py_GT, Py_LE, Py_LT, Py_NE
from libc.stdlib cimport rand

from uuid cimport int32_t
from uuid cimport memcmp
from uuid cimport memcpy
from uuid cimport uint64_t
from uuid cimport uuid_parse
from uuid cimport uuid_t
from uuid cimport uuid_unparse


cdef class UUIDType:
  LOWEST = 0
  HIGHEST = 1
  RANDOM = 2


cdef inline copy_time_to_uuid_bytes(uint64_t time, uuid_t bytes):
  cdef uint64_t tmp = 0
  # Bit-flipping logic from uuid1 implementation described in:
  # http://stackoverflow.com/questions/7153844/uuid1-from-utc-timestamp-in-python
  # time_low
  tmp = time & 0xffffffff
  for i, j in enumerate(range(24, -8, -8)):
    bytes[i] = (tmp >> j) & 0xff
  # time_mid
  tmp = (time >> 32) & 0xffff
  bytes[4] = (tmp >> 8) & 0xff
  bytes[5] = tmp & 0xff
  # time_hi
  tmp = (time >> 48) & 0xfff
  bytes[6] = ((tmp >> 8) & 0xf) | 0x10 # version 1
  bytes[7] = tmp & 0xff


cpdef timeuuid_from_time(uint64_t time, int32_t type=UUIDType.RANDOM):
  """
  Returns a TimeUUID instance which has the time attribute equal to `time`.
  `type` describes how the remaining bytes are set. It must be an attribute of
  `UUIDType`.
  """
  cdef uuid_t bytes
  copy_time_to_uuid_bytes(time, bytes)

  if type == UUIDType.LOWEST:
    for i in range(8, 16):
      bytes[i] = 0
  elif type == UUIDType.HIGHEST:
    for i in range(8, 16):
      bytes[i] = 0xff
  else:
    for i in range(8, 16):
      bytes[i] = rand()

  # Set the variant to RFC 4122.
  bytes[8] |= 0x80
  bytes[8] &= 0x8f

  return TimeUUID(bytes=bytes[:16])


cdef class TimeUUID:
  cdef uuid_t _bytes
  cdef readonly uint64_t time
  cdef public bint descending
  
  def __cinit__(TimeUUID self, hex=None, bytes=None, bool descending=False):
    """
    Creates a new TimeUUID object instance.
    `uuid_pystr`: A Python string type object which represents the UUID in its
                  canonical form, e.g. '550e8400-e29b-41d4-a716-446655440000'
    `descending`: Should the result of __richcmp__ sort based on descending
                  order? (optional, False by default, which sorts in ascending
                  order)
    """
    cdef char *tmp_cstr = NULL
    if hex:
      tmp_cstr = hex
      uuid_parse(tmp_cstr, self._bytes)
    else:
      tmp_cstr = bytes
      memcpy(self._bytes, tmp_cstr, 16)

    self.time = 0
    cdef uint64_t tmp = 0
    # time_low
    for i in range(4):
      self.time = (self.time << 8) | self._bytes[i]
    # time_mid
    tmp = (self._bytes[4] << 8) | self._bytes[5]
    self.time = self.time | tmp << 32
    # time_hi
    tmp = (self._bytes[6] << 8) | self._bytes[7]
    self.time = self.time | ((tmp & 0xfff) << 48)

    self.descending = descending

  def __richcmp__(TimeUUID self, TimeUUID other, int op):
    cdef bint result = 0
    cdef int32_t bytes_cmp = memcmp(&self._bytes[0], &other._bytes[0], 16)

    if op == Py_EQ:
      return bytes_cmp == 0
    if op == Py_NE:
      return bytes_cmp != 0
    
    if bytes_cmp == 0 and (op == Py_GE or op == Py_LE):
      return True

    if op == Py_GE or op == Py_GT:
      result = self.time > other.time or (self.time == other.time and
                                          bytes_cmp > 0)
    elif op == Py_LE or op == Py_LT:
      result = self.time < other.time or (self.time == other.time and
                                          bytes_cmp < 0)
    
    return result ^ self.descending

  def __str__(self):
    cdef char string[36]
    uuid_unparse(self._bytes, &string[0])
    cdef bytes py_bytes = string
    return py_bytes

  def __repr__(self):
    return 'TimeUUID(%s)' % self.__str__()

  property bytes:
    def __get__(self):
      cdef bytes py_bytes = self._bytes[:16]
      return py_bytes
