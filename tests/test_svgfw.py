import unittest
from svgfw import GFW
import base64
import re


def test_process_gfw_list():
    gfw = GFW()
    domain_pattern = r'^([a-z0-9][a-z0-9-]*\.)*[a-z0-9][a-z0-9-]{0,61}\.(xn--[a-z0-9]+|[a-z]{2,})$'
    with open('tests/gfwlist.txt') as fh:
        domains = gfw._process_gfw_list(fh.read())

    for domain in domains:
        m = re.match(domain_pattern, domain.lower())
        assert m is not None, "{} is not a valid domain".format(domain)
