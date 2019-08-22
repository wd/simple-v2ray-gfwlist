from utils import import_path
import tempfile

svgfw = import_path('./src/svgfw')


def test_get_command_version():
    args = ['v2ray', '--version']
    regex = r'V2Ray (\d)\.(\d+)\.(\d+)'
    version = svgfw.Utils.get_command_version(args, regex)

    assert version == [4, 20, 0]


def test_str_to_list():
    t = {
        '1.1.1.1': ['1.1.1.1'],
        '1.1.1.1, 2.3.2.1': ['1.1.1.1', '2.3.2.1'],
        '1.1.1.1; 2.3.2.1': ['1.1.1.1', '2.3.2.1'],
        '1.1.1.1;2.3.2.1': ['1.1.1.1', '2.3.2.1']
    }

    for ips, expect in t.items():
        res = svgfw.Utils.str_to_list(ips)
        assert res == expect


def test_split_ip_port():
    default_port = 53
    t = {
        '1.1.1.1': ('1.1.1.1', default_port),
        '1.1.1.1:34': ('1.1.1.1', 34)
    }
    for ip, expect in t.items():
        res = svgfw.Utils.split_ip_port(ip, default_port)
        assert res == expect


def test_read_file_to_list():
    tmpfile = tempfile.NamedTemporaryFile(delete=True)
    lines = ["xxxx", "ffffffffffffff"]
    tmpfile.write("\n".join(lines).encode('utf-8'))
    tmpfile.flush()
    assert lines == svgfw.Utils.read_file_to_list(tmpfile.name)
