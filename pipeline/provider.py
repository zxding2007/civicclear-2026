"""Resolve the optional AI provider when a request is made, never at import time."""
from __future__ import annotations

from dataclasses import dataclass, field
import os
from typing import Literal, Mapping


@dataclass(frozen=True)
class AIConfig:
    provider: Literal['anthropic', 'deepseek']
    model: str
    api_key: str = field(repr=False)
    key_env: str

    @property
    def label(self) -> str:
        return 'DeepSeek' if self.provider == 'deepseek' else 'Claude'


def get_config(environ: Mapping[str, str] | None = None) -> AIConfig:
    env = os.environ if environ is None else environ
    anthropic_key = env.get('ANTHROPIC_API_KEY', '').strip()
    deepseek_key = env.get('DEEPSEEK_API_KEY', '').strip()
    selected = env.get('CIVICCLEAR_PROVIDER', '').strip().lower()
    if not selected:
        selected = 'deepseek' if deepseek_key and not anthropic_key else 'anthropic'
    if selected not in {'anthropic', 'deepseek'}:
        raise ValueError('CIVICCLEAR_PROVIDER must be anthropic or deepseek.')
    is_deepseek = selected == 'deepseek'
    return AIConfig(
        provider=selected,
        model=env.get('CIVICCLEAR_MODEL', '').strip() or ('deepseek-flash' if is_deepseek else 'claude-opus-5-5'),
        api_key=deepseek_key if is_deepseek else anthropic_key,
        key_env='DEEPSEEK_API_KEY' if is_deepseek else 'ANTHROPIC_API_KEY',
    )
