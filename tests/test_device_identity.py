import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from pydantic import ValidationError

from src.models.device_identity import DeviceIdentity
from src.models.secrets import Secrets


ROOT = Path(__file__).resolve().parents[1]


class DeviceIdentityTests(unittest.TestCase):
    def test_boundaries(self):
        for model, manufacturer in [('ab', 'abc'), ('a' * 50, 'b' * 50), ('model ~', 'Maker Inc.')]:
            DeviceIdentity.model_validate({'model_name': model, 'manufacturer': manufacturer})
        for field, values in {
            'model_name': ['', 'a', 'a' * 51, 'Modèle', 'model\n', 'model\x7f'],
            'manufacturer': ['', 'ab', 'a' * 51, 'Société', 'maker\t', 'maker\x00'],
        }.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    payload = {'model_name': 'model', 'manufacturer': 'maker'}
                    payload[field] = value
                    with self.assertRaises(ValidationError):
                        DeviceIdentity.model_validate(payload)

    def test_secrets_reject_invalid_manufacturer(self):
        payload = dict(wifi_ssid='ssid', wifi_password='password', api_token='token',
                       server_domain='example.com', mqtt_domain='example.com',
                       mqtt_username='user', mqtt_password='password', manufacturer='ab')
        with self.assertRaises(ValidationError):
            Secrets.model_validate(payload)

    def test_cli_rejects_identity_without_overwriting_output(self):
        for model, manufacturer in [('a', 'maker'), ('a' * 51, 'maker'),
                                    ('Modèle', 'maker'), ('model', 'ab'), ('model', 'Société')]:
            with self.subTest(model=model, manufacturer=manufacturer), tempfile.TemporaryDirectory() as folder:
                directory = Path(folder)
                source = directory / 'config.yaml'
                source.write_text((ROOT / 'secrets-template.yaml').read_text() + f'\nmanufacturer: {manufacturer}\n')
                output = directory / 'secrets.h'
                output.write_text('existing header')
                result = subprocess.run([sys.executable, '-m', 'src', '--model', model,
                                         '--source', str(source), '--destination', folder],
                                        cwd=ROOT, capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('error', result.stderr.lower())
                self.assertIn('model_name' if model != 'model' else 'manufacturer', result.stderr)
                self.assertEqual(output.read_text(), 'existing header')


if __name__ == '__main__':
    unittest.main()
