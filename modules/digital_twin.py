
from datetime import datetime, timezone


def create_digital_twin(item_name, material="unknown", condition="unknown"):
    """Create a digital record for an item's recovery journey."""
    now = datetime.now(timezone.utc).isoformat()

    return {
        "item_name": item_name,
        "material": material,
        "condition": condition,
        "current_state": "identified",
        "selected_pathway": None,
        "events": [
            {
                "state": "identified",
                "timestamp": now,
                "note": "Item added to the recovery tracker."
            }
        ]
    }


def update_digital_twin(twin, new_state, note=""):
    """Record a state change in the item's recovery journey."""
    allowed_states = [
        "identified",
        "assessment",
        "pathway_selected",
        "in_progress",
        "recovered",
        "recycled",
        "disposed_safely"
    ]

    if new_state not in allowed_states:
        raise ValueError(f"Invalid state: {new_state}")

    now = datetime.now(timezone.utc).isoformat()

    twin["current_state"] = new_state
    twin["events"].append({
        "state": new_state,
        "timestamp": now,
        "note": note
    })

    return twin


def select_recovery_pathway(twin, pathway):
    """Record the recovery pathway chosen for an item."""
    twin["selected_pathway"] = pathway

    return update_digital_twin(
        twin,
        "pathway_selected",
        f"Selected recovery pathway: {pathway}"
    )
