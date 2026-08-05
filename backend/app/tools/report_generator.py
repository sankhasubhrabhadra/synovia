import os
import io
import logging
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

logger = logging.getLogger("synovia.report_generator")

# Register Unicode fonts
font_dir = os.path.dirname(os.path.abspath(__file__))
pdfmetrics.registerFont(TTFont('NotoSans', os.path.join(font_dir, 'NotoSans-Regular.ttf')))
pdfmetrics.registerFont(TTFont('NotoSans-Bold', os.path.join(font_dir, 'NotoSans-Bold.ttf')))
pdfmetrics.registerFontFamily('NotoSans', normal='NotoSans', bold='NotoSans-Bold')

class PDFReportGenerator:
    @staticmethod
    def generate_blueprint_pdf(blueprint: Dict[str, Any]) -> bytes:
        """
        Generates a sleek, VC-ready startup blueprint & validation PDF document.
        Replaces Technical Architecture with Validation & Strategy Report.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
        )
        
        styles = getSampleStyleSheet()
        
        # Custom palette
        PRIMARY = colors.HexColor("#0F172A") # Slate 900
        ACCENT = colors.HexColor("#4F46E5")  # Indigo 600
        SECONDARY = colors.HexColor("#334155")
        LIGHT_BG = colors.HexColor("#F8FAFC")
        SUCCESS = colors.HexColor("#059669")
        
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Normal"],
            fontName="NotoSans-Bold",
            fontSize=22,
            leading=26,
            textColor=PRIMARY,
            spaceAfter=4
        )
        
        tagline_style = ParagraphStyle(
            "DocTagline",
            parent=styles["Normal"],
            fontName="NotoSans-Bold",
            fontSize=10,
            leading=13,
            textColor=ACCENT,
            spaceAfter=10
        )
        
        h1_style = ParagraphStyle(
            "Heading1_Custom",
            parent=styles["Normal"],
            fontName="NotoSans-Bold",
            fontSize=14,
            leading=17,
            textColor=ACCENT,
            spaceBefore=12,
            spaceAfter=6
        )

        h2_style = ParagraphStyle(
            "Heading2_Custom",
            parent=styles["Normal"],
            fontName="NotoSans-Bold",
            fontSize=11,
            leading=14,
            textColor=PRIMARY,
            spaceBefore=6,
            spaceAfter=4
        )

        body_style = ParagraphStyle(
            "Body_Custom",
            parent=styles["Normal"],
            fontName="NotoSans",
            fontSize=9.5,
            leading=13.5,
            textColor=SECONDARY,
            spaceAfter=5
        )

        bullet_style = ParagraphStyle(
            "Bullet_Custom",
            parent=styles["Normal"],
            fontName="NotoSans",
            fontSize=9,
            leading=12.5,
            textColor=SECONDARY,
            leftIndent=10,
            spaceAfter=3
        )

        elements = []

        elements = []

        def clean(val: Any) -> str:
            if val is None:
                return ""
            if isinstance(val, (int, float, bool)):
                return str(val)
            if isinstance(val, dict):
                parts = [f"{k}: {clean(v)}" for k, v in val.items() if v]
                return " • ".join(parts)
            if isinstance(val, list):
                return ", ".join(clean(v) for v in val if v)
            return str(val).replace("■", "").strip()

        def parse_score(val: Any, default: int = 80) -> int:
            if isinstance(val, (int, float)):
                return int(val)
            if isinstance(val, dict):
                return parse_score(val.get("score") or val.get("value"), default)
            if isinstance(val, str):
                digits = "".join(filter(str.isdigit, val))
                return int(digits) if digits else default
            return default

        # Title & Banner
        idea_title = clean(blueprint.get("idea", "Startup Blueprint")).title()
        elements.append(Paragraph("SYNOVIA // STARTUP BLUEPRINT & VALIDATION REPORT", tagline_style))
        elements.append(Paragraph(f"Blueprint: {idea_title}", title_style))
        elements.append(Paragraph(f"<b>Generated:</b> {blueprint.get('created_at', '2026-08-03')} | <b>Target Market:</b> {blueprint.get('target_market', 'Global')}", body_style))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT, spaceBefore=8, spaceAfter=12))

        # 1. Executive Summary
        exec_summary = clean(blueprint.get("executive_summary", ""))
        if exec_summary:
            elements.append(Paragraph("1. Executive Summary", h1_style))
            elements.append(Paragraph(exec_summary, body_style))
            elements.append(Spacer(1, 8))

        # 2. Market Analysis
        research = blueprint.get("research", {})
        if research:
            elements.append(Paragraph("2. Market Analysis & Target Audience", h1_style))
            elements.append(Paragraph(f"<b>Industry Focus:</b> {clean(research.get('industry', 'Technology'))}", body_style))
            
            m_size = research.get("market_size", {})
            m_data = [
                [Paragraph("<b>TAM (Total Addressable Market)</b>", body_style), Paragraph(clean(m_size.get("tam", "Multi-Billion Dollar Opportunity")), body_style)],
                [Paragraph("<b>SAM (Serviceable Addressable Market)</b>", body_style), Paragraph(clean(m_size.get("sam", "High-growth Target Segment")), body_style)],
                [Paragraph("<b>SOM (Serviceable Obtainable Market)</b>", body_style), Paragraph(clean(m_size.get("som", "Year 1-2 Achievable Target")), body_style)],
            ]
            t_market = Table(m_data, colWidths=[190, 340])
            t_market.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
                ('PADDING', (0,0), (-1,-1), 5),
            ]))
            elements.append(t_market)
            elements.append(Spacer(1, 6))

            pains = research.get("customer_pain_points", [])
            if pains:
                elements.append(Paragraph("<b>Key Customer Pain Points:</b>", h2_style))
                for pain in pains:
                    elements.append(Paragraph(f"• {clean(pain)}", bullet_style))
            elements.append(Spacer(1, 8))

        # 3. Competitor Analysis
        competitor = blueprint.get("competitor", {})
        if competitor:
            elements.append(Paragraph("3. Competitor Intelligence & Market Gaps", h1_style))
            comps = competitor.get("competitors", [])
            if comps:
                comp_table_data = [[
                    Paragraph("<b>Competitor</b>", h2_style),
                    Paragraph("<b>Strengths</b>", h2_style),
                    Paragraph("<b>Weaknesses / Gaps</b>", h2_style)
                ]]
                for c in comps:
                    comp_name = clean(c.get('name', 'Market Player'))
                    comp_cat = clean(c.get('category', 'Competitor'))
                    strengths_list = [f"• {clean(s)}" for s in c.get('strengths', [])]
                    weaknesses_list = [f"• {clean(w)}" for w in c.get('weaknesses', [])]
                    
                    comp_table_data.append([
                        Paragraph(f"<b>{comp_name}</b><br/><font size=8 color='#64748B'>{comp_cat}</font>", body_style),
                        Paragraph("<br/>".join(strengths_list) if strengths_list else "Established market brand", bullet_style),
                        Paragraph("<br/>".join(weaknesses_list) if weaknesses_list else "High pricing & legacy workflow", bullet_style),
                    ])
                t_comp = Table(comp_table_data, colWidths=[125, 202, 203])
                t_comp.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('PADDING', (0,0), (-1,-1), 5),
                ]))
                elements.append(t_comp)
            
            moat = clean(competitor.get("defensability_strategy", ""))
            if moat:
                elements.append(Paragraph(f"<b>Defensability & Moat Strategy:</b> {moat}", body_style))
            elements.append(Spacer(1, 8))

        # 4. Product Features
        product = blueprint.get("product", {})
        if product:
            elements.append(Paragraph("4. Product Specification & Core MVP Features", h1_style))
            mvp_feats = product.get("mvp_features", [])
            if mvp_feats:
                for f in mvp_feats:
                    if isinstance(f, dict):
                        fname = clean(f.get("name") or f.get("title") or f.get("feature") or "Feature")
                        fdesc = clean(f.get("description") or f.get("desc") or "")
                    else:
                        fname = clean(str(f))
                        fdesc = ""
                    elements.append(Paragraph(f"• <b>{fname}:</b> {fdesc}", bullet_style))
            elements.append(Spacer(1, 8))

        # 5. Validation & Strategy Report (REPLACES Technical Architecture)
        validation = blueprint.get("validation", {})
        if validation:
            elements.append(Paragraph("5. Validation & Strategy Report (VC & Mentor Evaluation)", h1_style))
            
            # Scores Table
            viab = parse_score(validation.get('viability_score'), 80)
            innov = parse_score(validation.get('innovation_score'), 75)
            mopp = parse_score(validation.get('market_opportunity_score'), 85)
            feas = parse_score(validation.get('feasibility_score'), 70)
            scal = parse_score(validation.get('scalability_score'), 82)
            verdict_str = clean(validation.get('final_verdict', 'PROCEED')).split(':')[0]

            score_data = [
                [Paragraph("<b>Viability Score</b>", h2_style), Paragraph(f"<b>{viab} / 100</b>", h2_style),
                 Paragraph("<b>Innovation Score</b>", h2_style), Paragraph(f"<b>{innov} / 100</b>", h2_style)],
                [Paragraph("<b>Market Opportunity</b>", h2_style), Paragraph(f"<b>{mopp} / 100</b>", h2_style),
                 Paragraph("<b>Feasibility Score</b>", h2_style), Paragraph(f"<b>{feas} / 100</b>", h2_style)],
                [Paragraph("<b>Scalability Score</b>", h2_style), Paragraph(f"<b>{scal} / 100</b>", h2_style),
                 Paragraph("<b>Overall Evaluation</b>", h2_style), Paragraph(f"<b>{verdict_str}</b>", h2_style)],
            ]
            t_scores = Table(score_data, colWidths=[130, 135, 130, 135])
            t_scores.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
                ('PADDING', (0,0), (-1,-1), 5),
            ]))
            elements.append(t_scores)
            elements.append(Spacer(1, 6))

            # Major Risks
            b_risks = validation.get("major_business_risks", [])
            if b_risks:
                elements.append(Paragraph("<b>Major Business & Market Risks:</b>", h2_style))
                for r in b_risks:
                    elements.append(Paragraph(f"• {clean(r)}", bullet_style))

            t_risks = validation.get("technical_risks", [])
            if t_risks:
                elements.append(Paragraph("<b>Technical & Operational Risks:</b>", h2_style))
                for r in t_risks:
                    elements.append(Paragraph(f"• {clean(r)}", bullet_style))

            c_risks = validation.get("competitive_risks", [])
            if c_risks:
                elements.append(Paragraph("<b>Competitive Risks:</b>", h2_style))
                for r in c_risks:
                    elements.append(Paragraph(f"• {clean(r)}", bullet_style))

            # Validation & Next Actions
            rec_actions = validation.get("validation_recommendations", [])
            if rec_actions:
                elements.append(Paragraph("<b>Actionable Validation Recommendations:</b>", h2_style))
                for act in rec_actions:
                    elements.append(Paragraph(f"• {clean(act)}", bullet_style))

            first_cust = validation.get("suggested_first_customers", [])
            if first_cust:
                elements.append(Paragraph("<b>Suggested First Customers:</b>", h2_style))
                for cust in first_cust:
                    elements.append(Paragraph(f"• {clean(cust)}", bullet_style))

            # Growth Strategy & Verdict
            growth = clean(validation.get("long_term_growth_strategy", ""))
            if growth:
                elements.append(Paragraph(f"<b>Long-Term Growth Strategy:</b> {growth}", body_style))

            verdict = clean(validation.get("final_verdict", ""))
            if verdict:
                elements.append(Paragraph(f"<b>Final VC Mentor Verdict:</b> {verdict}", ParagraphStyle("VerdictStyle", parent=body_style, fontName="NotoSans-Bold", textColor=ACCENT)))
            elements.append(Spacer(1, 8))

        # 6. Execution Roadmap
        roadmap = blueprint.get("roadmap", {})
        if roadmap:
            elements.append(Paragraph("6. 4-Week Agile Execution Roadmap", h1_style))
            schedule = roadmap.get("schedule", [])
            for wk in schedule:
                title = clean(wk.get("title", f"Week {wk.get('week')}"))
                goals = clean(wk.get("goals", ""))
                elements.append(Paragraph(f"<b>Week {wk.get('week')}: {title}</b>", h2_style))
                if goals:
                    elements.append(Paragraph(f"<i>Focus:</i> {goals}", body_style))
                for deliv in wk.get("deliverables", []):
                    elements.append(Paragraph(f"• {clean(deliv)}", bullet_style))
            elements.append(Spacer(1, 8))

        # 7. Pitch Deck & Monetization
        pitch = blueprint.get("pitch", {})
        if pitch:
            elements.append(Paragraph("7. Investor Pitch & Business Monetization", h1_style))
            elements.append(Paragraph(f"<b>Unique Value Proposition:</b> {clean(pitch.get('usp', ''))}", body_style))
            elements.append(Paragraph(f"<b>Business Model:</b> {clean(pitch.get('business_model', ''))}", body_style))
            
            revs = pitch.get("revenue_streams", [])
            if revs:
                elements.append(Paragraph("<b>Monetization & Revenue Streams:</b>", h2_style))
                for r in revs:
                    elements.append(Paragraph(f"• {clean(r)}", bullet_style))
            elements.append(Spacer(1, 6))

            pitch_script = clean(pitch.get('hackathon_pitch', ''))
            if pitch_script:
                elements.append(Paragraph("<b>60-Second Investor Elevator Pitch:</b>", h2_style))
                elements.append(Paragraph(f"<i>\"{pitch_script}\"</i>", body_style))

        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
