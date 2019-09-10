import re
from utils import import_path
import unittest
import os
import configparser
import json

svgfw = import_path('./src/svgfw')
GFW = svgfw.GFW
Dnsmasq = svgfw.Dnsmasq
Iptable = svgfw.Iptable
GFWException = svgfw.GFWException


class GFWTest(unittest.TestCase):
    def test_process_gfw_list(self):
        gfw = GFW()
        domain_pattern = r'^([a-z0-9][a-z0-9-]*\.)*[a-z0-9][a-z0-9-]{0,61}\.(xn--[a-z0-9]+|[a-z]{2,})$'
        with open('tests/gfwlist.txt') as fh:
            domains = gfw._process_gfw_list(fh.read())

        for domain in domains:
            m = re.match(domain_pattern, domain.lower())
            assert m is not None, "{} is not a valid domain".format(domain)

    def test_init(self):
        config_file = os.path.dirname(os.path.abspath(__file__)) + '/config.ini'
        config = open(config_file).read()
        gfw = GFW(config)

        self.assertIsInstance(gfw.dnsmasq, Dnsmasq)
        self.assertIsInstance(gfw.iptable, Iptable)
        self.assertEqual(gfw.config_err, [])

        conf = configparser.ConfigParser()
        conf.read_string(config)
        conf['v2ray']['outbounds'] = json.dumps([])

        class ConfigToString():
            def __init__(self):
                self.lines = []

            def write(self, data):
                self.lines.append(data)

        cts = ConfigToString()
        conf.write(cts)

        self.assertRaisesRegex(GFWException, r'Outbound tag for .* not found', GFW, "".join(cts.lines))
