"""start flask(FLASKAPP=perch)"""


def test_rend_main(client):
    """load / , check page returned"""
    received = client.get('/')
    assert b'meta charset="utf-8"' in received.data
