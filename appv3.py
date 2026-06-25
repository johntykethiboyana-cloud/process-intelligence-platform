import os
import tempfile
from numpy import rint
import streamlit as st
st.info("APPV3 VERSION LOADED")

from comparison_v3.document_extractor import DocumentExtractor
from comparison_v3.comparison_engine import ComparisonEngine

from comparison_v3.automation_detector import AutomationDetector
from comparison_v3.exporter import Exporter

st.set_page_config(
    page_title="L4 vs SOP Comparison Engine V3",
    page_icon="📄",
    layout="wide"
)

st.title("📄 L4 vs SOP Comparison Engine V3")
st.caption("Business Process Comparison powered by AI")
st.markdown("---")

if "comparison_result" not in st.session_state:
    st.session_state.comparison_result = None
if "l4_data" not in st.session_state:
    st.session_state.l4_data = None
if "sop_data" not in st.session_state:
    st.session_state.sop_data = None

col1, col2 = st.columns(2)

with col1:
    l4_file = st.file_uploader("Upload L4 Document", type=["docx"], key="l4")

with col2:
    sop_file = st.file_uploader("Upload SOP Document", type=["docx"], key="sop")

if st.button("🚀 Compare Documents", use_container_width=True):

    if l4_file is None or sop_file is None:
        st.error("Please upload both documents.")
        st.stop()

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

    engine = ComparisonEngine()

    try:

        result = engine.compare(
            l4_data,
            sop_data
        )

        detector = AutomationDetector()

        automation_opps = detector.detect(
            sop_data.get("activities", [])
        )

        st.session_state.comparison_result = result
        st.session_state.l4_data = l4_data
        st.session_state.sop_data = sop_data
        st.session_state.automation_opps = automation_opps

        st.success("Comparison completed successfully.")

    except Exception as e:

        st.error(f"COMPARE ERROR: {e}")
        raise


result = st.session_state.get(
    "comparison_result",
    None
)

automation_opps = st.session_state.get(
    "automation_opps",
    []
)

if result is None:
    st.info("Upload both documents and click Compare.")
    st.stop()

st.markdown("---")
st.header("📊 Comparison Dashboard")

st.metric(
    "Overall Match",
    f"{result['overall']}%"
)

st.progress(
    min(result["overall"] / 100, 1.0)
)

st.markdown("---")

metrics = [
    ("Process", "process_name"),
    ("Activities", "activities"),
    ("Roles", "roles"),
    ("Applications", "applications"),
    ("Sequence", "sequence"),
    ("Risks", "risks")
]

cols = st.columns(3)

for i, (title, key) in enumerate(metrics):
    with cols[i % 3]:
        st.metric(
            title,
            f"{result[key]['percentage']}%"
        )

st.markdown("### Process Insights")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Missing Activities",
        len(result["activities"]["missing"])
    )

with c2:
    st.metric(
        "Automation Candidates",
        len(automation_opps)
    )

with c3:
    st.metric(
        "Happy Flow Steps",
        len(result["flow"]["happy_flow"])
    )

st.markdown("---")


tabs = st.tabs([
    "Matched Activities",
    "Missing Activities",
    "Applications",
    "Controls",
    "Risks",
    "L4 Roles",
    "SOP Roles",
    "Steps",
    "Automation",
    "Happy & Unhappy Flow",
    "Role Intelligence",
    "Executive Summary"
])

# ---------------------------------------------------
# MATCHED ACTIVITIES
# ---------------------------------------------------

