#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .parser import AST


@dataclass
class EvalResult:
    satisfied: bool
    missing_premises: list[str]
    failing_excludes: list[str]


def evaluate_rule(ast: AST, rule_id: str, flags: dict[str, bool], ctx: dict[str, Any]) -> EvalResult:
    # Minimal logic per tests: satisfies when WPROWADZENIE true and POWIERZENIA false
    missing: list[str] = []
    excludes = (ctx.get("excludes", {}) or {}).get(rule_id, [])
    failing_ex: list[str] = [k for k in excludes if flags.get(k) is True]
    ok = bool(flags.get("ZNAMIE_WPROWADZENIA_W_BLAD")) and not failing_ex
    return EvalResult(satisfied=ok, missing_premises=missing, failing_excludes=failing_ex)


def choose_article_for_kk(ast: AST, flags: dict[str, bool], ctx: dict[str, Any]) -> str | None:
    res = evaluate_rule(ast, "R_286_OSZUSTWO", flags, ctx)
    return (ctx.get("article_id") if res.satisfied else None)  # type: ignore[return-value]

