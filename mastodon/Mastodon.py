# coding: utf-8

import requests
import os
import os.path
import mimetypes
import time
import random
import string

class Mastodon:
    """ 
    Super basic but thorough and easy to use mastodon.social 
    api wrapper in python.
        
    If anything is unclear, check the official API docs at
    https://github.com/Gargron/mastodon/wiki/API
        
    Presently, only username-password login is supported, somebody please
    patch in Real Proper OAuth if desired.
    """
    __DEFAULT_BASE_URL = 'https://mastodon.social'
    
    ###
    # Registering apps
    ###
    @staticmethod    
    def create_app(client_name, scopes = ['read', 'write', 'follow'], redirect_uris = None, to_file = None, api_base_url = __DEFAULT_BASE_URL):                 
        """
        Creates a new app with given client_name and scopes (read, write, follow)
        
        Specify redirect_uris if you want users to be redirected to a certain page after authenticating.
        Specify to_file to persist your apps info to a file so you can use them in the constructor.
        Specify api_base_url if you want to register an app on an instance different from the flagship one.
           
        Returns client_id and client_secret.
        """
        request_data = {
            'client_name': client_name,
            'scopes': " ".join(scopes)
        }
        
        if redirect_uris != None:
            request_data['redirect_uris'] = redirect_uris;
        else:
            request_data['redirect_uris'] = 'urn:ietf:wg:oauth:2.0:oob';
        
        response = requests.post(api_base_url + '/api/v1/apps', data = request_data).json()
        
        if to_file != None:
            with open(to_file, 'w') as secret_file:
                secret_file.write(response['client_id'] + '\n')
                secret_file.write(response['client_secret'] + '\n')
        
        return (response['client_id'], response['client_secret'])
    
    ###
    # Authentication, including constructor
    ###
    def __init__(self, client_id, client_secret = None, access_token = None, api_base_url = __DEFAULT_BASE_URL, debug_requests = False):
        """
        Creates a new API wrapper instance based on the given client_secret and client_id. If you
        give a client_id and it is not a file, you must also give a secret.
           
        You can also directly specify an access_token, directly or as a file.
            
        Specify api_base_url if you wish to talk to an instance other than the flagship one.
        If a file is given as client_id, read client ID and secret from that file
        """
        self.api_base_url = api_base_url
        self.client_id = client_id                      
        self.client_secret = client_secret
        self.access_token = access_token
        self.debug_requests = debug_requests
        
        if os.path.isfile(self.client_id):
            with open(self.client_id, 'r') as secret_file:
                self.client_id = secret_file.readline().rstrip()
                self.client_secret = secret_file.readline().rstrip()
        else:
            if self.client_secret == None:
                raise ValueError('Specified client id directly, but did not supply secret')
                
        if self.access_token != None and os.path.isfile(self.access_token):
            with open(self.access_token, 'r') as token_file:
                self.access_token = token_file.readline().rstrip()
                
    def log_in(self, username, password, scopes = ['read', 'write', 'follow'], to_file = None):
        """
        Logs in and sets access_token to what was returned.
        Can persist access token to file.
        
        Will throw an exception if username / password are wrong, scopes are not
        valid or granted scopes differ from requested.
        
        Returns the access_token, as well.
        """
        params = self.__generate_params(locals())
        params['client_id'] = self.client_id
        params['client_secret'] = self.client_secret
        params['grant_type'] = 'password'
        params['scope'] = " ".join(scopes)
        
        try:
            response = self.__api_request('POST', '/oauth/token', params)      
            self.access_token = response['access_token']
        except:
            raise ValueError('Invalid user name, password or scopes.')
        
        requested_scopes = " ".join(sorted(scopes))
        received_scopes = " ".join(sorted(response["scope"].split(" ")))
        
        if requested_scopes != received_scopes:
            raise ValueError('Granted scopes "' + received_scopes + '" differ from requested scopes "' + requested_scopes + '".')
        
        if to_file != None:
            with open(to_file, 'w') as token_file:
                token_file.write(response['access_token'] + '\n')
        
        return response['access_token']
    
    ###
    # Reading data: Timelines
    ##
    def timeline(self, timeline = "home", max_id = None, since_id = None, limit = None):
        """
        Returns statuses, most recent ones first. Timeline can be home, mentions, public
        or tag/hashtag. See the following functions documentation for what those do.
        
        The default timeline is the "home" timeline.
        """
        params = self.__generate_params(locals(), ['timeline'])
        return self.__api_request('GET', '/api/v1/timelines/' + timeline, params)
    
    def timeline_home(self, max_id = None, since_id = None, limit = None):
        """
        Returns the authenticated users home timeline (i.e. followed users and self).
        """
        return self.timeline('home', max_id = max_id, since_id = since_id, limit = limit)
    
    def timeline_mentions(self, max_id = None, since_id = None, limit = None):
        """
        Returns the authenticated users mentions.
        """
        return self.timeline('mentions', max_id = max_id, since_id = since_id, limit = limit)
    
    def timeline_public(self, max_id = None, since_id = None, limit = None):
        """
        Returns the public / visible-network timeline.
        """
        return self.timeline('public', max_id = max_id, since_id = since_id, limit = limit)
    
    def timeline_hashtag(self, hashtag, max_id = None, since_id = None, limit = None):
        """
        Returns all toots with a given hashtag.
        """
        return self.timeline('tag/' + str(hashtag), max_id = max_id, since_id = since_id, limit = limit)
    
    ###
    # Reading data: Statuses
    ###
    def status(self, id):
        """
        Returns a status.
        """
        return self.__api_request('GET', '/api/v1/statuses/' + str(id))

    def status_context(self, id):
        """
        Returns ancestors and descendants of the status.
        """
        return self.__api_request('GET', '/api/v1/statuses/' + str(id) + '/context')
    
    def status_reblogged_by(self, id):
        """
        Returns a list of users that have reblogged a status.
        """
        return self.__api_request('GET', '/api/v1/statuses/' + str(id) + '/reblogged_by')
    
    def status_favourited_by(self, id):
        """
        Returns a list of users that have favourited a status.
        """
        return self.__api_request('GET', '/api/v1/statuses/' + str(id) + '/favourited_by')
    
    ###
    # Reading data: Notifications
    ###
    def notifications(self):
        """
        Returns notifications (mentions, favourites, reblogs, follows) for the authenticated
        user.
        """
        return self.__api_request('GET', '/api/v1/notifications')
    
    ###
    # Reading data: Accounts
    ###
    def account(self, id):
        """
        Returns account.
        """
        return self.__api_request('GET', '/api/v1/accounts/' + str(id))

    def account_verify_credentials(self):
        """
        Returns authenticated user's account.
        """
        return self.__api_request('GET', '/api/v1/accounts/verify_credentials')
    
    def account_statuses(self, id, max_id = None, since_id = None, limit = None):
        """
        Returns statuses by user. Same options as timeline are permitted.
        """
        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('GET', '/api/v1/accounts/' + str(id) + '/statuses', params)

    def account_following(self, id):
        """
        Returns users the given user is following.
        """
        return self.__api_request('GET', '/api/v1/accounts/' + str(id) + '/following')

    def account_followers(self, id):
        """
        Returns users the given user is followed by.
        """
        return self.__api_request('GET', '/api/v1/accounts/' + str(id) + '/followers')

    def account_relationships(self, id):
        """
        Returns relationships (following, followed_by, blocking) of the logged in user to 
        a given account. id can be a list.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/accounts/relationships', params)
    
    def account_suggestions(self):
        """
        Returns accounts that the system suggests the authenticated user to follow.
        """
        return self.__api_request('GET', '/api/v1/accounts/suggestions') 

    def account_search(self, q, limit = None):
        """
        Returns matching accounts. Will lookup an account remotely if the search term is 
        in the username@domain format and not yet in the database.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/accounts/search', params)
    
    ###
    # Writing data: Statuses
    ###
    def status_post(self, status, in_reply_to_id = None, media_ids = None):
        """
        Posts a status. Can optionally be in reply to another status and contain
        up to four pieces of media (Uploaded via media_post()).
           
        Returns the new status.
        """
        params = self.__generate_params(locals())
        return self.__api_request('POST', '/api/v1/statuses', params)
    
    def toot(self, status):
        """
        Synonym for status_post that only takes the status text as input.
        """
        return self.status_post(status)
        
    def status_delete(self, id):
        """
        Deletes a status
        """
        return self.__api_request('DELETE', '/api/v1/statuses/' + str(id))

    def status_reblog(self, id):
        """Reblogs a status.
        
        Returns a new status that wraps around the reblogged one."""
        return self.__api_request('POST', '/api/v1/statuses/' + str(id) + "/reblog")

    def status_unreblog(self, id):
        """
        Un-reblogs a status.
        
        Returns the status that used to be reblogged.
        """
        return self.__api_request('POST', '/api/v1/statuses/' + str(id) + "/unreblog")

    def status_favourite(self, id):
        """
        Favourites a status.
        
        Returns the favourited status.
        """
        return self.__api_request('POST', '/api/v1/statuses/' + str(id) + "/favourite")
    
    def status_unfavourite(self, id):
        """Favourites a status.
        
        Returns the un-favourited status.
        """
        return self.__api_request('POST', '/api/v1/statuses/' + str(id) + "/unfavourite")
    
    ###
    # Writing data: Accounts
    ###
    def account_follow(self, id):
        """
        Follows a user.
        
        Returns the updated relationship to the user.
        """
        return self.__api_request('POST', '/api/v1/accounts/' + str(id) + "/follow")
    
    def account_unfollow(self, id):
        """
        Unfollows a user.
        
        Returns the updated relationship to the user.
        """
        return self.__api_request('POST', '/api/v1/accounts/' + str(id) + "/unfollow")
    
    def account_block(self, id):
        """
        Blocks a user.
        
        Returns the updated relationship to the user.
        """
        return self.__api_request('POST', '/api/v1/accounts/' + str(id) + "/block")
    
    def account_unblock(self, id):
        """
        Unblocks a user.
        
        Returns the updated relationship to the user.
        """
        return self.__api_request('POST', '/api/v1/accounts/' + str(id) + "/unblock")

    ###
    # Writing data: Media
    ###
    def media_post(self, media_file, mime_type = None):
        """
        Posts an image. media_file can either be image data or
        a file name. If image data is passed directly, the mime
        type has to be specified manually, otherwise, it is
        determined from the file name.
        
        Returns the uploaded media metadata object. Importantly, this contains 
        the ID that can then be used in status_post() to attach the media to
        a toot.
        
        Throws a ValueError if the mime type of the passed data or file can
        not be determined properly.
        """
        
        if os.path.isfile(media_file):
            mime_type = mimetypes.guess_type(media_file)[0]
            media_file = open(media_file, 'rb')
            
        if mime_type == None:
            raise ValueError('Could not determine mime type or data passed directly without mime type.')
        
        random_suffix = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        file_name = "mastodonpyupload_" + str(time.time()) + "_" + str(random_suffix) + mimetypes.guess_extension(mime_type)
        
        media_file_description = (file_name, media_file, mime_type)
        return self.__api_request('POST', '/api/v1/media', files = {'file': media_file_description})
    
    ###
    # Internal helpers, dragons probably
    ###
    def __api_request(self, method, endpoint, params = {}, files = {}):
        """
        Internal API request helper.
        """
        response = None
        headers = None
        

        if self.access_token != None:
            headers = {'Authorization': 'Bearer ' + self.access_token}
        
        if self.debug_requests == True:
            print('Mastodon: Request to endpoint "' + endpoint + '" using method "' + method + '".')
            print('Parameters: ' + str(params))
            print('Headers: ' + str(headers))
            print('Files: ' + str(files))

        if method == 'GET':
            response = requests.get(self.api_base_url + endpoint, data = params, headers = headers, files = files)
        
        if method == 'POST':
            response = requests.post(self.api_base_url + endpoint, data = params, headers = headers, files = files)
            
        if method == 'DELETE':
            response = requests.delete(self.api_base_url + endpoint, data = params, headers = headers, files = files)
        
        if response.status_code == 404:
            raise IOError('Endpoint not found.')
        
        if response.status_code == 500:
            raise IOError('General API problem.')
        
        try:
            response = response.json()
        except:
            raise ValueError("Could not parse response as JSON, respose code was " + str(response.status_code))
        
        return response
    
    def __generate_params(self, params, exclude = []):
        """
        Internal named-parameters-to-dict helper.
        """
        params = dict(params)
        
        del params['self']
        param_keys = list(params.keys())
        for key in param_keys:
            if params[key] == None or key in exclude:
                del params[key]
        
        param_keys = list(params.keys())
        for key in param_keys:
            if isinstance(params[key], list):
                params[key + "[]"] = params[key]
                del params[key]
                
        return params
