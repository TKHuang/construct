from declarativeunittest import *
from shio.lib.hex import *


def test_hexdump():
    for i in range(100):
        assert hexundump(hexdump(b"?"*i,32),32) == b"?"*i
