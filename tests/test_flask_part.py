"""start flask(FLASKAPP=perch)"""
import pytest
from perch.db import update


def test_rend_main(client, app):
    """load / , check page returned"""
    with app.app_context():
        update()
        received = client.get('/')
        print(received.data)
        assert b'meta charset="utf-8"' in received.data


# def test_rend_actress(client, fixture_db):
#     """load / , check page returned"""
#     update(fixture_db, SAMPLE_LIB, True)
#     received = client.get('/actress/food')
#     print(received.data)
#     pass
