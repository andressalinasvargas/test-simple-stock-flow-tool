"""Pure HTTP client for Simple Stock Flow API using standard library urllib."""

import json
import urllib.error
import urllib.request
from typing import Any, Dict, Optional


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.token: Optional[str] = None

    def set_token(self, token: str) -> None:
        self.token = token

    def request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        url = f"{self.base_url}{path}"
        req_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if self.token:
            req_headers["Authorization"] = f"Bearer {self.token}"
        if headers:
            req_headers.update(headers)

        body_bytes = json.dumps(data).encode("utf-8") if data is not None else None
        req = urllib.request.Request(url, data=body_bytes, headers=req_headers, method=method)

        try:
            with urllib.request.urlopen(req) as resp:
                status = resp.status
                if status == 204:
                    return None
                resp_bytes = resp.read()
                if not resp_bytes:
                    return None
                return json.loads(resp_bytes.decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {e.code} on {method} {path}: {err_body}") from e
