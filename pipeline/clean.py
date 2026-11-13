"""Redact sections containing public correspondents/speakers before API use.

Conservative design: a new top-level named heading ends a sensitive block,
but unknown headings do not, avoiding accidental disclosure of names.
"""
import re

SENSITIVE = re.compile(r'^#{0,6}\s*(Communications|Speakers)(?:\s*\([^)]*\))?\s*:?\s*$', re.I)
SAFE_SECTIONS = re.compile(
    r'^#{0,6}\s*(?:Motions|Background Information|Origin|Summary|Declared Interests|Vote|'
    r'Recommendations|City Council Decision|Committee Decision|Committee Recommendations|'
    r'Decision Advice and Other Information|Public Notice Given|Tracking Status|Financial Impact)'
    r'(?:\s*\([^)]*\))?\s*:?\s*$', re.I,
)
# Recognize HTML-style headings after copy/paste, e.g. "#### Communications (Committee)".

def strip_personal_sections(text: str) -> str:
    result: list[str] = []
    skipping = False
    for line in text.splitlines():
        heading = line.strip()
        if SENSITIVE.fullmatch(heading):
            skipping = True
            continue
        if skipping and SAFE_SECTIONS.fullmatch(heading):
            skipping = False
        if not skipping:
            result.append(line)
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(result)).strip()
