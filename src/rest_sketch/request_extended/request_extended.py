import logging

import requests
from requests import PreparedRequest, Response, Request

from .formatters import format_request_string, format_response_string
from .log_level import LogLevel


def log_request(
        request: Request,
        log_level: LogLevel
):
    request_string = format_request_string(request)
    logging.log(log_level.value, f"{request_string}")


def log_response(
        response: Response,
        log_level: LogLevel
):
    response_string = format_response_string(response)
    logging.log(log_level.value, f"{response_string}")


class ExtSession(requests.Session):
    request_log_level: LogLevel | None = None

    def prepare_request(self, request: Request):
        if self.request_log_level is not None:
            log_request(request, self.request_log_level)
        return super(ExtSession, self).prepare_request(request)

    def send(self, request: PreparedRequest, **kwargs):
        response = super(ExtSession, self).send(request, **kwargs)
        if self.request_log_level is not None:
            log_response(response, self.request_log_level)
        return response


def request(
        method,
        url,
        log_level: LogLevel = None,
        **kwargs):
    with ExtSession() as session:
        if log_level is not None:
            session.request_log_level = log_level
        return session.request(method, url, **kwargs)
