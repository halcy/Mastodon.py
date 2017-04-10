#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import requests

from mastodon.exceptions import *
import Mastodon


class ResponseObject(object):
    def __init__(self, response: dict, response_object: requests.models.Response, method: str, params: dict, files: dict, do_ratelimiting: bool, api_base_url: str):
        self._response = None
        self.response = response
        self.response_object = response_object
        self.method = method
        self.params = params
        self.files = files
        self.do_ratelimiting = do_ratelimiting
        self.api_base_url = api_base_url
        self.temp_m = Mastodon("temp")
        
    
    @classmethod
    def _load(cls, response: requests.models.Response, method: str = "GET", params: dict = {}, files = {}, do_ratelimiting = True, api_base_url: str = 'https://mastodon.social'):
        if type(response) is requests.models.Response:
            try:
                r = response.json()
                print("worked")
                return cls(r, response, method, params, files, do_ratelimiting, api_base_url)
            except Exception:
                return None
        else:
            return None
                    
    
    def __iter__(self):
        try:
            while True:
                if 'Link' in self.response_object.headers:
                    tmp_url = requests.utils.parse_header_links(self.response_object.headers['Link'].rstrip('>').replace('>,<', ',<'))
                    next_url = None
                    if tmp_url:
                        for url in tmp_url:
                            if url['rel'] == 'next':
                                next_url = url['url'].replace(self.api_base_url,'')
                                break
                    if next_url is not None:
                        tmp_response = self.temp_m.__api_request(self.method, next_url, params=self.params, files=self.files, do_ratelimiting=self.do_ratelimiting)
                        if type(tmp_response) is dict:
                            self.response = tmp_response
                            yield tmp_response
                        else:
                            return
                else:
                    self.response = self.response_object.json()
                    return self.response_object.json()
        except Exception as e:
            raise e
            
            
    def __repr__(self):
        return '<ResponseObject [%s]>' % (self.response_object.url)
    
    def __str__(self):
        if self.response is None:
            return ""
        elif type(self.response) is str:
            return self.response
        elif type(self.response) is list:
            return "\n".join(self.response)
        elif type(self.response) is dict:
            return json.dumps(self.response)
        else:
            return str(self.response)
    
    def __dict__(self):
        if type(self.response) is not dict:
            return {"response": None}
        else:
            return {"response": self.response}
    
    @property
    def response(self) -> dict:
        return self._response
    
    @response.setter
    def response(self, value: dict):
        self._response = value
        return
    
    def fetch_all(self):
        r = []
        for page in self:
            if page is not None:
                r.append(page)
            else:
                return self.response
        return r