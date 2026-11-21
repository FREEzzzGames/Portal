import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from hub.main import app, container_snapshot, health, system_snapshot


class HubApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["ok"])
        self.assertEqual(body["service"], "freezzz-hub")

    def test_system_endpoint_contains_expected_metrics(self):
        response = self.client.get("/api/v1/system")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        for key in ("host", "cpu", "memory", "swap", "storage", "network", "uptime_seconds"):
            self.assertIn(key, body)
        self.assertGreaterEqual(body["memory"]["total"], 0)

    def test_overview_endpoint_contains_system_and_docker(self):
        response = self.client.get("/api/v1/overview")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("system", body)
        self.assertIn("docker", body)

    def test_docker_missing_socket_is_reported_not_crashed(self):
        with patch("hub.main.os.path.exists", return_value=False):
            result = container_snapshot()
        self.assertFalse(result["available"])
        self.assertEqual(result["containers"], [])

    def test_root_serves_dashboard(self):
        response = self.client.get("/")
        self.assertIn(response.status_code, (200, 503))
        if response.status_code == 200:
            self.assertIn("FREEzzz HUB", response.text)


if __name__ == "__main__":
    unittest.main()
