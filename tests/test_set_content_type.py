"""Tests for the set_content_type event hook."""

import asyncio

import httpx
import pytest

from obsidian_rest_mcp.server import set_content_type


def run(coro):
    return asyncio.run(coro)


def make_request(method: str, body: bytes, extra_headers: dict | None = None) -> httpx.Request:
    headers = {"Authorization": "Bearer test"}
    if extra_headers:
        headers.update(extra_headers)
    return httpx.Request(method, "https://example.com/api", content=body, headers=headers)


def test_post_json_body_sets_application_json():
    req = make_request("POST", b'{"key": "value"}')
    run(set_content_type(req))
    assert req.headers["content-type"] == "application/json"


def test_post_markdown_body_sets_text_markdown():
    req = make_request("POST", b"# My Note\n\nSome content")
    run(set_content_type(req))
    assert req.headers["content-type"] == "text/markdown"


def test_patch_json_body_sets_application_json():
    req = make_request("PATCH", b'{"heading": "Intro", "content": "text"}')
    run(set_content_type(req))
    assert req.headers["content-type"] == "application/json"


def test_patch_markdown_body_sets_text_markdown():
    req = make_request("PATCH", b"plain text content")
    run(set_content_type(req))
    assert req.headers["content-type"] == "text/markdown"


def test_get_request_unchanged():
    req = make_request("GET", b"")
    run(set_content_type(req))
    assert "content-type" not in req.headers


def test_put_request_unchanged():
    req = make_request("PUT", b"some content")
    run(set_content_type(req))
    assert "content-type" not in req.headers


def test_existing_content_type_not_overwritten():
    req = make_request("POST", b'{"x": 1}', {"content-type": "text/plain"})
    run(set_content_type(req))
    assert req.headers["content-type"] == "text/plain"


def test_post_empty_body_no_content_type_set():
    req = make_request("POST", b"")
    run(set_content_type(req))
    assert "content-type" not in req.headers
