
from datetime import datetime, timezone
from uuid import uuid4


def create_recovery_passport(
    item_name,
    material="unknown",
    selected_pathway="undecided",
):
    """Create a record of an item's planned recovery journey."""
    return {
        "passport_id": str(uuid4()),
        "item_name": item_name,
        "material": material,
        "selected_pathway": selected_pathway,
        "status": "planned",
        "planned_outcome": None,
        "confirmed_outcome": None,
        "events": [
            {
                "event": "passport_created",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "details": "Recovery journey recorded as planned."
            }
        ]
    }


def set_planned_outcome(passport, outcome):
    """Record what the user intends to do with the item."""
    passport["planned_outcome"] = outcome

    passport["events"].append({
        "event": "outcome_planned",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "details": outcome
    })

    return passport


def confirm_recovery_outcome(passport, outcome, evidence_note=""):
    """Record a recovery outcome reported as completed."""
    if not outcome or not outcome.strip():
        raise ValueError("Outcome cannot be empty.")

    passport["confirmed_outcome"] = outcome
    passport["status"] = "completed"

    passport["events"].append({
        "event": "outcome_confirmed",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "details": outcome,
        "evidence_note": evidence_note
    })

    return passport
