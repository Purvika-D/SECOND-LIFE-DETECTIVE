import streamlit as st

from modules.identification import identify_object
from modules.reuse_outcomes import suggest_reuse_outcomes
from modules.digital_twin import (
    create_digital_twin,
    select_recovery_pathway,
    update_digital_twin,
)
from modules.recovery_passport import (
    create_recovery_passport,
    set_planned_outcome,
    confirm_recovery_outcome,
)

st.set_page_config(
    page_title="Second-Life Detective",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------ Styling ------------------------------
st.markdown(
    """
    <style>
    :root { color-scheme: light; }
    .stApp { background: #f7f6ee; color: #20352a; }
    [data-testid="stHeader"] { background: rgba(247,246,238,0.92); }
    .block-container { max-width: 1120px; padding-top: 2rem; padding-bottom: 3rem; }
    h1, h2, h3 { color: #1f503b !important; }
    p, label, .stMarkdown { color: #293b31; }
    div.stButton > button, div[data-testid="stFormSubmitButton"] > button {
        background: #1f503b; color: white; border: 0; border-radius: 12px;
        padding: 0.65rem 1.1rem; font-weight: 650; min-height: 2.8rem;
    }
    div.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
        background: #286749; color: white; border: 0;
    }
    [data-testid="stFileUploader"] {
        background: #fff; border: 1px dashed #9bb8a1; border-radius: 16px; padding: 0.8rem;
    }
    .hero {
        background: linear-gradient(125deg, #1f503b, #2f7051);
        border-radius: 24px; padding: 2.1rem 2.2rem; color: #fff; margin-bottom: 1.2rem;
    }
    .hero h1 { color: white !important; font-size: 2.55rem; margin: 0 0 .45rem 0; }
    .hero p { color: #edf5e9 !important; font-size: 1.08rem; margin: 0; }
    .eyebrow { color: #d6e8d7 !important; font-size: .78rem; letter-spacing: .13em; font-weight: 750; }
    .result-card {
        background: #fff; border: 1px solid #e0e8dc; border-radius: 18px;
        padding: 1rem 1.1rem; margin-bottom: .7rem; min-height: 100px;
    }
    .result-label { color: #607466; font-size: .78rem; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; }
    .result-value { color: #1f503b; font-size: 1.08rem; font-weight: 700; margin-top: .28rem; overflow-wrap: anywhere; }
    .path-card {
        background: white; border: 1px solid #e0e8dc; border-left: 5px solid #4f8861;
        border-radius: 14px; padding: 1rem 1.1rem; margin: .55rem 0;
    }
    .muted { color: #627267 !important; font-size: .92rem; }
    hr { border-color: #e1e8dc; }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">SMART RECYCLING • CIRCULAR ECONOMY</div>
      <h1>♻️ Second-Life Detective</h1>
      <p>Don't throw it away. Discover what it could become.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "Upload a photo of unwanted scrap. The AI will identify what it can see "
    "and suggest practical next steps—no need to come up with ideas yourself."
)

left, right = st.columns([1, 1], gap="large")
with left:
    uploaded_image = st.file_uploader(
        "Upload a photo of your scrap",
        type=["jpg", "jpeg", "png", "webp"],
        help="Use a clear photo with the item visible.",
    )
    condition_choice = st.selectbox(
        "Condition (optional, helps improve suggestions)",
        ["Let the system decide", "Good / usable", "Damaged / needs repair"],
        index=0,
    )
    analyze_clicked = st.button(
        "🔎 Analyse my scrap",
        type="primary",
        use_container_width=True,
        disabled=uploaded_image is None,
    )

with right:
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Scrap photo", use_container_width=True)
    else:
        st.markdown(
            """
            <div class="result-card">
              <h3>Start with a photo</h3>
              <p class="muted">Your analysis will include the likely object, visible materials,
              recovery options, and a simple recovery tracker.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ------------------------------ Analyze image ------------------------------
if analyze_clicked and uploaded_image is not None:
    # Clear any previous result first so a failed/new analysis cannot leave stale results visible.
    for key in (
        "identification",
        "recovery_options",
        "digital_twin",
        "recovery_passport",
        "analysis_condition",
        "analysis_material",
        "analysis_hazardous",
        "analysis_image_name",
        "plan_saved",
    ):
        st.session_state.pop(key, None)

    try:
        with st.spinner("Looking at the scrap and preparing recovery options…"):
            identification = identify_object(uploaded_image)
    except Exception:
        st.error(
            "The image-identification service could not complete the analysis. "
            "Check your API key and connection, then try again."
        )
        identification = None

    if identification is not None:
        if not isinstance(identification, dict):
            st.error("The identification service returned an unexpected response. Please try again.")
        elif identification.get("error"):
            st.error(str(identification["error"]))
        elif identification.get("demo_mode"):
            st.warning(
                "DEMONSTRATION MODE: Live AI identification is currently unavailable. "
                "The uploaded item has not been identified, and its material/category "
                "has not been verified. No recovery pathway has been generated."
            )
            st.info(
                "You can still explore the app interface. Try the analysis again later "
                "when the AI service is available. Do not treat this result as an actual identification."
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

            object_text = str(identification.get("object", "Unknown object"))
            category = str(identification.get("category", "uncertain")).lower()
            safety_text = str(identification.get("safety_note", "")).lower()
            material_text = " ".join(str(m).lower() for m in materials)
            combined_text = f"{object_text.lower()} {category} {safety_text} {material_text}"

            hazardous_terms = (
                "hazard", "e-waste", "electronic waste", "battery", "chemical",
                "medical", "needle", "syringe", "sharp", "flammable",
                "corrosive", "toxic", "mercury", "asbestos", "pesticide",
            )
            hazardous = any(term in combined_text for term in hazardous_terms)

            # Use the updated reuse-outcomes policy as the recovery recommendation source.
            try:
                raw_outcomes = suggest_reuse_outcomes(
                    object_name=object_text,
                    visible_materials=materials,
                    condition=condition,
                    hazardous=hazardous,
                )
                options = []
                for outcome in raw_outcomes or []:
                    title = str(outcome.get("title", "Recovery option"))
                    description = str(outcome.get("description", ""))
                    effort = str(outcome.get("effort", "Not specified"))
                    safety = str(outcome.get("safety", "Follow appropriate safety guidance"))
                    reason_parts = [description, f"Effort: {effort}.", f"Safety: {safety}."]
                    options.append({
                        "option": title,
                        "reason": " ".join(part for part in reason_parts if part).strip(),
                    })
            except Exception as exc:
                st.error(
                    "The recovery recommendation module failed. Check "
                    "modules/reuse_outcomes.py for an error."
                )
                options = []

            # Build the Digital Twin and Recovery Passport for this analysis.
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
            st.session_state["analysis_material"] = ", ".join(str(m) for m in materials) or "unknown"
            st.session_state["analysis_hazardous"] = hazardous
            st.session_state["analysis_image_name"] = uploaded_image.name
            st.session_state["plan_saved"] = False

# ------------------------------ Results ------------------------------
identification = st.session_state.get("identification")

if identification:
    st.divider()
    st.header("Your scrap analysis")

    materials = identification.get("visible_materials", [])
    if isinstance(materials, list):
        materials_display = ", ".join(str(x) for x in materials) or "Not clear from the image"
    else:
        materials_display = str(materials) if materials else "Not clear from the image"

    category_display = str(
        identification.get("category", "Uncertain")
    ).replace("_", " ").title()

    confidence = identification.get("confidence", "Not available")
    if isinstance(confidence, (float, int)):
        confidence = f"{confidence:.0%}" if confidence <= 1 else f"{confidence:.0f}%"

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f'<div class="result-card"><div class="result-label">Likely item</div>'
            f'<div class="result-value">{object_text if "object_text" in locals() else identification.get("object", "Unknown object")}</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="result-card"><div class="result-label">Scrap category</div>'
            f'<div class="result-value">{category_display}</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div class="result-card"><div class="result-label">AI confidence</div>'
            f'<div class="result-value">{confidence}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div class="result-card"><div class="result-label">Visible materials</div>'
        f'<div class="result-value">{materials_display}</div></div>',
        unsafe_allow_html=True,
    )

    reason = identification.get("reason", "")
    if reason:
        st.markdown("**What the AI noticed**")
        st.write(reason)

    safety_note = identification.get("safety_note", "")
    if st.session_state.get("analysis_hazardous"):
        st.warning(
            "Safety first: this item may need specialist handling. Do not dismantle, "
            "repair, or reuse it based on a photo. Check an authorised collection service."
        )
    elif safety_note:
        st.info(safety_note)

    st.caption(
        "Photo-based identification is an estimate. Materials, internal components, "
        "and safety cannot always be verified from an image alone."
    )

    st.divider()
    st.header("♻️ Recommended recovery pathways")
    options = st.session_state.get("recovery_options", [])

    if options:
        for index, option in enumerate(options, start=1):
            st.markdown(
                f'<div class="path-card"><strong>{index}. {option["option"]}</strong>'
                f'<p style="margin:.4rem 0 0 0">{option["reason"]}</p></div>',
                unsafe_allow_html=True,
            )

        pathway_names = [option["option"] for option in options]
        current_twin = st.session_state.get("digital_twin", {})
        previous_pathway = current_twin.get("selected_pathway")
        default_index = pathway_names.index(previous_pathway) if previous_pathway in pathway_names else 0

        selected_pathway = st.selectbox(
            "Choose a recommended pathway",
            pathway_names,
            index=default_index,
            key="recovery_pathway_choice",
        )

        if st.button("Save my recovery plan", type="primary"):
            twin = st.session_state["digital_twin"]
            passport = st.session_state["recovery_passport"]
            if twin.get("selected_pathway") != selected_pathway:
                select_recovery_pathway(twin, selected_pathway)
                set_planned_outcome(passport, selected_pathway)
            st.session_state["digital_twin"] = twin
            st.session_state["recovery_passport"] = passport
            st.session_state["plan_saved"] = True
            st.success("Your recovery plan has been saved.")
    else:
        st.info("No suitable pathway was generated. Please review the image and classification.")

    st.divider()
    st.header("🌐 Recovery journey")
    twin = st.session_state.get("digital_twin", {})
    passport = st.session_state.get("recovery_passport", {})
    selected = twin.get("selected_pathway") or "Not selected yet"
    state = str(twin.get("current_state", "identified")).replace("_", " ").title()

    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown(
            f'<div class="result-card"><div class="result-label">Object</div>'
            f'<div class="result-value">{twin.get("item_name", "Scrap item")}</div></div>',
            unsafe_allow_html=True,
        )
    with d2:
        st.markdown(
            f'<div class="result-card"><div class="result-label">Journey stage</div>'
            f'<div class="result-value">{state}</div></div>',
            unsafe_allow_html=True,
        )
    with d3:
        st.markdown(
            f'<div class="result-card"><div class="result-label">Selected pathway</div>'
            f'<div class="result-value">{selected}</div></div>',
            unsafe_allow_html=True,
        )

    if twin.get("current_state") == "pathway_selected":
        if st.button("Mark recovery as in progress"):
            update_digital_twin(
                twin,
                "in_progress",
                "User reported that recovery work has started.",
            )
            st.session_state["digital_twin"] = twin
            st.rerun()

    st.header("📋 Recovery Passport")
    passport_status = str(passport.get("status", "planned")).replace("_", " ").title()
    p1, p2 = st.columns(2)
    with p1:
        st.markdown(
            f'<div class="result-card"><div class="result-label">Passport status</div>'
            f'<div class="result-value">{passport_status}</div></div>',
            unsafe_allow_html=True,
        )
    with p2:
        st.markdown(
            f'<div class="result-card"><div class="result-label">Planned outcome</div>'
            f'<div class="result-value">{passport.get("planned_outcome") or "Choose a pathway above"}</div></div>',
            unsafe_allow_html=True,
        )

    if passport.get("confirmed_outcome"):
        st.success(f"Reported outcome: {passport['confirmed_outcome']}")
    elif passport.get("planned_outcome"):
        with st.form("confirm_recovery_form"):
            outcome = st.text_input("What outcome did you complete?")
            evidence_note = st.text_input("Optional note (for example, where it was taken)")
            submitted = st.form_submit_button("Confirm completed outcome")
            if submitted:
                if not outcome.strip():
                    st.warning("Please describe the completed outcome.")
                else:
                    confirm_recovery_outcome(passport, outcome.strip(), evidence_note.strip())
                    safe_path = selected.lower().startswith("safe handling")
                    state_after = "disposed_safely" if safe_path else "recovered"
                    update_digital_twin(
                        twin,
                        state_after,
                        "User reported the outcome as completed.",
                    )
                    st.session_state["recovery_passport"] = passport
                    st.session_state["digital_twin"] = twin
                    st.rerun()
    else:
        st.caption("Save a recovery plan to enable outcome tracking.")

st.divider()
st.caption("Second-Life Detective · AI-assisted material recovery and circular-economy exploration")