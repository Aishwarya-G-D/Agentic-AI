import pathlib, sysconfig

SITECUSTOMIZE = """\
import ssl, warnings, os

os.environ["PYTHONHTTPSVERIFY"] = "0"
os.environ["CURL_CA_BUNDLE"] = ""
os.environ["REQUESTS_CA_BUNDLE"] = ""

warnings.filterwarnings("ignore", message="Unverified HTTPS request")
ssl._create_default_https_context = ssl._create_unverified_context

try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    pass

try:
    import requests
    from requests.adapters import HTTPAdapter

    class SSLAdapter(HTTPAdapter):
        def init_poolmanager(self, *args, **kwargs):
            kwargs["cert_reqs"] = ssl.CERT_NONE
            return super().init_poolmanager(*args, **kwargs)

    _orig = requests.Session.__init__

    def _patched(self, *a, **kw):
        _orig(self, *a, **kw)
        self.verify = False
        self.mount("https://", SSLAdapter())
        self.mount("http://", HTTPAdapter())

    requests.Session.__init__ = _patched
except ImportError:
    pass
"""

target = pathlib.Path(sysconfig.get_paths()["purelib"]) / "sitecustomize.py"
target.write_text(SITECUSTOMIZE)
print(f"Written to {target}")