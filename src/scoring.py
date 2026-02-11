"""Rubric scoring helpers for paired LLM answers."""

from __future__ import annotations

from typing import Any


def score_answer(answer: str, criteria: list[dict[str, Any]]) -> dict[str, Any]:
    scores: dict[str, float] = {}
    notes: list[str] = []
    lowered = answer.lower()

    for item in criteria:
        key = item["id"]
        keywords = [k.lower() for k in item.get("keywords", [])]
        hits = sum(1 for keyword in keywords if keyword in lowered)
        if not keywords:
            value = 4.0 if len(answer.strip()) > 20 else 2.0
        else:
            ratio = hits / len(keywords)
            value = round(1 + ratio * 4, 2)
        scores[key] = value
        notes.append(f"{key}: {value} ({hits}/{len(keywords) or 1} keyword hits)")

    weighted = 0.0
    for item in criteria:
        weighted += scores[item["id"]] * float(item.get("weight", 1.0))
    total_weight = sum(float(item.get("weight", 1.0)) for item in criteria) or 1.0
    return {
        "scores": scores,
        "total": round(weighted / total_weight, 2),
        "notes": notes,
    }


def compare_pair(pair: dict[str, Any], rubric: dict[str, Any]) -> dict[str, Any]:
    criteria = rubric["criteria"]
    result_a = score_answer(pair["answer_a"], criteria)
    result_b = score_answer(pair["answer_b"], criteria)
    preferred = "A" if result_a["total"] >= result_b["total"] else "B"
    return {
        "pair_id": pair["id"],
        "preferred": preferred,
        "A": result_a,
        "B": result_b,
        "criteria_version": rubric.get("version", "1.0"),
    }
