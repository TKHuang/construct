from declarativeunittest import *
from shio import *
from shio.lib import *

from gallery import pe32file


def test_pe32():
    commondump(pe32file, "python37-win32.exe")
    commondump(pe32file, "python37-win64.exe")
    commondump(pe32file, "SharpZipLib0860-dotnet20.dll")
