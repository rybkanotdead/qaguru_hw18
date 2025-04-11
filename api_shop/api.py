import requests
import json
import logging
import allure
from allure_commons.types import AttachmentType
from allure import step

from tests.conftest import BASE_URL


class WebShopApi:

    @staticmethod
    def send_request(
        endpoint: str,
        method: str,
        data=None,
        params=None,
        headers=None,
        cookies=None,
        allow_redirects=True,
        timeout=10,
        check_status=True,
    ):
        url = BASE_URL + endpoint

        with step(f"API Request {method} {url}"):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    data=data,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    allow_redirects=allow_redirects,
                    timeout=timeout,
                )
            except requests.exceptions.RequestException as e:
                allure.attach(
                    str(e), "Request Exception", AttachmentType.TEXT, ".txt"
                )
                raise

            allure.attach(
                f"URL: {response.request.url}\n"
                f"Method: {response.request.method}\n"
                f"Headers: {response.request.headers}\n"
                f"Body: {response.request.body}",
                "Request",
                AttachmentType.TEXT,
                ".txt",
            )

            try:
                response_json = response.json()
                allure.attach(
                    json.dumps(response_json, indent=4, ensure_ascii=False),
                    "Response",
                    AttachmentType.JSON,
                    ".json",
                )
            except ValueError:
                allure.attach(response.text, "Response", AttachmentType.TEXT, ".txt")

            allure.attach(
                json.dumps(dict(response.headers), indent=4, ensure_ascii=False),
                "Response Headers",
                AttachmentType.JSON,
                ".json",
            )

            allure.attach(
                str(response.cookies.get_dict()),
                "Cookies",
                AttachmentType.TEXT,
                ".txt",
            )

            logging.info(f"URL: {response.request.url}")
            logging.info(f"Status code: {response.status_code}")
            logging.info(f"Response text: {response.text}")

            if check_status:
                assert response.status_code < 400, f"Bad response: {response.status_code}"

            return response