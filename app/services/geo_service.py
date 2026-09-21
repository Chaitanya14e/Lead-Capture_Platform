import requests


def get_geo_from_provider_a(ip_address: str) -> dict:
    response = requests.get(
        f"http://ip-api.com/json/{ip_address}",
        timeout=3,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("status") != "success":
        raise RuntimeError("Provider A failed")

    return {
        "country": data.get("country"),
        "city": data.get("city"),
    }


def get_geo_from_provider_b(ip_address: str) -> dict:
    response = requests.get(
        f"https://ipapi.co/{ip_address}/json/",
        timeout=3,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("error"):
        raise RuntimeError("Provider B failed")

    return {
        "country": data.get("country_name"),
        "city": data.get("city"),
    }


def get_geo(ip_address: str | None) -> dict:
    if not ip_address:
        return {
            "country": None,
            "city": None,
        }

    try:
        return get_geo_from_provider_a(ip_address)

    except Exception:
        try:
            return get_geo_from_provider_b(ip_address)

        except Exception:
            return {
                "country": None,
                "city": None,
            }