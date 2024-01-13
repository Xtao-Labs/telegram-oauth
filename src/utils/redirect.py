import http.cookies
import typing
from datetime import datetime
from email.utils import format_datetime

from starlette.datastructures import MutableHeaders
from starlette.responses import RedirectResponse


class RedirectResponseBuilder:
    def __init__(self):
        self.raw_headers = []

    def set_cookie(
        self,
        key: str,
        value: str = "",
        max_age: typing.Optional[int] = None,
        expires: typing.Optional[typing.Union[datetime, str, int]] = None,
        path: str = "/",
        domain: typing.Optional[str] = None,
        secure: bool = False,
        httponly: bool = False,
        samesite: typing.Optional[typing.Literal["lax", "strict", "none"]] = "lax",
    ) -> None:
        cookie: "http.cookies.BaseCookie[str]" = http.cookies.SimpleCookie()
        cookie[key] = value
        if max_age is not None:
            cookie[key]["max-age"] = max_age
        if expires is not None:
            if isinstance(expires, datetime):
                cookie[key]["expires"] = format_datetime(expires, usegmt=True)
            else:
                cookie[key]["expires"] = expires
        if path is not None:
            cookie[key]["path"] = path
        if domain is not None:
            cookie[key]["domain"] = domain
        if secure:
            cookie[key]["secure"] = True
        if httponly:
            cookie[key]["httponly"] = True
        if samesite is not None:
            assert samesite.lower() in [
                "strict",
                "lax",
                "none",
            ], "samesite must be either 'strict', 'lax' or 'none'"
            cookie[key]["samesite"] = samesite
        cookie_val = cookie.output(header="").strip()
        self.raw_headers.append((b"set-cookie", cookie_val.encode("latin-1")))

    def delete_cookie(
        self,
        key: str,
        path: str = "/",
        domain: typing.Optional[str] = None,
        secure: bool = False,
        httponly: bool = False,
        samesite: typing.Optional[typing.Literal["lax", "strict", "none"]] = "lax",
    ) -> None:
        self.set_cookie(
            key,
            max_age=0,
            expires=0,
            path=path,
            domain=domain,
            secure=secure,
            httponly=httponly,
            samesite=samesite,
        )

    @property
    def headers(self) -> MutableHeaders:
        return MutableHeaders(raw=self.raw_headers)

    def build(self, url: str, status_code: int = 307):
        return RedirectResponse(url, headers=self.headers, status_code=status_code)
