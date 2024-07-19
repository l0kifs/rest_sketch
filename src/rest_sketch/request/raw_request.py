from dataclasses import dataclass

import requests

from .method import Method
from ..request_extended.log_level import LogLevel
from ..request_extended.request_extended import request


@dataclass
class RawRequest:
    method: Method
    url: str
    params: dict | None = None
    headers: dict | None = None
    body: str | None = None

    def send(
        self,
        log_level: LogLevel | None = None,
        proxies: dict[str, str] | None = None,
        verify: bool | None = None
    ) -> requests.Response:
        response = request(
            method=self.method.value,
            url=self.url,
            params=self.params,
            headers=self.headers,
            data=self.body,
            log_level=log_level,
            proxies=proxies,
            verify=verify
        )
        return response
