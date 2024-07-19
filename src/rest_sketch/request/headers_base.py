from abc import ABC
from dataclasses import dataclass


@dataclass
class Header:
    """
    Represents a header for a request

    Attributes:
        key: str - the name of the header
        optional: bool - whether the header is optional
        value: str - the value of the header
    """
    key: str
    optional: bool
    value: str = ""


class HeadersBase(ABC):
    def to_dict(self) -> dict:
        """
        Converts the headers to a dictionary
        """
        result = {}
        for key, value in self.__dict__.items():
            if not isinstance(value, Header):
                if not key.startswith("_"):
                    raise ValueError(f"Attribute '{key}' is not an instance of Header")
                continue
            if value.value == "":
                if not value.optional:
                    raise ValueError(f"Header '{value.key}' is not optional but has no value")
                continue
            result[value.key] = value.value
        return result
