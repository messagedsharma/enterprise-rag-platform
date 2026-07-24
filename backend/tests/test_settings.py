import unittest

from app.config.settings import settings


class SettingsTests(unittest.TestCase):
    def test_processing_version_is_a_positive_integer(self):
        self.assertIsInstance(settings.processing_version, int)
        self.assertGreater(settings.processing_version, 0)

    def test_bedrock_model_is_configured(self):
        self.assertEqual(
            settings.bedrock_model,
            "amazon.nova-lite-v2",
        )


if __name__ == "__main__":
    unittest.main()
