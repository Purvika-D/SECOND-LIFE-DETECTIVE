
from modules.digital_twin import (
    create_digital_twin,
    update_digital_twin,
    select_recovery_pathway,
)


def test_create_digital_twin():
    twin = create_digital_twin(
        "Plastic bottle",
        material="plastic",
        condition="usable",
    )

    assert twin["item_name"] == "Plastic bottle"
    assert twin["current_state"] == "identified"
    assert len(twin["events"]) == 1


def test_update_digital_twin():
    twin = create_digital_twin("Old chair")

    update_digital_twin(
        twin,
        "in_progress",
        "Repair has started.",
    )

    assert twin["current_state"] == "in_progress"
    assert len(twin["events"]) == 2


def test_select_recovery_pathway():
    twin = create_digital_twin("Old chair")

    select_recovery_pathway(twin, "repair")

    assert twin["selected_pathway"] == "repair"
    assert twin["current_state"] == "pathway_selected"
