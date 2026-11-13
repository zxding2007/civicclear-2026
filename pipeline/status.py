"""Verified stage -> status, with final council decisions taking precedence.

A *committee* receipt must never override a later *council* adoption.
"""
from .schema import DecisionCard

LABELS = {
    'final_adopted': 'Adopted by City Council',
    'final_amended': 'Adopted with amendments by City Council',
    'received': 'Received for information — not an approval',
    'referred': 'Referred for further consideration',
    'deferred': 'Decision deferred',
    'not_adopted': 'Not adopted',
    'committee_only': 'Committee action — not final Council approval',
    'recommendation_only': 'Staff recommendation only',
    'unclear': 'Unclear — refer to official record',
}


def _resolved_outcome(outcome: str, stage_type: str) -> str:
    if outcome == 'received_for_information': return 'received'
    if outcome == 'referred': return 'referred'
    if outcome == 'deferred': return 'deferred'
    if outcome == 'not_adopted': return 'not_adopted'
    if stage_type == 'council_decision':
        if outcome == 'adopted': return 'final_adopted'
        if outcome == 'adopted_with_amendments': return 'final_amended'
    return 'unclear'


def overall_status(card: DecisionCard, verified: list[bool]) -> str:
    if len(verified) != len(card.stages):
        raise ValueError('Verification flags must match stage count')
    trustworthy = [s for s, ok in zip(card.stages, verified) if ok]
    council = [s for s in trustworthy if s.stage_type == 'council_decision']
    committee = [s for s in trustworthy if s.stage_type == 'committee_decision']
    # Stage ordering is chronological: the most recent Council decision wins.
    if council:
        return _resolved_outcome(council[-1].outcome, 'council_decision')
    if committee:
        latest = committee[-1]
        if latest.outcome in {'received_for_information', 'referred', 'deferred', 'not_adopted'}:
            return _resolved_outcome(latest.outcome, 'committee_decision')
        return 'committee_only'
    if any(s.stage_type == 'staff_recommendation' for s in trustworthy):
        return 'recommendation_only'
    return 'unclear'
