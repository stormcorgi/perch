"""start flask(FLASKAPP=perch)"""


def test_rend_main(client):
    """load / , check page returned. check api same time"""
    received = client.get('/')
    assert b'neon' in received.data


def test_rend_actress(client):
    """load /actress/<name>, get some data..."""
    received = client.get('/actress/nature')
    assert b'bTTZ' in received.data


def test_rend_tag(client):
    """render tag page"""
    received = client.get('/tag/forest')
    assert b'Pz3th' in received.data
    assert b'bTTZ' in received.data
    received = client.get('/tag/not-exist')
    assert received.data is not None


def test_rend_player(client):
    """load /player, get player"""
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


def test_admin_post_drop_db(client):
    """post drop_db task → success response"""
    received = client.post(
        '/admin', data=dict(task='drop_db'), follow_redirects=True)
    assert b'drop_db done!' in received.data


def test_admin_post_update_db(client):
    """post update_db task → 'request queued' (background thread)"""
    received = client.post(
        '/admin', data=dict(task='update_db'), follow_redirects=True)
    assert b'request queued' in received.data


def test_jump_random(client):
    """test random jump to player mech"""
    received = client.get('/random')
    assert received.status_code == 302
    assert b'Redirecting...' in received.data
    assert b'player' in received.data


# ── Tag API ──


def test_tag_add(client):
    """add a tag via JSON POST"""
    received = client.post(
        '/player/tag/add',
        content_type='application/json',
        data='{"fileid":"L03BG2NK1ERKW","tag":"テストタグ_API"}',
    )
    assert received.status_code == 200
    body = received.get_json()
    assert body['success'] is True
    assert body['added'] is True

    # Verify it's visible in the player page
    page = client.get('player?id=L03BG2NK1ERKW&name=Pz3thr4MRFI')
    assert 'テストタグ_API'.encode('utf-8') in page.data


def test_tag_add_idempotent(client):
    """adding same tag twice — second call returns added:false"""
    body = client.post(
        '/player/tag/add',
        content_type='application/json',
        data='{"fileid":"L03BG2NK1ERKW","tag":"重複タグ"}',
    ).get_json()
    assert body['added'] is True

    body = client.post(
        '/player/tag/add',
        content_type='application/json',
        data='{"fileid":"L03BG2NK1ERKW","tag":"重複タグ"}',
    ).get_json()
    assert body['success'] is True
    assert body['added'] is False


def test_tag_add_missing_params(client):
    """missing fileid or tag → 400"""
    body = client.post(
        '/player/tag/add',
        content_type='application/json',
        data='{"fileid":"L03BG2NK1ERKW"}',
    ).get_json()
    assert body['success'] is False

    body = client.post(
        '/player/tag/add',
        content_type='application/json',
        data='{"tag":"test"}',
    ).get_json()
    assert body['success'] is False

    body = client.post(
        '/player/tag/add',
        content_type='application/json',
        data='{"fileid":"L03BG2NK1ERKW","tag":"  "}',
    ).get_json()
    assert body['success'] is False


def test_tag_remove(client):
    """add then remove a tag"""
    client.post('/player/tag/add',
                content_type='application/json',
                data='{"fileid":"L03BG2NK1ERKW","tag":"消すタグ"}')

    body = client.post(
        '/player/tag/remove',
        content_type='application/json',
        data='{"fileid":"L03BG2NK1ERKW","tag":"消すタグ"}',
    ).get_json()
    assert body['success'] is True

    # Verify it's gone from the page
    page = client.get('player?id=L03BG2NK1ERKW&name=Pz3thr4MRFI')
    assert '消すタグ'.encode('utf-8') not in page.data


def test_tag_remove_nonexistent(client):
    """removing a tag that doesn't exist silently succeeds"""
    body = client.post(
        '/player/tag/remove',
        content_type='application/json',
        data='{"fileid":"L03BG2NK1ERKW","tag":"絶対に存在しないタグ名"}',
    ).get_json()
    assert body['success'] is True


def test_tag_remove_missing_params(client):
    """missing fileid or tag on remove → 400"""
    body = client.post(
        '/player/tag/remove',
        content_type='application/json',
        data='{"fileid":"L03BG2NK1ERKW"}',
    ).get_json()
    assert body['success'] is False

    body = client.post(
        '/player/tag/remove',
        content_type='application/json',
        data='{"tag":"test"}',
    ).get_json()
    assert body['success'] is False


# ── Stream route ──


def test_stream_not_found(client):
    """unknown fileid → plain 'not found', 404"""
    r = client.get('/stream/NO_SUCH_FILE')
    assert r.status_code == 404
    assert r.data == b'not found'


def test_stream_no_file_on_disk(client):
    """known fileid but no actual video file → Flask 404 HTML"""
    r = client.get('/stream/L03BG2NK1ERKW')
    assert r.status_code == 404
    # Flask's own 404 page, not our 'not found' string
    assert r.data.startswith(b'<!doctype html>')
