import streamlit as st
import os

from modules.sop_engine import SOPEngine
from modules.ai_engine import AIEngine
from modules.quality_checker import QualityChecker
from modules.process_analyzer import ProcessAnalyzer
from modules.repository_discovery import RepositoryDiscovery

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="SOP Intelligence Platform",
    page_icon="📘",
    layout="wide"
)

# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.title("📘 SOP Intelligence Platform")

st.caption("AI Powered SOP Analysis & Intelligence Dashboard")

st.divider()

uploaded_file = st.file_uploader(
    "Choose SOP Document",
    type=["docx"]
)

if st.button("▶ Run Analysis", use_container_width=True):

    if uploaded_file is None:
        st.warning("Please select an SOP document.")

    else:

        os.makedirs("temp", exist_ok=True)

        temp_path = os.path.join(
            "temp",
            uploaded_file.name
        )

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("SOP Uploaded Successfully")

        st.info(uploaded_file.name)

        engine = SOPEngine(temp_path)

        engine.load_document()

        summary = AIEngine().summarize(engine.sections)

        quality = QualityChecker().evaluate(engine.sections)

        analysis = ProcessAnalyzer().analyze(engine.sections)
        repository = RepositoryDiscovery()

        matches = repository.compare(engine.sections)

        st.divider()

        st.header("📊 Executive Dashboard")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Overall Score",
                f"{quality['score']}%"
            )

        with c2:
            st.metric(
                "Sections",
                analysis["statistics"]["Sections"]
            )

        with c3:
            st.metric(
                "Paragraphs",
                analysis["statistics"]["Paragraphs"]
            )

        with c4:
            st.metric(
                "Applications",
                len(analysis["applications"])
            )

        c5, c6, c7, c8 = st.columns(4)

        with c5:
            st.metric(
                "Roles",
                len(analysis["roles"])
            )

        with c6:
            st.metric(
                "Controls",
                len(analysis["controls"])
            )

        with c7:
            st.metric(
                "Risks",
                len(analysis["risks"])
            )

        with c8:
            st.metric(
                "Manual Steps",
                len(analysis["manual_steps"])
            )

        st.divider()

        st.subheader("📌 Top Improvement Areas")

        recommendations = analysis["recommendations"]

        if recommendations:

            for rec in recommendations:
                st.warning(rec)

        else:
            st.success("No major improvements required.")

        st.divider()

                # =====================================================
        # AI SUMMARY
        # =====================================================

        with st.expander("📖 AI Summary", expanded=True):

            for heading, info in summary.items():

                st.markdown(f"### {heading}")

                col1, col2 = st.columns([1, 5])

                with col1:
                    st.metric(
                        "Paragraphs",
                        info["paragraphs"]
                    )

                with col2:
                    st.write(info["preview"])

                st.divider()

        # =====================================================
        # APPLICATIONS
        # =====================================================

        with st.expander("💻 Applications Used"):

            if analysis["applications"]:

                for app in analysis["applications"]:
                    st.success(app)

            else:
                st.info("No applications detected.")

        # =====================================================
        # ROLES
        # =====================================================

        with st.expander("👤 Roles Identified"):

            if analysis["roles"]:

                for role in analysis["roles"]:
                    st.success(role)

            else:
                st.info("No roles detected.")

        # =====================================================
        # CONTROLS
        # =====================================================

        with st.expander("🛡 Controls Found"):

            if analysis["controls"]:

                st.write(analysis["controls"])

            else:
                st.info("No controls detected.")

        # =====================================================
        # RISKS
        # =====================================================

        with st.expander("⚠ Risks Found"):

            if analysis["risks"]:

                st.write(analysis["risks"])

            else:
                st.info("No risks detected.")

        # =====================================================
        # MANUAL ACTIVITIES
        # =====================================================

        with st.expander("📝 Manual Activities"):

            if analysis["manual_steps"]:

                st.write(analysis["manual_steps"])

            else:
                st.success("No manual activities detected.")

        # =====================================================
        # AUTOMATION OPPORTUNITIES
        # =====================================================

        with st.expander("🤖 Automation Opportunities"):

            opportunities = analysis["automation_opportunities"]

            if opportunities:

                for i, item in enumerate(opportunities, start=1):

                    st.markdown(f"### Opportunity {i}")

                    st.write(
                        f"**Section :** {item['section']}"
                    )

                    st.write(
                        f"**Suggested Technology :** {item['solution']}"
                    )

                    st.write(
                        f"**Estimated Saving :** {item['estimated_saving']}"
                    )

                    st.write(
                        f"**Business Impact :** {item['business_impact']}"
                    )

                    st.write(
                        f"**Priority :** {item['priority']}"
                    )

                    st.divider()

            else:

                st.success("No automation opportunities found.")

        # =====================================================
        # PROCESS STATISTICS
        # =====================================================

        st.divider()

        st.header("📈 Process Statistics")

        statistics = analysis["statistics"]

        st.dataframe(
            statistics,
            use_container_width=True
        )
                # =====================================================
        # REPOSITORY DISCOVERY
        # =====================================================

        st.divider()

        st.header("🔍 Repository Discovery")

        top_matches = matches[:10]

        table = []

        highest = top_matches[0][1] if top_matches else 1

        for category, score in top_matches:

            percentage = round((score / highest) * 100, 1) if highest else 0

            table.append({
                "Repository Category": category,
                "Similarity %": f"{percentage}%"
            })

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )

        st.success("Analysis Completed Successfully ✅")