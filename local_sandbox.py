from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CommandResult:
    stdout: str
    stderr: str
    exit_code: int | None


class LocalFiles:
    def write(self, path: str, content: str) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


class LocalCommands:
    def run(self, command: str, timeout: int = 120, user: str | None = None) -> CommandResult:
        try:
            completed = subprocess.run(
                command,
                shell=True,
                executable="/bin/bash",
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
                check=False,
            )
            return CommandResult(
                stdout=completed.stdout,
                stderr=completed.stderr,
                exit_code=completed.returncode,
            )
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout if isinstance(exc.stdout, str) else ""
            stderr = exc.stderr if isinstance(exc.stderr, str) else ""
            return CommandResult(
                stdout=stdout,
                stderr=f"{stderr}\nTimed out after {timeout}s".strip(),
                exit_code=None,
            )


class LocalSandbox:
    def __init__(self) -> None:
        self.files = LocalFiles()
        self.commands = LocalCommands()

    def set_timeout(self, *args, **kwargs) -> None:
        return None

    def kill(self) -> None:
        return None


def create_sandbox() -> LocalSandbox:
    return LocalSandbox()
