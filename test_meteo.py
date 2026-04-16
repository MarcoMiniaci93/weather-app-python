import unittest
from unittest.mock import patch, Mock
import pandas as pd

from meteo import (
    get_weather_description,
    get_weather_symbol,
    data_in_italiano,
    get_weather_by_city,
    get_forecast_by_city,
)


GEO_OK = {
    "results": [
        {
            "name": "Torino",
            "latitude": 45.0703,
            "longitude": 7.6869
        }
    ]
}

WEATHER_OK = {
    "current": {
        "temperature_2m": 18.5,
        "weather_code": 2
    }
}

FORECAST_OK = {
    "daily": {
        "time": ["2026-04-16", "2026-04-17", "2026-04-18"],
        "temperature_2m_max": [24.2, 23.4, 24.3],
        "temperature_2m_min": [11.4, 14.2, 14.3],
        "weather_code": [45, 3, 3]
    }
}


def make_mock_response(data, status=200):
    mock_resp = Mock()
    mock_resp.status_code = status
    mock_resp.json.return_value = data
    mock_resp.raise_for_status.return_value = None
    return mock_resp


class TestUtilityFunctions(unittest.TestCase):

    def test_descrizione_codice_zero(self):
        self.assertEqual(get_weather_description(0), "Cielo sereno")

    def test_descrizione_codice_sconosciuto(self):
        self.assertEqual(
            get_weather_description(999),
            "Descrizione non disponibile"
        )

    def test_simbolo_temporale(self):
        self.assertEqual(get_weather_symbol(95), "[TEMPORALE]")

    def test_data_in_italiano(self):
        risultato = data_in_italiano("2026-04-16")
        self.assertTrue("16" in risultato)
        self.assertTrue("Apr" in risultato)


class TestGetWeatherByCity(unittest.TestCase):

    @patch("meteo.requests.get")
    def test_ritorna_dataframe(self, mock_get):
        mock_get.side_effect = [
            make_mock_response(GEO_OK),
            make_mock_response(WEATHER_OK),
        ]

        result = get_weather_by_city("Torino")
        self.assertIsInstance(result, pd.DataFrame)

    @patch("meteo.requests.get")
    def test_colonne_attese(self, mock_get):
        mock_get.side_effect = [
            make_mock_response(GEO_OK),
            make_mock_response(WEATHER_OK),
        ]

        df = get_weather_by_city("Torino")
        colonne_attese = {
            "city",
            "latitude",
            "longitude",
            "temperature_celsius",
            "weather_description",
            "weather_symbol",
        }
        self.assertEqual(set(df.columns), colonne_attese)

    @patch("meteo.requests.get")
    def test_valori_corretti(self, mock_get):
        mock_get.side_effect = [
            make_mock_response(GEO_OK),
            make_mock_response(WEATHER_OK),
        ]

        df = get_weather_by_city("Torino")

        self.assertEqual(df.iloc[0]["city"], "Torino")
        self.assertAlmostEqual(df.iloc[0]["latitude"], 45.0703)
        self.assertAlmostEqual(df.iloc[0]["longitude"], 7.6869)
        self.assertAlmostEqual(df.iloc[0]["temperature_celsius"], 18.5)
        self.assertEqual(
            df.iloc[0]["weather_description"],
            "Parzialmente nuvoloso"
        )
        self.assertEqual(df.iloc[0]["weather_symbol"], "[NUVOLE]")


class TestGetForecastByCity(unittest.TestCase):

    @patch("meteo.requests.get")
    def test_previsioni_dataframe(self, mock_get):
        mock_get.side_effect = [
            make_mock_response(GEO_OK),
            make_mock_response(FORECAST_OK),
        ]

        df = get_forecast_by_city("Torino", 3)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)

    @patch("meteo.requests.get")
    def test_previsioni_colonne(self, mock_get):
        mock_get.side_effect = [
            make_mock_response(GEO_OK),
            make_mock_response(FORECAST_OK),
        ]

        df = get_forecast_by_city("Torino", 3)
        colonne_attese = {
            "city",
            "date",
            "date_it",
            "temperature_max_c",
            "temperature_min_c",
            "weather_code",
            "weather_description",
            "weather_symbol",
        }
        self.assertEqual(set(df.columns), colonne_attese)

    @patch("meteo.requests.get")
    def test_previsioni_valori(self, mock_get):
        mock_get.side_effect = [
            make_mock_response(GEO_OK),
            make_mock_response(FORECAST_OK),
        ]

        df = get_forecast_by_city("Torino", 3)

        self.assertEqual(df.iloc[0]["city"], "Torino")
        self.assertEqual(df.iloc[0]["date"], "2026-04-16")
        self.assertAlmostEqual(df.iloc[0]["temperature_max_c"], 24.2)
        self.assertAlmostEqual(df.iloc[0]["temperature_min_c"], 11.4)
        self.assertEqual(df.iloc[0]["weather_code"], 45)
        self.assertEqual(df.iloc[0]["weather_description"], "Nebbia")
        self.assertEqual(df.iloc[0]["weather_symbol"], "[NEBBIA]")


if __name__ == "__main__":
    unittest.main()
