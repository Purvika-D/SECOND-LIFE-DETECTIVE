import streamlit as st
from modules.identification import identify_object

st.set_page_config(
    page_title="Second-Life Detective",
    page_icon="♻️",
    layout="wide"
)

st.title("♻️ Second-Life Detective")
st.subheader("Don't throw it away. Discover what it could become.")

st.write(
    "Upload an unwanted object to discover its possible "
    "repair, reuse, repurposing, and recycling pathways."
)

st.divider()
st.header("🔍 Investigate Your Object")

uploaded_image = st.file_uploader(
    "Upload a photograph of your unwanted object",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_image is not None:
    st.image(
        uploaded_image,
        caption="Your uploaded object",
        use_container_width=True
    )

    st.success("Image uploaded successfully!")

    st.divider()
    st.subheader("Tell us more about your object")

    object_name = st.text_input(
        "What is the object? (Optional)",
        placeholder="Example: Old wooden chair"
    )

    object_condition = st.selectbox(
        "What condition is it in?",
        [
            "Select condition",
            "Like new",
            "Good condition",
            "Needs repair",
            "Damaged",
            "Unknown"
        ]
    )

    budget = st.selectbox(
        "What is your approximate budget?",
        [
            "Select budget",
            "Free solutions only",
            "Under ₹100",
            "₹100–₹500",
            "Above ₹500"
        ]
    )

    available_tools = st.multiselect(
        "Which tools do you have available?",
        [
            "None",
            "Glue",
            "Scissors",
            "Screwdriver",
            "Basic repair tools",
            "Sewing kit",
            "Other"
        ]
    )

    if st.button("🔎 Investigate Object", type="primary"):

        if object_condition == "Select condition":
            st.warning("Please select the object's condition.")

        elif budget == "Select budget":
            st.warning("Please select your budget.")

        else:
            st.session_state["object_details"] = {
                "name": object_name,
                "condition": object_condition,
                "budget": budget,
                "tools": available_tools
            }

            with st.spinner("AI is analysing your object..."):
                identification = identify_object(uploaded_image)

            if "error" in identification:
                st.error(identification["error"])

            else:
                st.session_state["identification"] = identification

    identification = st.session_state.get("identification")

    if identification:
        st.divider()
        st.header("🧠 AI Identification Results")

        st.write(
            "**Likely object:**",
            identification.get("object", "Unknown")
        )

        st.write(
            "**Visible materials:**",
            ", ".join(identification.get("visible_materials", []))
        )

        st.write(
            "**Suggested category:**",
            identification.get("category", "Uncertain")
        )

        st.write(
            "**Confidence:**",
            identification.get("confidence", "Unknown")
        )

        st.write(
            "**Reason:**",
            identification.get("reason", "")
        )

        st.warning(
            "Visual identification is an estimate. Verify material "
            "composition and use authorised collection services for "
            "potentially hazardous waste."
        )

        st.info(
            identification.get(
                "safety_note",
                "Follow appropriate safety guidance."
            )
        )

st.divider()

st.caption(
    "Second-Life Detective | AI-assisted material recovery "
    "and circular-economy exploration"
)