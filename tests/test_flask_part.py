"""start flask(FLASKAPP=perch)"""


def test_rend_main(client):
    """load / , check page returned. check api same time"""
    client.post('/admin', data=dict(task='update_db'), follow_redirects=True)
    received = client.get('/')
    # print(received.data)
    assert b'neon' in received.data

    client.post('/admin', data=dict(task='drop_db'), follow_redirects=True)
    received = client.get('/')
    assert b'neon' not in received.data


def test_rend_actress(client):
    """load /actress/<name>, get some data..."""
    client.post('/admin', data=dict(task='update_db'), follow_redirects=True)
    received = client.get('/actress/nature')
    assert b'bTTZ' in received.data


def test_rend_tag(client):
    """render tag page"""
    client.post('/admin', data=dict(task='update_db'), follow_redirects=True)
    received = client.get('/tag/forest')
    assert b'Pz3th' in received.data
    assert b'bTTZ' in received.data
    received = client.get('/tag/not-exist')
    assert received.data is not None


def test_rend_player(client):
    """load /player, get player"""
    client.post('/admin', data=dict(task='update_db'), follow_redirects=True)
    received = client.get('player?id=L03BG2NLRKV5A&name=8Qgtq880d18')
    assert b'chill' in received.data
    assert b'daylight' in received.data
    assert b'scenary' in received.data
    assert b'8Qgtq' in received.data
    assert b'non-exist' not in received.data


def test_rend_admin(client):
    """render admin page,"""
    received = client.get('/admin')
    assert b'update_db' in received.data
    assert b'drop_db' in received.data
    assert b'non-exist' not in received.data

    received = client.post(
        '/admin', data=dict(task='non-exist-task'), follow_redirects=True)
    assert b'unknown task' in received.data


def test_jump_random(client):
    """test random jump to player mech"""
    client.post('/admin', data=dict(task='update_db'), follow_redirects=True)
    received = client.get('/random')
    assert received.status_code == 302
    assert b'Redirecting...' in received.data
    assert b'player' in received.data
