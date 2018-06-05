import pytest
import time
from mastodon.Mastodon import MastodonNotFoundError

def test_decrypt(api):
    priv = {
        'auth': b'\xe7y\x0fp\xb9\x92\xe0\xa0\xc5\xd5~Qr\xd7\xaa\x16',
        'privkey': 86377660131518823691452242868806126400423244879788569019894692873283793307753
    }

    # Yes, I am aware that there is an access token in there. It's not valid anymore.
    encryption_header = "salt=O14vjCdbxxhRUTkrsp98vw"
    crypto_key_header = "dh=BKz_CMlF6kVURVImPDsz3bNbTv-9QTGtXpE4Fd3wQGF44fVTj32-APndoccYdjXY2U-mdTen1PDm_pHacpEmD0M;p256ecdsa=BDSAB3e_l5Qp4X50UYSSrKiZFZWDAgHlWIDhgBjXJuUzb0HrpqoCdFhMCh4o2xYHTqpvyTJ3SfFtrILLiXXWT5k"
    data = b'\x10\\b<\xddi\xacd\x86\xc8J1\xb6}5\x01K\x85;\xd2\xd4WzN\xab\x0b|3D\xe9_YPcsG\x9fh\xae\xfe\xbb:z&\xc4\x8ek\x89\xde\xa2\xdbF\xdc\xdd[p<h\x9e\x95\x8d\xd4\xf0\xd0\xc1\x89\t\x01\xebuV\xb1\xa4Fp\xe3\xbf\x91g\x93\xbe \xe5\xd4\xee\xe2\xb0FaB\x8a\xd0\x00b\xe4Q\x83\xd5\xd9\x83\x9a\x1d\xd5j\xdb"\xc5\xb0\xf5W\xa72r4r]aLs\xa8\x8c\x1a\x19h\xfeX)_t\xd4p\xc9\xd2d\x1b?\x19\xc8X(\x02\xd5\x18\xe4\x93\xe2\xda\x01\xb4b\xe4\xd0F\x08`\x13;>\xc4\x89\xbc\xc3\x8e\xb8\x9bJ~\xc4}]\xdb\xdc\xf1wY\x16g\xf8\x91N\xee\xfd\x92\x1e\xcd\xd2~\xf2\x06\x89\xcd\xa5\xcd\x97\xb7{\xc5\xe1\xe4\xb0\x9f7\xc6\x8a5\xda\xbbm\xce\xc5\x8d\x93`&\x0e\xa9\x83\xa2|p;\xa4\x8b)\xc8\x07\rb!a\x82\xf5E\x92\x00Y{\xd4\x94\xf8\xf0\r\xb5c\x86\xfb\xd0*\xbb\xa1!\x14\xd5\x11\xc8\xafI\xb3j\xca7\xc4\x9c\xe0\x9c0\x12\xc0\xd1\x8a{\xcd\xc4~\\\xc2\x99\xf0d)\x03E\x91;m\xbe\xdb\x86\xef\xd7\xa7>\xd1a\xf1\x83!\xaeB\xaa\xf0\xda\x1b;\x86\xd8;]\x9e\xe3\xfa*!\x07,\t\xbd\xe7\xfc\xa7\xa8\xba[\xcf\x89e\xac\'\xdb\x88g\xd9\\\xe4C\x08Lb\xb6CAT\xcc!\xa4\xce\x92t3\x1c1\x01'
    
    decrypted = api.push_subscription_decrypt_push(
        data, 
        priv, 
        encryption_header,
        crypto_key_header
    )
    
    assert decrypted
    assert decrypted.title == 'You were mentioned by fake halcy'

@pytest.mark.vcr(match_on=['path'])
def test_push_set(api):
    priv, pub = api.push_subscription_generate_keys()
    sub = api.push_subscription_set("example.com", pub)
    
    assert sub == api.push_subscription()
    assert sub.endpoint == "https://example.com"

@pytest.mark.vcr(match_on=['path'])
def test_push_update(api):
    priv, pub = api.push_subscription_generate_keys()
    sub = api.push_subscription_set("example.com", pub,follow_events=False,
                                    favourite_events=False, reblog_events=False, 
                                    mention_events=False)
    
    sub2 = api.push_subscription_update(follow_events=True, favourite_events=True, 
                                        reblog_events=True, mention_events=True)
    time.sleep(1)
    assert sub2 == api.push_subscription()
    
    sub3 = api.push_subscription_update(follow_events=False, favourite_events=False, 
                                        reblog_events=False, mention_events=False)
    time.sleep(1)
    assert sub3 == api.push_subscription()
    
    assert sub3.alerts.follow == False
    assert sub3.alerts.favourite == False
    assert sub3.alerts.reblog == False
    assert sub3.alerts.mention == False
    assert sub2.alerts.follow == True
    assert sub2.alerts.favourite == True
    assert sub2.alerts.reblog == True
    assert sub2.alerts.mention == True
  

@pytest.mark.vcr(match_on=['path'])
def test_push_delete(api):
    priv, pub = api.push_subscription_generate_keys()
    sub = api.push_subscription_set("example.com", pub)
    assert sub 
    
    api.push_subscription_delete()
    with pytest.raises(MastodonNotFoundError):
        api.push_subscription()