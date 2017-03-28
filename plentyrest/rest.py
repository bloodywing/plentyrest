# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import plentymarkets_compliance_fix
import logging
from pprint import pformat


class Plenty(object):

    def __init__(self, oauth_domain, username=None, password=None, access_token=None):
        self.domain = oauth_domain
        self.lastresponse = None
        token_url = 'https://%s/rest/login' % oauth_domain
        refresh_url = 'https://%s/rest/login/refresh' % oauth_domain

        if access_token:
            token = {
                'access_token': access_token,
                'token_type': 'Bearer'
            }
        else:
            token = None

        session = OAuth2Session(client=LegacyApplicationClient('plenty-rest'),
                                auto_refresh_url=refresh_url,
                                token=token,
                                token_updater=self.token_saver)
        self.session = plentymarkets_compliance_fix(session)
        self.token = token

        if not access_token:
            self.token = self.session.fetch_token(token_url=token_url,
                                                  username=username,
                                                  password=password)

    def token_saver(self, token):
        return NotImplemented

    def request(self, path, method='GET', params=None, data=None, json=None):
        path = path.lstrip('/')
        response = self.session.request(method, 'https://%s/%s' % (self.domain, path), params=params, data=data, json=json)
        self.lastresponse = response
        if 'json' in response.headers['content-type']:
            logging.info(pformat(response.json()))
            return response.json()
        logging.info(pformat(response.content))
        return response.content
