
from modules.decision_engine import evaluate_options


def test_recyclable_item():
    item = {
        "condition": "damaged",
        "material": "plastic",
        "repairable": False
    }

    options = evaluate_options(item)

    names = [option["option"] for option in options]

    assert "Repurpose" in names
    assert "Recycle" in names


def test_hazardous_item():
    item = {
        "condition": "damaged",
        "material": "metal",
        "repairable": False,
        "hazardous": True
    }

    options = evaluate_options(item)

    assert len(options) == 1
    assert options[0]["option"] == "Safe handling"
