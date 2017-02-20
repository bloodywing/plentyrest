# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import plentymarkets_compliance_fix
import logging
from pprint import pformat

logging.basicConfig()

logger = logging.getLogger()
logger.setLevel(logging.WARN)


class Plenty(object):

    def __init__(self, oauth_domain, username=None, password=None, access_token=None, ):
        self.domain = oauth_domain
        self.lastresponse = None
        token_url = 'https://%s/rest/login' % oauth_domain
        refresh_url = 'https://%s/rest/login/refresh' % oauth_domain

        if access_token:
            token = {
                'access_token': access_token,
                'token_type': 'Bearer'
            }

            extra = None

        else:
            token = None
            extra = None

        session = OAuth2Session(client=LegacyApplicationClient('plenty-rest'),
                                auto_refresh_url=refresh_url,
                                auto_refresh_kwargs=extra,
                                token=token,
                                token_updater=self.token_saver)
        self.session = plentymarkets_compliance_fix(session)
        self.token = token

        if not access_token:
            self.token = self.session.fetch_token(token_url=token_url,
                                                  username=username,
                                                  password=password)

    def token_saver(self, token):
        return NotImplementedError

    def request(self, path, method='GET', params=None, data=None, json=None):
        path = path.lstrip('/')
        response = self.session.request(method, 'https://%s/%s' % (self.domain, path), params=params, data=data, json=json)
        self.lastresponse = response
        logging.info(pformat(response.json()))
        if 'json' in response.headers['content-type']:
            return response.json()
        return response.content
