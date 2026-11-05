import unittest
from src.config import validate

class ProtocolTests(unittest.TestCase):
    def test_rejects_extra_classes_in_single(self):
        with self.assertRaises(ValueError):
            validate({'data': {'mode':'single','classes':['A','B']}})
    def test_rejects_incomplete_all(self):
        with self.assertRaises(ValueError):
            validate({'data': {'mode':'all','classes':['C']}})
    def test_configs(self):
        import json
        from pathlib import Path
        for path in Path('configs').glob('*.json'):
            validate(json.loads(path.read_text()))
