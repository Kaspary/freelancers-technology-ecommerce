from enum import Enum


class BaseEnum(bytes, Enum):

    def __new__(cls, value, label):
        obj = bytes.__new__(cls, [value])
        obj._value_ = value
        obj.label = label
        return obj

    @classmethod
    def get_value(cls, key):
        if key in cls._member_names_:
            return cls[key].value
        return cls(key).value

    @classmethod
    def get_value_or_none(cls, key):
        try:
            return cls.get_value(key)
        except:
            return None
