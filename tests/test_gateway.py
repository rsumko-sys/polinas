from app.gateway import dispatch_clubs_nearest


def test_dispatch_routes_to_new_and_legacy():
    # New path
    new_res = dispatch_clubs_nearest(50.0, 30.0, limit=2, use_legacy=False)
    # Legacy path
    old_res = dispatch_clubs_nearest(50.0, 30.0, limit=2, use_legacy=True)

    assert isinstance(new_res, list)
    assert isinstance(old_res, list)
    assert len(new_res) <= 2
    assert len(old_res) <= 2
    # Legacy intentionally returns entries with distance_km == None
    if old_res:
        assert old_res[0].get("distance_km") is None
