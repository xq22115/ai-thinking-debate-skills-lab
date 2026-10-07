import http.client
import importlib.util
import json
import pathlib
import threading
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "ordinary-chat-dashboard" / "server.py"
spec = importlib.util.spec_from_file_location("ordinary_chat_dashboard", MODULE_PATH)
assert spec and spec.loader
dashboard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dashboard)


class OrdinaryChatDashboardTests(unittest.TestCase):
    def setUp(self):
        self.server = dashboard.DashboardServer(("127.0.0.1", 0), dashboard.Handler)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def request(self, method: str, path: str):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=2)
        connection.request(method, path)
        response = connection.getresponse()
        body = response.read()
        headers = dict(response.getheaders())
        connection.close()
        return response.status, headers, body

    def test_index_has_security_headers(self):
        status, headers, body = self.request("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn(b"Ordinary Chat Agent Control", body)
        self.assertEqual(headers.get("X-Frame-Options"), "DENY")
        self.assertEqual(headers.get("X-Content-Type-Options"), "nosniff")
        self.assertIn("frame-ancestors 'none'", headers.get("Content-Security-Policy", ""))

    def test_source_file_is_not_served(self):
        status, _, body = self.request("GET", "/server.py")
        self.assertEqual(status, 404)
        self.assertEqual(json.loads(body), {"error": "not_found"})

    def test_mutations_are_rejected(self):
        for method in ("POST", "PUT", "PATCH", "DELETE"):
            status, _, body = self.request(method, "/api/run/" + "a" * 32)
            self.assertEqual(status, 405)
            self.assertEqual(json.loads(body), {"error": "read_only_dashboard"})

    def test_health_is_read_only(self):
        status, _, body = self.request("GET", "/api/healthz")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body), {"ok": True, "read_only": True})


if __name__ == "__main__":
    unittest.main()
