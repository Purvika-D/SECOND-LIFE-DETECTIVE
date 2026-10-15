
from modules.recovery_passport import (
    create_recovery_passport,
    set_planned_outcome,
    confirm_recovery_outcome,
)


def test_create_passport():
    passport = create_recovery_passport(
        "Plastic bottle",
        material="plastic",
        selected_pathway="recycle",
    )

    assert passport["item_name"] == "Plastic bottle"
    assert passport["selected_pathway"] == "recycle"
    assert passport["status"] == "planned"
    assert passport["confirmed_outcome"] is None


def test_set_planned_outcome():
    passport = create_recovery_passport("Old chair")

    set_planned_outcome(passport, "Donate to a local charity")

    assert passport["planned_outcome"] == "Donate to a local charity"


def test_confirm_outcome():
    passport = create_recovery_passport("Old chair")

    confirm_recovery_outcome(
        passport,
        "Donated",
        evidence_note="User reported donation completed",
    )

    assert passport["status"] == "completed"
    assert passport["confirmed_outcome"] == "Donated"
    assert passport["events"][-1]["evidence_note"] == (
        "User reported donation completed"
    )
