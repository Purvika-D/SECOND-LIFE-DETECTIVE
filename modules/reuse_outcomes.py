def suggest_reuse_outcomes(
    object_name,
    visible_materials=None,
    condition="unknown",
    hazardous=False,
):
    """
    Suggest possible second-life outcomes for an identified scrap item.

    Returns a list of suggestions for display in the website.
    """

    name = str(object_name or "").lower()
    materials = " ".join(
        str(material).lower()
        for material in (visible_materials or [])
    )
    condition = str(condition or "unknown").lower()

    # Safety takes priority over reuse.
    if hazardous:
        return [
            {
                "title": "Safe handling and specialist recovery",
                "description": (
                    "Do not dismantle or repurpose this item. "
                    "Check an authorised collection or recycling service."
                ),
                "effort": "Specialist assistance",
                "safety": "Safety first",
            }
        ]

    # Electronic equipment
    if any(word in name for word in [
        "computer", "laptop", "phone", "mobile",
        "electronic", "printer", "keyboard", "monitor",
    ]):
        return [
            {
                "title": "Repair and reuse",
                "description": (
                    "If the device is functional or repairable, "
                    "consider using it again or donating it after "
                    "appropriate data removal and safety checks."
                ),
                "effort": "Depends on condition",
                "safety": "Check electrical safety",
            },
            {
                "title": "Component recovery",
                "description": (
                    "A qualified electronics recycler may recover "
                    "suitable components and materials."
                ),
                "effort": "Specialist assistance",
                "safety": "Do not dismantle casually",
            },
        ]

    # Plastic bottles and containers
    if any(word in name for word in [
        "plastic bottle", "water bottle", "plastic container",
    ]):
        return [
            {
                "title": "Plant watering container",
                "description": (
                    "A clean, suitable container may be reused "
                    "for watering plants."
                ),
                "effort": "Easy",
                "safety": "Avoid containers that held chemicals",
            },
            {
                "title": "Seedling pot",
                "description": (
                    "A suitable container can be adapted into "
                    "a small pot with appropriate drainage."
                ),
                "effort": "Easy",
                "safety": "Use only clean, suitable containers",
            },
            {
                "title": "Material recycling",
                "description": (
                    "If reuse is unsuitable, check local rules "
                    "for recycling the plastic type."
                ),
                "effort": "Depends on local facilities",
                "safety": "Check material and local rules",
            },
        ]

    # Cardboard and paper
    if any(word in name or word in materials for word in [
        "cardboard", "paper", "carton",
    ]):
        return [
            {
                "title": "Storage organiser",
                "description": (
                    "Clean, dry cardboard can be repurposed "
                    "for lightweight storage or drawer dividers."
                ),
                "effort": "Easy",
                "safety": "Keep away from moisture",
            },
            {
                "title": "Packing material",
                "description": (
                    "Suitable cardboard can be reused to protect "
                    "items during storage or moving."
                ),
                "effort": "Easy",
                "safety": "Avoid contaminated material",
            },
            {
                "title": "Paper or cardboard recycling",
                "description": (
                    "Recycle it where local collection rules permit."
                ),
                "effort": "Easy",
                "safety": "Keep it clean and dry",
            },
        ]

    # Wooden furniture
    if any(word in name for word in [
        "chair", "table", "wood", "furniture", "shelf",
    ]) or "wood" in materials:
        return [
            {
                "title": "Repair and reuse",
                "description": (
                    "If structurally sound, repair the item "
                    "for continued use."
                ),
                "effort": "Depends on damage",
                "safety": "Check stability before use",
            },
            {
                "title": "Plant stand or storage shelf",
                "description": (
                    "Suitable, stable wooden parts may be adapted "
                    "for another household use."
                ),
                "effort": "Moderate",
                "safety": "Check load-bearing strength",
            },
        ]

    # Clothing and fabric
    if any(word in name or word in materials for word in [
        "shirt", "t-shirt", "cloth", "fabric", "jeans", "clothing",
    ]):
        return [
            {
                "title": "Cleaning cloth",
                "description": (
                    "Clean, suitable fabric can be cut into "
                    "reusable household cleaning cloths."
                ),
                "effort": "Easy",
                "safety": "Wash before reuse",
            },
            {
                "title": "Reusable fabric pouch",
                "description": (
                    "Suitable fabric can be sewn into a small "
                    "pouch or storage bag."
                ),
                "effort": "Moderate",
                "safety": "Check fabric condition",
            },
        ]

    # Glass jars
    if any(word in name for word in [
        "glass jar", "jar", "glass bottle",
    ]):
        return [
            {
                "title": "Storage container",
                "description": (
                    "An intact, clean jar may be reused to store "
                    "suitable household items."
                ),
                "effort": "Easy",
                "safety": "Do not reuse chipped or cracked glass",
            },
            {
                "title": "Decorative container",
                "description": (
                    "An intact jar can be used as a simple "
                    "decorative container."
                ),
                "effort": "Easy",
                "safety": "Check for cracks and sharp edges",
            },
        ]

    # General fallback when the object is not recognised by these rules.
    return [
        {
            "title": "Explore repair or continued use",
            "description": (
                "Check whether the item can be safely repaired, "
                "donated, or used again in its current form."
            ),
            "effort": "Depends on condition",
            "safety": "Inspect before reuse",
        },
        {
            "title": "Explore creative repurposing",
            "description": (
                "Consider another practical use based on the item's "
                "shape, condition, and verified material."
            ),
            "effort": "Depends on the item",
            "safety": "Avoid unsafe modifications",
        },
        {
            "title": "Check recycling options",
            "description": (
                "Identify the material and check which local "
                "recycling facilities accept it."
            ),
            "effort": "Depends on local facilities",
            "safety": "Verify material and local rules",
        },
    ]