# Learn more about the following directives at:
# http://docs.cython.org/src/reference/compilation.html#compiler-directives
#
# cython: boundscheck=False, wraparound=False, embedsignature=True

from cpython.object cimport Py_EQ, Py_GE, Py_GT, Py_LE, Py_LT, Py_NE

from uuid cimport memcmp
from uuid cimport uuid_parse
from uuid cimport uuid_t
from uuid cimport uint64_t

cdef class TimeUUID:
  cdef uuid_t _bytes
  cdef readonly uint64_t time
  
  def __cinit__(TimeUUID self, str uuid_pystr):
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

  def __richcmp__(TimeUUID self, TimeUUID other, int op):
    cdef int bytes_cmp = memcmp(&self._bytes[0], &other._bytes[0], 16)

    if op == Py_EQ:
      return bytes_cmp == 0
    if op == Py_NE:
      return bytes_cmp != 0

    if op == Py_GE:
      return self.time > other.time or (self.time == other.time and
                                        bytes_cmp >= 0)
    if op == Py_GT:
      return self.time > other.time or (self.time == other.time and
                                        bytes_cmp > 0)
    if op == Py_LE:
      return self.time < other.time or (self.time == other.time and
                                        bytes_cmp <= 0)
    if op == Py_LT:
      return self.time < other.time or (self.time == other.time and
                                        bytes_cmp < 0)

  property bytes:
    def __get__(self):
      cdef bytes py_bytes = self._bytes[:16]
      return py_bytes
