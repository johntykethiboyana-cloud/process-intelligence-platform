import os
import tempfile
import streamlit as st

from comparison_v2.document_extractor import DocumentExtractor
from comparison_v2.comparison_engine import ComparisonEngine

st.set_page_config(
    page_title="L4 vs SOP Comparison",
    page_icon="📄",
    layout="wide"
)

st.title("📄 L4 vs SOP Comparison Engine V2")
st.markdown("---")

# ==========================================================
# Upload
# ==========================================================

col1, col2 = st.columns(2)

with col1:
    l4_file = st.file_uploader(
        "Upload L4 Document",
        type=["docx"],
        key="l4"
    )

with col2:
    sop_file = st.file_uploader(
        "Upload SOP Document",
        type=["docx"],
        key="sop"
    )

compare = st.button(
    "🚀 Compare Documents",
    use_container_width=True
)

result = None

# ==========================================================
# Compare
# ==========================================================

if compare:

    if not l4_file or not sop_file:
        st.error("Please upload both documents.")
        st.stop()

    with st.spinner("Reading documents..."):

        temp_dir = tempfile.mkdtemp()

        l4_path = os.path.join(temp_dir, l4_file.name)
        sop_path = os.path.join(temp_dir, sop_file.name)

        with open(l4_path, "wb") as f:
            f.write(l4_file.getbuffer())

        with open(sop_path, "wb") as f:
            f.write(sop_file.getbuffer())

        extractor = DocumentExtractor()

        l4_data = extractor.extract(l4_path)
        sop_data = extractor.extract(sop_path)

    with st.spinner("Running intelligent comparison..."):

        engine = ComparisonEngine()

        result = engine.compare(
            l4_data,
            sop_data
        )

    st.success("Comparison Completed.")

# ==========================================================
# Dashboard
# ==========================================================

if result:

    st.markdown("---")
    st.header("📊 Comparison Dashboard")

    st.metric(
        "Overall Match",
        f"{result['overall']}%"
    )

    st.progress(result["overall"] / 100)

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Process",
            f"{result['process_name']['percentage']}%"
        )

        st.metric(
            "Activities",
            f"{result['activities']['percentage']}%"
        )

        st.metric(
            "Roles",
            f"{result['roles']['percentage']}%"
        )

    with c2:

        st.metric(
            "Applications",
            f"{result['applications']['percentage']}%"
        )

        st.metric(
            "Controls",
            f"{result['controls']['percentage']}%"
        )

        st.metric(
            "Risks",
            f"{result['risks']['percentage']}%"
        )

    with c3:

        st.metric(
            "Inputs",
            f"{result['inputs']['percentage']}%"
        )

        st.metric(
            "Outputs",
            f"{result['outputs']['percentage']}%"
        )

        st.metric(
            "Steps",
            f"{result['steps']['percentage']}%"
        )

    st.markdown("---")

    st.subheader("Matched Activities")
    st.dataframe(
        result["activities"]["matched"],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    st.subheader("Missing L4 Activities")
    st.dataframe(
        result["activities"]["missing"],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    st.subheader("Extra SOP Activities")
    st.dataframe(
        result["activities"]["extra"],
        use_container_width=True,
        hide_index=True
    )