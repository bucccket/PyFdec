from dataclasses import dataclass
from enum import Enum

from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class Instruction:

    class ArgType(Enum):
        ByteLiteral = 1
        UByteLiteral = 2
        IntLiteral = 3
        UintLiteral = 4
        Int = 5
        Uint = 6
        Double = 7
        String = 8
        Namespace = 9
        Multiname = 10
        Class = 11
        Method = 12
        JumpTarget = 13
        SwitchDefaultTarget = 14
        SwitchTargets = 15
        Unknown = 16

    opcode: int
    arguments: list[tuple[ArgType, int | list[int] | None]]

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'Instruction':
        opcode = buffer.read_ui8()
        _, arg_types = cls.get_info(opcode)

        arguments: list[tuple['Instruction.ArgType', int | list[int] | None]] = []
        for arg_type in arg_types:
            value: int | list[int] | None = None
            match arg_type:
                case cls.ArgType.ByteLiteral:
                    value = buffer.read_si8()
                case cls.ArgType.UByteLiteral:
                    value = buffer.read_ui8()
                case cls.ArgType.IntLiteral:
                    value = buffer.read_encoded_si32()
                case cls.ArgType.UintLiteral:
                    value = buffer.read_encoded_u32()
                case cls.ArgType.Int:
                    value = buffer.read_encoded_u30()
                case cls.ArgType.Uint:
                    value = buffer.read_encoded_u30()
                case cls.ArgType.Double:
                    value = buffer.read_encoded_u30()
                case cls.ArgType.String:
                    value = buffer.read_encoded_u30()
                case cls.ArgType.Namespace:
                    value = buffer.read_encoded_u30()
                case cls.ArgType.Multiname:
                    value = buffer.read_encoded_u30()
                case cls.ArgType.Class:
                    value = buffer.read_encoded_u30()
                case cls.ArgType.Method:
                    value = buffer.read_encoded_u30()

                # TODO: convert relative byte offset to instruction offset
                case cls.ArgType.JumpTarget:
                    buffer.read_si24()
                case cls.ArgType.SwitchDefaultTarget:
                    buffer.read_si24()
                case cls.ArgType.SwitchTargets:
                    target_count = buffer.read_encoded_u30() + 1
                    value = [buffer.read_si24() for _ in range(target_count)]

                case cls.ArgType.Unknown:
                    value = None
                    pass
                case _:
                    raise NotImplementedError(f'Unimplemented arg type: {arg_type}')
            arguments.append((arg_type, value))

        return cls(opcode, arguments)

    @classmethod
    def get_info(cls, opcode: int) -> tuple[str, list[ArgType]]:
        match opcode:
            case 0x00:
                return ('db', [cls.ArgType.UByteLiteral])
            case 0x01:
                return ('bkpt', [cls.ArgType.Unknown])
            case 0x02:
                return ('nop', [])
            case 0x03:
                return ('throw', [])
            case 0x04:
                return ('getsuper', [cls.ArgType.Multiname])
            case 0x05:
                return ('setsuper', [cls.ArgType.Multiname])
            case 0x06:
                return ('dxns', [cls.ArgType.String])
            case 0x07:
                return ('dxnslate', [])
            case 0x08:
                return ('kill', [cls.ArgType.UintLiteral])
            case 0x09:
                return ('label', [])
            case 0x0A:
                return ('0x0A', [cls.ArgType.Unknown])
            case 0x0B:
                return ('0x0B', [cls.ArgType.Unknown])
            case 0x0C:
                return ('ifnlt', [cls.ArgType.JumpTarget])
            case 0x0D:
                return ('ifnle', [cls.ArgType.JumpTarget])
            case 0x0E:
                return ('ifngt', [cls.ArgType.JumpTarget])
            case 0x0F:
                return ('ifnge', [cls.ArgType.JumpTarget])
            case 0x10:
                return ('jump', [cls.ArgType.JumpTarget])
            case 0x11:
                return ('iftrue', [cls.ArgType.JumpTarget])
            case 0x12:
                return ('iffalse', [cls.ArgType.JumpTarget])
            case 0x13:
                return ('ifeq', [cls.ArgType.JumpTarget])
            case 0x14:
                return ('ifne', [cls.ArgType.JumpTarget])
            case 0x15:
                return ('iflt', [cls.ArgType.JumpTarget])
            case 0x16:
                return ('ifle', [cls.ArgType.JumpTarget])
            case 0x17:
                return ('ifgt', [cls.ArgType.JumpTarget])
            case 0x18:
                return ('ifge', [cls.ArgType.JumpTarget])
            case 0x19:
                return ('ifstricteq', [cls.ArgType.JumpTarget])
            case 0x1A:
                return ('ifstrictne', [cls.ArgType.JumpTarget])
            case 0x1B:
                return ('lookupswitch', [cls.ArgType.SwitchDefaultTarget, cls.ArgType.SwitchTargets])
            case 0x1C:
                return ('pushwith', [])
            case 0x1D:
                return ('popscope', [])
            case 0x1E:
                return ('nextname', [])
            case 0x1F:
                return ('hasnext', [])
            case 0x20:
                return ('pushnull', [])
            case 0x21:
                return ('pushundefined', [])
            case 0x22:
                return ('pushuninitialized', [cls.ArgType.Unknown])
            case 0x23:
                return ('nextvalue', [])
            case 0x24:
                return ('pushbyte', [cls.ArgType.ByteLiteral])
            case 0x25:
                return ('pushshort', [cls.ArgType.IntLiteral])
            case 0x26:
                return ('pushtrue', [])
            case 0x27:
                return ('pushfalse', [])
            case 0x28:
                return ('pushnan', [])
            case 0x29:
                return ('pop', [])
            case 0x2A:
                return ('dup', [])
            case 0x2B:
                return ('swap', [])
            case 0x2C:
                return ('pushstring', [cls.ArgType.String])
            case 0x2D:
                return ('pushint', [cls.ArgType.Int])
            case 0x2E:
                return ('pushuint', [cls.ArgType.Uint])
            case 0x2F:
                return ('pushdouble', [cls.ArgType.Double])
            case 0x30:
                return ('pushscope', [])
            case 0x31:
                return ('pushnamespace', [cls.ArgType.Namespace])
            case 0x32:
                return ('hasnext2', [cls.ArgType.UintLiteral, cls.ArgType.UintLiteral])
            case 0x33:
                return ('pushdecimal', [cls.ArgType.Unknown])
            case 0x34:
                return ('pushdnan', [cls.ArgType.Unknown])
            case 0x35:
                return ('li8', [])
            case 0x36:
                return ('li16', [])
            case 0x37:
                return ('li32', [])
            case 0x38:
                return ('lf32', [])
            case 0x39:
                return ('lf64', [])
            case 0x3A:
                return ('si8', [])
            case 0x3B:
                return ('si16', [])
            case 0x3C:
                return ('si32', [])
            case 0x3D:
                return ('sf32', [])
            case 0x3E:
                return ('sf64', [])
            case 0x3F:
                return ('0x3F', [cls.ArgType.Unknown])
            case 0x40:
                return ('newfunction', [cls.ArgType.Method])
            case 0x41:
                return ('call', [cls.ArgType.UintLiteral])
            case 0x42:
                return ('construct', [cls.ArgType.UintLiteral])
            case 0x43:
                return ('callmethod', [cls.ArgType.UintLiteral, cls.ArgType.UintLiteral])
            case 0x44:
                return ('callstatic', [cls.ArgType.Method, cls.ArgType.UintLiteral])
            case 0x45:
                return ('callsuper', [cls.ArgType.Multiname, cls.ArgType.UintLiteral])
            case 0x46:
                return ('callproperty', [cls.ArgType.Multiname, cls.ArgType.UintLiteral])
            case 0x47:
                return ('returnvoid', [])
            case 0x48:
                return ('returnvalue', [])
            case 0x49:
                return ('constructsuper', [cls.ArgType.UintLiteral])
            case 0x4A:
                return ('constructprop', [cls.ArgType.Multiname, cls.ArgType.UintLiteral])
            case 0x4B:
                return ('callsuperid', [cls.ArgType.Unknown])
            case 0x4C:
                return ('callproplex', [cls.ArgType.Multiname, cls.ArgType.UintLiteral])
            case 0x4D:
                return ('callinterface', [cls.ArgType.Unknown])
            case 0x4E:
                return ('callsupervoid', [cls.ArgType.Multiname, cls.ArgType.UintLiteral])
            case 0x4F:
                return ('callpropvoid', [cls.ArgType.Multiname, cls.ArgType.UintLiteral])
            case 0x50:
                return ('sxi1', [])
            case 0x51:
                return ('sxi8', [])
            case 0x52:
                return ('sxi16', [])
            case 0x53:
                return ('applytype', [cls.ArgType.UintLiteral])
            case 0x54:
                return ('0x54', [cls.ArgType.Unknown])
            case 0x55:
                return ('newobject', [cls.ArgType.UintLiteral])
            case 0x56:
                return ('newarray', [cls.ArgType.UintLiteral])
            case 0x57:
                return ('newactivation', [])
            case 0x58:
                return ('newclass', [cls.ArgType.Class])
            case 0x59:
                return ('getdescendants', [cls.ArgType.Multiname])
            case 0x5A:
                return ('newcatch', [cls.ArgType.UintLiteral])
            case 0x5B:
                return ('deldescendants', [cls.ArgType.Unknown])
            case 0x5C:
                return ('0x5C', [cls.ArgType.Unknown])
            case 0x5D:
                return ('findpropstrict', [cls.ArgType.Multiname])
            case 0x5E:
                return ('findproperty', [cls.ArgType.Multiname])
            case 0x5F:
                return ('finddef', [cls.ArgType.Multiname])
            case 0x60:
                return ('getlex', [cls.ArgType.Multiname])
            case 0x61:
                return ('setproperty', [cls.ArgType.Multiname])
            case 0x62:
                return ('getlocal', [cls.ArgType.UintLiteral])
            case 0x63:
                return ('setlocal', [cls.ArgType.UintLiteral])
            case 0x64:
                return ('getglobalscope', [])
            case 0x65:
                return ('getscopeobject', [cls.ArgType.UByteLiteral])
            case 0x66:
                return ('getproperty', [cls.ArgType.Multiname])
            case 0x67:
                return ('getouterscope', [cls.ArgType.UintLiteral])
            case 0x68:
                return ('initproperty', [cls.ArgType.Multiname])
            case 0x69:
                return ('setpropertylate', [])
            case 0x6A:
                return ('deleteproperty', [cls.ArgType.Multiname])
            case 0x6B:
                return ('deletepropertylate', [])
            case 0x6C:
                return ('getslot', [cls.ArgType.UintLiteral])
            case 0x6D:
                return ('setslot', [cls.ArgType.UintLiteral])
            case 0x6E:
                return ('getglobalslot', [cls.ArgType.UintLiteral])
            case 0x6F:
                return ('setglobalslot', [cls.ArgType.UintLiteral])
            case 0x70:
                return ('convert_s', [])
            case 0x71:
                return ('esc_xelem', [])
            case 0x72:
                return ('esc_xattr', [])
            case 0x73:
                return ('convert_i', [])
            case 0x74:
                return ('convert_u', [])
            case 0x75:
                return ('convert_d', [])
            case 0x76:
                return ('convert_b', [])
            case 0x77:
                return ('convert_o', [])
            case 0x78:
                return ('checkfilter', [])
            case 0x79:
                return ('convert_m', [cls.ArgType.Unknown])
            case 0x7A:
                return ('convert_m_p', [cls.ArgType.Unknown])
            case 0x7B:
                return ('0x7B', [cls.ArgType.Unknown])
            case 0x7C:
                return ('0x7C', [cls.ArgType.Unknown])
            case 0x7D:
                return ('0x7D', [cls.ArgType.Unknown])
            case 0x7E:
                return ('0x7E', [cls.ArgType.Unknown])
            case 0x7F:
                return ('0x7F', [cls.ArgType.Unknown])
            case 0x80:
                return ('coerce', [cls.ArgType.Multiname])
            case 0x81:
                return ('coerce_b', [])
            case 0x82:
                return ('coerce_a', [])
            case 0x83:
                return ('coerce_i', [])
            case 0x84:
                return ('coerce_d', [])
            case 0x85:
                return ('coerce_s', [])
            case 0x86:
                return ('astype', [cls.ArgType.Multiname])
            case 0x87:
                return ('astypelate', [])
            case 0x88:
                return ('coerce_u', [cls.ArgType.Unknown])
            case 0x89:
                return ('coerce_o', [cls.ArgType.Unknown])
            case 0x8A:
                return ('0x8A', [cls.ArgType.Unknown])
            case 0x8B:
                return ('0x8B', [cls.ArgType.Unknown])
            case 0x8C:
                return ('0x8C', [cls.ArgType.Unknown])
            case 0x8D:
                return ('0x8D', [cls.ArgType.Unknown])
            case 0x8E:
                return ('0x8E', [cls.ArgType.Unknown])
            case 0x8F:
                return ('negate_p', [cls.ArgType.Unknown])
            case 0x90:
                return ('negate', [])
            case 0x91:
                return ('increment', [])
            case 0x92:
                return ('inclocal', [cls.ArgType.UintLiteral])
            case 0x93:
                return ('decrement', [])
            case 0x94:
                return ('declocal', [cls.ArgType.UintLiteral])
            case 0x95:
                return ('typeof', [])
            case 0x96:
                return ('not', [])
            case 0x97:
                return ('bitnot', [])
            case 0x98:
                return ('0x98', [cls.ArgType.Unknown])
            case 0x99:
                return ('0x99', [cls.ArgType.Unknown])
            case 0x9A:
                return ('concat', [cls.ArgType.Unknown])
            case 0x9B:
                return ('add_d', [cls.ArgType.Unknown])
            case 0x9C:
                return ('increment_p', [cls.ArgType.Unknown])
            case 0x9D:
                return ('inclocal_p', [cls.ArgType.Unknown])
            case 0x9E:
                return ('decrement_p', [cls.ArgType.Unknown])
            case 0x9F:
                return ('declocal_p', [cls.ArgType.Unknown])
            case 0xA0:
                return ('add', [])
            case 0xA1:
                return ('subtract', [])
            case 0xA2:
                return ('multiply', [])
            case 0xA3:
                return ('divide', [])
            case 0xA4:
                return ('modulo', [])
            case 0xA5:
                return ('lshift', [])
            case 0xA6:
                return ('rshift', [])
            case 0xA7:
                return ('urshift', [])
            case 0xA8:
                return ('bitand', [])
            case 0xA9:
                return ('bitor', [])
            case 0xAA:
                return ('bitxor', [])
            case 0xAB:
                return ('equals', [])
            case 0xAC:
                return ('strictequals', [])
            case 0xAD:
                return ('lessthan', [])
            case 0xAE:
                return ('lessequals', [])
            case 0xAF:
                return ('greaterthan', [])
            case 0xB0:
                return ('greaterequals', [])
            case 0xB1:
                return ('instanceof', [])
            case 0xB2:
                return ('istype', [cls.ArgType.Multiname])
            case 0xB3:
                return ('istypelate', [])
            case 0xB4:
                return ('in', [])
            case 0xB5:
                return ('add_p', [cls.ArgType.Unknown])
            case 0xB6:
                return ('subtract_p', [cls.ArgType.Unknown])
            case 0xB7:
                return ('multiply_p', [cls.ArgType.Unknown])
            case 0xB8:
                return ('divide_p', [cls.ArgType.Unknown])
            case 0xB9:
                return ('modulo_p', [cls.ArgType.Unknown])
            case 0xBA:
                return ('0xBA', [cls.ArgType.Unknown])
            case 0xBB:
                return ('0xBB', [cls.ArgType.Unknown])
            case 0xBC:
                return ('0xBC', [cls.ArgType.Unknown])
            case 0xBD:
                return ('0xBD', [cls.ArgType.Unknown])
            case 0xBE:
                return ('0xBE', [cls.ArgType.Unknown])
            case 0xBF:
                return ('0xBF', [cls.ArgType.Unknown])
            case 0xC0:
                return ('increment_i', [])
            case 0xC1:
                return ('decrement_i', [])
            case 0xC2:
                return ('inclocal_i', [cls.ArgType.UintLiteral])
            case 0xC3:
                return ('declocal_i', [cls.ArgType.UintLiteral])
            case 0xC4:
                return ('negate_i', [])
            case 0xC5:
                return ('add_i', [])
            case 0xC6:
                return ('subtract_i', [])
            case 0xC7:
                return ('multiply_i', [])
            case 0xC8:
                return ('0xC8', [cls.ArgType.Unknown])
            case 0xC9:
                return ('0xC9', [cls.ArgType.Unknown])
            case 0xCA:
                return ('0xCA', [cls.ArgType.Unknown])
            case 0xCB:
                return ('0xCB', [cls.ArgType.Unknown])
            case 0xCC:
                return ('0xCC', [cls.ArgType.Unknown])
            case 0xCD:
                return ('0xCD', [cls.ArgType.Unknown])
            case 0xCE:
                return ('0xCE', [cls.ArgType.Unknown])
            case 0xCF:
                return ('0xCF', [cls.ArgType.Unknown])
            case 0xD0:
                return ('getlocal0', [])
            case 0xD1:
                return ('getlocal1', [])
            case 0xD2:
                return ('getlocal2', [])
            case 0xD3:
                return ('getlocal3', [])
            case 0xD4:
                return ('setlocal0', [])
            case 0xD5:
                return ('setlocal1', [])
            case 0xD6:
                return ('setlocal2', [])
            case 0xD7:
                return ('setlocal3', [])
            case 0xD8:
                return ('0xD8', [cls.ArgType.Unknown])
            case 0xD9:
                return ('0xD9', [cls.ArgType.Unknown])
            case 0xDA:
                return ('0xDA', [cls.ArgType.Unknown])
            case 0xDB:
                return ('0xDB', [cls.ArgType.Unknown])
            case 0xDC:
                return ('0xDC', [cls.ArgType.Unknown])
            case 0xDD:
                return ('0xDD', [cls.ArgType.Unknown])
            case 0xDE:
                return ('0xDE', [cls.ArgType.Unknown])
            case 0xDF:
                return ('0xDF', [cls.ArgType.Unknown])
            case 0xE0:
                return ('0xE0', [cls.ArgType.Unknown])
            case 0xE1:
                return ('0xE1', [cls.ArgType.Unknown])
            case 0xE2:
                return ('0xE2', [cls.ArgType.Unknown])
            case 0xE3:
                return ('0xE3', [cls.ArgType.Unknown])
            case 0xE4:
                return ('0xE4', [cls.ArgType.Unknown])
            case 0xE5:
                return ('0xE5', [cls.ArgType.Unknown])
            case 0xE6:
                return ('0xE6', [cls.ArgType.Unknown])
            case 0xE7:
                return ('0xE7', [cls.ArgType.Unknown])
            case 0xE8:
                return ('0xE8', [cls.ArgType.Unknown])
            case 0xE9:
                return ('0xE9', [cls.ArgType.Unknown])
            case 0xEA:
                return ('0xEA', [cls.ArgType.Unknown])
            case 0xEB:
                return ('0xEB', [cls.ArgType.Unknown])
            case 0xEC:
                return ('0xEC', [cls.ArgType.Unknown])
            case 0xED:
                return ('0xED', [cls.ArgType.Unknown])
            case 0xEE:
                return ('0xEE', [cls.ArgType.Unknown])
            case 0xEF:
                return ('debug', [cls.ArgType.UByteLiteral, cls.ArgType.String, cls.ArgType.UByteLiteral, cls.ArgType.UintLiteral])
            case 0xF0:
                return ('debugline', [cls.ArgType.UintLiteral])
            case 0xF1:
                return ('debugfile', [cls.ArgType.String])
            case 0xF2:
                return ('bkptline', [cls.ArgType.Unknown])
            case 0xF3:
                return ('timestamp', [cls.ArgType.Unknown])
            case 0xF4:
                return ('0xF4', [cls.ArgType.Unknown])
            case 0xF5:
                return ('0xF5', [cls.ArgType.Unknown])
            case 0xF6:
                return ('0xF6', [cls.ArgType.Unknown])
            case 0xF7:
                return ('0xF7', [cls.ArgType.Unknown])
            case 0xF8:
                return ('0xF8', [cls.ArgType.Unknown])
            case 0xF9:
                return ('0xF9', [cls.ArgType.Unknown])
            case 0xFA:
                return ('0xFA', [cls.ArgType.Unknown])
            case 0xFB:
                return ('0xFB', [cls.ArgType.Unknown])
            case 0xFC:
                return ('0xFC', [cls.ArgType.Unknown])
            case 0xFD:
                return ('0xFD', [cls.ArgType.Unknown])
            case 0xFE:
                return ('0xFE', [cls.ArgType.Unknown])
            case 0xFF:
                return ('0xFF', [cls.ArgType.Unknown])
            case _:
                raise NotImplementedError(f'opcode {cls.opcode} is not implemented')
