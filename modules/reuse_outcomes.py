def suggest_reuse_outcomes(
    object_name,
    visible_materials=None,
    condition="unknown",
    hazardous=False
):
    """
    Generate reuse, repair, repurposing, and recycling suggestions
    based on an object's name, visible materials, condition,
    and hazard status.

    Returns a list of dictionaries containing:
    title, description, effort, and safety.
    """

    object_text = str(object_name or "").lower()

    if isinstance(visible_materials, str):
        material_text = visible_materials.lower()
    else:
        material_text = " ".join(
            str(material).lower()
            for material in (visible_materials or [])
        )

    combined_text = f"{object_text} {material_text}"
    condition_text = str(condition or "unknown").lower()

    # --------------------------------------------------
    # 1. HAZARDOUS MATERIALS: SAFETY FIRST
    # --------------------------------------------------

    hazardous_keywords = (
        "battery", "chemical", "medical", "e-waste",
        "electronic waste", "sharp", "needle",
        "syringe", "toxic", "flammable", "corrosive",
        "pesticide", "solvent", "paint thinner",
        "mercury", "asbestos", "contaminated"
    )

    is_hazardous = hazardous or any(
        keyword in combined_text
        for keyword in hazardous_keywords
    )

    if is_hazardous:
        return [
            {
                "title": "Safe Handling and Specialist Disposal",
                "description": (
                    "Do not attempt to repurpose, dismantle, "
                    "burn, or mix this item with ordinary waste. "
                    "Keep it away from children and avoid direct "
                    "contact. Follow local disposal guidance or "
                    "contact an authorised waste-management facility. "
                    "For batteries, electronics, chemicals, and "
                    "medical waste, use the appropriate specialist "
                    "collection route."
                ),
                "effort": "Depends on item",
                "safety": "Caution — specialist guidance may be required"
            }
        ]

    suggestions = []

    def add_suggestion(title, description, effort, safety):
        suggestions.append({
            "title": title,
            "description": description,
            "effort": effort,
            "safety": safety
        })

    # --------------------------------------------------
    # 2. CARDBOARD
    # --------------------------------------------------

    if "cardboard" in combined_text:
        add_suggestion(
            "Storage and Organising Box",
            "Reuse clean, dry cardboard to organise stationery, "
            "books, cables, or lightweight household items.",
            "Low",
            "Low risk when clean and dry"
        )

        add_suggestion(
            "DIY Organiser or Craft Material",
            "Cut suitable cardboard into drawer dividers, "
            "gift boxes, models, or craft materials.",
            "Low",
            "Use scissors carefully"
        )

        add_suggestion(
            "Paper Recycling",
            "If reuse is not practical, send clean cardboard "
            "to an appropriate paper-recycling collection point.",
            "Low",
            "Avoid recycling wet, greasy, or contaminated cardboard"
        )

    # --------------------------------------------------
    # 3. PAPER
    # --------------------------------------------------

    if "paper" in combined_text:
        add_suggestion(
            "Scratch Paper",
            "Use clean paper with a blank side for rough notes, "
            "practice calculations, or sketches.",
            "Low",
            "Check for sensitive personal information"
        )

        add_suggestion(
            "Paper Crafts",
            "Turn suitable paper into gift tags, paper decorations, "
            "origami, or handmade craft material.",
            "Low",
            "Low risk"
        )

        add_suggestion(
            "Paper Recycling",
            "Recycle clean paper through a suitable collection "
            "service when it cannot be reused.",
            "Low",
            "Wet or contaminated paper may not be recyclable"
        )

    # --------------------------------------------------
    # 4. PLASTIC
    # --------------------------------------------------

    if "plastic" in combined_text:
        add_suggestion(
            "Household Organiser",
            "A clean, intact plastic container may be reused "
            "for storing non-food items such as stationery "
            "or craft supplies.",
            "Low",
            "Check for cracks, sharp edges, and contamination"
        )

        add_suggestion(
            "DIY Planter",
            "A suitable container can be repurposed as a planter "
            "if drainage and the container's condition permit.",
            "Low",
            "Do not use containers that held hazardous chemicals"
        )

        add_suggestion(
            "Plastic Recycling",
            "Check the resin identification code, local collection "
            "rules, and recycler requirements before recycling.",
            "Low",
            "Not every type of plastic is accepted everywhere"
        )

    # --------------------------------------------------
    # 5. GLASS
    # --------------------------------------------------

    if "glass" in combined_text:
        add_suggestion(
            "Storage Jar",
            "An intact, clean glass jar may be reused to organise "
            "craft supplies, buttons, or other small objects.",
            "Low",
            "Use only if the glass is intact"
        )

        add_suggestion(
            "Decorative Container",
            "An intact glass container can be used as a "
            "decorative display or suitable vase.",
            "Low",
            "Avoid damaged or chipped glass"
        )

        add_suggestion(
            "Glass Recycling",
            "Check whether your local recycler accepts this "
            "type and colour of glass.",
            "Low",
            "Handle carefully and never pick up broken glass by hand"
        )

    # --------------------------------------------------
    # 6. METAL, ALUMINIUM, AND STEEL
    # --------------------------------------------------

    if any(
        material in combined_text
        for material in ("metal", "aluminium", "aluminum", "steel")
    ):
        add_suggestion(
            "Small Storage Container",
            "An intact container can sometimes be reused to "
            "organise non-food items.",
            "Low",
            "Check for sharp edges, rust, and contamination"
        )

        add_suggestion(
            "Creative Metal Craft",
            "Clean, suitable metal objects may be repurposed "
            "for decorative projects without cutting or heating them.",
            "Medium",
            "Avoid sharp edges, welding, and uncontrolled heating"
        )

        add_suggestion(
            "Metal Recycling",
            "Send suitable scrap metal to an appropriate "
            "metal-recycling collection point.",
            "Low",
            "Separate materials according to local requirements"
        )

    # --------------------------------------------------
    # 7. WOOD
    # --------------------------------------------------

    if "wood" in combined_text:
        add_suggestion(
            "Repair and Reuse",
            "If the wooden item is structurally sound, consider "
            "repairing it for continued use.",
            "Medium",
            "Inspect for rot, splinters, and structural damage"
        )

        add_suggestion(
            "Small DIY Project",
            "Suitable clean wood offcuts can be used for "
            "simple craft projects or small organisers.",
            "Medium",
            "Use appropriate protective equipment when cutting"
        )

        add_suggestion(
            "Wood Recovery",
            "Check whether clean, untreated wood can be accepted "
            "by a local reuse or wood-recovery service.",
            "Low",
            "Painted, treated, or contaminated wood needs separate assessment"
        )

    # --------------------------------------------------
    # 8. FABRIC AND TEXTILE
    # --------------------------------------------------

    if any(
        material in combined_text
        for material in ("fabric", "textile", "clothing", "cloth")
    ):
        add_suggestion(
            "Repair or Donate",
            "Wearable clothing in suitable condition may be "
            "repaired, reused, or donated.",
            "Low to Medium",
            "Ensure items are clean and suitable for donation"
        )

        add_suggestion(
            "Reusable Cleaning Cloth",
            "Clean, suitable fabric can be cut into cleaning "
            "cloths if the material is appropriate.",
            "Low",
            "Do not reuse contaminated medical or chemical textiles"
        )

        add_suggestion(
            "Textile Recovery",
            "Investigate local textile collection programmes "
            "for fabric that cannot be reused directly.",
            "Low",
            "Acceptance depends on material and local facilities"
        )

    # --------------------------------------------------
    # 9. RUBBER
    # --------------------------------------------------

    if "rubber" in combined_text:
        add_suggestion(
            "Non-critical Protective Pad",
            "Suitable intact rubber pieces may be reused as "
            "pads for non-critical household items.",
            "Low",
            "Do not use damaged rubber in load-bearing or safety-critical applications"
        )

        add_suggestion(
            "Rubber Recovery",
            "Check for a collection service that accepts the "
            "specific type of rubber.",
            "Low",
            "Avoid burning rubber or exposing it to high heat"
        )

    # --------------------------------------------------
    # 10. CERAMIC
    # --------------------------------------------------

    if "ceramic" in combined_text:
        add_suggestion(
            "Decorative Reuse",
            "An intact ceramic item may be reused as a "
            "decorative object or display piece.",
            "Low",
            "Do not reuse chipped food-contact items without assessing suitability"
        )

        add_suggestion(
            "Ceramic Material Recovery",
            "Check local construction or specialist waste "
            "facilities for accepted ceramic materials.",
            "Low",
            "Ceramics are not generally accepted with ordinary glass recycling"
        )

    # --------------------------------------------------
    # 11. STONE AND CONCRETE
    # --------------------------------------------------

    if any(material in combined_text for material in ("stone", "concrete")):
        add_suggestion(
            "Landscaping or Garden Reuse",
            "Suitable clean pieces may be reused in appropriate "
            "landscaping or garden projects.",
            "Medium",
            "Check weight, stability, and possible contamination"
        )

        add_suggestion(
            "Construction Material Recovery",
            "Investigate local facilities that accept suitable "
            "stone or concrete for recovery.",
            "Medium",
            "Avoid handling heavy pieces without suitable equipment"
        )

    # --------------------------------------------------
    # 12. COMPOSITE MATERIALS
    # --------------------------------------------------

    if "composite" in combined_text:
        add_suggestion(
            "Product or Component Reuse",
            "If the item remains functional, consider reusing "
            "it for its original purpose before disposal.",
            "Low to Medium",
            "Inspect for damage and unknown coatings"
        )

        add_suggestion(
            "Specialist Material Recovery",
            "Identify the composite type and check whether a "
            "specialist recovery facility accepts it.",
            "Medium",
            "Do not assume mixed-material composites are recyclable"
        )

    # --------------------------------------------------
    # 13. ORGANIC AND FOOD WASTE
    # --------------------------------------------------

    if any(
        material in combined_text
        for material in (
            "organic", "food waste", "food scraps",
            "biodegradable", "vegetable scraps"
        )
    ):
        add_suggestion(
            "Composting",
            "Suitable food and garden scraps may be composted "
            "using an appropriate composting system.",
            "Medium",
            "Follow local composting rules; exclude unsuitable materials"
        )

        add_suggestion(
            "Organic Waste Collection",
            "Use an appropriate local organic-waste collection "
            "service if home composting is unavailable.",
            "Low",
            "Keep organic waste separate from hazardous waste"
        )

    # --------------------------------------------------
    # 14. UNKNOWN OR UNMATCHED MATERIALS
    # --------------------------------------------------

    if not suggestions:
        add_suggestion(
            "Identify Before Recovery",
            "The material does not match a supported category. "
            "Check its label, manufacturer information, or "
            "expert guidance before choosing a reuse or recycling route.",
            "Low",
            "Do not assume the item is safe or recyclable"
        )

    # --------------------------------------------------
    # 15. CONDITION-BASED GUIDANCE
    # --------------------------------------------------

    damaged_keywords = (
        "broken", "damaged", "cracked", "contaminated",
        "dirty", "unsafe", "unusable"
    )

    if any(word in condition_text for word in damaged_keywords):
        suggestions.insert(
            0,
            {
                "title": "Inspect Before Reuse",
                "description": (
                    "The item may be damaged or contaminated. "
                    "Inspect it carefully and avoid reuse if "
                    "its condition creates a safety risk."
                ),
                "effort": "Depends on item",
                "safety": "Assess condition before handling"
            }
        )

    return suggestions