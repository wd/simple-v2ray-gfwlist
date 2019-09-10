from utils import import_path
import tempfile
import os
import threading
import socket
import unittest
import time
import logging

svgfw = import_path('./src/svgfw')
fake_bin_path = os.path.dirname(os.path.abspath(__file__)) + '/bin'
Utils = svgfw.Utils
Utils.logger.setLevel(logging.DEBUG)


class UtilsTest(unittest.TestCase):
    def test_get_command_version(self):
        cmd = svgfw.Utils.which('v2ray', path_list=[fake_bin_path])
        args = [cmd, '--version']
        regex = r'V2Ray (\d)\.(\d+)\.(\d+)'
        version = svgfw.Utils.get_command_version(args, regex)

        self.assertEqual(version, [4, 20, 0])

    def test_str_to_list(self):
        t = {
            '1.1.1.1': ['1.1.1.1'],
            '1.1.1.1, 2.3.2.1': ['1.1.1.1', '2.3.2.1'],
            '1.1.1.1; 2.3.2.1': ['1.1.1.1', '2.3.2.1'],
            '1.1.1.1;2.3.2.1': ['1.1.1.1', '2.3.2.1']
        }

        for ips, expect in t.items():
            res = Utils.str_to_list(ips)
            self.assertEqual(res, expect)

    def test_split_ip_port(self):
        default_port = 53
        t = {
            '1.1.1.1': ('1.1.1.1', default_port),
            '1.1.1.1:34': ('1.1.1.1', 34)
        }
        for ip, expect in t.items():
            res = Utils.split_ip_port(ip, default_port)
            self.assertEqual(res, expect)

    def test_read_file_to_list(self):
        tmpfile = tempfile.NamedTemporaryFile(delete=True)
        lines = ["xxxx", "ffffffffffffff"]
        tmpfile.write("\n".join(lines).encode('utf-8'))
        tmpfile.flush()
        self.assertEqual(lines, Utils.read_file_to_list(tmpfile.name))

    def test_which(self):
        cmd = Utils.which('iptables', path_list=[fake_bin_path])
        self.assertEqual(cmd, fake_bin_path + '/iptables')

    def test_run_command(self):
        cmd = Utils.which('test_command', path_list=[fake_bin_path])
        tmpfile = tempfile.NamedTemporaryFile(delete=True)
        test_str = 'test'
        code = Utils.run_command([cmd, 'output', test_str], stdout=tmpfile)
        self.assertEqual(code, 0, 'success exit code')
        tmpfile.seek(0)
        self.assertEqual(test_str, tmpfile.read().decode('utf8').rstrip(), 'output to a file')

        code = Utils.run_command([cmd, 'error_quit'])
        self.assertGreater(code, 0, 'faild exit code')

    def test_is_port_open(self):
        port = 23456
        self.assertFalse(Utils.is_port_open(port))

        def open_port(port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                try:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.bind(('127.0.0.1', port))
                    sock.listen(1)
                    sock.accept()
                except Exception:
                    print('bind faild')

        t = threading.Thread(target=open_port, args=[port])
        t.start()

        self.assertTrue(Utils.is_port_open(port))
        t.join()

    def test_get_pid(self):
        with tempfile.NamedTemporaryFile(delete=True) as fh:
            pid = 1923
            fh.write(str(pid).encode('utf8'))
            fh.seek(0)
            self.assertEqual(Utils.get_pid(fh.name), pid)
