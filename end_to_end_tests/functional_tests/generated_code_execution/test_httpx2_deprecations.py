import asyncio
import ssl
import warnings

import httpx2 as httpx

from end_to_end_tests.functional_tests.helpers import (
    with_generated_client_fixture,
    with_generated_code_import,
)


def _recording_transport(seen: list[httpx.Request]) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={})

    return httpx.MockTransport(handler)


@with_generated_client_fixture(
    """
paths:
  "/with-cookie":
    get:
      operationId: getWithCookie
      parameters:
        - name: session
          in: cookie
          required: true
          schema:
            type: string
      responses:
        "200":
          description: Success
"""
)
@with_generated_code_import(".api.default.get_with_cookie.sync_detailed")
@with_generated_code_import(".api.default.get_with_cookie.asyncio_detailed")
@with_generated_code_import(".client.Client")
class TestCookieParameters:
    def test_sync_sends_cookie_param_without_deprecation_warning(self, sync_detailed, Client):
        seen: list[httpx.Request] = []
        client = Client(
            base_url="https://api.example.com",
            cookies={"client": "c"},
            httpx_args={"transport": _recording_transport(seen)},
        )

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            sync_detailed(client=client, session="abc")

        assert seen[0].headers["Cookie"] == "client=c; session=abc"
        # The per-request cookie must not leak into the client's cookie jar
        assert dict(client.get_httpx_client().cookies) == {"client": "c"}

    def test_async_sends_cookie_param_without_deprecation_warning(self, asyncio_detailed, Client):
        seen: list[httpx.Request] = []
        client = Client(
            base_url="https://api.example.com",
            cookies={"client": "c"},
            httpx_args={"transport": _recording_transport(seen)},
        )

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            asyncio.run(asyncio_detailed(client=client, session="abc"))

        assert seen[0].headers["Cookie"] == "client=c; session=abc"
        assert dict(client.get_async_httpx_client().cookies) == {"client": "c"}


@with_generated_client_fixture(
    """
paths: {}
"""
)
@with_generated_code_import(".client.Client")
class TestVerifySslPath:
    def test_ca_directory_builds_ssl_context_without_deprecation_warning(self, Client, tmp_path):
        client = Client(base_url="https://api.example.com", verify_ssl=str(tmp_path))

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            client.get_httpx_client()
            client.get_async_httpx_client()

    def test_ca_file_is_passed_as_cafile(self, Client, tmp_path, monkeypatch):
        calls: list[dict[str, str]] = []
        real_create_default_context = ssl.create_default_context

        def spy(**kwargs: str) -> ssl.SSLContext:
            calls.append(kwargs)
            return real_create_default_context()

        monkeypatch.setattr(ssl, "create_default_context", spy)
        ca_file = tmp_path / "ca.pem"
        ca_file.write_text("")
        client = Client(base_url="https://api.example.com", verify_ssl=str(ca_file))

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            client.get_httpx_client()

        assert calls == [{"cafile": str(ca_file)}]
