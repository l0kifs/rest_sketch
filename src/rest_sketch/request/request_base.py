from abc import ABC, abstractmethod
from dataclasses import dataclass

import requests
from pydantic import BaseModel

from .raw_request import RawRequest
from .method import Method
from .headers_base import HeadersBase
from .params_base import ParamsBase
from ..request_extended.log_level import LogLevel
from ..request_extended.request_extended import request


@dataclass
class RequestBase(ABC):
    base_url: str

    @property
    @abstractmethod
    def method(self) -> Method:
        pass

    @property
    @abstractmethod
    def endpoint(self) -> str:
        pass

    @property
    @abstractmethod
    def params(self) -> ParamsBase | None:
        pass

    @property
    @abstractmethod
    def headers(self) -> HeadersBase | None:
        pass

    @property
    @abstractmethod
    def body(self) -> BaseModel | str | None:
        pass

    def __repr__(self) -> str:
        return self.get_http_repr()

    def get_http_repr(self) -> str:
        request = f"{self.method.value} {self.base_url}{self.endpoint}"
        if self.params:
            request += "?" + "&".join([f"{key}={value}" for key, value in self.params.to_dict().items()])
        if self.headers:
            request += "\n" + "\n".join([f"{key}: {value}" for key, value in self.headers.to_dict().items()])
        if self.body:
            request += "\n\n" + self.body.model_dump_json()
        return request

    def get_curl_repr(self) -> str:
        request = f"curl -X {self.method.value} {self.base_url}{self.endpoint}"
        if self.params:
            request += "?" + "&".join([f"{key}={value}" for key, value in self.params.to_dict().items()])
        if self.headers:
            request += " -H " + " -H ".join([f'"{key}: {value}"' for key, value in self.headers.to_dict().items()])
        if self.body:
            request += f" -d '{self.body.model_dump_json()}'"
        return request

    def get_raw_request(self) -> RawRequest:
        return RawRequest(
            method=self.method,
            url=self.base_url + self.endpoint,
            params=self.params.to_dict() if self.params else None,
            headers=self.headers.to_dict() if self.headers else None,
            body=self.body.model_dump_json() if self.body and isinstance(self.body, BaseModel) else self.body
        )

    def send(
        self,
        log_level: LogLevel | None = None,
        proxies: dict[str, str] | None = None,
        verify: bool | None = None
    ) -> requests.Response:
        response = request(
            method=self.method.value,
            url=self.base_url + self.endpoint,
            params=self.params.to_dict() if self.params else None,
            headers=self.headers.to_dict() if self.headers else None,
            data=self.body.model_dump_json() if self.body and isinstance(self.body, BaseModel) else self.body,
            log_level=log_level,
            proxies=proxies,
            verify=verify
        )
        return response
