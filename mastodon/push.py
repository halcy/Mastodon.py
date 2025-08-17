# push.py - webpush endpoints and tooling

import base64
import os
import json

from mastodon.errors import MastodonIllegalArgumentError
from mastodon.utility import api_version
from mastodon.compat import IMPL_HAS_CRYPTO, ec, serialization, default_backend
from mastodon.compat import IMPL_HAS_ECE, http_ece

from mastodon.internals import Mastodon as Internals
from mastodon.return_types import WebpushCryptoParamsPubkey, WebpushCryptoParamsPrivkey, WebPushSubscription, PushNotification, try_cast_recurse
from typing import Optional, Tuple

class Mastodon(Internals):
    ###
    # Reading data: Webpush subscriptions
    ###
    @api_version("2.4.0", "2.4.0")
    def push_subscription(self) -> WebPushSubscription:
        """
        Fetch the current push subscription the logged-in user has for this app.

        Only one webpush subscription can be active at a time for any given app.
        """
        return self.__api_request('GET', '/api/v1/push/subscription')

    ###
    # Writing data: Push subscriptions
    ###
    @api_version("2.4.0", "4..0")
    def push_subscription_set(self, endpoint: str, encrypt_params: WebpushCryptoParamsPubkey, follow_events: Optional[bool] = None,
                              favourite_events: Optional[bool] = None, reblog_events: Optional[bool] = None,
                              mention_events: Optional[bool] = None, poll_events: Optional[bool] = None,
                              follow_request_events: Optional[bool] = None, status_events: Optional[bool] = None, 
                              policy: str = 'all', update_events: Optional[bool] = None, admin_sign_up_events: Optional[bool] = None,
                              admin_report_events: Optional[bool] = None, standard: bool = None) -> WebPushSubscription:
        """
        Sets up or modifies the push subscription the logged-in user has for this app.

        `endpoint` is the endpoint URL mastodon should call for pushes. Note that mastodon
        requires https for this URL. `encrypt_params` is a dict with key parameters that allow
        the server to encrypt data for you: A public key `pubkey` and a shared secret `auth`.
        You can generate this as well as the corresponding private key using the
        :ref:`push_subscription_generate_keys() <push_subscription_generate_keys()>` function.

        `policy` controls what sources will generate webpush events. Valid values are
        `all`, `none`, `follower` and `followed`.

        The rest of the parameters controls what kind of events you wish to subscribe to.
        Events whose names start with "admin" require admin privileges to subscribe to.

        * `follow_events` controls whether you receive events when someone follows the logged in user.
        * `favourite_events` controls whether you receive events when someone favourites one of the logged in users statuses.
        * `reblog_events` controls whether you receive events when someone boosts one of the logged in users statuses.
        * `mention_events` controls whether you receive events when someone mentions the logged in user in a status.
        * `poll_events` controls whether you receive events when a poll the logged in user has voted in has ended.
        * `follow_request_events` controls whether you receive events when someone requests to follow the logged in user.
        * `status_events` controls whether you receive events when someone the logged in user has subscribed to notifications for posts a new status.
        * `update_events` controls whether you receive events when a status that the logged in user has boosted has been edited.
        * `admin_sign_up_events` controls whether you receive events when a new user signs up.
        * `admin_report_events` controls whether you receive events when a new report is received.

        Pass `standard=True` to use the standard webpush subscription format, instead of the pre-release RFC format
        mastodon was using before.
        """
        if not policy in ['all', 'none', 'follower', 'followed']:
            raise MastodonIllegalArgumentError("Valid values for policy are 'all', 'none', 'follower' or 'followed'.")

        endpoint = Mastodon.__protocolize(endpoint)

        push_pubkey_b64 = base64.b64encode(encrypt_params['pubkey'])
        push_auth_b64 = base64.b64encode(encrypt_params['auth'])

        params = {
            'subscription[endpoint]': endpoint,
            'subscription[keys][p256dh]': push_pubkey_b64,
            'subscription[keys][auth]': push_auth_b64,
            'policy': policy
        }

        if follow_events is not None:
            params['data[alerts][follow]'] = follow_events

        if favourite_events is not None:
            params['data[alerts][favourite]'] = favourite_events

        if reblog_events is not None:
            params['data[alerts][reblog]'] = reblog_events

        if mention_events is not None:
            params['data[alerts][mention]'] = mention_events

        if poll_events is not None:
            params['data[alerts][poll]'] = poll_events

        if follow_request_events is not None:
            params['data[alerts][follow_request]'] = follow_request_events

        if follow_request_events is not None:
            params['data[alerts][status]'] = status_events

        if update_events is not None:
            params['data[alerts][update]'] = update_events
        
        if admin_sign_up_events is not None:
            params['data[alerts][admin.sign_up]'] = admin_sign_up_events
        
        if admin_report_events is not None:
            params['data[alerts][admin.report]'] = admin_report_events

        # Canonicalize booleans
        params = self.__generate_params(params)

        return self.__api_request('POST', '/api/v1/push/subscription', params)

    @api_version("2.4.0", "2.4.0")
    def push_subscription_update(self, follow_events: Optional[bool] = None,
                              favourite_events: Optional[bool] = None, reblog_events: Optional[bool] = None,
                              mention_events: Optional[bool] = None, poll_events: Optional[bool] = None,
                              follow_request_events: Optional[bool] = None, status_events: Optional[bool] = None, 
                              policy: Optional[str] = 'all', update_events: Optional[bool] = None, admin_sign_up_events: Optional[bool] = None,
                              admin_report_events: Optional[bool] = None) -> WebPushSubscription:
        """
        Modifies what kind of events the app wishes to subscribe to.

        Parameters are as in push_subscription_set().

        Returned object reflects the updated push subscription.
        """
        params = {}
        if policy is not None:
            params['policy'] = policy

        if follow_events is not None:
            params['data[alerts][follow]'] = follow_events

        if favourite_events is not None:
            params['data[alerts][favourite]'] = favourite_events

        if reblog_events is not None:
            params['data[alerts][reblog]'] = reblog_events

        if mention_events is not None:
            params['data[alerts][mention]'] = mention_events

        if poll_events is not None:
            params['data[alerts][poll]'] = poll_events

        if follow_request_events is not None:
            params['data[alerts][follow_request]'] = follow_request_events

        if follow_request_events is not None:
            params['data[alerts][status]'] = status_events

        if update_events is not None:
            params['data[alerts][update]'] = update_events
        
        if admin_sign_up_events is not None:
            params['data[alerts][admin.sign_up]'] = admin_sign_up_events
        
        if admin_report_events is not None:
            params['data[alerts][admin.report]'] = admin_report_events

        # Canonicalize booleans
        params = self.__generate_params(params)

        return self.__api_request('PUT', '/api/v1/push/subscription', params)

    @api_version("2.4.0", "2.4.0")
    def push_subscription_delete(self):
        """
        Remove the current push subscription the logged-in user has for this app.
        """
        self.__api_request('DELETE', '/api/v1/push/subscription')

    ###
    # Push subscription crypto utilities
    ###
    def push_subscription_generate_keys(self) -> Tuple[WebpushCryptoParamsPubkey, WebpushCryptoParamsPrivkey]:
        """
        Generates a private key, public key and shared secret for use in webpush subscriptions.

        Returns two dicts: One with the private key and shared secret and another with the
        public key and shared secret.
        """
        if not IMPL_HAS_CRYPTO:
            raise NotImplementedError('To use the crypto tools, please install the webpush feature dependencies.')

        push_key_pair = ec.generate_private_key(ec.SECP256R1(), default_backend())
        push_key_priv = push_key_pair.private_numbers().private_value
        try:
            push_key_pub = push_key_pair.public_key().public_bytes(
                serialization.Encoding.X962,
                serialization.PublicFormat.UncompressedPoint,
            )
        except:
            push_key_pub = push_key_pair.public_key().public_numbers().encode_point()

        push_shared_secret = os.urandom(16)

        priv_dict = {
            'privkey': push_key_priv,
            'auth': push_shared_secret
        }

        pub_dict = {
            'pubkey': push_key_pub,
            'auth': push_shared_secret
        }

        return priv_dict, pub_dict

    @api_version("2.4.0", "2.4.0")
    def push_subscription_decrypt_push(self, data: bytes, decrypt_params: WebpushCryptoParamsPrivkey, encryption_header: str, crypto_key_header: str) -> PushNotification:
        """
        Decrypts `data` received in a webpush request. Requires the private key dict
        from :ref:`push_subscription_generate_keys() <push_subscription_generate_keys()>` (`decrypt_params`) as well as the
        Encryption and server Crypto-Key headers from the received webpush
        """
        if (not IMPL_HAS_ECE) or (not IMPL_HAS_CRYPTO):
            raise NotImplementedError('To use the crypto tools, please install the webpush feature dependencies.')

        salt = self.__decode_webpush_b64(encryption_header.split("salt=")[1].strip())
        dhparams = self.__decode_webpush_b64(crypto_key_header.split("dh=")[1].split(";")[0].strip())
        p256ecdsa = self.__decode_webpush_b64(crypto_key_header.split("p256ecdsa=")[1].strip())
        dec_key = ec.derive_private_key(decrypt_params['privkey'], ec.SECP256R1(), default_backend())
        decrypted = http_ece.decrypt(
            data,
            salt=salt,
            key=p256ecdsa,
            private_key=dec_key,
            dh=dhparams,
            auth_secret=decrypt_params['auth'],
            keylabel="P-256",
            version="aesgcm"
        )

        return try_cast_recurse(PushNotification, json.loads(decrypted.decode('utf-8')))
