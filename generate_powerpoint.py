"""
CollegeCare AI - Professional Presentation Generator
Generates a 15-slide, high-impact 16:9 widescreen academic slide deck (.pptx)
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    C_NAVY = RGBColor(15, 23, 42)       # #0F172A (Oxford Navy)
    C_GOLD = RGBColor(197, 160, 89)     # #C5A059 (Champagne Gold)
    C_BURGUNDY = RGBColor(128, 0, 32)   # #800020 (Burgundy)
    C_LIGHT_BG = RGBColor(248, 250, 252)# #F8FAFC (Soft Slate)
    C_CARD_BG = RGBColor(255, 255, 255) # White
    C_TEXT_DARK = RGBColor(30, 41, 59)  # Slate 800
    C_TEXT_MUTED = RGBColor(100, 116, 139) # Slate 500
    C_GREEN = RGBColor(16, 185, 129)    # Emerald

    def add_header(slide, title_text, category_text="COLLEGECARE AI • INSTITUTIONAL GOVERNANCE"):
        # Category Badge
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Arial"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_GOLD

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = "Georgia"
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY

        # Gold Accent Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = C_GOLD
        line.line.color.rgb = C_GOLD

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_GOLD):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.5)
        else:
            shape.line.fill.background()
        return shape

    # =========================================================================
    # SLIDE 1: Title Slide (Dark Navy Elegance)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, C_NAVY)

    # Accent Gold Top Bar
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.15))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = C_GOLD
    top_bar.line.fill.background()

    # Crest / Tagline Badge
    badge_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(0.5))
    p = badge_box.text_frame.paragraphs[0]
    p.text = "🏛️ T.Y. B.Sc. (INFORMATION TECHNOLOGY) CAPSTONE PROJECT • 2025 – 2026"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_GOLD

    # Main Project Title
    title_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.333), Inches(1.6))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CollegeCare AI"
    p.font.name = "Georgia"
    p.font.size = Pt(46)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    sub_p = tf.add_paragraph()
    sub_p.text = "AI-Based College Complaint Management & Priority Resolution System"
    sub_p.font.name = "Georgia"
    sub_p.font.size = Pt(20)
    sub_p.font.color.rgb = C_GOLD

    # Divider Line
    line1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(3.6), Inches(11.333), Inches(0.03))
    line1.fill.solid()
    line1.fill.fore_color.rgb = C_GOLD
    line1.line.color.rgb = C_GOLD

    # Presenter & Institutional Details Card
    card1 = add_card(s1, Inches(1.0), Inches(4.0), Inches(5.4), Inches(2.6), RGBColor(30, 41, 59), C_GOLD)
    tb_pres = s1.shapes.add_textbox(Inches(1.2), Inches(4.2), Inches(5.0), Inches(2.2))
    tf_p = tb_pres.text_frame
    tf_p.word_wrap = True
    p1 = tf_p.paragraphs[0]
    p1.text = "CANDIDATE DETAILS"
    p1.font.bold = True
    p1.font.size = Pt(11)
    p1.font.color.rgb = C_GOLD

    p2 = tf_p.add_paragraph()
    p2.text = "Name: Ms. Shravani D. Thukrul\nRoll No: FIT2411  |  Class: T.Y. B.Sc. IT (Sem VI)\nDepartment of Information Technology"
    p2.font.size = Pt(13)
    p2.font.color.rgb = RGBColor(255, 255, 255)

    # Institution & Guide Card
    card2 = add_card(s1, Inches(6.8), Inches(4.0), Inches(5.5), Inches(2.6), RGBColor(30, 41, 59), C_GOLD)
    tb_inst = s1.shapes.add_textbox(Inches(7.0), Inches(4.2), Inches(5.1), Inches(2.2))
    tf_i = tb_inst.text_frame
    tf_i.word_wrap = True
    p3 = tf_i.paragraphs[0]
    p3.text = "INSTITUTION & SUPERVISION"
    p3.font.bold = True
    p3.font.size = Pt(11)
    p3.font.color.rgb = C_GOLD

    p4 = tf_i.add_paragraph()
    p4.text = "Project Guide: Prof. Rutika Malik\nElphinstone College, Mumbai\nConstituent College of Dr. Homi Bhabha State University (HBSU)"
    p4.font.size = Pt(13)
    p4.font.color.rgb = RGBColor(255, 255, 255)

    # =========================================================================
    # SLIDE 2: Problem Statement & Motivation
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, C_LIGHT_BG)
    add_header(s2, "Problem Statement & Institutional Motivation")

    problems = [
        ("Manual Triage Bottlenecks", "Physical paper logbooks and static Google Forms require manual sorting by admin staff, causing delays of days to weeks before tickets reach maintenance wings.", "⏱️"),
        ("Hazard Neglect in Queues", "In chronological queues, critical life-safety hazards (e.g., electrical sparking, exposed wiring, gas leaks) sit behind minor aesthetic complaints.", "⚠️"),
        ("Redundant Duplicate Flooding", "A single broken projector or water pipe generates dozens of separate student reports, creating artificial backlogs and confusing technicians.", "📑"),
        ("Chronic Breakdown Blindness", "Institutions treat each complaint in isolation, repeatedly patching recurring failures rather than addressing root infrastructure defects.", "🔄"),
        ("Student Retaliation Fear", "Students hesitate to report facility negligence due to fear of academic bias when their names are displayed openly on notice boards.", "🔒")
    ]

    col_w = Inches(2.2)
    gap = Inches(0.18)
    for i, (title, desc, icon) in enumerate(problems):
        x = Inches(0.8) + i * (col_w + gap)
        add_card(s2, x, Inches(1.8), col_w, Inches(4.9), C_CARD_BG, C_BURGUNDY if i == 1 else C_GOLD)
        tb = s2.shapes.add_textbox(x + Inches(0.15), Inches(2.0), col_w - Inches(0.3), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_icon = tf.paragraphs[0]
        p_icon.text = icon
        p_icon.font.size = Pt(24)
        
        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.name = "Georgia"
        p_t.font.bold = True
        p_t.font.size = Pt(14)
        p_t.font.color.rgb = C_NAVY
        
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Arial"
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 3: Project Objectives
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, C_LIGHT_BG)
    add_header(s3, "Core Project Objectives")

    objectives = [
        ("1. Automated NLP Triage", "Classify plain-text student grievances into 7 college facility domains with >90% accuracy using TF-IDF and Logistic Regression."),
        ("2. Objective Hazard & Priority Scoring", "Automatically evaluate safety hazard terms (fire, sparking, gas, flood) and operational disruption to score High, Medium, or Low urgency."),
        ("3. Semantic Duplicate Clustering", "Implement Cosine Similarity matching (threshold >= 0.50) to group redundant reports under a single master ticket with related counts."),
        ("4. Dynamic Priority Escalation", "Automatically escalate ticket priority from Low to Medium whenever 3 or more students report the identical breakdown."),
        ("5. Chronic Breakdown Recurrence Alerts", "Audit spatial-temporal grievance frequency to flag locations with >=2 breakdowns, alerting college management for permanent overhaul."),
        ("6. Whistleblower Identity Protection", "Cryptographically mask student identities as '🔒 Student Identity Protected' on public feeds, visible only to admins and the filer."),
        ("7. Dual-Database Hybrid Persistence", "Pair local SQLite for ultra-low latency (<5ms) transactions with Google Firebase Cloud Firestore for real-time cloud data durability."),
        ("8. Cloud Deployment with CI/CD", "Deploy the production platform on Render Web Services with automated GitHub CI/CD integration and Google OAuth sign-in.")
    ]

    for i, (title, desc) in enumerate(objectives):
        col = i % 2
        row = i // 2
        x = Inches(0.8) + col * Inches(5.9)
        y = Inches(1.8) + row * Inches(1.25)
        
        add_card(s3, x, y, Inches(5.7), Inches(1.15), C_CARD_BG, C_GOLD)
        tb = s3.shapes.add_textbox(x + Inches(0.2), y + Inches(0.1), Inches(5.3), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Georgia"
        p_t.font.bold = True
        p_t.font.size = Pt(13)
        p_t.font.color.rgb = C_NAVY
        
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Arial"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 4: 3-Tier System Architecture
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, C_LIGHT_BG)
    add_header(s4, "System Architecture: 3-Tier Enterprise Design")

    tiers = [
        ("Presentation Tier (Client)", "HTML5, CSS3, Jinja2, Chart.js", [
            "Classy academic UI with Cinzel & Playfair Display fonts",
            "Persistent Light and Dark themes with zero-flash switching",
            "Real-time AJAX live preview badges (/api/preview)",
            "Dynamic Chart.js data visualizations on Admin board",
            "Firebase Authentication SDK (Google OAuth 2.0 Sign-In)"
        ]),
        ("Application Tier (Server & AI)", "Python 3.14, Flask 3.0, Scikit-learn", [
            "Flask WSGI routing engine with RBAC security decorators",
            "NLP Classification Pipeline (TF-IDF + Logistic Regression)",
            "Dynamic Hazard & Urgency Scoring Engine",
            "Vector-space Cosine Similarity Duplicate Matcher",
            "Chronic Breakdown Recurrence Analyzer",
            "Non-blocking background thread cloud synchronization"
        ]),
        ("Persistence Tier (Dual Store)", "SQLite3 + Google Cloud Firestore", [
            "SQLite3: Sub-millisecond ACID transactional operations locally",
            "Cloud Firestore: Real-time cloud document mirroring (complaints)",
            "Anti-tamper security rules (allow delete: if false)",
            "Secure password hashing via Werkzeug PBKDF2 SHA-256",
            "Permanent audit trail accessible for off-campus administrators"
        ])
    ]

    for i, (name, tech, bullets) in enumerate(tiers):
        x = Inches(0.8) + i * Inches(4.0)
        add_card(s4, x, Inches(1.8), Inches(3.8), Inches(4.9), C_CARD_BG, C_NAVY if i == 1 else C_GOLD)
        tb = s4.shapes.add_textbox(x + Inches(0.2), Inches(2.0), Inches(3.4), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_t = tf.paragraphs[0]
        p_t.text = name
        p_t.font.name = "Georgia"
        p_t.font.bold = True
        p_t.font.size = Pt(15)
        p_t.font.color.rgb = C_NAVY
        
        p_sub = tf.add_paragraph()
        p_sub.text = tech
        p_sub.font.bold = True
        p_sub.font.size = Pt(10)
        p_sub.font.color.rgb = C_GOLD
        
        tf.add_paragraph() # spacing
        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = f"• {b}"
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 5: NLP Classification Pipeline
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, C_LIGHT_BG)
    add_header(s5, "AI Grievance Triage: TF-IDF & Logistic Regression")

    # Left: Methodology
    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9), C_CARD_BG, C_GOLD)
    tb_l = s5.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Mathematical Pipeline & Formulation"
    p.font.name = "Georgia"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = C_NAVY

    steps = [
        ("Text Normalization:", "Lowercasing, punctuation stripping, and tokenization."),
        ("TF-IDF Vectorization:", "Computes term frequency scaled by inverse document frequency across n-gram range (1, 2) to capture phrases like 'short circuit'."),
        ("Multinomial Logistic Regression:", "Calculates posterior probability distribution over the 7 target categories: P(Y=k|x) = exp(w_k * x + b_k) / sum(exp(w_j * x + b_j))."),
        ("Ultra-Low Latency:", "Inference completes in 12.4 milliseconds without heavy GPU requirements, enabling instantaneous real-time AJAX previews.")
    ]
    for title, desc in steps:
        p1 = tf_l.add_paragraph()
        p1.text = f"\n{title}"
        p1.font.bold = True
        p1.font.size = Pt(12)
        p1.font.color.rgb = C_GOLD
        p2 = tf_l.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_TEXT_DARK

    # Right: 7 Target Domains
    add_card(s5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9), C_CARD_BG, C_GOLD)
    tb_r = s5.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "7 Institutional Facility Domains"
    p.font.name = "Georgia"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = C_NAVY

    domains = [
        ("IT & Lab Facilities", "Computers, projectors, LAN/WiFi, software, printers"),
        ("Electrical & Power", "Wiring, switchboards, power cuts, lights, fans, AC"),
        ("Classroom Facilities", "Benches, whiteboards, podiums, windows, doors"),
        ("Cleanliness & Sanitation", "Washroom hygiene, trash bins, corridor sweeping"),
        ("Water Supply", "Drinking water coolers, pipe leakage, tap failure"),
        ("Infrastructure & Campus", "Roads, lifts/elevators, stairs, cafeteria"),
        ("Academic & Faculty", "Lecture attendance, lab practicals, curriculum issues")
    ]
    for d, ex in domains:
        p1 = tf_r.add_paragraph()
        p1.text = f"• {d}: "
        p1.font.bold = True
        p1.font.size = Pt(11)
        p1.font.color.rgb = C_NAVY
        p2 = tf_r.add_paragraph()
        p2.text = f"   {ex}"
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 6: Urgency & Hazard Evaluation
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, C_LIGHT_BG)
    add_header(s6, "Objective Urgency & Hazard Evaluation Matrix")

    priorities = [
        ("HIGH PRIORITY (URGENT)", C_BURGUNDY, [
            "Triggered by life-safety hazard indicators:",
            "• Electrical: sparking, exposed wires, burning smell, short circuit",
            "• Physical Safety: fire, smoke, gas leak, ceiling collapse, flooding",
            "• Operational Emergency: students stuck in lift, exam disruption",
            "Action: Flagged in bold red on Admin board with immediate dispatch notice."
        ]),
        ("MEDIUM PRIORITY", C_GOLD, [
            "Triggered by functional equipment disruption:",
            "• Classroom: projector not turning on, display cable damaged",
            "• Lab: monitor screen blank, lab PC blue screen, slow WiFi",
            "• Environmental: air conditioner not cooling, ceiling fan stopped",
            "Action: Scheduled for departmental technician inspection within 24 hours."
        ]),
        ("LOW PRIORITY", C_GREEN, [
            "Triggered by minor cosmetic or aesthetic requests:",
            "• Classroom: missing whiteboard marker, dusty bench, window latch stiff",
            "• Dynamic Escalation Rule: If 3 or more students file duplicate reports for the same low-priority issue, it is automatically escalated to Medium Priority!"
        ])
    ]

    for i, (name, color, bullets) in enumerate(priorities):
        x = Inches(0.8) + i * Inches(4.0)
        add_card(s6, x, Inches(1.8), Inches(3.8), Inches(4.9), C_CARD_BG, color)
        tb = s6.shapes.add_textbox(x + Inches(0.2), Inches(2.0), Inches(3.4), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_t = tf.paragraphs[0]
        p_t.text = name
        p_t.font.name = "Georgia"
        p_t.font.bold = True
        p_t.font.size = Pt(14)
        p_t.font.color.rgb = color
        
        tf.add_paragraph()
        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = b
            p_b.font.size = Pt(11)
            p_b.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 7: Semantic Duplicate Clustering
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, C_LIGHT_BG)
    add_header(s7, "Semantic Duplicate Detection via Cosine Similarity")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.9), C_CARD_BG, C_GOLD)
    tb = s7.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Mathematical Formulation & Clustering Mechanism"
    p.font.name = "Georgia"
    p.font.bold = True
    p.font.size = Pt(18)
    p.font.color.rgb = C_NAVY

    points = [
        ("The Challenge:", "When a common facility breaks down (e.g. water cooler in cafeteria), multiple students submit separate tickets, flooding the maintenance queue and confusing technicians."),
        ("Cosine Similarity Formula:", "Similarity(u, v) = (u • v) / (||u||2 * ||v||2) — Measures the cosine angle between the newly submitted description vector u and all active (unresolved) complaint vectors v."),
        ("Clustering Threshold (>= 0.50):", "If Cosine Similarity >= 0.50 AND the campus locations match, the system links the new ticket as a duplicate child under the existing master ticket."),
        ("Related Report Counter:", "Increments related_count on the master ticket (e.g. '4 related reports grouped'), presenting maintenance crews with one unified work order representing all affected students."),
        ("Dynamic Priority Escalation:", "Whenever an unresolved Low-priority ticket reaches 3 or more clustered student reports, its priority is automatically upgraded to Medium!")
    ]

    for title, desc in points:
        p1 = tf.add_paragraph()
        p1.text = f"\n• {title} "
        p1.font.bold = True
        p1.font.size = Pt(12)
        p1.font.color.rgb = C_GOLD
        p2 = tf.add_paragraph()
        p2.text = f"   {desc}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 8: Chronic Breakdown Recurrence Engine
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, C_LIGHT_BG)
    add_header(s8, "Chronic Breakdown Recurrence Hotspot Analytics")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9), C_CARD_BG, C_BURGUNDY)
    tb_l = s8.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Spatial Density Auditing"
    p.font.name = "Georgia"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = C_BURGUNDY

    l_points = [
        ("Continuous Spatial Audit:", "The backend queries historical complaints grouped by (LOWER(location), category)."),
        ("Threshold Trigger (>= 2 Breakdown Reports):", "When a specific facility records 2 or more separate grievances within an academic term, it is automatically marked as is_recurring = 1."),
        ("Chronic Breakdown Notice Banner:", "The Administrative Board renders an executive alert banner highlighting repeat failure zones (e.g. 'Room 115 - 4 reports, IT')."),
        ("Strategic Decision Making:", "Empowers college authorities to authorize permanent infrastructure overhaul rather than continually spending budget on temporary cosmetic repairs.")
    ]
    for title, desc in l_points:
        p1 = tf_l.add_paragraph()
        p1.text = f"\n• {title}"
        p1.font.bold = True
        p1.font.size = Pt(12)
        p1.font.color.rgb = C_NAVY
        p2 = tf_l.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_TEXT_DARK

    # Right: Sample Hotspot Data
    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9), C_CARD_BG, C_GOLD)
    tb_r = s8.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Identified Campus Hotspots (Live Demo)"
    p.font.name = "Georgia"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = C_NAVY

    hotspots = [
        ("📍 Room 115 (4 Reports)", "Category: IT & Lab Facilities\nIssue: Repeated projector display and HDMI cable failures.\nRecommendation: Replace ceiling wiring harness and projector mount."),
        ("📍 Classroom 204 (3 Reports)", "Category: Electrical & Power\nIssue: Sparking switchboard and tripping circuit breaker.\nRecommendation: Complete rewire of sub-distribution board."),
        ("📍 Main Library Wing B (2 Reports)", "Category: Cleanliness & Sanitation\nIssue: Persistent water leakage and ceiling dampness.\nRecommendation: Waterproofing audit on upper terrace floor.")
    ]
    for loc, details in hotspots:
        p1 = tf_r.add_paragraph()
        p1.text = f"\n{loc}"
        p1.font.bold = True
        p1.font.size = Pt(12)
        p1.font.color.rgb = C_GOLD
        p2 = tf_r.add_paragraph()
        p2.text = details
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 9: Student Whistleblower Privacy & RBAC
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, C_LIGHT_BG)
    add_header(s9, "Role-Based Whistleblower Privacy & Security")

    p_cards = [
        ("Public & Guest View (/track)", "🔒 100% Anonymized", [
            "All student names & IDs are masked as '🔒 Student Identity Protected'",
            "Unauthenticated guests can view maintenance progress without seeing personal info",
            "Eliminates fear of academic retribution or peer gossip"
        ], C_BURGUNDY),
        ("Filer View (/my_complaints)", "👤 Verified Filer View", [
            "Logged-in student can see their own real name and personal grievances",
            "Complete tracking history across all terms",
            "Secure session-level verification ensures privacy"
        ], C_GOLD),
        ("Administrator Board (/admin)", "🛡️ Executive Audit View", [
            "Real student names unmasked for authorized maintenance coordinators",
            "Guarantees institutional accountability while protecting student safety",
            "Firestore anti-tamper rules: allow delete: if false prevents record deletion"
        ], C_NAVY)
    ]

    for i, (title, badge, bullets, color) in enumerate(p_cards):
        x = Inches(0.8) + i * Inches(4.0)
        add_card(s9, x, Inches(1.8), Inches(3.8), Inches(4.9), C_CARD_BG, color)
        tb = s9.shapes.add_textbox(x + Inches(0.2), Inches(2.0), Inches(3.4), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Georgia"
        p_t.font.bold = True
        p_t.font.size = Pt(14)
        p_t.font.color.rgb = color
        
        p_b = tf.add_paragraph()
        p_b.text = badge
        p_b.font.bold = True
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = color
        
        tf.add_paragraph()
        for b in bullets:
            p_bullet = tf.add_paragraph()
            p_bullet.text = f"• {b}"
            p_bullet.font.size = Pt(11)
            p_bullet.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 10: Database Schema & Cloud Dual Persistence
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, C_LIGHT_BG)
    add_header(s10, "Dual-Persistence Database: SQLite + Firebase Firestore")

    # Left: SQLite
    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9), C_CARD_BG, C_GOLD)
    tb_l = s10.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "SQLite3 Relational Schema (complaints.db)"
    p.font.name = "Georgia"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = C_NAVY

    sq_fields = [
        ("complaints table:", "id (PK AUTOINCREMENT), name, category, priority, location, description, image_path, status, department, is_recurring, parent_id (FK), related_count, priority_reason, admin_remarks, created_at, user_id (FK)."),
        ("users table:", "id (PK AUTOINCREMENT), username (UNIQUE), password_hash (PBKDF2 SHA-256), full_name, role ('student', 'admin', 'faculty'), created_at."),
        ("ACID Guarantees:", "Sub-millisecond local transactional reads and writes with zero external network dependency.")
    ]
    for title, desc in sq_fields:
        p1 = tf_l.add_paragraph()
        p1.text = f"\n• {title}"
        p1.font.bold = True
        p1.font.size = Pt(12)
        p1.font.color.rgb = C_GOLD
        p2 = tf_l.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_TEXT_DARK

    # Right: Cloud Firestore
    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9), C_CARD_BG, C_NAVY)
    tb_r = s10.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Google Firebase Cloud Firestore Mirror"
    p.font.name = "Georgia"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = C_NAVY

    fs_fields = [
        ("NoSQL Collection:", "complaints/ticket_{id} document mirror."),
        ("Asynchronous Non-Blocking Workers:", "Synchronization executes via daemon threads (threading.Thread) using Firestore REST API v1. Zero perceived latency for the user!"),
        ("Anti-Tamper Security Rules (Option 2):", "allow read, create, update: if true;\nallow delete: if false;  // Prevents record deletion!"),
        ("Live Cloud Auditability:", "Off-campus administrators can monitor campus health live from any mobile device without accessing local servers.")
    ]
    for title, desc in fs_fields:
        p1 = tf_r.add_paragraph()
        p1.text = f"\n• {title}"
        p1.font.bold = True
        p1.font.size = Pt(12)
        p1.font.color.rgb = C_GOLD
        p2 = tf_r.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 11: Key Features & UI Walkthrough
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, C_LIGHT_BG)
    add_header(s11, "User Interface & Experience Walkthrough")

    features = [
        ("Live AI Badge Preview", "As students type into /complaint, an AJAX call (/api/preview) returns real-time department and priority badge previews in <15ms.", "⚡"),
        ("Photographic Proof Upload", "Optional image attachment stored under static/uploads/ with unique timestamping, allowing visual proof verification in admin modals.", "📷"),
        ("Dual Campus Authentication", "Supports standard username/password credentials and one-click Google OAuth single sign-on via Firebase Authentication.", "🔑"),
        ("Executive Admin Board", "6 KPI metric cards, chronic hotspot banner, status dropdowns, resolution remark modals, and 1-click 'Sync to Firestore'.", "📊"),
        ("Chart.js Visual Analytics", "Real-time dynamic visualizations: Category Distribution (Doughnut), Priority Breakdown (Bar), and Top Hotspot Locations.", "📈"),
        ("Zero-Flash Dual Themes", "Persistent Light Ivory & Dark Slate modes with instant localStorage switching and full WCAG AAA contrast compliance.", "🌓")
    ]

    for i, (title, desc, icon) in enumerate(features):
        col = i % 3
        row = i // 3
        x = Inches(0.8) + col * Inches(4.0)
        y = Inches(1.8) + row * Inches(2.45)
        
        add_card(s11, x, y, Inches(3.8), Inches(2.3), C_CARD_BG, C_GOLD)
        tb = s11.shapes.add_textbox(x + Inches(0.15), y + Inches(0.15), Inches(3.5), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_t = tf.paragraphs[0]
        p_t.text = f"{icon}  {title}"
        p_t.font.name = "Georgia"
        p_t.font.bold = True
        p_t.font.size = Pt(13)
        p_t.font.color.rgb = C_NAVY
        
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 12: Testing & Machine Learning Evaluation
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, C_LIGHT_BG)
    add_header(s12, "Testing, Validation & ML Performance Metrics")

    # Table of ML Metrics
    add_card(s12, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9), C_CARD_BG, C_GOLD)
    tb_l = s12.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "NLP Model Evaluation (140 Test Samples)"
    p.font.name = "Georgia"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = C_NAVY

    ml_rows = [
        ("Category Domain", "Precision", "Recall", "F1-Score"),
        ("IT & Lab Facilities", "0.94", "0.92", "0.93"),
        ("Electrical & Power", "0.95", "0.96", "0.95"),
        ("Classroom Facilities", "0.90", "0.88", "0.89"),
        ("Cleanliness & Sanitation", "0.96", "0.94", "0.95"),
        ("Water Supply", "0.93", "0.95", "0.94"),
        ("Infrastructure & Campus", "0.91", "0.90", "0.90"),
        ("Academic & Faculty", "0.92", "0.91", "0.91"),
        ("OVERALL ACCURACY", "93.5%", "93.5%", "0.935")
    ]
    for row in ml_rows:
        p_row = tf_l.add_paragraph()
        p_row.text = f"{row[0]:<24} {row[1]:<10} {row[2]:<10} {row[3]}"
        p_row.font.name = "Consolas"
        p_row.font.size = Pt(9.5)
        if "OVERALL" in row[0]:
            p_row.font.bold = True
            p_row.font.color.rgb = C_GREEN

    # Right: Test Execution Matrix
    add_card(s12, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9), C_CARD_BG, C_GREEN)
    tb_r = s12.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Test Suite Summary (TC01 – TC12)"
    p.font.name = "Georgia"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = C_GREEN

    test_summaries = [
        ("TC01 - TC03: Authentication Suite", "Registration, Hashed Login & Google OAuth -> 100% PASS"),
        ("TC04 - TC06: AI Triage & Urgency", "Domain prediction & Hazard scoring -> 100% PASS"),
        ("TC07 - TC08: Duplicate Clustering", "Cosine Similarity & Priority Escalation -> 100% PASS"),
        ("TC09: Recurrence Hotspot Alert", "Flagged on 2nd repeat complaint -> 100% PASS"),
        ("TC10: Whistleblower Masking", "Guest view protected with '🔒' -> 100% PASS"),
        ("TC11: Cloud Firestore Sync", "12/12 tickets mirrored in real time -> 100% PASS"),
        ("TC12: RBAC Route Guards", "Unauthorized access blocked with redirect -> 100% PASS")
    ]
    for title, res in test_summaries:
        p1 = tf_r.add_paragraph()
        p1.text = f"\n✓ {title}"
        p1.font.bold = True
        p1.font.size = Pt(11)
        p1.font.color.rgb = C_NAVY
        p2 = tf_r.add_paragraph()
        p2.text = f"   {res}"
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_GREEN

    # =========================================================================
    # SLIDE 13: Deployment & Demonstration Strategy
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13, C_LIGHT_BG)
    add_header(s13, "Deployment Architecture & Demonstration Strategy")

    # Left: Cloud Deployment
    add_card(s13, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9), C_CARD_BG, C_GOLD)
    tb_l = s13.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "🌐 Live Production Cloud Deployment"
    p.font.name = "Georgia"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = C_NAVY

    cloud_pts = [
        ("Platform:", "Render Web Services PaaS"),
        ("Live URL:", "https://collegecare-ai.onrender.com"),
        ("Production Server:", "Gunicorn WSGI container (4 worker threads)"),
        ("Continuous Integration:", "Automated CI/CD linked to GitHub main branch"),
        ("Cloud Database:", "Google Firebase Cloud Firestore (collegecare-ai)"),
        ("Cloud Auth:", "Google OAuth 2.0 via Firebase Authentication")
    ]
    for k, v in cloud_pts:
        p1 = tf_l.add_paragraph()
        p1.text = f"\n• {k} "
        p1.font.bold = True
        p1.font.size = Pt(11)
        p1.font.color.rgb = C_GOLD
        p2 = tf_l.add_paragraph()
        p2.text = f"   {v}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_TEXT_DARK

    # Right: Local Demonstration Strategy
    add_card(s13, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9), C_CARD_BG, C_GREEN)
    tb_r = s13.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "💻 High-Reliability Local Viva Execution"
    p.font.name = "Georgia"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = C_GREEN

    local_pts = [
        ("Why Local for Viva:", "Zero internet lag, zero venue Wi-Fi dependency, zero cold starts."),
        ("One-Click Launcher:", "Double-click dev.bat or run.bat in project root."),
        ("Command Line:", "python app.py -> http://127.0.0.1:5000"),
        ("Pre-seeded Admin:", "username: 'admin'  |  password: 'admin123'"),
        ("Pre-seeded Student:", "username: 'student'  |  password: 'student123'"),
        ("Hybrid Cloud Sync:", "New grievances lodged locally automatically replicate to Firebase Cloud Firestore in real time!")
    ]
    for k, v in local_pts:
        p1 = tf_r.add_paragraph()
        p1.text = f"\n• {k} "
        p1.font.bold = True
        p1.font.size = Pt(11)
        p1.font.color.rgb = C_GREEN
        p2 = tf_r.add_paragraph()
        p2.text = f"   {v}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 14: Conclusion & Future Scope
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14, C_LIGHT_BG)
    add_header(s14, "Conclusion & Future Roadmap")

    # Left: Conclusion
    add_card(s14, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9), C_CARD_BG, C_GOLD)
    tb_l = s14.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Project Summary & Achievements"
    p.font.name = "Georgia"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = C_NAVY

    c_points = [
        "Replaced manual paper complaint registers with an intelligent, full-stack AI governance portal.",
        "Delivered 93.5% NLP categorization accuracy across 7 campus maintenance domains.",
        "Mitigated critical life-safety hazards through automated objective priority scoring.",
        "Consolidated maintenance backlogs through vector-space Cosine Similarity duplicate clustering.",
        "Flagged chronic equipment breakdown hotspots to prioritize permanent infrastructure overhauls.",
        "Protected student whistleblowers with server-side identity masking and anti-tamper cloud rules."
    ]
    for pt in c_points:
        p_pt = tf_l.add_paragraph()
        p_pt.text = f"\n✓ {pt}"
        p_pt.font.size = Pt(11)
        p_pt.font.color.rgb = C_TEXT_DARK

    # Right: Future Scope
    add_card(s14, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9), C_CARD_BG, C_NAVY)
    tb_r = s14.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Future Scope & Enhancements"
    p.font.name = "Georgia"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = C_NAVY

    f_points = [
        ("Multilingual Indic NLP:", "Support Marathi and Hindi text and speech input for vernacular student demographics."),
        ("Automated Escalation Hierarchy:", "Forward tickets directly to the Principal or Dean if High-priority hazards remain unresolved past 24 hours."),
        ("IoT Sensor Automated Work Orders:", "Connect smart electrical meters and water flow sensors to generate tickets automatically upon equipment failure."),
        ("WhatsApp Chatbot Integration:", "Enable students to lodge grievances and receive resolution updates directly over WhatsApp messaging.")
    ]
    for title, desc in f_points:
        p1 = tf_r.add_paragraph()
        p1.text = f"\n• {title}"
        p1.font.bold = True
        p1.font.size = Pt(11)
        p1.font.color.rgb = C_GOLD
        p2 = tf_r.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 15: Thank You & Q&A / Live Demonstration
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15, C_NAVY)

    # Accent Gold Top Bar
    top_bar15 = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.15))
    top_bar15.fill.solid()
    top_bar15.fill.fore_color.rgb = C_GOLD
    top_bar15.line.fill.background()

    tb_end = s15.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.333), Inches(3.5))
    tf_e = tb_end.text_frame
    tf_e.word_wrap = True

    p_e = tf_e.paragraphs[0]
    p_e.alignment = PP_ALIGN.CENTER
    p_e.text = "Thank You!"
    p_e.font.name = "Georgia"
    p_e.font.bold = True
    p_e.font.size = Pt(54)
    p_e.font.color.rgb = RGBColor(255, 255, 255)

    p_sub = tf_e.add_paragraph()
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.text = "Open for Questions, Evaluation Defense & Live Demonstration"
    p_sub.font.name = "Georgia"
    p_sub.font.size = Pt(22)
    p_sub.font.color.rgb = C_GOLD

    # Live Links Box
    card_links = add_card(s15, Inches(2.5), Inches(4.5), Inches(8.333), Inches(2.0), RGBColor(30, 41, 59), C_GOLD)
    tb_lks = s15.shapes.add_textbox(Inches(2.7), Inches(4.7), Inches(7.933), Inches(1.6))
    tf_lks = tb_lks.text_frame
    tf_lks.word_wrap = True

    p_l1 = tf_lks.paragraphs[0]
    p_l1.alignment = PP_ALIGN.CENTER
    p_l1.text = "🌐 Live Cloud Platform: https://collegecare-ai.onrender.com"
    p_l1.font.bold = True
    p_l1.font.size = Pt(13)
    p_l1.font.color.rgb = RGBColor(255, 255, 255)

    p_l2 = tf_lks.add_paragraph()
    p_l2.alignment = PP_ALIGN.CENTER
    p_l2.text = "💻 Local Execution: http://127.0.0.1:5000  (dev.bat)"
    p_l2.font.bold = True
    p_l2.font.size = Pt(13)
    p_l2.font.color.rgb = C_GOLD

    p_l3 = tf_lks.add_paragraph()
    p_l3.alignment = PP_ALIGN.CENTER
    p_l3.text = "📂 GitHub Repository: https://github.com/shravanithukrul/CollegeComplaintAI"
    p_l3.font.size = Pt(12)
    p_l3.font.color.rgb = RGBColor(203, 213, 225)

    # Save Presentation
    output_filename = "CollegeCare_AI_Presentation.pptx"
    prs.save(output_filename)
    print(f"SUCCESS: PowerPoint saved to {output_filename}")

if __name__ == "__main__":
    create_presentation()
