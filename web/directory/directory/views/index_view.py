# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import requests
from django.views.generic import TemplateView

from django.conf import settings

ORGANIZATION_LIST_VIEW_URL_PATH = "api/v1/organization/"
DEFAULT_LIMIT = "50"


class IndexView(TemplateView):
    view_name = "home_page_view"
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        name = self.request.GET.get("name")
        if not name:
            return {"results": []}
        response = filter_organizations_by_name(name)
        data = response.json()
        if response.status_code < 400:
            return {"results": data.get("results", []),
                    "current": name}
        return {"results": [],
                "status_code": response.status_code,
                "error_detail": data.get("detail")}


def filter_organizations_by_name(name):
    url = _organization_list_url(name)
    return request(url, _headers())


def request(url, headers):
    return requests.request("GET", url, headers=headers)  # pragma: no cover


def _organization_list_url(name):
    return ("{}/{}?limit={}&name={}".format(
        settings.IMPACT_API_URL,
        ORGANIZATION_LIST_VIEW_URL_PATH,
        DEFAULT_LIMIT,
        name))


def _headers():
    return {"content-type": "application/x-www-form-urlencoded",
            "accept": "application/json; indent=4",
            "authorization": ("Bearer {}".format(
                settings.IMPACT_API_ACCESS_TOKEN)),
            "cache-control": "no-cache"}
