import app.main as main


def test_clubs_nearest():
    # Call the function directly to avoid requiring httpx in the test environment
    data = main.clubs_nearest(lat=50.4501, lon=30.5234, limit=3)
    assert 'clubs' in data
    assert isinstance(data['clubs'], list)
    assert len(data['clubs']) >= 1
    first = data['clubs'][0]
    assert 'name' in first
    # Expect phone to be present for the dataset entries
    assert 'phone' in first and first['phone']
