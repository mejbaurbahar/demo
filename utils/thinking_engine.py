import json
import os
from datetime import datetime


class ThinkingEngine:
    """
    AI Thinking & Transparency Engine.
    Logs every reasoning step made by the autonomous QA system.
    Provides a full audit trail for the Transparency Report.
    """

    LEVELS = {"INFO", "WARNING", "ERROR", "CRITICAL"}

    def __init__(self, log_path: str = "reports/ai_thinking_log.json"):
        self.log_path = log_path
        self.session_thoughts: list = []
        self._init_log()

    def _init_log(self):
        os.makedirs("reports", exist_ok=True)
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def think(self, thought: str, level: str = "INFO"):
        """Record a reasoning step and print it to stdout (ASCII-safe)."""
        level = level if level in self.LEVELS else "INFO"
        entry = {
            "timestamp": str(datetime.now()),
            "level":     level,
            "thought":   thought
        }
        # ASCII-safe console output (no emojis to avoid Windows cp1252 issues)
        prefix = {"INFO": "[AI]", "WARNING": "[WARN]", "ERROR": "[ERR]", "CRITICAL": "[CRIT]"}
        print(f"{prefix.get(level, '[AI]')} {thought}")

        self.session_thoughts.append(entry)
        self._persist(entry)

    def _persist(self, entry: dict):
        """Append entry to the JSON log file."""
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
            logs.append(entry)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    def clear_session(self):
        """Clears in-memory session thoughts (does not clear persisted log)."""
        self.session_thoughts = []

    def get_summary(self) -> list:
        """Returns the list of reasoning steps recorded this session."""
        return self.session_thoughts

    def get_decisions_by_level(self, level: str) -> list:
        """Filters session thoughts by severity level."""
        return [t for t in self.session_thoughts if t["level"] == level]
