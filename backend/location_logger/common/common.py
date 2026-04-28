from fastapi import Response


def set_common_response_header(response: Response):
    response.headers['Cache-Control'] = 'no-cache, no-store'
