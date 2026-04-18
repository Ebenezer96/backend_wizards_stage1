import requests


TIMEOUT = 10


class ExternalAPIError(Exception):
    pass


def normalize_name(name: str) -> str:
    return name.strip().lower()


def get_age_group(age: int) -> str:
    if age < 0:
        raise ExternalAPIError("Agify returned an invalid response")
    if 0 <= age <= 12:
        return "child"
    if 13 <= age <= 19:
        return "teenager"
    if 20 <= age <= 59:
        return "adult"
    return "senior"


def fetch_gender_data(name: str) -> dict:
    response = requests.get(
        "https://api.genderize.io",
        params={"name": name},
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("gender") is None or data.get("count", 0) == 0:
        raise ExternalAPIError("Genderize returned an invalid response")

    return {
        "gender": data["gender"],
        "gender_probability": float(data["probability"]),
        "sample_size": int(data["count"]),
    }


def fetch_age_data(name: str) -> dict:
    response = requests.get(
        "https://api.agify.io",
        params={"name": name},
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()

    age = data.get("age")
    if age is None:
        raise ExternalAPIError("Agify returned an invalid response")

    age = int(age)

    return {
        "age": age,
        "age_group": get_age_group(age),
    }


def fetch_country_data(name: str) -> dict:
    response = requests.get(
        "https://api.nationalize.io",
        params={"name": name},
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()

    countries = data.get("country", [])
    if not countries:
        raise ExternalAPIError("Nationalize returned an invalid response")

    best_country = max(
        countries,
        key=lambda item: item.get("probability", 0),
    )

    if not best_country.get("country_id"):
        raise ExternalAPIError("Nationalize returned an invalid response")

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