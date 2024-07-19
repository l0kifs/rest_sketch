import json

from requests import Response, Request


def is_json(json_string: str) -> bool:
    try:
        json.loads(json_string)
    except ValueError:
        return False
    return True


def format_request_string(request: Request):
    """Format request to string.
    
    Example:
        GET http://example.com
        Content-Type: application/json
        Authorization: Bearer token
        {
            "key": "value"
        }

    Args:
        request (Request): request from requests library

    Returns:
        str: request string
    """
    request_string = f'{request.method} {request.url}'
    if request.params:
        params_string = '&'.join([f"{key}={value}" for key, value in request.params.items()])
        request_string += f'?{params_string}'
    if request.headers:
        headers_string = '\n'.join([f"{key}: {value}" for key, value in request.headers.items()])
        request_string += f'\n{headers_string}'
    if request.json:
        body_string = json.dumps(request.json, indent=4)
        request_string += f'\n{body_string}'
    else:
        body_string = str(request.data)
        request_string += f'\n{body_string}'
    return request_string


def format_response_string(response: Response):
    """Format response to string.
    
    Example:
        200 OK
        Content-Type: application/json
        {
            "key": "value"
        }

    Args:
        response (Response): response from requests library

    Returns:
        str: response string
    """
    response_string = f'{response.status_code} {response.reason}'
    if response.headers:
        headers_string = '\n'.join([f"{key}: {value}" for key, value in response.headers.items()])
        response_string += f'\n{headers_string}'
    if response.text:
        if is_json(response.text):
            body_string = json.dumps(json.loads(response.text), indent=4)
        else:
            body_string = response.text
        response_string += f'\n{body_string}'
    return response_string


def format_request_curl(request: Request):
    """Format request to curl command.
    
    Example:
        curl -X POST -H "Content-Type: application/json" -d '{"key": "value"}' http://example.com

    Args:
        request (Request): request from requests library

    Returns:
        str: curl command
    """
    curl_command = f"curl -X {request.method}"
    if request.headers:
        curl_command = curl_command + ' -H ' + ' -H '.join([f'"{k}: {v}"' for k, v in request.headers.items()])
    if request.data:
        curl_command = curl_command + f" -d \'{request.data}\'"
    curl_command = curl_command + f" {request.url}"
    if request.params:
        params_string = '&'.join([f"{key}={value}" for key, value in request.params.items()])
        curl_command += f'?{params_string}'
    return curl_command
