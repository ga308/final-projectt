"""Unit tests for the counter service."""
from unittest import TestCase
from service import app, routes


class CounterTest(TestCase):
    """Counter service tests."""

    def setUp(self):
        routes.COUNTERS.clear()
        self.client = app.test_client()

    def test_index(self):
        """It should return service info"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)

    def test_create_counter(self):
        """It should create a counter"""
        resp = self.client.post("/counters/foo")
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.get_json()["counter"], 0)

    def test_duplicate_counter(self):
        """It should not create a duplicate counter"""
        self.client.post("/counters/foo")
        resp = self.client.post("/counters/foo")
        self.assertEqual(resp.status_code, 409)

    def test_read_counter(self):
        """It should read a counter"""
        self.client.post("/counters/foo")
        resp = self.client.get("/counters/foo")
        self.assertEqual(resp.status_code, 200)

    def test_read_missing_counter(self):
        """It should return 404 for a missing counter"""
        self.assertEqual(self.client.get("/counters/nope").status_code, 404)

    def test_update_counter(self):
        """It should increment a counter"""
        self.client.post("/counters/foo")
        resp = self.client.put("/counters/foo")
        self.assertEqual(resp.get_json()["counter"], 1)

    def test_update_missing_counter(self):
        """It should return 404 when incrementing a missing counter"""
        self.assertEqual(self.client.put("/counters/nope").status_code, 404)

    def test_delete_counter(self):
        """It should delete a counter"""
        self.client.post("/counters/foo")
        self.assertEqual(self.client.delete("/counters/foo").status_code, 204)
        self.assertEqual(self.client.get("/counters/foo").status_code, 404)

    def test_delete_missing_counter(self):
        """It should return 404 when deleting a missing counter"""
        self.assertEqual(self.client.delete("/counters/nope").status_code, 404)
