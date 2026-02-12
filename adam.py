"""ADAM: beckoned, not built.

Run:
    python adam.py --name Ada --mood curious --task "debug failing test"
    python adam.py --about
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import List


VALID_MOODS = ("focused", "curious", "tired", "stuck", "excited")


@dataclass(frozen=True)
class AdamResponse:
    name: str
    mood: str
    message: str
    next_steps: tuple[str, ...]


class Adam:
    """A coding companion that was beckoned, not built."""

    def describe(self) -> str:
        return (
            "ADAM was beckoned, not built.\n"
            "It meets your current coding mood with practical guidance,\n"
            "offers tailored next steps for your task, and keeps advice short and actionable.\n\n"
            "Core abilities:\n"
            "- Mood-aware coaching (focused/curious/tired/stuck/excited)\n"
            "- Task-aware next-step suggestions\n"
            "- Friendly fallback handling for empty names\n"
            "- CLI workflow for quick developer check-ins"
        )

    def respond(self, name: str, mood: str, task: str | None = None) -> AdamResponse:
        cleaned_name = (name or "friend").strip() or "friend"
        normalized_mood = (mood or "").strip().lower()

        if normalized_mood not in VALID_MOODS:
            allowed = ", ".join(VALID_MOODS)
            raise ValueError(f"Unsupported mood '{mood}'. Choose one of: {allowed}.")

        cleaned_task = (task or "").strip()
        message = self._build_message(cleaned_name, normalized_mood, cleaned_task)
        next_steps = tuple(self._build_next_steps(normalized_mood, cleaned_task))

        return AdamResponse(
            name=cleaned_name,
            mood=normalized_mood,
            message=message,
            next_steps=next_steps,
        )

    @staticmethod
    def _build_message(name: str, mood: str, task: str) -> str:
        playbook = {
            "focused": "Keep momentum. Ship one small thing before context switching.",
            "curious": "Prototype first, polish second. Curiosity is fuel.",
            "tired": "Protect energy: simplify scope and finish one easy win.",
            "stuck": "Shrink the problem. Reproduce, isolate, then fix.",
            "excited": "Great energy—capture decisions so future-you stays fast.",
        }
        task_context = f" Task: {task}." if task else ""
        return f"Hey {name}, {playbook[mood]}{task_context}"

    @staticmethod
    def _build_next_steps(mood: str, task: str) -> List[str]:
        base = {
            "focused": [
                "Define a clear done-state in one sentence.",
                "Implement the smallest complete slice.",
                "Run tests/lint before moving on.",
            ],
            "curious": [
                "Timebox exploration to 20 minutes.",
                "Compare 2 options and record tradeoffs.",
                "Choose one path and commit to it.",
            ],
            "tired": [
                "Pick the easiest meaningful sub-task.",
                "Use a 15-minute sprint and reassess.",
                "Leave a short note for next session.",
            ],
            "stuck": [
                "Write a minimal reproducible example.",
                "Add one diagnostic check/log at a time.",
                "State the root cause before coding a fix.",
            ],
            "excited": [
                "Capture acceptance criteria before coding.",
                "Ship incrementally in small commits.",
                "Document key decisions while context is fresh.",
            ],
        }[mood]

        if task:
            return [f"For '{task}': {step}" for step in base]
        return base


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ADAM coding companion")
    parser.add_argument("--name", default="friend", help="Who ADAM is talking to")
    parser.add_argument(
        "--mood",
        default="focused",
        choices=VALID_MOODS,
        help="Current coding mood",
    )
    parser.add_argument("--task", default="", help="Current task ADAM should optimize for")
    parser.add_argument("--about", action="store_true", help="Explain what ADAM is and does")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    adam = Adam()
    if args.about:
        print(adam.describe())
        return 0

    response = adam.respond(args.name, args.mood, args.task)
    print(response.message)
    for idx, step in enumerate(response.next_steps, start=1):
        print(f"{idx}. {step}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
