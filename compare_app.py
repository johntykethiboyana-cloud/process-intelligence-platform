import os
import streamlit as st

from comparison.document_extractor import DocumentExtractor
from comparison.comparison_engine import ComparisonEngine

st.set_page_config(
    page_title="L4 vs SOP Governance Comparator",
    page_icon="📊",
    layout="wide"
)

st.title("📊 L4 vs SOP Governance Comparator")
st.divider()

col1, col2 = st.columns(2)

with col1:
    l4_file = st.file_uploader(
        "Upload L4 Process",
        type=["docx"],
        key="l4"
    )

with col2:
    sop_file = st.file_uploader(
        "Upload SOP",
        type=["docx"],
        key="sop"
    )

if st.button("🚀 Compare", use_container_width=True):

    if not l4_file or not sop_file:
        st.warning("Please upload both documents.")
        st.stop()

    os.makedirs("temp", exist_ok=True)

    l4_path = os.path.join("temp", l4_file.name)
    sop_path = os.path.join("temp", sop_file.name)

    with open(l4_path, "wb") as f:
        f.write(l4_file.getbuffer())

    with open(sop_path, "wb") as f:
        f.write(sop_file.getbuffer())

    extractor = DocumentExtractor()

    l4 = extractor.extract(l4_path)
    sop = extractor.extract(sop_path)

    result = ComparisonEngine().compare(l4, sop)

    with st.expander("L4 Parsed Data"):
        st.json(l4)

    with st.expander("SOP Parsed Data"):
        st.json(sop)

    with st.expander("Comparison Result"):
        st.json(result)

    st.divider()

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Overall", f"{result['overall']}%")
    c2.metric("Activities", f"{result['activities']['percentage']}%")
    c3.metric("Applications", f"{result['applications']['percentage']}%")
    c4.metric("Roles", f"{result['roles']['percentage']}%")
    c5.metric("Sequence", f"{result['sequence']['percentage']}%")

    st.divider()

    st.subheader("Process Name")

    st.write("**L4**")
    st.info(l4.get("process_name",""))

    st.write("**SOP**")
    st.info(sop.get("process_name",""))

    st.metric(
        "Similarity",
        f"{result['process_name']['percentage']}%"
    )

    def show(name, data):

        with st.expander(f"{name} ({data['percentage']}%)", expanded=True):

            a, b, c = st.columns(3)

            with a:
                st.markdown("### ✅ Matched")
                if data["matched"]:
                    for item in data["matched"]:
                        st.success(f"{item['l4']} ({item['score']}%)")
                else:
                    st.info("None")

            with b:
                st.markdown("### ❌ Missing in SOP")
                if data["missing"]:
                    for item in data["missing"]:
                        st.error(item)
                else:
                    st.success("None")

            with c:
                st.markdown("### ➕ Extra in SOP")
                if data["extra"]:
                    for item in data["extra"]:
                        st.warning(item)
                else:
                    st.success("None")

    show("Activities", result["activities"])
    show("Applications", result["applications"])
    show("Roles", result["roles"])
    show("Controls", result["controls"])
    show("Inputs", result["inputs"])
    show("Outputs", result["outputs"])
    show("Risks", result["risks"])
    show("Steps", result["steps"])

    st.divider()

    st.metric("Sequence Match", f"{result['sequence']['percentage']}%")

    st.success("Comparison completed successfully.")
