import pandas as pd
from enum import Enum

class NetType(Enum):
    INPUT = 1
    FAN = 2
    AND = 3
    OR = 4
    NOT = 5
    NAND = 6
    NOR = 7
    BUF = 8
    XOR = 9
    XNOR = 10

    @staticmethod
    def fromString(str):
        if str in ('inpt', 'input'):
            return NetType.INPUT
        elif str in ('from'):
            return NetType.FAN
        elif str in ('and'):
            return NetType.AND
        elif str in ('or'):
            return NetType.OR
        elif str in ('not'):
            return NetType.NOT
        elif str in ('nand'):
            return NetType.NAND
        elif str in ('nor'):
            return NetType.NOR
        elif str in ('buf'):
            return NetType.BUF
        elif str in ('xor'):
            return NetType.XOR
        elif str in ('xnor'):
            return NetType.XNOR
        else:
            raise ValueError('Invalid net type: ' + str)

class LogicValue(Enum):
    ZERO = 0
    ONE = 1
    X = 2
    D = 3
    SA0 = 3
    DBAR = 4
    SA1 = 4

    @staticmethod
    def fromString(str):
        if str in ('0', 'zero'):
            return LogicValue.ZERO
        elif str in ('1', 'one'):
            return LogicValue.ONE
        elif str in ('x', 'X'):
            return LogicValue.X
        elif str in ('d', 'D', 'SA0', 'sa0', 'SA_0', 'sa_0'):
            return LogicValue.D
        elif str in ('dbar', 'DBAR', 'SA1', 'sa1', 'SA_1', 'sa_1'):
            return LogicValue.DBAR
        else:
            raise ValueError('Invalid logic value: ' + str)