import requests
import pandas as pd
from datetime import datetime


WEATHER_DESCRIPTIONS = {
    0: "Cielo sereno",
    1: "Prevalentemente sereno",
    2: "Parzialmente nuvoloso",
    3: "Coperto",
    45: "Nebbia",
    48: "Nebbia con brina",
    51: "Pioviggine leggera",
    53: "Pioviggine moderata",
    55: "Pioviggine intensa",
    61: "Pioggia leggera",
    63: "Pioggia moderata",
    65: "Pioggia intensa",
    71: "Neve leggera",
    73: "Neve moderata",
    75: "Neve intensa",
    80: "Rovesci leggeri",
    81: "Rovesci moderati",
    82: "Rovesci forti",
    95: "Temporale",
}

WEATHER_SYMBOLS = {
    0: "[SOLE]",
    1: "[SOLE]",
    2: "[NUVOLE]",
    3: "[COPERTO]",
    45: "[NEBBIA]",
    48: "[NEBBIA]",
    51: "[PIOGGIA]",
    53: "[PIOGGIA]",
    55: "[PIOGGIA]",
    61: "[PIOGGIA]",
    63: "[PIOGGIA]",
    65: "[PIOGGIA]",
    71: "[NEVE]",
    73: "[NEVE]",
    75: "[NEVE]",
    80: "[ROVESCI]",
    81: "[ROVESCI]",
    82: "[ROVESCI]",
    95: "[TEMPORALE]",
}

GIORNI_ITALIANI = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]
MESI_ITALIANI = [
    "Gen", "Feb", "Mar", "Apr", "Mag", "Giu",
    "Lug", "Ago", "Set", "Ott", "Nov", "Dic"
]


def get_weather_description(code: int) -> str:
    return WEATHER_DESCRIPTIONS.get(code, "Descrizione non disponibile")


def get_weather_symbol(code: int) -> str:
    return WEATHER_SYMBOLS.get(code, "[?]")


def data_in_italiano(data_str: str) -> str:
    dt = datetime.strptime(data_str, "%Y-%m-%d")
    giorno_sett = GIORNI_ITALIANI[dt.weekday()]
    mese = MESI_ITALIANI[dt.month - 1]
    return f"{giorno_sett} {dt.day:02d} {mese}"


def geocode_city(city: str) -> dict:
    if not city or not city.strip():
        raise ValueError("Nome città non valido")

    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name": city.strip(),
            "count": 1,
            "language": "it",
            "format": "json"
        },
        timeout=10
    )
    response.raise_for_status()
    data = response.json()

    if "results" not in data or not data["results"]:
        raise RuntimeError("Città non trovata")

    result = data["results"][0]
    return {
        "city": result["name"],
        "latitude": result["latitude"],
        "longitude": result["longitude"]
    }


def get_weather_by_city(city: str) -> pd.DataFrame:
    location = geocode_city(city)

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": "temperature_2m,weather_code",
            "timezone": "auto"
        },
        timeout=10
    )
    response.raise_for_status()
    data = response.json()

    if "current" not in data:
        raise RuntimeError("Dati meteo correnti non disponibili")

    current = data["current"]

    return pd.DataFrame([{
        "city": location["city"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "temperature_celsius": current["temperature_2m"],
        "weather_description": get_weather_description(current["weather_code"]),
        "weather_symbol": get_weather_symbol(current["weather_code"])
    }])


def get_forecast_by_city(city: str, days: int = 5) -> pd.DataFrame:
    if days < 1 or days > 16:
        raise ValueError("Il numero di giorni deve essere compreso tra 1 e 16")

    location = geocode_city(city)

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "daily": "weather_code,temperature_2m_max,temperature_2m_min",
            "forecast_days": days,
            "timezone": "auto"
        },
        timeout=10
    )
    response.raise_for_status()
    data = response.json()

    if "daily" not in data:
        raise RuntimeError("Previsioni giornaliere non disponibili")

    daily = data["daily"]

    rows = []
    for date_str, tmax, tmin, code in zip(
        daily["time"],
        daily["temperature_2m_max"],
        daily["temperature_2m_min"],
        daily["weather_code"]
    ):
        rows.append({
            "city": location["city"],
            "date": date_str,
            "date_it": data_in_italiano(date_str),
            "temperature_max_c": tmax,
            "temperature_min_c": tmin,
            "weather_code": code,
            "weather_description": get_weather_description(code),
            "weather_symbol": get_weather_symbol(code)
        })

    return pd.DataFrame(rows)


def scegli_giorni() -> int:
    valore = input("Quanti giorni di previsione? (3-5, invio = 5): ").strip()
    if valore == "":
        return 5

    try:
        giorni = int(valore)
    except ValueError:
        raise ValueError("Inserisci un numero valido tra 3 e 5")

    if giorni < 3 or giorni > 5:
        raise ValueError("Il numero di giorni deve essere tra 3 e 5")

    return giorni


def stampa_meteo_attuale(df: pd.DataFrame) -> None:
    row = df.iloc[0]
    print(f"\n{row['city'].upper()} - Meteo attuale")
    print(f"{row['weather_symbol']} {row['weather_description']}")
    print(f"Temperatura: {row['temperature_celsius']:.1f} C")


def stampa_previsioni(df: pd.DataFrame) -> None:
    print(f"\nPREVISIONI {len(df)} GIORNI")
    for _, row in df.iterrows():
        print(
            f"{row['date_it']}  "
            f"MAX {row['temperature_max_c']:.1f}C  "
            f"MIN {row['temperature_min_c']:.1f}C  "
            f"{row['weather_symbol']}"
        )
        print(f"   {row['weather_description']}")


def main():
    print("APP METEO - Open-Meteo")
    city = input("Inserisci il nome della città: ").strip()

    try:
        giorni = scegli_giorni()
        meteo_attuale = get_weather_by_city(city)
        previsioni = get_forecast_by_city(city, giorni)

        stampa_meteo_attuale(meteo_attuale)
        stampa_previsioni(previsioni)

    except Exception as e:
        print(f"\nErrore: {e}")


if __name__ == "__main__":
    main()
