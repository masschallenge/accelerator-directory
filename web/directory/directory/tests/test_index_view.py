from mock import (
    patch,
    MagicMock
)
from django.test import TestCase
from directory.views import IndexView
from django.shortcuts import reverse


def fake_json_response(*args, **kwargs):
    magic_mock = MagicMock()
    attrs = {'json.return_value': {"results": ["1", "2", "3"]}}
    magic_mock.configure_mock(**attrs)
    return magic_mock


class TestIndexView(TestCase):
    url = reverse(IndexView.view_name)

    def test_index_view_loads_successfully(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context["results"]), 0)

    @patch("directory.views.index_view.request", fake_json_response)
    def test_index_view_returns_results_to_context(self):
        response = self.client.get(self.url + '?name=foo')
        self.assertGreater(len(response.context["results"]), 0)

        pass
