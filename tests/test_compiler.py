# -*- coding: utf-8 -*-

from declarativeunittest import *
from shio import *
from shio.lib import *


embeddedswitch1 = EmbeddedSwitch(
    Struct(
        "type" / Byte,
    ),
    this.type,
    {
        0: Struct("name" / PascalString(Byte, "utf8")),
        1: Struct("value" / Byte),
    }
)
example = Struct(
    "num" / Byte,

    "bytes1" / Bytes(4),
    "bytes2" / Bytes(this.num),
    "greedybytes" / Prefixed(Byte, GreedyBytes),
    "bitwise1" / Bitwise(BitsInteger(8, swapped=False)),
    "bitwise2" / Bitwise(BitsInteger(8, swapped=True)),
    "bytewise1" / Bitwise(Bytewise(BytesInteger(16, swapped=True))),
    "bytewise2" / Bitwise(Bytewise(BytesInteger(16, swapped=False))),

    "formatfield" / FormatField(">", "B"),
    "bytesinteger0" / BytesInteger(0),
    "bytesinteger1" / BytesInteger(16, swapped=True),
    "bytesinteger2" / BytesInteger(16, swapped=False),
    "bytesinteger3" / BytesInteger(this.num),
    "bitsinteger0" / Bitwise(BitsInteger(0)),
    "bitsinteger1" / Bitwise(BitsInteger(8, swapped=False)),
    "bitsinteger2" / Bitwise(BitsInteger(8, swapped=True)),
    # - unknown cause (SizeofError: cannot calculate size, key not found in context)
    # "bitsinteger3" / Bitwise(BitsInteger(this.num)),
    "varint" / VarInt,
    "byte" / Byte,
    "float1" / Single,
    "float2" / Double,

    "string2" / PaddedString(12, "ascii"),
    "string2" / PaddedString(12, "utf8"),
    "string3" / PaddedString(12, "utf16"),
    "string4" / PaddedString(12, "utf32"),
    "pascalstring1" / PascalString(Byte, "ascii"),
    "pascalstring2" / PascalString(Byte, "utf8"),
    "cstring1" / CString("ascii"),
    "cstring2" / CString("utf8"),
    "cstring3" / CString("utf16"),
    "cstring4" / CString("utf32"),
    "greedystring1" / Prefixed(Byte, GreedyString("ascii")),
    "greedystring2" / Prefixed(Byte, GreedyString("utf8")),

    "flag" / Flag,
    "enum1" / Enum(Byte, zero=0),
    "enum2" / Enum(Byte),
    "flagsenum1" / FlagsEnum(Byte, zero=0, one=1),
    "flagsenum2" / FlagsEnum(Byte),
    "mapping" / Mapping(Byte, {"zero":0}),

    "struct" / Struct("field" / Byte),
    "embeddedstruct" / Embedded(Struct("embeddedfield1" / Byte)),
    "sequence1" / Sequence(Byte, Byte),
    "sequence2" / Sequence("num1" / Byte, "num2" / Byte),
    "embeddedsequence1" / Sequence(Embedded(Sequence(Byte, Byte))),
    "embeddedsequence2" / Sequence(Embedded(Sequence("num1" / Byte, "num2" / Byte))),

    "array1" / Array(5, Byte),
    "array2" / Array(this.num, Byte),
    "greedyrange0" / Prefixed(Byte, GreedyRange(Byte)),
    "repeatuntil1" / RepeatUntil(obj_ == 0, Byte),

    "const1" / Const(bytes(4)),
    "const2" / Const(0, Int32ub),
    "computed" / Computed(this.num),
    "index1" / Array(3, Index),
    "index2" / RestreamData(b"\x00", GreedyRange(Byte >> Index)),
    "index3" / RestreamData(b"\x00", RepeatUntil(True, Byte >> Index)),
    "rebuild" / Rebuild(Byte, len_(this.array1)),
    "default" / Default(Byte, 0),
    Check(this.num == 0),
    "check" / Check(this.num == 0),
    "error0" / If(False, Error),
    "focusedseq1" / FocusedSeq("num", Const(bytes(4)), "num"/Byte),
    "focusedseq2_select" / Computed("num"),
    "focusedseq2" / FocusedSeq(this._.focusedseq2_select, "num"/Byte),
    "pickled_data" / Computed(b"(lp0\n(taI1\naF2.3\na(dp1\na(lp2\naS'1'\np3\naS''\np4\na."),
    "pickled" / RestreamData(this.pickled_data, Pickled),
    "numpy_data" / Computed(b"\x93NUMPY\x01\x00F\x00{'descr': '<i8', 'fortran_order': False, 'shape': (3,), }            \n\x01\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00"),
    "numpy1" / If(supportsnumpy, RestreamData(this.numpy_data, Numpy)),
    "namedtuple1" / NamedTuple("coord", "x y z", Byte[3]),
    "namedtuple2" / RestreamData(b"\x00\x00\x00", NamedTuple("coord", "x y z", GreedyRange(Byte))),
    "namedtuple3" / NamedTuple("coord", "x y z", Byte >> Byte >> Byte),
    "namedtuple4" / NamedTuple("coord", "x y z", "x"/Byte + "y"/Byte + "z"/Byte),
    "timestamp1" / RestreamData(b'\x00\x00\x00\x00ZIz\x00', Timestamp(Int64ub, 1, 1970)),
    "timestamp2" / RestreamData(b'H9\x8c"', Timestamp(Int32ub, "msdos", "msdos")),
    "hex1" / Hex(Byte),
    "hex2" / Hex(Bytes(1)),
    "hex3" / Hex(RawCopy(Byte)),
    "hexdump1" / HexDump(Bytes(1)),
    "hexdump2" / HexDump(RawCopy(Byte)),

    "union1" / Union(None, "char"/Byte, "short"/Short, "int"/Int),
    "union2" / Union(1, "char"/Byte, "short"/Short, "int"/Int),
    "union3" / Union(0, "char1"/Byte, "char2"/Byte, "char3"/Byte),
    "union4" / Union("char1", "char1"/Byte, "char2"/Byte, "char3"/Byte),
    "unionembedded" / Union(None, Embedded(Struct("char"/Byte))),
    "select" / Select(Byte, CString("ascii")),
    "optional" / Optional(Byte),
    "if1" / If(this.num == 0, Byte),
    "ifthenelse" / IfThenElse(this.num == 0, Byte, Byte),
    "switch1" / Switch(this.num, {0 : Byte, 255 : Error}),
    "switch2" / Switch(this.num, {}),
    "switch3" / Switch(this.num, {}, default=Byte),
    "embeddedswitch1" / embeddedswitch1,
    "stopif0" / StopIf(this.num == 255),
    "stopif1" / Struct(StopIf(this._.num == 0), Error),
    "stopif2" / Sequence(StopIf(this._.num == 0), Error),
    "stopif3" / GreedyRange(StopIf(this.num == 0)),

    "padding" / Padding(2),
    "paddedbyte" / Padded(4, Byte),
    "alignedbyte" / Aligned(4, Byte),
    "alignedstruct" / AlignedStruct(4, "a"/Byte, "b"/Short),
    "bitstruct" / BitStruct("a"/Octet),

    "pointer" / Pointer(0, Byte),
    "peek" / Peek(Byte),
    "seek0" / Seek(0, 1),
    "tell" / Tell,
    "pass1" / Pass,
    "terminated0" / Prefixed(Byte, Terminated),

    "rawcopy1" / RawCopy(Byte),
    "rawcopy2" / RawCopy(RawCopy(RawCopy(Byte))),
    "bytesswapped" / ByteSwapped(BytesInteger(8)),
    "bitsswapped" / BitsSwapped(BytesInteger(8)),
    "prefixed1" / Prefixed(Byte, GreedyBytes),
    "prefixed2" / RestreamData(b"\x01", Prefixed(Byte, GreedyBytes, includelength=True)),
    "prefixedarray" / PrefixedArray(Byte, Byte),
    "fixedsized" / FixedSized(10, GreedyBytes),
    "nullterminated" / RestreamData(b'\x01\x00', NullTerminated(GreedyBytes)),
    "nullstripped" / RestreamData(b'\x01\x00', NullStripped(GreedyBytes)),
    "restreamdata" / RestreamData(b"\xff", Byte),
    "restreamdata_verify" / Check(this.restreamdata == 255),
    # Transformed
    # Restreamed
    # ProcessXor
    # ProcessRotateLeft
    # Checksum
    "compressed_bzip2_data" / Computed(b'BZh91AY&SYSc\x11\x99\x00\x00\x00A\x00@\x00@\x00 \x00!\x00\x82\x83\x17rE8P\x90Sc\x11\x99'),
    "compressed_bzip2" / RestreamData(this.compressed_bzip2_data, Compressed(GreedyBytes, "bzip2", level=9)),
    # Rebuffered

    # Lazy
    # LazyStruct
    # LazyArray
    # LazyBound

    # adapters and validators

    Probe(),
    # - fails due to unknown causes (Expected an identifier or literal)
    # "probe" / Probe(),
    "debugger" / Debugger(Byte),

    "items1" / Computed([1,2,3]),
    "len_" / Computed(len_(this.items1)),
    # - faulty list_ implementation, compiles into correct code
    # "repeatuntil2" / RepeatUntil(list_ == [0], Byte),
    # "repeatuntil3" / RepeatUntil(list_[-1] == 0, Byte),
)
exampledata = bytes(1000)


def test_example_benchmark():
    d = example.compile(filename="example_compiled.py")
    d.benchmark(exampledata, filename="example_benchmark.txt")

def test_compiled_benchmark():
    d = Struct().compile()
    d.benchmark(b"")
    d = Struct(Error).compile()
    d.benchmark(b"")

def test_compiler_recursion():
    raises(Construct().compile) == NotImplementedError
