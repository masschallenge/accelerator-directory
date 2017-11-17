# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from mock import (
    patch,
    MagicMock
)
from django.test import TestCase
from directory.views import IndexView
from django.shortcuts import reverse

ERROR_CODE = 401

SUCCESSFUL_RESPONSE_ATTRS = {"json.return_value": {"results": ["1", "2", "3"]},
                             "status_code": 200}
ERRONEOUS_RESPONSE_ATTRS = {"json.return_value": {
    "detail": "Authentication credentials were not provided."},
    "status_code": ERROR_CODE}


def fake_successful_response(*args, **kwargs):
    magic_mock = MagicMock()
    magic_mock.configure_mock(**SUCCESSFUL_RESPONSE_ATTRS)
    return magic_mock


def fake_failed_response(*args, **kwargs):
    magic_mock = MagicMock()
    magic_mock.configure_mock(**ERRONEOUS_RESPONSE_ATTRS)
    return magic_mock


class TestIndexView(TestCase):
    url = reverse(IndexView.view_name)

    def test_index_view_loads_successfully(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context["results"]), 0)

    @patch("directory.views.index_view.request", fake_successful_response)
    def test_index_view_returns_results_to_context(self):
        response = self.client.get(self.url + "?name=foo")
        self.assertGreater(len(response.context["results"]), 0)

    @patch("directory.views.index_view.request", fake_failed_response)
    def test_index_view_shows_error_message_in_context(self):
        response = self.client.get(self.url + "?name=foo")
        self.assertEquals(len(response.context["results"]), 0)
        self.assertEquals(response.context["status_code"], ERROR_CODE)
