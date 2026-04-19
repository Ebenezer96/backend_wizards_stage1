import requests


TIMEOUT = 10


class ExternalAPIError(Exception):
    pass


def normalize_name(name: str) -> str:
    return name.strip().lower()


def get_age_group(age: int) -> str:
    if age < 0:
        raise ExternalAPIError("Invalid age returned by upstream service")
    if age <= 12:
        return "child"
    if age <= 19:
        return "teenager"
    if age <= 59:
        return "adult"
    return "senior"


def fetch_json(url: str, name: str) -> dict:
    try:
        response = requests.get(url, params={"name": name}, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        raise


def fetch_gender_data(name: str) -> dict:
    data = fetch_json("https://api.genderize.io", name)

    if data.get("gender") is None or data.get("count", 0) == 0:
        raise ExternalAPIError("No prediction available for the provided name")

    return {
        "gender": data["gender"],
        "gender_probability": float(data["probability"]),
        "sample_size": int(data["count"]),
    }


def fetch_age_data(name: str) -> dict:
    data = fetch_json("https://api.agify.io", name)

    age = data.get("age")
    if age is None:
        raise ExternalAPIError("No prediction available for the provided name")

    age = int(age)

    return {
        "age": age,
        "age_group": get_age_group(age),
    }


def fetch_country_data(name: str) -> dict:
    data = fetch_json("https://api.nationalize.io", name)

    countries = data.get("country", [])
    if not countries:
        raise ExternalAPIError("No prediction available for the provided name")

    best_country = max(countries, key=lambda item: item.get("probability", 0))

    if not best_country.get("country_id"):
        raise ExternalAPIError("No prediction available for the provided name")

    return {
        "country_id": best_country["country_id"],
        "country_probability": float(best_country["probability"]),
    }


def build_profile_data(name: str) -> dict:
    normalized_name = normalize_name(name)

    gender_data = fetch_gender_data(normalized_name)
    age_data = fetch_age_data(normalized_name)
    country_data = fetch_country_data(normalized_name)

    return {
        "name": normalized_name,
        **gender_data,
        **age_data,
        **country_data,
    }