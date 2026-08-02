import os
import io
import logging
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

logger = logging.getLogger("synovia.report_generator")

class PDFReportGenerator:
    @staticmethod
    def generate_startup_blueprint_pdf(blueprint: Dict[str, Any]) -> bytes:
        """
        Generates a sleek, executive investor-ready PDF blueprint document.
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
        
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=PRIMARY,
            spaceAfter=4
        )
        
        tagline_style = ParagraphStyle(
            "DocTagline",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=14,
            textColor=ACCENT,
            spaceAfter=15
        )
        
        h1_style = ParagraphStyle(
            "Heading1_Custom",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=18,
            textColor=ACCENT,
            spaceBefore=14,
            spaceAfter=6
        )

        h2_style = ParagraphStyle(
            "Heading2_Custom",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=PRIMARY,
            spaceBefore=8,
            spaceAfter=4
        )

        body_style = ParagraphStyle(
            "Body_Custom",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=SECONDARY,
            spaceAfter=6
        )

        bullet_style = ParagraphStyle(
            "Bullet_Custom",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=SECONDARY,
            leftIndent=12,
            firstLineIndent=-8,
            spaceAfter=3
        )

        elements = []

        # Title & Banner
        idea_title = blueprint.get("idea", "Startup Blueprint")
        elements.append(Paragraph("SYNOVIA // STARTUP BLUEPRINT", tagline_style))
        elements.append(Paragraph(f"Blueprint: {idea_title}", title_style))
        elements.append(Paragraph(f"<b>Generated:</b> {blueprint.get('created_at', '2026')}", body_style))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT, spaceBefore=10, spaceAfter=15))

        # 1. Executive Summary
        exec_summary = blueprint.get("executive_summary", "")
        if exec_summary:
            elements.append(Paragraph("1. Executive Summary", h1_style))
            elements.append(Paragraph(exec_summary, body_style))
            elements.append(Spacer(1, 10))

        # 2. Market Research
        research = blueprint.get("research", {})
        if research:
            elements.append(Paragraph("2. Market Analysis & Target Audience", h1_style))
            elements.append(Paragraph(f"<b>Industry:</b> {research.get('industry', 'N/A')}", body_style))
            
            # Market Size Table
            m_size = research.get("market_size", {})
            m_data = [
                [Paragraph("<b>TAM (Total Addressable Market)</b>", body_style), Paragraph(m_size.get("tam", ""), body_style)],
                [Paragraph("<b>SAM (Serviceable Addressable Market)</b>", body_style), Paragraph(m_size.get("sam", ""), body_style)],
                [Paragraph("<b>SOM (Serviceable Obtainable Market)</b>", body_style), Paragraph(m_size.get("som", ""), body_style)],
            ]
            t_market = Table(m_data, colWidths=[200, 330])
            t_market.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
                ('PADDING', (0,0), (-1,-1), 6),
            ]))
            elements.append(t_market)
            elements.append(Spacer(1, 8))

            pains = research.get("customer_pain_points", [])
            if pains:
                elements.append(Paragraph("<b>Customer Pain Points:</b>", h2_style))
                for pain in pains:
                    elements.append(Paragraph(f"• {pain}", bullet_style))
            elements.append(Spacer(1, 10))

        # 3. Competitor Analysis
        competitor = blueprint.get("competitor", {})
        if competitor:
            elements.append(Paragraph("3. Competitor Analysis & Gaps", h1_style))
            comps = competitor.get("competitors", [])
            if comps:
                comp_table_data = [[
                    Paragraph("<b>Competitor</b>", h2_style),
                    Paragraph("<b>Strengths</b>", h2_style),
                    Paragraph("<b>Weaknesses / Gaps</b>", h2_style)
                ]]
                for c in comps:
                    comp_table_data.append([
                        Paragraph(f"<b>{c.get('name')}</b><br/><font size=8 color='#64748B'>{c.get('category')}</font>", body_style),
                        Paragraph("<br/>".join([f"• {s}" for s in c.get('strengths', [])]), bullet_style),
                        Paragraph("<br/>".join([f"• {w}" for w in c.get('weaknesses', [])]), bullet_style),
                    ])
                t_comp = Table(comp_table_data, colWidths=[120, 205, 205])
                t_comp.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('PADDING', (0,0), (-1,-1), 6),
                ]))
                elements.append(t_comp)
            elements.append(Spacer(1, 10))

        # 4. Product Features
        product = blueprint.get("product", {})
        if product:
            elements.append(Paragraph("4. Product Specification & MVP Features", h1_style))
            mvp_feats = product.get("mvp_features", [])
            if mvp_feats:
                elements.append(Paragraph("<b>Core MVP Features:</b>", h2_style))
                for f in mvp_feats:
                    name = f.get("name") if isinstance(f, dict) else f
                    desc = f.get("description", "") if isinstance(f, dict) else ""
                    elements.append(Paragraph(f"• <b>{name}:</b> {desc}", bullet_style))
            elements.append(Spacer(1, 10))

        # 5. Technical Architecture
        architect = blueprint.get("architect", {})
        if architect:
            elements.append(Paragraph("5. Technical Architecture", h1_style))
            tech_layers = [
                ("Frontend", architect.get("frontend", {})),
                ("Backend", architect.get("backend", {})),
                ("Database", architect.get("database", {})),
                ("Authentication", architect.get("authentication", {})),
                ("AI Infrastructure", architect.get("ai_apis", {})),
                ("Deployment", architect.get("deployment", {})),
            ]
            tech_data = [[Paragraph("<b>Layer</b>", h2_style), Paragraph("<b>Technology & Rationale</b>", h2_style)]]
            for layer_name, layer_obj in tech_layers:
                tech_val = layer_obj.get("technology", "N/A") if isinstance(layer_obj, dict) else str(layer_obj)
                rationale = layer_obj.get("rationale", "") if isinstance(layer_obj, dict) else ""
                tech_data.append([
                    Paragraph(f"<b>{layer_name}</b>", body_style),
                    Paragraph(f"<b>{tech_val}</b> - {rationale}", body_style)
                ])
            t_tech = Table(tech_data, colWidths=[130, 400])
            t_tech.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
                ('PADDING', (0,0), (-1,-1), 5),
            ]))
            elements.append(t_tech)
            elements.append(Spacer(1, 10))

        # 6. Execution Roadmap
        roadmap = blueprint.get("roadmap", {})
        if roadmap:
            elements.append(Paragraph("6. 4-Week Execution Roadmap", h1_style))
            schedule = roadmap.get("schedule", [])
            for wk in schedule:
                title = wk.get("title", f"Week {wk.get('week')}")
                goals = wk.get("goals", "")
                elements.append(Paragraph(f"<b>Week {wk.get('week')}: {title}</b>", h2_style))
                if goals:
                    elements.append(Paragraph(f"<i>Focus:</i> {goals}", body_style))
                for deliv in wk.get("deliverables", []):
                    elements.append(Paragraph(f"• {deliv}", bullet_style))
            elements.append(Spacer(1, 10))

        # 7. Pitch Deck & Monetization
        pitch = blueprint.get("pitch", {})
        if pitch:
            elements.append(Paragraph("7. Investor Pitch & Monetization", h1_style))
            elements.append(Paragraph(f"<b>Unique Value Proposition:</b> {pitch.get('usp', '')}", body_style))
            elements.append(Paragraph(f"<b>Business Model:</b> {pitch.get('business_model', '')}", body_style))
            revs = pitch.get("revenue_streams", [])
            if revs:
                elements.append(Paragraph("<b>Revenue Streams:</b>", h2_style))
                for r in revs:
                    elements.append(Paragraph(f"• {r}", bullet_style))
            elements.append(Spacer(1, 8))

            elements.append(Paragraph("<b>60-Second Elevator Pitch:</b>", h2_style))
            elements.append(Paragraph(f"<i>\"{pitch.get('hackathon_pitch', '')}\"</i>", body_style))

        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
