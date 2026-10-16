    if identification is not None:
        if not isinstance(identification, dict):
            st.error(
                "The identification service returned an unexpected response. "
                "Please try again."
            )

        elif identification.get("error"):
            st.error(str(identification["error"]))

        elif identification.get("demo_mode"):
            st.warning(
                "⚠️ DEMONSTRATION MODE: Live AI identification is currently "
                "unavailable. The uploaded item has not been identified, "
                "and its material/category has not been verified."
            )
            st.info(
                "You can still explore the app interface. Try the analysis "
                "again later when the AI service is available. Do not treat "
                "this result as an actual identification."
            )

        else:
            condition_map = {
                "Let the system decide": "unknown",
                "Good / usable": "good",
                "Damaged / needs repair": "damaged",
            }
            condition = condition_map[condition_choice]

            materials = identification.get("visible_materials", [])
            if isinstance(materials, str):
                materials = [materials]
            elif not isinstance(materials, list):
                materials = [str(materials)] if materials else []

            object_text = str(
                identification.get("object", "Unknown object")
            )
            category = str(
                identification.get("category", "uncertain")
            ).lower()
            safety_text = str(
                identification.get("safety_note", "")
            ).lower()
            material_text = " ".join(
                str(m).lower() for m in materials
            )
            combined_text = (
                f"{object_text.lower()} {category} "
                f"{safety_text} {material_text}"
            )

            hazardous_terms = (
                "hazard", "e-waste", "electronic waste", "battery",
                "chemical", "medical", "needle", "syringe", "sharp",
                "flammable", "corrosive", "toxic", "mercury",
                "asbestos", "pesticide",
            )
            hazardous = any(
                term in combined_text for term in hazardous_terms
            )

            try:
                raw_outcomes = suggest_reuse_outcomes(
                    object_name=object_text,
                    visible_materials=materials,
                    condition=condition,
                    hazardous=hazardous,
                )

                options = []
                for outcome in raw_outcomes or []:
                    title = str(
                        outcome.get("title", "Recovery option")
                    )
                    description = str(
                        outcome.get("description", "")
                    )
                    effort = str(
                        outcome.get("effort", "Not specified")
                    )
                    safety = str(
                        outcome.get(
                            "safety",
                            "Follow appropriate safety guidance",
                        )
                    )

                    reason_parts = [
                        description,
                        f"Effort: {effort}.",
                        f"Safety: {safety}.",
                    ]

                    options.append({
                        "option": title,
                        "reason": " ".join(
                            part for part in reason_parts if part
                        ).strip(),
                    })

            except Exception as exc:
                st.error(
                    "The recovery recommendation module failed. "
                    "Check modules/reuse_outcomes.py for an error."
                )
                options = []

            twin = create_digital_twin(
                item_name=object_text,
                material=", ".join(str(m) for m in materials) or "unknown",
                condition=condition,
            )

            passport = create_recovery_passport(
                item_name=object_text,
                material=", ".join(str(m) for m in materials) or "unknown",
            )

            st.session_state["identification"] = identification
            st.session_state["recovery_options"] = options
            st.session_state["digital_twin"] = twin
            st.session_state["recovery_passport"] = passport
            st.session_state["analysis_condition"] = condition
            st.session_state["analysis_material"] = (
                ", ".join(str(m) for m in materials) or "unknown"
            )
            st.session_state["analysis_hazardous"] = hazardous
            st.session_state["analysis_image_name"] = uploaded_image.name
            st.session_state["plan_saved"] = False