# Learn more about the following directives at:
# http://docs.cython.org/src/reference/compilation.html#compiler-directives
#
# cython: boundscheck=False, wraparound=False, embedsignature=True

from cpython cimport bool
from cpython.object cimport Py_EQ, Py_GE, Py_GT, Py_LE, Py_LT, Py_NE

from uuid cimport int32_t
from uuid cimport memcmp
from uuid cimport uint64_t
from uuid cimport uuid_parse
from uuid cimport uuid_t


cdef class TimeUUID:
  cdef uuid_t _bytes
  cdef readonly uint64_t time
  cdef public bint descending
  
  def __cinit__(TimeUUID self, uuid_pystr, bool descending=False):
    """
    Creates a new TimeUUID object instance.
    `uuid_pystr`: A Python string type object which represents the UUID in its
                  canonical form, e.g. '550e8400-e29b-41d4-a716-446655440000'
    `descending`: Should the result of __richcmp__ sort based on descending
                  order? (optional, False by default)
    """
    uuid_pyutf8 = uuid_pystr.encode('utf-8')
    cdef char *uuid_cstr = uuid_pyutf8
    uuid_parse(uuid_cstr, self._bytes)

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
    # XXX: This is a slow function. Purposefully so because the main goal
    # is low memory footprint, fast object construction and fast cmp.
    i = 0
    for b in self._bytes[:16]:
      i = (i << 8) | ord(b)
    h = '%032x' % i
    return '%s-%s-%s-%s-%s' % (h[:8], h[8:12], h[12:16], h[16:20], h[20:])

  def __repr__(self):
    return 'TimeUUID(%s)' % self.__str__()

  property bytes:
    def __get__(self):
      cdef bytes py_bytes = self._bytes[:16]
      return py_bytes
