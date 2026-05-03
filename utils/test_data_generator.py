"""
Autonomous Test Data Generator
Generates realistic, context-aware data for all field types:
  - Valid / Invalid / Boundary / XSS / SQLi / Unicode / Large / Empty
"""
import random
import string
import json
from datetime import date, timedelta


class TestDataGenerator:
    """Produces intelligent, multi-category test data without requiring an LLM."""

    # ── Username / Password ───────────────────────────────────────────────────

    @staticmethod
    def usernames() -> dict:
        return {
            "valid":      "standard_user",
            "locked":     "locked_out_user",
            "invalid":    "nonexistent_user_xyz",
            "empty":      "",
            "sqli":       "' OR '1'='1",
            "sqli_admin": "admin'--",
            "xss":        "<script>alert('xss')</script>",
            "unicode":    "用户名",
            "boundary_max": "u" * 255,
            "spaces_only":  "   ",
            "special":    "!@#$%^&*()_+",
        }

    @staticmethod
    def passwords() -> dict:
        return {
            "valid":      "secret_sauce",
            "invalid":    "wrong_password",
            "empty":      "",
            "weak":       "123",
            "strong":     "P@$$w0rd!2024#Secure",
            "unicode":    "密码123",
            "xss":        "<img src=x onerror=alert(1)>",
            "boundary_max": "p" * 255,
            "spaces_only":  "   ",
        }

    # ── Personal Info ─────────────────────────────────────────────────────────

    @staticmethod
    def first_names() -> dict:
        return {
            "valid":      "John",
            "empty":      "",
            "numeric":    "12345",
            "xss":        "<b>Injection</b>",
            "boundary":   "A" * 50,
            "unicode":    "田中",
            "special":    "O'Brien",
        }

    @staticmethod
    def last_names() -> dict:
        return {
            "valid":      "Doe",
            "empty":      "",
            "numeric":    "67890",
            "boundary":   "B" * 50,
            "unicode":    "Москва",
            "special":    "Von Trapp",
        }

    @staticmethod
    def zip_codes() -> dict:
        return {
            "valid_us":   "12345",
            "valid_uk":   "SW1A 1AA",
            "empty":      "",
            "invalid":    "ZZZZZ",
            "numeric_boundary": "0" * 20,
            "unicode":    "郵便番号",
            "negative":   "-1",
            "alpha":      "ABCDE",
        }

    # ── Email ─────────────────────────────────────────────────────────────────

    @staticmethod
    def emails() -> dict:
        return {
            "valid":      "user@example.com",
            "invalid_no_at": "userexample.com",
            "invalid_no_domain": "user@",
            "empty":      "",
            "xss":        "<script>@evil.com",
            "unicode":    "用戶@example.com",
            "boundary":   f"{'a' * 64}@{'b' * 63}.com",
        }

    # ── Dates ─────────────────────────────────────────────────────────────────

    @staticmethod
    def dates() -> dict:
        today = date.today()
        return {
            "past":           str(today - timedelta(days=365)),
            "future":         str(today + timedelta(days=365)),
            "today":          str(today),
            "far_past":       "1900-01-01",
            "far_future":     "2099-12-31",
            "invalid_format": "32-13-2024",
            "empty":          "",
        }

    # ── Security Payloads ─────────────────────────────────────────────────────

    @staticmethod
    def xss_payloads() -> list:
        return [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert(document.cookie)",
            "'><svg/onload=alert(1)>",
            "<body onload=alert('xss')>",
        ]

    @staticmethod
    def sqli_payloads() -> list:
        return [
            "' OR '1'='1",
            "admin'--",
            "'; DROP TABLE users;--",
            "1' AND SLEEP(5)--",
            "' UNION SELECT null, username, password FROM users--",
        ]

    # ── Random / Stress ───────────────────────────────────────────────────────

    @staticmethod
    def random_string(length: int = 16) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def large_payload(length: int = 10_000) -> str:
        return "A" * length

    # ── Parametrize Helpers ───────────────────────────────────────────────────

    @classmethod
    def login_matrix(cls) -> list:
        """Returns a list of (scenario, username, password, expect_error) tuples."""
        u = cls.usernames()
        p = cls.passwords()
        return [
            ("valid_login",      "standard_user",  "secret_sauce",  False),
            ("empty_both",       u["empty"],        p["empty"],       True),
            ("empty_password",   "standard_user",  p["empty"],       True),
            ("locked_user",      u["locked"],       "secret_sauce",  True),
            ("invalid_user",     u["invalid"],      "secret_sauce",  True),
            ("wrong_password",   "standard_user",  p["invalid"],     True),
            ("sqli_username",    u["sqli"],         "any",            True),
            ("xss_username",     u["xss"],          "any",            True),
            ("unicode_password", "standard_user",  p["unicode"],     True),
            ("boundary_username",u["boundary_max"],"secret_sauce",  True),
            ("spaces_only",      u["spaces_only"], p["spaces_only"], True),
        ]

    @classmethod
    def checkout_matrix(cls) -> list:
        """Returns (scenario, first, last, zip, expect_error) tuples."""
        f = cls.first_names()
        l = cls.last_names()
        z = cls.zip_codes()
        return [
            ("valid_data",      "John",           "Doe",     "12345",    False),
            ("empty_all",       "",               "",         "",         True),
            ("empty_zip",       "John",           "Doe",     "",         True),
            ("xss_first",       f["xss"],         "Doe",     "12345",    False),
            ("unicode_zip",     "John",           "Doe",     z["unicode"],False),
            ("numeric_names",   f["numeric"],     l["numeric"],"12345",  False),
            ("boundary_names",  f["boundary"],    l["boundary"],"99999", False),
            ("special_char",    f["special"],     "O'Hara",  "10001",    False),
        ]
