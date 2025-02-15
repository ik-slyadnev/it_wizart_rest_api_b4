import json
import allure
import curlify


def allure_attach(fn):
    def wrapper(*args, **kwargs):
        body = kwargs.get("json")
        if body:
            allure.attach(
                json.dumps(body, indent=4),
                name="request_body",
                attachment_type=allure.attachment_type.JSON
            )

        response = fn(*args, **kwargs)
        curl = curlify.to_curl(response.request)
        allure.attach(
            curl,
            name="request",
            attachment_type=allure.attachment_type.TEXT
        )

        try:
            response_json = response.json()
            allure.attach(
                json.dumps(response_json, indent=4),
                name="response_body",
                attachment_type=allure.attachment_type.JSON
            )
        except json.decoder.JSONDecodeError:
            response_text = response.text
            status_code = f"status code = {response.status_code}"
            allure.attach(
                response_text if len(response_text) > 0 else status_code,
                name="response_body",
                attachment_type=allure.attachment_type.TEXT
            )

        return response

    return wrapper