with tabs[0]:

    st.subheader("✅ Matched Activities")

    st.caption(
        f"Total Matched Activities: {len(result['activities']['matched'])}"
    )

    st.dataframe(
        result["activities"]["matched"],
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------
# MISSING ACTIVITIES
# ---------------------------------------------------

with tabs[1]:

    st.subheader("❌ Missing Activities")

    st.caption(
        f"Total Missing Activities: {len(result['activities']['missing'])}"
    )

    st.dataframe(
        result["activities"]["missing"],
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------
# APPLICATIONS
# ---------------------------------------------------

with tabs[2]:

    st.subheader("🖥️ Applications")

    st.caption(
        f"Matched Applications: {len(result['applications']['matched'])}"
    )

    st.dataframe(
        result["applications"]["matched"],
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------
# CONTROLS
# ---------------------------------------------------

with tabs[3]:

    st.subheader("🛡️ Controls")

    st.caption(
        f"Matched Controls: {len(result['controls']['matched'])}"
    )

    st.dataframe(
        result["controls"]["matched"],
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------
# RISKS
# ---------------------------------------------------

with tabs[4]:

    st.subheader("⚠️ Risks")

    st.caption(
        f"Matched Risks: {len(result['risks']['matched'])}"
    )

    st.dataframe(
        result["risks"]["matched"],
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------
# L4 ROLES
# ---------------------------------------------------

with tabs[5]:

    st.subheader("L4 Roles")

    l4_roles = st.session_state.l4_data.get("roles", [])

    st.write("L4 Roles Count:", len(l4_roles))

    if l4_roles:
        st.write(l4_roles)
    else:
        st.warning("No L4 Roles Found")

# ---------------------------------------------------
# SOP ROLES
# ---------------------------------------------------

with tabs[6]:

    st.subheader("SOP Roles")

    sop_roles = st.session_state.sop_data.get("roles", [])

    st.write("SOP Roles Count:", len(sop_roles))

    if sop_roles:
        st.write(sop_roles)
    else:
        st.warning("No SOP Roles Found")

# ---------------------------------------------------
# STEPS
# ---------------------------------------------------

with tabs[7]:

    st.subheader("Raw L4 Steps")

    st.write(st.session_state.l4_data.get("steps", []))

    st.markdown("---")

    st.subheader("Raw SOP Steps")

    st.write(st.session_state.sop_data.get("steps", []))

# ---------------------------------------------------
# AUTOMATION
# ---------------------------------------------------

with tabs[8]:

    st.subheader("Automation Opportunities")

    st.metric(
        "Automation Candidates",
        len(automation_opps)
    )

    st.dataframe(
        automation_opps,
        use_container_width=True
    )


# ---------------------------------------------------
# HAPPY & UNHAPPY FLOW
# ---------------------------------------------------

with tabs[9]:

    st.subheader("Happy Flow")

    happy = result["flow"]["happy_flow"]

    if happy:
        st.dataframe(happy, use_container_width=True)
    else:
        st.info("No happy flow identified.")

    st.divider()

    st.subheader("Unhappy Flow")

    unhappy = result["flow"]["unhappy_flow"]

    if unhappy:
        st.dataframe(unhappy, use_container_width=True)
    else:
        st.success("No unhappy flow detected.")

    st.divider()

    st.subheader("Automation Opportunities")

    automation = result["flow"]["automation"]

    if automation:
        st.dataframe(automation, use_container_width=True)
    else:
        st.info("No automation opportunities identified.")

# ---------------------------------------------------
# ROLE INTELLIGENCE
# ---------------------------------------------------

with tabs[10]:

    st.subheader("👥 Workforce Analytics")

    summary = result["role_intelligence"]["summary"]

    details = result["role_intelligence"]["details"]

    st.markdown("### Workload Summary")

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    roles = sorted({
        step.get("role") or "Unassigned"
        for step in details
    })

    selected_role = st.selectbox(
        "Select Role",
        roles
    )

    role_steps = [

        step

        for step in details

        if (step.get("role") or "Unassigned") == selected_role

    ]

    st.markdown(f"### Activities performed by **{selected_role}**")

    st.dataframe(
        role_steps,
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------
# EXECUTIVE SUMMARY
# ---------------------------------------------------

with tabs[11]:

    st.subheader("Executive Summary")

    st.write("### L4 Roles")
    st.write(st.session_state.l4_data.get("roles", []))

    st.write("### SOP Roles")
    st.write(st.session_state.sop_data.get("roles", []))

    st.write("### Missing Activities")
    st.dataframe(
        result["activities"]["missing"],
        use_container_width=True
    )

    st.write("### Extra SOP Activities")
    st.dataframe(
        result["activities"]["extra"],
        use_container_width=True
    )

st.markdown("---")
st.markdown("---")

exporter = Exporter()

if st.button("📥 Export Comparison Report to Excel", use_container_width=True):

    filename = "L4_vs_SOP_Comparison_Report.xlsx"

    exporter.export(
        result,
        automation_opps,
        filename
    )

    with open(filename, "rb") as f:

        st.download_button(
            label="⬇️ Download Excel Report",
            data=f,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
st.success("Analysis Completed.")
