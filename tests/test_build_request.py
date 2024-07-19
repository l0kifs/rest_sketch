from pydantic import BaseModel
from rest_sketch.request.headers_base import HeadersBase, Header
from rest_sketch.request.params_base import ParamsBase, Param
from rest_sketch.request.request_base import RequestBase
from rest_sketch.request.method import Method


def test_build_request():
    class SomeParams(ParamsBase):
        def __init__(self):
            self.param1 = Param(key="param1", optional=False, value="value1")
            self.param2 = Param(key="param2", optional=True)

    class SomeHeaders(HeadersBase):
        def __init__(self):
            self.header1 = Header(key="header1", optional=False, value="value1")
            self.header2 = Header(key="header2", optional=True)

    class SomeBody(BaseModel):
        key: str
        value: str

    class SomeRequest(RequestBase):
        @property
        def method(self):
            return Method.POST

        @property
        def endpoint(self) -> str:
            return '/some_endpoint'

        @property
        def params(self) -> SomeParams:
            return SomeParams()

        @property
        def headers(self) -> SomeHeaders:
            return SomeHeaders()

        @property
        def body(self) -> SomeBody:
            return SomeBody(key="default", value="default")

    print(SomeRequest("http://localhost:8000").get_raw_request())
