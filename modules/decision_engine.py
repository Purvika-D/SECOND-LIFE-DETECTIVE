
def evaluate_options(item):
    """
    Compare recovery pathways for an unwanted item.

    Expected input:
        item = {
            "condition": "damaged",
            "material": "plastic",
            "repairable": False
        }
    """
    condition = item.get("condition", "unknown").lower()
    material = item.get("material", "unknown").lower()
    repairable = item.get("repairable", False)

    options = []

    # Repair: consider this when the item can be fixed.
    if repairable:
        options.append({
            "option": "Repair",
            "reason": "The item may be restored for continued use.",
            "priority": 1
        })

    # Reuse: consider items that are still in usable condition.
    if condition in ["good", "usable", "working"]:
        options.append({
            "option": "Reuse",
            "reason": "The item may be used again without major changes.",
            "priority": 1
        })

    # Repurpose: give an item a different use.
    if condition in ["damaged", "worn", "usable", "unknown"]:
        options.append({
            "option": "Repurpose",
            "reason": "Consider another use before discarding the item.",
            "priority": 2
        })

    # Recycling: material-specific recycling needs local verification.
    if material in [
        "plastic", "paper", "cardboard", "glass", "metal"
    ]:
        options.append({
            "option": "Recycle",
            "reason": "Check local recycling rules for this material.",
            "priority": 3
        })

    # Hazardous materials require safe handling first.
    if item.get("hazardous", False):
        options = [{
            "option": "Safe handling",
            "reason": (
                "Do not repair, reuse, or dismantle it until "
                "appropriate hazardous-waste guidance is checked."
            ),
            "priority": 0
        }]

    options.sort(key=lambda option: option["priority"])

    return options
