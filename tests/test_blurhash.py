import pytest

def test_blurhash_decode(api):
    fake_media_dict = {
        'width': 320,
        'height': 240,
        'blurhash': '=~NdOWof1PbIPUXSvgbI$f'
    }
    decoded_image = api.decode_blurhash(fake_media_dict)
    assert len(decoded_image) == 9 * 16
    assert len(decoded_image[0]) == 16
    
    decoded_image_2 = api.decode_blurhash(
        fake_media_dict, 
        out_size = (fake_media_dict["width"], fake_media_dict["height"]),
        size_per_component = False,
        return_linear = False
    )
    assert len(decoded_image_2) == 240
    assert len(decoded_image_2[0]) == 320
    
