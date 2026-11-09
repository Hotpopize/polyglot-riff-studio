from __future__ import annotations

import re
from typing import Any, Optional, Sequence

ALLOWED_STAGES = ("COMPLIMENT", "CHAMELEON", "COUNTERACT", "CURIOSITY")
STAGE_ORDER = {stage: idx + 1 for idx, stage in enumerate(ALLOWED_STAGES)}

# Known Russian Cyrillic homonym stems / hazardous calque mistakes when writing Czech
RUSSIAN_CYRILLIC_RE = re.compile(r"[\u0400-\u04FF]")


def strip_html_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text or "").strip()


def ensure_slang_spans(text_html: str, idiom_terms: Sequence[str]) -> str:
    """Wrap any un-anchored idiom occurrences in <span class='slang-token'>."""
    updated = text_html
    for term in idiom_terms:
        if not term:
            continue
        if f'data-term="{term}"' in updated:
            continue
        pattern = re.compile(re.escape(term), flags=re.IGNORECASE)
        match = pattern.search(updated)
        if match:
            matched_surface = match.group(0)
            updated = (
                updated[: match.start()]
                + f'<span class="slang-token" data-term="{term}">{matched_surface}</span>'
                + updated[match.end() :]
            )
    return updated


def validate_graph_commit(
    *,
    card: Optional[dict[str, Any]] = None,
    idiom: Optional[dict[str, Any]] = None,
    edge: Optional[dict[str, Any]] = None,
    target_register: Optional[str] = None,
    false_friends: Optional[Sequence[dict[str, Any]]] = None,
) -> dict[str, Any]:
    """Python port & extension of db/graph_relation_validator.js with false-friend checks."""
    checks: list[dict[str, Any]] = []
    warnings: list[str] = []

    if card:
        stage = card.get("stage", "")
        valid_stage = stage in ALLOWED_STAGES
        checks.append(
            {
                "rule": "(:Card) 4-C Stage Constraint",
                "passed": valid_stage,
                "detail": f"Valid stage: {stage}" if valid_stage else f"Invalid stage: {stage}",
            }
        )

        card_reg = card.get("register_id") or card.get("lang")
        reg_ok = not target_register or target_register == "ALL" or card_reg == target_register
        checks.append(
            {
                "rule": "2-Tier Language -> Register Partition Rule",
                "passed": bool(reg_ok and card_reg),
                "detail": (
                    f"Bound cleanly to register {card_reg}"
                    if reg_ok and card_reg
                    else f"Register mismatch ({card_reg} vs {target_register})"
                ),
            }
        )

        plain = strip_html_tags(card.get("text_html") or card.get("text") or "")
        if card_reg and card_reg.startswith("CZ_"):
            has_cyrillic_leak = bool(RUSSIAN_CYRILLIC_RE.search(plain))
            checks.append(
                {
                    "rule": "Slavic Script Isolation (No Cyrillic Leak in Czech)",
                    "passed": not has_cyrillic_leak,
                    "detail": (
                        "Clean Latin/Czech orthography"
                        if not has_cyrillic_leak
                        else "Detected Cyrillic characters inside Czech card text"
                    ),
                }
            )

        if false_friends and card_reg and card_reg.startswith("CZ_"):
            lowered = plain.lower()
            for ff in false_friends:
                term = (ff.get("target_term") or ff.get("cz") or "").lower()
                if term and term in lowered:
                    warnings.append(
                        f"False-friend shield note on '{term}': ensure Czech sense ({ff.get('safe_meaning')}), not RU {ff.get('trap_term')}."
                    )

    if idiom and card:
        term = idiom.get("term", "")
        text_val = card.get("text_html") or card.get("text") or ""
        anchored = f'data-term="{term}"' in text_val or term.lower() in text_val.lower()
        checks.append(
            {
                "rule": "[:INJECTS_SLANG] Lexical Anchor Rule",
                "passed": anchored,
                "detail": (
                    f'Idiom "{term}" anchored in Card text'
                    if anchored
                    else f'Idiom "{term}" missing from Card text'
                ),
            }
        )

    if edge:
        w = edge.get("weight")
        valid_w = isinstance(w, (int, float)) and 0.15 <= float(w) <= 0.99
        checks.append(
            {
                "rule": "FSRS Edge Weight & Stability Bounds",
                "passed": valid_w,
                "detail": (
                    f"w={w}, S={edge.get('stability', 5.0)}d"
                    if valid_w
                    else f"Edge weight {w} outside [0.15, 0.99]"
                ),
            }
        )

    return {
        "valid": all(c["passed"] for c in checks),
        "checks": checks,
        "warnings": warnings,
    }

