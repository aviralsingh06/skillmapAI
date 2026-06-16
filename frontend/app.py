import sys
import os

from frontend.auth import init_auth_session, render_auth_page, render_sidebar_user_panel

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
from html import escape
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle
)

from services.resume_parser import (
    extract_resume_text
)

from services.database_service import (
    save_resume,
    save_extracted_skills
)

from services.skill_extractor import (
    extract_skills
)

from services.job_matcher import (
    analyze_skill_gap
)

from services.learning_recommender import (
    get_learning_recommendations
)

from services.roadmap_generator import (
    create_roadmap
)

from services.course_recommender import (
    recommend_courses
)

from services.resume_improver import (
    generate_resume_suggestions
)

from services.resume_scorer import (
    calculate_resume_score
)

from services.ats_scorer import (
    analyze_ats_resume
)

from datasets.job_roles import (
    JOB_ROLES
)


BRAND_PRIMARY = "#7C3AED"
BRAND_SECONDARY = "#22D3EE"
BRAND_SUCCESS = "#22C55E"
BRAND_WARNING = "#F59E0B"
BRAND_DANGER = "#EF4444"
PANEL_BACKGROUND = "#111827"


def inject_custom_css():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at 15% 0%, rgba(124, 58, 237, 0.14), transparent 30%),
                radial-gradient(circle at 85% 10%, rgba(34, 211, 238, 0.10), transparent 26%),
                #070b14;
        }
        [data-testid="stHeader"] {
            background: rgba(7, 11, 20, 0.72);
        }
        [data-testid="stSidebar"] {
            background: #0b1120;
            border-right: 1px solid rgba(148, 163, 184, 0.14);
        }
        .block-container {
            max-width: 1380px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }
        .hero-panel {
            padding: 1.6rem 1.8rem;
            border: 1px solid rgba(124, 58, 237, 0.34);
            border-radius: 22px;
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.18), rgba(17, 24, 39, 0.88));
            box-shadow: 0 20px 55px rgba(0, 0, 0, 0.28);
            margin-bottom: 1.35rem;
        }
        .hero-eyebrow {
            color: #67e8f9;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-bottom: 0.45rem;
        }
        .hero-title {
            color: #f8fafc;
            font-size: clamp(1.75rem, 4vw, 2.75rem);
            font-weight: 800;
            line-height: 1.08;
            margin: 0;
        }
        .hero-copy {
            color: #cbd5e1;
            max-width: 760px;
            margin: 0.75rem 0 0;
            line-height: 1.65;
        }
        .metric-card {
            min-height: 150px;
            padding: 1.25rem;
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 18px;
            background: linear-gradient(150deg, rgba(30, 41, 59, 0.92), rgba(15, 23, 42, 0.96));
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
        }
        .metric-accent {
            width: 42px;
            height: 4px;
            border-radius: 999px;
            margin-bottom: 1rem;
        }
        .metric-label {
            color: #94a3b8;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }
        .metric-value {
            color: #f8fafc;
            font-size: 2rem;
            font-weight: 800;
            margin: 0.35rem 0 0.25rem;
        }
        .metric-note {
            color: #cbd5e1;
            font-size: 0.86rem;
        }
        .section-kicker {
            color: #22d3ee;
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-top: 1.2rem;
        }
        .section-title {
            color: #f8fafc;
            font-size: 1.45rem;
            font-weight: 800;
            margin: 0.2rem 0 0.25rem;
        }
        .section-copy {
            color: #94a3b8;
            margin-bottom: 0.9rem;
        }
        .insight-panel {
            height: 100%;
            padding: 1.2rem 1.3rem;
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 17px;
            background: rgba(15, 23, 42, 0.82);
        }
        .insight-label {
            color: #67e8f9;
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }
        .insight-title {
            color: #f8fafc;
            font-size: 1.05rem;
            font-weight: 750;
            margin: 0.45rem 0;
        }
        .insight-copy {
            color: #cbd5e1;
            line-height: 1.58;
        }
        .skill-chip {
            display: inline-block;
            padding: 0.38rem 0.72rem;
            border-radius: 999px;
            margin: 0.22rem 0.18rem;
            font-size: 0.82rem;
            font-weight: 650;
        }
        .skill-chip.matched {
            color: #bbf7d0;
            background: rgba(34, 197, 94, 0.14);
            border: 1px solid rgba(34, 197, 94, 0.28);
        }
        .skill-chip.missing {
            color: #fecaca;
            background: rgba(239, 68, 68, 0.13);
            border: 1px solid rgba(239, 68, 68, 0.26);
        }
        div[data-testid="stProgress"] > div > div > div > div {
            background: linear-gradient(90deg, #7c3aed, #22d3ee);
        }
        div[data-testid="stDownloadButton"] button {
            width: 100%;
            min-height: 3rem;
            border: 0;
            border-radius: 12px;
            color: white;
            font-weight: 750;
            background: linear-gradient(90deg, #7c3aed, #4f46e5);
        }
        div[data-testid="stDownloadButton"] button:hover {
            box-shadow: 0 10px 26px rgba(124, 58, 237, 0.32);
            transform: translateY(-1px);
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def get_readiness(match_score):
    if match_score >= 80:
        return "Ready to Apply", "Strong role alignment", BRAND_SUCCESS
    if match_score >= 60:
        return "Almost Ready", "Close the priority skill gaps", BRAND_WARNING
    return "Needs Improvement", "Build core role fundamentals", BRAND_DANGER


def get_career_insight(match_score):
    if match_score >= 80:
        return (
            "High role alignment",
            "Your profile is strongly aligned with this role. Prioritize "
            "portfolio depth, measurable project outcomes, and relevant certifications."
        )
    if match_score >= 60:
        return (
            "Promising foundation",
            "You have moderate alignment with this role. Strengthen the most important "
            "missing skills and demonstrate them through focused projects."
        )
    return (
        "Foundation-building phase",
        "Your current profile has a meaningful skill gap for this role. Focus on "
        "fundamentals and one practical project before beginning applications."
    )


def get_smart_recommendation(missing_skills):
    if missing_skills:
        priority_skills = ", ".join(missing_skills[:3])
        return (
            "Prioritize critical skills",
            f"Adding {priority_skills} to your demonstrated experience can "
            "significantly improve role alignment and resume relevance."
        )
    return (
        "Maintain your advantage",
        "Your resume covers the role's core skills. Deepen your strongest areas "
        "with advanced projects, certifications, and measurable impact."
    )


def get_next_step(missing_skills):
    if missing_skills:
        return f"Start learning {missing_skills[0]} and apply it in a portfolio project."
    return "Advance to role-specific projects, system design, and interview preparation."


def render_section_header(kicker, title, copy=""):
    copy_markup = (
        f'<div class="section-copy">{escape(copy)}</div>'
        if copy
        else ""
    )
    st.markdown(
        f"""
        <div class="section-kicker">{escape(kicker)}</div>
        <div class="section-title">{escape(title)}</div>
        {copy_markup}
        """,
        unsafe_allow_html=True
    )


def render_metric_card(label, value, note, accent):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-accent" style="background:{accent};"></div>
            <div class="metric-label">{escape(label)}</div>
            <div class="metric-value">{escape(str(value))}</div>
            <div class="metric-note">{escape(note)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_insight_card(label, title, copy):
    st.markdown(
        f"""
        <div class="insight-panel">
            <div class="insight-label">{escape(label)}</div>
            <div class="insight-title">{escape(title)}</div>
            <div class="insight-copy">{escape(copy)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_skill_chips(skills, chip_type):
    if not skills:
        st.caption("No skills to display.")
        return

    chips = "".join(
        f'<span class="skill-chip {chip_type}">{escape(skill)}</span>'
        for skill in skills
    )
    st.markdown(chips, unsafe_allow_html=True)


def create_skill_charts(matched_count, missing_count):
    chart_df = pd.DataFrame({
        "Category": ["Matched", "Missing"],
        "Count": [matched_count, missing_count]
    })

    pie_chart = px.pie(
        chart_df,
        names="Category",
        values="Count",
        hole=0.62,
        color="Category",
        color_discrete_map={
            "Matched": BRAND_SUCCESS,
            "Missing": BRAND_DANGER
        }
    )
    pie_chart.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker_line_color="#0f172a",
        marker_line_width=3,
        hovertemplate="%{label}: %{value} skills<extra></extra>"
    )

    bar_chart = px.bar(
        chart_df,
        x="Category",
        y="Count",
        text="Count",
        color="Category",
        color_discrete_map={
            "Matched": BRAND_SUCCESS,
            "Missing": BRAND_DANGER
        }
    )
    bar_chart.update_traces(
        textposition="outside",
        marker_line_width=0,
        hovertemplate="%{x}: %{y} skills<extra></extra>"
    )

    for figure in (pie_chart, bar_chart):
        figure.update_layout(
            height=360,
            margin=dict(l=20, r=20, t=25, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cbd5e1", family="Inter, sans-serif"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.12,
                xanchor="center",
                x=0.5
            ),
            showlegend=True
        )

    bar_chart.update_layout(
        xaxis_title=None,
        yaxis_title="Number of skills",
        yaxis=dict(gridcolor="rgba(148,163,184,0.12)")
    )

    return pie_chart, bar_chart


def build_pdf_report(
    selected_role,
    resume_score,
    ats_result,
    result,
    smart_recommendation,
    next_step,
    readiness,
    personalized_suggestions
):
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=22 * mm,
        bottomMargin=20 * mm,
        title="SkillMap AI Resume Intelligence Report",
        author="SkillMap AI"
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="BrandTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=colors.HexColor(BRAND_PRIMARY),
        alignment=TA_LEFT,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        name="ReportSubtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#475569"),
        spaceAfter=16
    ))
    styles.add(ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=13,
        spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        name="BodyClean",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=5
    ))
    styles.add(ParagraphStyle(
        name="SmallLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        textColor=colors.HexColor("#64748B"),
        alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        name="ScoreValue",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0F172A"),
        alignment=TA_CENTER
    ))

    generated_at = datetime.now().strftime("%d %B %Y, %I:%M %p")
    story = [
        Paragraph("SKILLMAP AI", styles["BrandTitle"]),
        Paragraph(
            "Resume Intelligence &amp; Career Readiness Report",
            styles["ReportSubtitle"]
        )
    ]

    metadata = Table(
        [
            ["TARGET ROLE", "DATE GENERATED"],
            [selected_role, generated_at]
        ],
        colWidths=[84 * mm, 84 * mm]
    )
    metadata.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEF2FF")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor(BRAND_PRIMARY)),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, 1), 10),
        ("TEXTCOLOR", (0, 1), (-1, 1), colors.HexColor("#1E293B")),
        ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#CBD5E1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#E2E8F0")),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 9)
    ]))
    story.extend([metadata, Spacer(1, 12)])

    summary_data = [
        [
            Paragraph("RESUME SCORE", styles["SmallLabel"]),
            Paragraph("ATS SCORE", styles["SmallLabel"]),
            Paragraph("MATCH RATE", styles["SmallLabel"]),
            Paragraph("JOB READINESS", styles["SmallLabel"])
        ],
        [
            Paragraph(f"{resume_score}/100", styles["ScoreValue"]),
            Paragraph(f"{ats_result['score']}/100", styles["ScoreValue"]),
            Paragraph(f"{result['match_score']}%", styles["ScoreValue"]),
            Paragraph(readiness, styles["ScoreValue"])
        ]
    ]
    summary = Table(summary_data, colWidths=[42 * mm] * 4)
    summary.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 3),
        ("TOPPADDING", (0, 1), (-1, 1), 3),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 11)
    ]))
    story.extend([
        Paragraph("Executive Summary", styles["SectionHeading"]),
        summary
    ])

    def add_list_section(title, items, empty_message):
        content = [Paragraph(title, styles["SectionHeading"])]
        if items:
            content.extend(
                Paragraph(f"&bull;&nbsp; {escape(str(item))}", styles["BodyClean"])
                for item in items
            )
        else:
            content.append(Paragraph(empty_message, styles["BodyClean"]))
        story.append(KeepTogether(content))

    add_list_section(
        "Matched Skills",
        result["matched_skills"],
        "No matched skills were detected for this role."
    )
    add_list_section(
        "Missing Skills",
        result["missing_skills"],
        "No critical skill gaps were detected."
    )
    add_list_section(
        "ATS Strengths",
        ats_result["strengths"],
        "No ATS strengths were detected."
    )

    insight_rows = [
        ["Smart Recommendation", smart_recommendation],
        ["Recommended Next Step", next_step]
    ]
    insight_table = Table(
        [
            [
                Paragraph(f"<b>{escape(label)}</b>", styles["BodyClean"]),
                Paragraph(escape(copy), styles["BodyClean"])
            ]
            for label, copy in insight_rows
        ],
        colWidths=[49 * mm, 119 * mm],
        splitByRow=0
    )
    insight_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EEF2FF")),
        ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#F8FAFC")),
        ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#CBD5E1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#E2E8F0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9)
    ]))
    story.append(KeepTogether([
        Paragraph("AI Guidance", styles["SectionHeading"]),
        insight_table
    ]))

    add_list_section(
        "Personalized Resume Improvements",
        personalized_suggestions,
        "Continue refining role-specific achievements and keywords."
    )

    def add_page_details(canvas, doc):
        canvas.saveState()
        width, height = A4
        canvas.setStrokeColor(colors.HexColor(BRAND_PRIMARY))
        canvas.setLineWidth(2)
        canvas.line(18 * mm, height - 13 * mm, width - 18 * mm, height - 13 * mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#64748B"))
        canvas.drawString(18 * mm, 11 * mm, "SkillMap AI | Resume Intelligence System")
        canvas.drawRightString(
            width - 18 * mm,
            11 * mm,
            f"Page {doc.page}"
        )
        canvas.restoreState()

    document.build(
        story,
        onFirstPage=add_page_details,
        onLaterPages=add_page_details
    )
    buffer.seek(0)
    return buffer.getvalue()

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="SkillMap AI",
    page_icon="📊",
    layout="wide"
)
# Initialize authentication
init_auth_session()

# Show login page if not logged in
render_auth_page()

# Stop app until login
if not st.session_state.authenticated:
    st.stop()

# Show logged in user
render_sidebar_user_panel()

inject_custom_css()

st.markdown(
    """
    <div class="hero-panel">
        <div class="hero-eyebrow">Resume Intelligence Platform</div>
        <h1 class="hero-title">SkillMap AI</h1>
        <p class="hero-copy">
            Transform your resume into a role-ready career plan with ATS analysis,
            skill-gap intelligence, personalized recommendations, and learning roadmaps.
        </p>
    </div>
    """
    ,
    unsafe_allow_html=True
)

# ---------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------

st.sidebar.title(
    "📌 Navigation"
)
st.sidebar.caption(
    "Analyze your resume, close skill gaps, and build a focused learning plan."
)

page = st.sidebar.radio(
    "Go To",
    [
        "Dashboard",
        "Resume Analysis",
        "ATS Analysis",
        "Learning Plan",
        "Skill Roadmap",
        "Courses",
        "Resume Suggestions"
    ]
)

# ---------------------------------
# FILE UPLOAD
# ---------------------------------

uploaded_file = st.file_uploader(
    "Upload your resume to begin",
    type=["pdf"],
    help="Upload a text-based PDF for the most accurate analysis."
)

if uploaded_file is not None:

    extracted_text = (
        extract_resume_text(
            uploaded_file
        )
    )

    resume_id = save_resume(
        uploaded_file.name,
        extracted_text
    )

    skills = extract_skills(
        extracted_text
    )

    save_extracted_skills(
        resume_id,
        skills
    )

    st.success(
        "✅ Resume uploaded and analyzed!"
    )

    selected_role = st.selectbox(
        "Choose Target Job Role",
        list(JOB_ROLES.keys())
    )

    result = analyze_skill_gap(
        skills,
        selected_role
    )

    resume_score = (
        calculate_resume_score(
            result["match_score"],
            skills,
            result["missing_skills"],
            extracted_text
        )
    )

    ats_result = analyze_ats_resume(
        extracted_text,
        result["matched_skills"],
        result["missing_skills"],
        selected_role
    )

    # ---------------------------------
    # DASHBOARD
    # ---------------------------------

    if page == "Dashboard":

        total_target_skills = (
            len(result["matched_skills"])
            + len(result["missing_skills"])
        )

        skill_match = (
            len(result["matched_skills"])
            / total_target_skills
            * 100
            if total_target_skills
            else 0
        )

        readiness, readiness_note, readiness_color = (
            get_readiness(result["match_score"])
        )
        insight_title, insight_copy = get_career_insight(
            result["match_score"]
        )
        recommendation_title, recommendation_copy = (
            get_smart_recommendation(result["missing_skills"])
        )
        next_step = get_next_step(result["missing_skills"])
        personalized_suggestions = generate_resume_suggestions(
            extracted_text,
            selected_role,
            result["missing_skills"]
        )
        pie_chart, bar_chart = create_skill_charts(
            len(result["matched_skills"]),
            len(result["missing_skills"])
        )

        st.markdown(
            f"""
            <div class="hero-panel">
                <div class="hero-eyebrow">Executive Dashboard</div>
                <h2 class="hero-title">Resume intelligence for {escape(selected_role)}</h2>
                <p class="hero-copy">
                    A consolidated view of ATS performance, role alignment, skill coverage,
                    and the highest-impact actions for your next application.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        metric_columns = st.columns(4, gap="medium")

        with metric_columns[0]:
            render_metric_card(
                "Resume Score",
                f"{resume_score}/100",
                "Overall resume quality",
                BRAND_PRIMARY
            )

        with metric_columns[1]:
            render_metric_card(
                "ATS Score",
                f"{ats_result['score']}/100",
                ats_result["status"],
                BRAND_SECONDARY
            )

        with metric_columns[2]:
            render_metric_card(
                "Match Rate",
                f"{skill_match:.1f}%",
                f"{len(result['matched_skills'])} of {total_target_skills} role skills",
                BRAND_SUCCESS
            )

        with metric_columns[3]:
            render_metric_card(
                "Job Readiness",
                readiness,
                readiness_note,
                readiness_color
            )

        render_section_header(
            "Performance",
            "Optimization Progress",
            "Track resume quality and role-specific skill completion."
        )

        progress_columns = st.columns(2, gap="large")

        with progress_columns[0]:
            st.markdown("**Resume Optimization Progress**")
            st.progress(ats_result["score"] / 100)
            st.caption(
                f"ATS optimization: {ats_result['score']}% · "
                f"Status: {ats_result['status']}"
            )

        with progress_columns[1]:
            st.markdown("**Skill Completion Progress**")
            st.progress(int(skill_match))
            st.caption(
                f"Skill coverage: {skill_match:.1f}% · "
                f"{len(result['missing_skills'])} priority gaps remaining"
            )

        render_section_header(
            "Analytics",
            "Skill Match Intelligence",
            "A visual comparison of demonstrated capabilities and target-role gaps."
        )

        chart_columns = st.columns(2, gap="large")

        with chart_columns[0]:
            st.markdown("**Skill Match Overview**")
            st.plotly_chart(
                pie_chart,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        with chart_columns[1]:
            st.markdown("**Matched vs Missing Skills**")
            st.plotly_chart(
                bar_chart,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        render_section_header(
            "Capability Map",
            "Skills & ATS Signals",
            "Review the evidence already present and the gaps that deserve attention."
        )

        skill_columns = st.columns(2, gap="large")

        with skill_columns[0]:
            st.markdown("**Matched Skills**")
            render_skill_chips(result["matched_skills"], "matched")
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**ATS Strengths**")
            for strength in ats_result["strengths"][:4]:
                st.success(strength)

        with skill_columns[1]:
            st.markdown("**Priority Skill Gaps**")
            render_skill_chips(result["missing_skills"], "missing")
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**ATS Improvement Priorities**")
            for suggestion in ats_result["suggestions"][:4]:
                st.warning(suggestion)

        render_section_header(
            "AI Intelligence",
            "Career Guidance",
            "Personalized interpretation of your role fit and highest-impact actions."
        )

        insight_columns = st.columns(3, gap="medium")

        with insight_columns[0]:
            render_insight_card(
                "AI Career Insight",
                insight_title,
                insight_copy
            )

        with insight_columns[1]:
            render_insight_card(
                "Smart Recommendation",
                recommendation_title,
                recommendation_copy
            )

        with insight_columns[2]:
            render_insight_card(
                "Recommended Next Step",
                readiness,
                next_step
            )

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander(
            "Personalized Resume Improvement Suggestions",
            expanded=True
        ):
            for index, suggestion in enumerate(
                personalized_suggestions,
                start=1
            ):
                st.markdown(f"**{index}.** {suggestion}")

        pdf_report = build_pdf_report(
            selected_role,
            resume_score,
            ats_result,
            result,
            recommendation_copy,
            next_step,
            readiness,
            personalized_suggestions
        )

        render_section_header(
            "Export",
            "Professional Analytics Report",
            "Download a branded PDF summary for portfolio reviews, mentoring, or interview preparation."
        )

        st.download_button(
            label="📥 Download Professional PDF Report",
            data=pdf_report,
            file_name="skillmap_ai_resume_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        st.divider()
    # ---------------------------------
    # RESUME ANALYSIS
    # ---------------------------------

    elif page == "Resume Analysis":

        render_section_header(
            "Deep Dive",
            "Resume Analysis",
            "Explore role alignment and the exact skills influencing your match rate."
        )

        readiness, readiness_note, readiness_color = (
            get_readiness(result["match_score"])
        )
        summary_columns = st.columns(3, gap="medium")

        with summary_columns[0]:
            render_metric_card(
                "Role Match",
                f"{result['match_score']}%",
                "Target-role skill alignment",
                BRAND_SUCCESS
            )

        with summary_columns[1]:
            render_metric_card(
                "Resume Score",
                f"{resume_score}/100",
                "Content and completeness",
                BRAND_PRIMARY
            )

        with summary_columns[2]:
            render_metric_card(
                "Readiness",
                readiness,
                readiness_note,
                readiness_color
            )

        pie_chart, bar_chart = create_skill_charts(
            len(result["matched_skills"]),
            len(result["missing_skills"])
        )

        chart_columns = st.columns(2, gap="large")

        with chart_columns[0]:
            st.plotly_chart(
                pie_chart,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        with chart_columns[1]:
            st.plotly_chart(
                bar_chart,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        skill_columns = st.columns(2, gap="large")

        with skill_columns[0]:
            st.markdown("### Matched Skills")
            render_skill_chips(result["matched_skills"], "matched")

        with skill_columns[1]:
            st.markdown("### Missing Skills")
            render_skill_chips(result["missing_skills"], "missing")

    # ---------------------------------
    # ATS ANALYSIS
    # ---------------------------------

    elif page == "ATS Analysis":

        st.subheader(
            "📄 ATS Resume Analysis"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "ATS Score",
                f"{ats_result['score']}/100"
            )

        with col2:

            st.metric(
                "Resume Score",
                f"{resume_score}/100"
            )

        st.info(
            ats_result["status"]
        )

        st.subheader(
            "✅ ATS Strengths"
        )

        for strength in ats_result[
            "strengths"
        ]:

            st.success(
                strength
            )

        st.subheader(
            "❌ ATS Weaknesses"
        )

        for weakness in ats_result[
            "weaknesses"
        ]:

            st.error(
                weakness
            )

        st.subheader(
            "💡 ATS Improvement Tips"
        )

        for suggestion in ats_result[
            "suggestions"
        ]:

            st.warning(
                suggestion
            )

    # ---------------------------------
    # LEARNING PLAN
    # ---------------------------------

    elif page == "Learning Plan":

        learning_plan = (
            get_learning_recommendations(
                result[
                    "missing_skills"
                ]
            )
        )

        st.subheader(
            "📚 Learning Recommendations"
        )

        for skill, content in (
            learning_plan.items()
        ):

            with st.expander(
                f"📌 {skill}",
                expanded=True
            ):

                st.write(
                    "Topics to Learn:"
                )

                for topic in content[
                    "topics"
                ]:

                    st.write(
                        f"• {topic}"
                    )

                st.write(
                    f"📖 Resource: "
                    f"{content['resource']}"
                )

    # ---------------------------------
    # ROADMAP
    # ---------------------------------

    elif page == "Skill Roadmap":

        roadmap = create_roadmap(
            result[
                "missing_skills"
            ]
        )

        st.subheader(
            "🗺️ Skill Gap Roadmap"
        )

        for step in roadmap:

            st.info(
                f"{step['step']}️⃣ "
                f"{step['skill']}"
            )

            st.write(
                f"Priority: "
                f"{step['priority']}"
            )

            st.write(
                f"Estimated Time: "
                f"{step['duration']}"
            )

            st.divider()

    # ---------------------------------
    # COURSES
    # ---------------------------------

    elif page == "Courses":

        st.subheader(
            "🎓 Course Recommendations"
        )

        courses = recommend_courses(
            selected_role,
            result[
                "missing_skills"
            ]
        )

        if courses:

            for course in courses:

                st.success(
                    f"📘 "
                    f"{course['title']}"
                )

                st.write(
                    f"Platform: "
                    f"{course['platform']}"
                )

                st.markdown(
                    f"[🔗 Open Course]"
                    f"({course['link']})"
                )

                st.divider()

    # ---------------------------------
    # RESUME SUGGESTIONS
    # ---------------------------------

    elif page == "Resume Suggestions":

        st.subheader(
            "📝 Resume Improvement Suggestions"
        )

        suggestions = (
            generate_resume_suggestions(
                extracted_text,
                selected_role,
                result[
                    "missing_skills"
                ]
            )
        )

        for suggestion in suggestions:

            st.warning(
                f"💡 {suggestion}"
            )

else:
    render_section_header(
        "Get Started",
        "Turn your resume into an action plan",
        "Upload a PDF resume to unlock role matching, ATS diagnostics, career insights, and a professional report."
    )

    welcome_columns = st.columns(3, gap="medium")

    with welcome_columns[0]:
        render_insight_card(
            "01 · Analyze",
            "Resume Intelligence",
            "Measure resume quality, ATS compatibility, and role-specific keyword coverage."
        )

    with welcome_columns[1]:
        render_insight_card(
            "02 · Improve",
            "Personalized Guidance",
            "Identify missing skills and receive focused recommendations for stronger applications."
        )

    with welcome_columns[2]:
        render_insight_card(
            "03 · Execute",
            "Learning Roadmap",
            "Translate gaps into courses, priorities, and a practical career development plan."
        )
