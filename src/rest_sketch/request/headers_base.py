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
    """
    Represents the headers of a request.

    The class should be extended to define the headers of a request.

    The class should define attributes that are instances of Header.

    Example:
        class SomeHeaders(HeadersBase):
            def __init__(self):
                self.header1 = Header(key="header1", optional=False, value="value1")
    """
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
