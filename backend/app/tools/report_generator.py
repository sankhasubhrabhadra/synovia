import os
import io
import logging
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

logger = logging.getLogger("synovia.report_generator")

class PDFReportGenerator:
    @staticmethod
    def generate_startup_blueprint_pdf(blueprint: Dict[str, Any]) -> bytes:
        """
        Generates a sleek, executive investor-ready PDF blueprint document.
        Handles nested dictionaries and string formats cleanly.
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
            fontSize=22,
            leading=26,
            textColor=PRIMARY,
            spaceAfter=4
        )
        
        tagline_style = ParagraphStyle(
            "DocTagline",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            textColor=ACCENT,
            spaceAfter=10
        )
        
        h1_style = ParagraphStyle(
            "Heading1_Custom",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=17,
            textColor=ACCENT,
            spaceBefore=12,
            spaceAfter=6
        )

        h2_style = ParagraphStyle(
            "Heading2_Custom",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=PRIMARY,
            spaceBefore=6,
            spaceAfter=4
        )

        body_style = ParagraphStyle(
            "Body_Custom",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=SECONDARY,
            spaceAfter=5
        )

        bullet_style = ParagraphStyle(
            "Bullet_Custom",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12.5,
            textColor=SECONDARY,
            leftIndent=10,
            spaceAfter=3
        )

        elements = []

        # Clean string helper
        def clean(val: str) -> str:
            if not val:
                return ""
            return str(val).replace("■", "").strip()

        # Title & Banner
        idea_title = clean(blueprint.get("idea", "Startup Blueprint")).title()
        elements.append(Paragraph("SYNOVIA // AUTONOMOUS STARTUP BLUEPRINT", tagline_style))
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
                        Paragraph("<br/>".join(weaknesses_list) if weaknesses_list else "High pricing & legacy Tech", bullet_style),
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
                        fname = clean(f.get("name", "Feature"))
                        fdesc = clean(f.get("description", ""))
                    else:
                        fname = clean(str(f))
                        fdesc = ""
                    elements.append(Paragraph(f"• <b>{fname}:</b> {fdesc}", bullet_style))
            elements.append(Spacer(1, 8))

        # 5. Technical Architecture (Robust parsing for dict or string)
        architect = blueprint.get("architect", {})
        if architect:
            elements.append(Paragraph("5. Technical Architecture & Tech Stack", h1_style))
            
            def parse_layer(layer_data: Any, default_tech: str, default_rat: str) -> tuple[str, str]:
                if isinstance(layer_data, dict):
                    tech = clean(layer_data.get("technology", layer_data.get("name", default_tech)))
                    rat = clean(layer_data.get("rationale", layer_data.get("description", default_rat)))
                    return tech or default_tech, rat or default_rat
                elif isinstance(layer_data, str) and layer_data.strip():
                    return clean(layer_data), default_rat
                return default_tech, default_rat

            # Smart defaults if physical product or web stack
            idea_lower = blueprint.get("idea", "").lower()
            is_hardware = any(k in idea_lower for k in ["backpack", "bag", "hardware", "shoe", "bottle", "watch", "wearable"])
            
            if is_hardware:
                tech_layers = [
                    ("Frontend / Mobile App", parse_layer(architect.get("frontend"), "React Native / Next.js 15 Web Portal", "Mobile companion app for IoT tracking & D2C Storefront")),
                    ("Backend Services", parse_layer(architect.get("backend"), "FastAPI (Python) + Node.js Microservices", "Order management, IoT Telemetry API, & Payment Webhooks")),
                    ("Database & Storage", parse_layer(architect.get("database"), "PostgreSQL + Redis Cache", "ACID transactional integrity for orders & fast session caching")),
                    ("Authentication & Security", parse_layer(architect.get("authentication"), "JWT + OAuth 2.0 (Google/Apple Sign-In)", "Secure user auth and device pairing encryption")),
                    ("Hardware / AI Specs", parse_layer(architect.get("ai_apis"), "Nordic BLE / Biometric Fingerprint Sensor", "Low-power Bluetooth 5.2 telemetry & TSA biometric locking")),
                    ("Production Hosting", parse_layer(architect.get("deployment"), "Vercel (Web) + AWS / Railway (Backend)", "Global CDN edge distribution with auto-scaling container API"))
                ]
            else:
                tech_layers = [
                    ("Frontend", parse_layer(architect.get("frontend"), "Next.js 15 + TypeScript + Tailwind CSS", "Server-side rendering & responsive UI")),
                    ("Backend API", parse_layer(architect.get("backend"), "FastAPI (Python 3.12) + Async SQLAlchemy", "High-throughput async IO & microservices")),
                    ("Database", parse_layer(architect.get("database"), "PostgreSQL + Redis Cache", "Relational data integrity & fast caching")),
                    ("Authentication", parse_layer(architect.get("authentication"), "Clerk / NextAuth.js + JWT", "Role-based access control")),
                    ("AI Infrastructure", parse_layer(architect.get("ai_apis"), "OpenAI GPT-4o / Gemini 1.5 Flash API", "Structured output extraction & natural language processing")),
                    ("Deployment / Cloud", parse_layer(architect.get("deployment"), "Vercel (Frontend) + Render / AWS (Backend)", "Global Edge deployment with automated CI/CD"))
                ]

            tech_data = [[Paragraph("<b>Layer</b>", h2_style), Paragraph("<b>Technology & Implementation Rationale</b>", h2_style)]]
            for layer_name, (tech_val, rationale) in tech_layers:
                tech_data.append([
                    Paragraph(f"<b>{layer_name}</b>", body_style),
                    Paragraph(f"<b>{tech_val}</b><br/><font size=8.5 color='#475569'>{rationale}</font>", body_style)
                ])
            
            t_tech = Table(tech_data, colWidths=[130, 400])
            t_tech.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('PADDING', (0,0), (-1,-1), 5),
            ]))
            elements.append(t_tech)
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
