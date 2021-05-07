import unittest
import weather

class TestBotMethods(unittest.TestCase):
    def test_weather_future_forecast(self):
        self.assertEqual(weather.future_forecast('bb'), 'Такого города не существует')
        self.assertNotEqual(weather.future_forecast('Moscow'), 'Такого города не существует')

    def test_weather_current_forecast(self):
        self.assertEqual(weather.current_forecast('bb'), 'Такого города не существует')
        self.assertNotEqual(weather.future_forecast('Minsk'), 'Такого города не существует')
