from abc import ABC
from dataclasses import dataclass


@dataclass
class Param:
    """
    Represents a parameter for a request

    Attributes:
        key: str - the name of the parameter
        optional: bool - whether the parameter is optional
        value: str - the value of the parameter
    """
    key: str
    optional: bool
    value: str = ""


class ParamsBase(ABC):
    """
    Represents the parameters of a request.

    The class should be extended to define the parameters of a request.

    The class should define attributes that are instances of Param.

    Example:
    class SomeParams(ParamsBase):
    def __init__(self):
        self.param1 = Param(key="param", optional=False, value="value1")
    """
    def to_dict(self) -> dict:
        """
        Converts the parameters to a dictionary.
        """
        result = {}
        for key, value in self.__dict__.items():
            if not isinstance(value, Param):
                if not key.startswith("_"):
                    raise ValueError(f"Attribute '{key}' is not an instance of Param")
                continue
            if value.value == "":
                if not value.optional:
                    raise ValueError(f"Param '{value.key}' is not optional but has no value")
                continue
            result[value.key] = value.value
        return result
