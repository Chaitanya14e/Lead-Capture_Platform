from app.services import geo_service


def test_provider_a_success(monkeypatch):
    def fake_provider_a(ip):
        return {
            "country": "India",
            "city": "Delhi",
        }

    monkeypatch.setattr(
        geo_service,
        "get_geo_from_provider_a",
        fake_provider_a,
    )

    result = geo_service.get_geo("8.8.8.8")

    assert result == {
        "country": "India",
        "city": "Delhi",
    }


def test_provider_a_fails_provider_b_succeeds(monkeypatch):
    def fake_provider_a(ip):
        raise RuntimeError("Provider A unavailable")

    def fake_provider_b(ip):
        return {
            "country": "India",
            "city": "Mumbai",
        }

    monkeypatch.setattr(
        geo_service,
        "get_geo_from_provider_a",
        fake_provider_a,
    )

    monkeypatch.setattr(
        geo_service,
        "get_geo_from_provider_b",
        fake_provider_b,
    )

    result = geo_service.get_geo("8.8.8.8")

    assert result == {
        "country": "India",
        "city": "Mumbai",
    }


def test_both_providers_fail(monkeypatch):
    def fake_provider_a(ip):
        raise RuntimeError("Provider A unavailable")

    def fake_provider_b(ip):
        raise RuntimeError("Provider B unavailable")

    monkeypatch.setattr(
        geo_service,
        "get_geo_from_provider_a",
        fake_provider_a,
    )

    monkeypatch.setattr(
        geo_service,
        "get_geo_from_provider_b",
        fake_provider_b,
    )

    result = geo_service.get_geo("8.8.8.8")

    assert result == {
        "country": None,
        "city": None,
    }