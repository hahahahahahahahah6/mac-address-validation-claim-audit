import json
from pathlib import Path
import tempfile
import unittest
from mac_address_validation_claim_audit.audit import audit, claims, evidence, main
from mac_address_validation_claim_audit.phrases import GENERIC_NAMES, MACADDRESSVALIDATION, NOMACADDRESSVALIDATION

ROOT = Path(__file__).resolve().parents[1]

class AuditTests(unittest.TestCase):
    def test_routes(self):
        routes = ['import validators\nvalidators.mac_address(x)', 'from validators import mac_address as m\nm(x)', 'import netaddr\nnetaddr.EUI(x)', 'from netaddr import EUI as e\ne(x)', 'from netaddr.eui import EUI\nEUI(x)', 'import netaddr as n\nn.valid_mac(x)', 'from netaddr import valid_mac\nvalid_mac(x)']
        routes += ['obj.%s(x)' % n for n in GENERIC_NAMES]
        routes += ['from library import %s as f\nf(x)' % n for n in GENERIC_NAMES]
        for route in routes:
            with self.subTest(route=route): self.assertTrue(evidence(route))
        self.assertTrue(evidence('obj = make()\nobj.validate_mac_address(x)'))

    def test_not_evidence(self):
        cases = ['import validators', 'import netaddr', 'mac_address(x)', 'EUI(x)', 'valid_mac(x)', 'x.mac_address(x)', 'x.EUI(x)', 'x.valid_mac(x)', 'import netaddr\nnetaddr.EUI(12345)', 'import netaddr\nx = netaddr.EUI\nx.oui', 'import netaddr\nnetaddr.OUI(x)', 'import netaddr\nnetaddr.IAB(x)', 'import getmac\ngetmac.get_mac_address()', 'import uuid\nuuid.getnode()', 'import psutil\npsutil.net_if_addrs()', 'import socket\nsocket.socket()', 'import fcntl\nfcntl.ioctl(x)', 'import re\nre.match("[0-9a-f:]+", x)', 'from urllib.parse import urlparse\nurlparse(x)', 'from urllib.parse import urlsplit\nurlsplit(x)', 'import netaddr\nnetaddr.IPAddress(x)', 'import isbnlib\nisbnlib.is_isbn10(x)', 'import stdnum\nstdnum.validate(x)', 'import schwifty\nschwifty.IBAN(x)', 'import packaging.version\npackaging.version.Version(x)', 'import semver\nsemver.Version.parse(x)', 'payments.charge(x)', 'extractor.extract(x)', 'import subprocess\nsubprocess.run(["validate_mac_address"])', '"validate mac address"', '# validate_mac_address(x)', 'from validators import mac_address\ndef mac_address(x): pass\nmac_address(x)', 'import validators\nvalidators = 3\nvalidators.mac_address(x)', 'from lib import validate_mac_address\nwith x as validate_mac_address: pass\nvalidate_mac_address(x)', 'validate_mac_address(x)', 'x.validate_mac_address(', 'from validators import mac_address']
        cases += ['import validators\nvalidators.%s(x)' % n for n in ('url','ipv4','ipv6','email','card_number','domain','uuid')]
        cases += ['import netaddr\nnetaddr.EUI.%s' % n for n in ('oui','ei','version','dialect','words','packed','bin','info')]
        for case in cases:
            with self.subTest(case=case): self.assertFalse(evidence(case))

    def test_phrases(self):
        self.assertEqual((len(MACADDRESSVALIDATION), len(NOMACADDRESSVALIDATION), len(GENERIC_NAMES)), (50,24,24))
        for phrase in MACADDRESSVALIDATION:
            with self.subTest(phrase=phrase): self.assertTrue(claims(phrase)[0])
        for phrase in NOMACADDRESSVALIDATION:
            with self.subTest(phrase=phrase): self.assertTrue(claims(phrase)[1]); self.assertFalse(claims(phrase)[0])
        self.assertEqual(claims('```\nvalidate mac address\n```'), (set(),set()))
        self.assertTrue(claims('`validate mac address`')[0])

    def test_findings(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'README.md').write_text('validate mac address')
            self.assertEqual(audit(p)[0]['severity'], 'HIGH')
            (p/'tests').mkdir(); (p/'tests/test_x.py').write_text('import validators\nvalidators.mac_address(x)')
            self.assertEqual(audit(p)[0]['severity'], 'MEDIUM')
            (p/'x.py').write_text('import validators\nvalidators.mac_address(x)')
            self.assertFalse(audit(p)); (p/'README.md').write_text('no mac address validation')
            self.assertEqual(audit(p)[0]['severity'], 'HIGH')
            self.assertFalse(audit(p, ['x.py']))
            (p/'x.py').write_text('import validators'); (p/'y.py').write_text('validators.mac_address(x)')
            (p/'README.md').write_text('validate mac address')
            self.assertEqual(audit(p)[0]['severity'], 'MEDIUM')

    def test_self_audit(self):
        self.assertEqual(audit(ROOT), [])
        self.assertEqual(audit(ROOT/'README.md'), [])

    def test_readme_limitations_prose(self):
        text=(ROOT/'README.md').read_text().split('## Limitations',1)[1]
        self.assertEqual(claims(text), (set(),set()))
