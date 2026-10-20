import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

# ==============================================================================
# MINIMALIST TYPOGRAPHY & PURE NEUTRAL PALETTE (ZINC / GRAPHITE / STONE)
# ==============================================================================
FONT_PRIMARY = "Helvetica Neue"

HEX_PRIMARY_DARK = "18181B"   # Zinc 900 (Deep Graphite / Charcoal)
HEX_ACCENT_NEUT  = "3F3F46"   # Zinc 700 (Neutral Slate-Graphite Accent)
HEX_BODY_TEXT    = "27272A"   # Zinc 800
HEX_MUTED_TEXT   = "71717A"   # Zinc 500
HEX_BORDER_LIGHT = "E4E4E7"   # Zinc 200 (Neutral Hairline)
HEX_SURFACE_SOFT = "FAFAFA"   # Zinc 50  (Warm Alabaster / Off-White)
HEX_SURFACE_ALT  = "F4F4F5"   # Zinc 100 (Soft Stone)

RGB_DARK   = RGBColor(24, 24, 27)     # #18181B
RGB_ACCENT = RGBColor(63, 63, 70)     # #3F3F46
RGB_BODY   = RGBColor(39, 39, 42)     # #27272A
RGB_MUTED  = RGBColor(113, 113, 122)  # #71717A
RGB_LIGHT  = RGBColor(212, 212, 216)  # #D4D4D8

# ==============================================================================
# DATA: 15 STEPS (100% PASSIVE VOICE, 15 UNIQUE VERBS, ZERO VERB REPETITION)
# ==============================================================================
STEPS_DATA = [
    # PHASE 01: ARCHITECTURE, CLOUD & SECURITY
    {
        "num": "01",
        "phase": 1,
        "title": "Ergonomic UI Conceptualization",
        "base_verb": "design",
        "participle": "designed",
        "passive_phrase": "was designed",
        "pre_text": "The mobile user interface ",
        "post_text": " with extra-large 56-dp buttons and high-contrast cards as a zero-error selling point for senior patients and families.",
        "sales_pitch": "Stress-free daily navigation and zero accidental taps for any age group.",
        "tech_tag": "UX/UI  ·  56-dp Touch Targets",
    },
    {
        "num": "02",
        "phase": 1,
        "title": "Cloud Server Containerization",
        "base_verb": "deploy",
        "participle": "deployed",
        "passive_phrase": "were deployed",
        "pre_text": "The core backend microservices ",
        "post_text": " inside modular Docker Compose containers for uninterrupted 24/7 clinical availability to every subscriber.",
        "sales_pitch": "Rock-solid 24/7 uptime without unexpected service interruptions.",
        "tech_tag": "Docker Compose  ·  Microservices",
    },
    {
        "num": "03",
        "phase": 1,
        "title": "Relational Database Modeling",
        "base_verb": "structure",
        "participle": "structured",
        "passive_phrase": "was structured",
        "pre_text": "A primary MySQL relational database ",
        "post_text": " under a strict entity-relationship model for safe storage of customer profiles, prescriptions, and schedules.",
        "sales_pitch": "Hospital-grade organization for an entire family's medical records.",
        "tech_tag": "MySQL 8.4  ·  E-R Schema",
    },
    {
        "num": "04",
        "phase": 1,
        "title": "Diagnostic Telemetry Integration",
        "base_verb": "integrate",
        "participle": "integrated",
        "passive_phrase": "was integrated",
        "pre_text": "A secondary MongoDB document engine ",
        "post_text": " into the server architecture for real-time diagnostic logging and commercial platform stability.",
        "sales_pitch": "Proactive technical quality control and transparent app reliability.",
        "tech_tag": "MongoDB 7  ·  Telemetry Logs",
    },
    {
        "num": "05",
        "phase": 1,
        "title": "Cryptographic Data Protection",
        "base_verb": "encrypt",
        "participle": "encrypted",
        "passive_phrase": "were encrypted",
        "pre_text": "All personal passwords and session tokens ",
        "post_text": " with bcrypt hashing and JSON Web Tokens (JWT) for bank-level medical privacy.",
        "sales_pitch": "Total cybersecurity and strict confidentiality for sensitive health data.",
        "tech_tag": "Bcrypt Hashing  ·  JWT Auth",
    },

    # PHASE 02: SMART BACKEND & CLINICAL PRECISION
    {
        "num": "06",
        "phase": 2,
        "title": "High-Speed API Engineering",
        "base_verb": "program",
        "participle": "programmed",
        "passive_phrase": "was programmed",
        "pre_text": "A high-speed RESTful API ",
        "post_text": " in Python with FastAPI for instant data synchronization between the cloud server and the buyer's smartphone.",
        "sales_pitch": "Instant screen updates and ultra-fast response times on mobile.",
        "tech_tag": "Python  ·  FastAPI REST",
    },
    {
        "num": "07",
        "phase": 2,
        "title": "Universal Timezone Calculation",
        "base_verb": "calculate",
        "participle": "calculated",
        "passive_phrase": "were calculated",
        "pre_text": "Exact daily intake timestamps ",
        "post_text": " automatically in Universal Coordinated Time (UTC) by the backend for effortless local timezone conversion.",
        "sales_pitch": "Zero manual clock math with automatic schedule precision during travel.",
        "tech_tag": "UTC Timestamps  ·  Auto-Sync",
    },
    {
        "num": "08",
        "phase": 2,
        "title": "Digital Medicine Cabinet Setup",
        "base_verb": "catalog",
        "participle": "cataloged",
        "passive_phrase": "were cataloged",
        "pre_text": "Tablets, oral drops, and injectable treatments ",
        "post_text": " inside a digital inventory with one-tap dosage chips (500 mg, 10 ml) for rapid consumer onboarding.",
        "sales_pitch": "A complete home pharmacy organized inside your pocket in seconds.",
        "tech_tag": "CRUD Catalog  ·  Dosage Chips",
    },
    {
        "num": "09",
        "phase": 2,
        "title": "Safe Snooze Limit Enforcement",
        "base_verb": "restrict",
        "participle": "restricted",
        "passive_phrase": "was restricted",
        "pre_text": "Alarm postponement ",
        "post_text": " by our clinical rules to a maximum of two 30-minute intervals as a smart safeguard against overdue medication.",
        "sales_pitch": "Built-in medical discipline against treatment delays and double-dosing.",
        "tech_tag": "Max 2x Snooze  ·  30-Min Rule",
    },
    {
        "num": "10",
        "phase": 2,
        "title": "Medical-Legal Audit Logging",
        "base_verb": "record",
        "participle": "recorded",
        "passive_phrase": "was recorded",
        "pre_text": "Every single dose status ",
        "post_text": " with a precise medical-legal timestamp inside an immutable audit history for transparent doctor consultations.",
        "sales_pitch": "Verifiable, accurate adherence history ready for your physician.",
        "tech_tag": "Audit Trail  ·  Compliance Log",
    },

    # PHASE 03: MOBILE EXPERIENCE & AI MARKET VALUE
    {
        "num": "11",
        "phase": 3,
        "title": "Native Android App Construction",
        "base_verb": "build",
        "participle": "built",
        "passive_phrase": "was built",
        "pre_text": "The native Android application ",
        "post_text": " in Kotlin with Jetpack Compose and the MVVM pattern for smooth animations and low battery consumption.",
        "sales_pitch": "Modern, fluid mobile experience with minimal battery drain.",
        "tech_tag": "Kotlin  ·  Jetpack Compose MVVM",
    },
    {
        "num": "12",
        "phase": 3,
        "title": "Anti-Double-Tap Touch Safeguard",
        "base_verb": "disable",
        "participle": "disabled",
        "passive_phrase": "were disabled",
        "pre_text": "Interactive confirmation buttons ",
        "post_text": " automatically during active network calls as a physical touch protection against duplicate entries.",
        "sales_pitch": "Foolproof touch protection for users with tremors or visual fatigue.",
        "tech_tag": "UI State Lock  ·  Zero Double-Tap",
    },
    {
        "num": "13",
        "phase": 3,
        "title": "Offline Local Alarm Scheduling",
        "base_verb": "trigger",
        "participle": "triggered",
        "passive_phrase": "were triggered",
        "pre_text": "Punctual acoustic notifications ",
        "post_text": " locally through Android's native AlarmManager for 100% offline reliability without Wi-Fi or mobile data.",
        "sales_pitch": "100% dependable reminders anywhere—even offline or on airplanes.",
        "tech_tag": "AlarmManager  ·  100% Offline",
    },
    {
        "num": "14",
        "phase": 3,
        "title": "Preventive Refill Alert System",
        "base_verb": "notify",
        "participle": "notified",
        "passive_phrase": "was notified",
        "pre_text": "The end user ",
        "post_text": " by preventive stock warnings below 20% of box capacity for timely pharmacy refills.",
        "sales_pitch": "Smart supply warnings before critical prescription depletion.",
        "tech_tag": "Stock Threshold  ·  Refill Alerts",
    },
    {
        "num": "15",
        "phase": 3,
        "title": "Algorithmic State Optimization",
        "base_verb": "analyze",
        "participle": "analyzed",
        "passive_phrase": "were analyzed",
        "pre_text": "Reminder lifecycle paths ",
        "post_text": " through Depth-First Search (DFS) and heuristic graph algorithms for conflict-free daily treatment routines.",
        "sales_pitch": "Mathematical precision and scientific peace of mind for every patient.",
        "tech_tag": "DFS  ·  Heuristic Graph Search",
    },
]


def load_minimal_font(size, bold=False):
    candidates = [
        ("/System/Library/Fonts/HelveticaNeue.ttc", 1 if bold else 0),
        ("/System/Library/Fonts/Helvetica.ttc", 1 if bold else 0),
        ("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf", 0),
    ]
    for path, index in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size, index=index)
            except Exception:
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    pass
    return ImageFont.load_default()


def generate_visual_assets(screenshots_dir, out_assets_dir):
    os.makedirs(out_assets_dir, exist_ok=True)

    # --------------------------------------------------------------------------
    # 1. COMPACT NEUTRAL PRODUCT SHOWCASE (2100 x 440)
    # --------------------------------------------------------------------------
    banner_w, banner_h = 2100, 440
    banner = Image.new("RGB", (banner_w, banner_h), (250, 250, 250))  # #FAFAFA
    draw = ImageDraw.Draw(banner)

    draw.rectangle([0, 0, banner_w - 1, banner_h - 1], outline=(228, 228, 231), width=3)
    draw.rectangle([0, 0, banner_w, 6], fill=(24, 24, 27))

    f_kicker = load_minimal_font(16, bold=True)
    f_title = load_minimal_font(24, bold=True)
    f_cap = load_minimal_font(18, bold=True)
    f_tag = load_minimal_font(15, bold=False)

    draw.text((40, 16), "PRODUCT INTERFACE ARCHITECTURE", fill=(113, 113, 122), font=f_kicker)
    draw.text((40, 38), "Five Core Mobile Views Engineered for Consumer Simplicity & Clinical Trust", fill=(24, 24, 27), font=f_title)

    screens = [
        ("01_login.png", "01 / Authentication", "Bcrypt & JWT Security (Step 05)"),
        ("02_hoy.png", "02 / Daily Regimen", "UTC & Offline Alarms (Steps 07, 13)"),
        ("03_nuevo_medicamento.png", "03 / Rx Onboarding", "56-dp Ergonomic UI (Steps 01, 08)"),
        ("04_botiquin.png", "04 / Stock Control", "20% Refill Warnings (Step 14)"),
        ("05_analisis_dfs.png", "05 / Graph Engine", "DFS State Verification (Step 15)"),
    ]

    card_w = 384
    card_h = 342
    start_x = 40
    gap = 25
    top_y = 78

    for idx, (fname, label, sublabel) in enumerate(screens):
        x = start_x + idx * (card_w + gap)
        y = top_y

        draw.rounded_rectangle([x, y, x + card_w, y + card_h], radius=8, fill=(255, 255, 255), outline=(228, 228, 231), width=2)
        draw.text((x + 20, y + 12), label, fill=(24, 24, 27), font=f_cap)
        draw.text((x + 20, y + 35), sublabel, fill=(113, 113, 122), font=f_tag)
        draw.line([(x + 20, y + 58), (x + card_w - 20, y + 58)], fill=(244, 244, 245), width=2)

        img_path = os.path.join(screenshots_dir, fname)
        if os.path.exists(img_path):
            im = Image.open(img_path).convert("RGB")
            im = ImageEnhance.Color(im).enhance(0.15)
            target_h = 262
            ratio = target_h / im.height
            target_w = int(im.width * ratio)
            im_resized = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
            paste_x = x + (card_w - target_w) // 2
            paste_y = y + 68
            draw.rounded_rectangle(
                [paste_x - 2, paste_y - 2, paste_x + target_w + 2, paste_y + target_h + 2],
                radius=6,
                outline=(212, 212, 216),
                width=2,
            )
            banner.paste(im_resized, (paste_x, paste_y))

    showcase_path = os.path.join(out_assets_dir, "showcase_banner.png")
    banner.save(showcase_path, dpi=(300, 300))

    # --------------------------------------------------------------------------
    # 2. COMPACT NEUTRAL 3-STAGE PIPELINE DIAGRAM (2100 x 160)
    # --------------------------------------------------------------------------
    flow_w, flow_h = 2100, 160
    flow = Image.new("RGB", (flow_w, flow_h), (255, 255, 255))
    fdraw = ImageDraw.Draw(flow)

    stages = [
        ("PHASE 01  ·  STEPS 01–05", "FOUNDATION & SECURITY", "Verbs: designed, deployed, structured, integrated, encrypted", "Focus: Consumer Trust & Privacy"),
        ("PHASE 02  ·  STEPS 06–10", "BACKEND & CLINICAL LOGIC", "Verbs: programmed, calculated, cataloged, restricted, recorded", "Focus: Automated Precision"),
        ("PHASE 03  ·  STEPS 11–15", "MOBILE UX & AI GRAPH SEARCH", "Verbs: built, disabled, triggered, notified, analyzed", "Focus: Offline & AI Reliability"),
    ]

    box_w = 668
    box_h = 144
    for i, (p_lbl, p_main, p_verbs, p_pitch) in enumerate(stages):
        bx = 12 + i * (box_w + 36)
        by = 8
        fdraw.rounded_rectangle([bx, by, bx + box_w, by + box_h], radius=8, fill=(250, 250, 250), outline=(212, 212, 216), width=2)
        fdraw.rounded_rectangle([bx, by, bx + 7, by + box_h], radius=3, fill=(39, 39, 42))

        fdraw.text((bx + 24, by + 10), p_lbl, fill=(113, 113, 122), font=load_minimal_font(15, bold=True))
        fdraw.text((bx + 24, by + 32), p_main, fill=(24, 24, 27), font=load_minimal_font(20, bold=True))
        fdraw.line([(bx + 24, by + 58), (bx + box_w - 24, by + 58)], fill=(228, 228, 231), width=2)
        fdraw.text((bx + 24, by + 68), p_verbs, fill=(82, 82, 91), font=load_minimal_font(16, bold=False))
        fdraw.text((bx + 24, by + 108), p_pitch, fill=(24, 24, 27), font=load_minimal_font(17, bold=True))

        if i < 2:
            ax = bx + box_w + 9
            ay = by + box_h // 2
            fdraw.line([(ax, ay), (ax + 18, ay)], fill=(161, 161, 170), width=3)
            fdraw.line([(ax + 10, ay - 7), (ax + 18, ay), (ax + 10, ay + 7)], fill=(161, 161, 170), width=3)

    flow_path = os.path.join(out_assets_dir, "pipeline_flow.png")
    flow.save(flow_path, dpi=(300, 300))

    return showcase_path, flow_path


# ==============================================================================
# DOCX XML HELPERS
# ==============================================================================
def configure_modern_word_settings(doc):
    """Eliminates 'Modo de compatibilidad' (sets Word 2016+ mode 15) and hides spell/grammar squiggles."""
    settings = doc.settings.element
    compat = settings.find(qn("w:compat"))
    if compat is None:
        compat = OxmlElement("w:compat")
        settings.append(compat)
    else:
        for child in list(compat):
            if child.get(qn("w:name")) == "compatibilityMode":
                compat.remove(child)

    compat_setting = parse_xml(
        f'<w:compatSetting {nsdecls("w")} w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>'
    )
    compat.append(compat_setting)

    if settings.find(qn("w:hideSpellingErrors")) is None:
        settings.append(parse_xml(f'<w:hideSpellingErrors {nsdecls("w")}/>'))
    if settings.find(qn("w:hideGrammaticalErrors")) is None:
        settings.append(parse_xml(f'<w:hideGrammaticalErrors {nsdecls("w")}/>'))


def force_table_col_widths(table, col_widths_inches):
    """Forces 100% exact table and cell widths in Word."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    total_dxa = int(sum(col_widths_inches) * 1440)
    tblPr = table._tbl.tblPr
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is not None:
        tblPr.remove(tblW)
    tblPr.append(parse_xml(f'<w:tblW {nsdecls("w")} w:w="{total_dxa}" w:type="dxa"/>'))

    tblLayout = tblPr.find(qn("w:tblLayout"))
    if tblLayout is not None:
        tblPr.remove(tblLayout)
    tblPr.append(parse_xml(f'<w:tblLayout {nsdecls("w")} w:type="fixed"/>'))

    tblGrid = table._tbl.find(qn("w:tblGrid"))
    if tblGrid is not None:
        table._tbl.remove(tblGrid)
    new_grid = OxmlElement("w:tblGrid")
    for w_in in col_widths_inches:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(int(w_in * 1440)))
        new_grid.append(gc)
    table._tbl.insert(1, new_grid)

    for row in table.rows:
        for i, w_in in enumerate(col_widths_inches):
            cell = row.cells[i]
            cell.width = Inches(w_in)


def set_explicit_cell_dxa(cell, width_inches):
    tcPr = cell._tc.get_or_add_tcPr()
    tcW = tcPr.find(qn("w:tcW"))
    if tcW is not None:
        tcPr.remove(tcW)
    tcPr.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{int(width_inches * 1440)}" w:type="dxa"/>'))


def add_micro_spacer(doc, pt_size=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    p.paragraph_format.line_spacing = Pt(pt_size)
    r = p.add_run()
    r.font.size = Pt(1)
    return p


def set_cell_margins(cell, top=50, bottom=50, left=95, right=95):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = tcPr.find(qn("w:tcMar"))
    if tcMar is not None:
        tcPr.remove(tcMar)
    tcMar = OxmlElement("w:tcMar")
    for m, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = tcPr.find(qn("w:shd"))
    if shd is not None:
        tcPr.remove(shd)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)


def set_minimal_card_borders(cell, left_accent_hex=HEX_ACCENT_NEUT, border_color=HEX_BORDER_LIGHT):
    tcPr = cell._tc.get_or_add_tcPr()
    old_b = tcPr.find(qn("w:tcBorders"))
    if old_b is not None:
        tcPr.remove(old_b)
    borders = parse_xml(
        f"""
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
            <w:left w:val="single" w:sz="16" w:space="0" w:color="{left_accent_hex}"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
        </w:tcBorders>
    """
    )
    tcPr.append(borders)


def set_hairline_box_borders(cell, border_color=HEX_BORDER_LIGHT, bottom_accent=None):
    b_col = bottom_accent if bottom_accent else border_color
    b_sz = "10" if bottom_accent else "4"
    tcPr = cell._tc.get_or_add_tcPr()
    old_b = tcPr.find(qn("w:tcBorders"))
    if old_b is not None:
        tcPr.remove(old_b)
    borders = parse_xml(
        f"""
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
            <w:left w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
            <w:bottom w:val="single" w:sz="{b_sz}" w:space="0" w:color="{b_col}"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
        </w:tcBorders>
    """
    )
    tcPr.append(borders)


def set_minimal_table_borders(table, border_color=HEX_BORDER_LIGHT):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f"""
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="8" w:space="0" w:color="{HEX_PRIMARY_DARK}"/>
            <w:bottom w:val="single" w:sz="8" w:space="0" w:color="{HEX_PRIMARY_DARK}"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
            <w:insideV w:val="none"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tblBorders>
    """
    )
    tblPr.append(borders)


def prevent_row_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))


def populate_step_cell(cell, step):
    set_cell_background(cell, "FFFFFF")
    set_minimal_card_borders(cell, left_accent_hex=HEX_ACCENT_NEUT, border_color=HEX_BORDER_LIGHT)
    set_cell_margins(cell, top=50, bottom=50, left=95, right=90)

    # Line 1: STEP NUMBER + TITLE
    p1 = cell.paragraphs[0]
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(1.5)
    p1.paragraph_format.line_spacing = 1.04

    r_num = p1.add_run(f"STEP {step['num']}   ")
    r_num.bold = True
    r_num.font.name = FONT_PRIMARY
    r_num.font.size = Pt(8.5)
    r_num.font.color.rgb = RGB_MUTED

    r_title = p1.add_run(step["title"])
    r_title.bold = True
    r_title.font.name = FONT_PRIMARY
    r_title.font.size = Pt(9.5)
    r_title.font.color.rgb = RGB_DARK

    # Line 2: GRAMMAR & STACK METADATA
    p2 = cell.add_paragraph()
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(2)
    p2.paragraph_format.line_spacing = 1.04

    r_verb_badge = p2.add_run(f"PASSIVE VERB #{step['num']}: {step['passive_phrase'].upper()} (to {step['base_verb']})")
    r_verb_badge.bold = True
    r_verb_badge.font.name = FONT_PRIMARY
    r_verb_badge.font.size = Pt(7)
    r_verb_badge.font.color.rgb = RGB_ACCENT

    r_tech = p2.add_run(f"   |   {step['tech_tag']}")
    r_tech.font.name = FONT_PRIMARY
    r_tech.font.size = Pt(7)
    r_tech.font.color.rgb = RGB_MUTED

    # Line 3: MAIN PASSIVE VOICE SENTENCE
    p3 = cell.add_paragraph()
    p3.paragraph_format.space_before = Pt(0)
    p3.paragraph_format.space_after = Pt(2.5)
    p3.paragraph_format.line_spacing = 1.08

    r_pre = p3.add_run(step["pre_text"])
    r_pre.font.name = FONT_PRIMARY
    r_pre.font.size = Pt(8.5)
    r_pre.font.color.rgb = RGB_BODY

    r_pas = p3.add_run(step["passive_phrase"])
    r_pas.bold = True
    r_pas.underline = True
    r_pas.font.name = FONT_PRIMARY
    r_pas.font.size = Pt(8.5)
    r_pas.font.color.rgb = RGB_DARK

    r_post = p3.add_run(step["post_text"])
    r_post.font.name = FONT_PRIMARY
    r_post.font.size = Pt(8.5)
    r_post.font.color.rgb = RGB_BODY

    # Line 4: COMMERCIAL VALUE
    p4 = cell.add_paragraph()
    p4.paragraph_format.space_before = Pt(0)
    p4.paragraph_format.space_after = Pt(0)
    p4.paragraph_format.line_spacing = 1.04

    r_slbl = p4.add_run("COMMERCIAL VALUE — ")
    r_slbl.bold = True
    r_slbl.font.name = FONT_PRIMARY
    r_slbl.font.size = Pt(7.5)
    r_slbl.font.color.rgb = RGB_DARK

    r_stxt = p4.add_run(step["sales_pitch"])
    r_stxt.font.name = FONT_PRIMARY
    r_stxt.font.size = Pt(7.5)
    r_stxt.font.color.rgb = RGB_MUTED


def add_unified_phase_block(doc, phase_code, phase_title, phase_sub, phase_steps):
    """
    Renders an entire 5-step Phase inside a SINGLE unified 2-column table:
    - Row 0: Phase Banner (merged across both columns)
    - Row 1: Step A | Step B
    - Row 2: Step C | Step D
    - Row 3: Step E (merged across both columns)
    This guarantees 100% identical outer alignment and zero stray page breaks!
    """
    tbl = doc.add_table(rows=4, cols=2)
    force_table_col_widths(tbl, [3.65, 3.65])
    for r in tbl.rows:
        prevent_row_split(r)

    # Row 0: Merged Phase Header
    c_hdr = tbl.cell(0, 0).merge(tbl.cell(0, 1))
    set_explicit_cell_dxa(c_hdr, 7.30)
    set_cell_background(c_hdr, HEX_SURFACE_ALT)
    set_hairline_box_borders(c_hdr, border_color=HEX_BORDER_LIGHT, bottom_accent=HEX_PRIMARY_DARK)
    set_cell_margins(c_hdr, top=45, bottom=45, left=95, right=95)

    p = c_hdr.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.keep_with_next = True

    r0 = p.add_run(f"{phase_code}   /   ")
    r0.bold = True
    r0.font.name = FONT_PRIMARY
    r0.font.size = Pt(8.5)
    r0.font.color.rgb = RGB_MUTED

    r1 = p.add_run(phase_title)
    r1.bold = True
    r1.font.name = FONT_PRIMARY
    r1.font.size = Pt(9)
    r1.font.color.rgb = RGB_DARK

    r2 = p.add_run(f"   —   {phase_sub}")
    r2.font.name = FONT_PRIMARY
    r2.font.size = Pt(8)
    r2.font.color.rgb = RGB_MUTED

    # Row 1: Step 0 & Step 1
    populate_step_cell(tbl.cell(1, 0), phase_steps[0])
    populate_step_cell(tbl.cell(1, 1), phase_steps[1])
    set_explicit_cell_dxa(tbl.cell(1, 0), 3.65)
    set_explicit_cell_dxa(tbl.cell(1, 1), 3.65)

    # Row 2: Step 2 & Step 3
    populate_step_cell(tbl.cell(2, 0), phase_steps[2])
    populate_step_cell(tbl.cell(2, 1), phase_steps[3])
    set_explicit_cell_dxa(tbl.cell(2, 0), 3.65)
    set_explicit_cell_dxa(tbl.cell(2, 1), 3.65)

    # Row 3: Merged Step 4 (5th step in phase)
    c_last = tbl.cell(3, 0).merge(tbl.cell(3, 1))
    populate_step_cell(c_last, phase_steps[4])
    set_explicit_cell_dxa(c_last, 7.30)


def build_infographic_docx(showcase_path, flow_path, out_docx_path):
    doc = Document()
    configure_modern_word_settings(doc)

    style_normal = doc.styles["Normal"]
    style_normal.font.name = FONT_PRIMARY
    style_normal.font.size = Pt(8.5)
    style_normal.font.color.rgb = RGB_BODY
    rPr = style_normal.element.get_or_add_rPr()
    rPr.append(parse_xml(f'<w:lang {nsdecls("w")} w:val="en-US" w:eastAsia="en-US" w:bidi="en-US"/>'))

    for s in doc.sections:
        s.page_width = Inches(8.5)
        s.page_height = Inches(11.0)
        s.top_margin = Inches(0.42)
        s.bottom_margin = Inches(0.42)
        s.left_margin = Inches(0.60)
        s.right_margin = Inches(0.60)

        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hr = hp.add_run("MEDREMINDER AI   /   15-STEP DEVELOPMENT & CONSUMER SALES INFOGRAPHIC")
        hr.font.name = FONT_PRIMARY
        hr.font.size = Pt(7.5)
        hr.font.color.rgb = RGB_MUTED

        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        fr1 = fp.add_run("English Coursework  ·  15 Unique Passive Verbs  ·  Page ")
        fr1.font.name = FONT_PRIMARY
        fr1.font.size = Pt(7.5)
        fr1.font.color.rgb = RGB_MUTED
        fp._p.append(parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls("w")))
        fr2 = fp.add_run(" of ")
        fr2.font.name = FONT_PRIMARY
        fr2.font.size = Pt(7.5)
        fr2.font.color.rgb = RGB_MUTED
        fp._p.append(parse_xml(r'<w:fldSimple %s w:instr="NUMPAGES"/>' % nsdecls("w")))

    # ==========================================================================
    # UNIFIED HERO + 4-KPI + VISUAL ARCHITECTURE TABLE (4 rows, 100% locked width)
    # ==========================================================================
    tbl_top = doc.add_table(rows=4, cols=4)
    force_table_col_widths(tbl_top, [1.825, 1.825, 1.825, 1.825])
    for r in tbl_top.rows:
        prevent_row_split(r)

    c_hero = tbl_top.cell(0, 0).merge(tbl_top.cell(0, 3))
    set_explicit_cell_dxa(c_hero, 7.30)
    set_cell_background(c_hero, HEX_PRIMARY_DARK)
    set_hairline_box_borders(c_hero, border_color=HEX_PRIMARY_DARK)
    set_cell_margins(c_hero, top=75, bottom=75, left=110, right=110)

    ph1 = c_hero.paragraphs[0]
    ph1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    ph1.paragraph_format.space_before = Pt(0)
    ph1.paragraph_format.space_after = Pt(2)
    rh_kicker = ph1.add_run("PRODUCT ENGINEERING & COMMERCIALIZATION INFOGRAPHIC")
    rh_kicker.bold = True
    rh_kicker.font.name = FONT_PRIMARY
    rh_kicker.font.size = Pt(7.5)
    rh_kicker.font.color.rgb = RGB_LIGHT

    ph2 = c_hero.add_paragraph()
    ph2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    ph2.paragraph_format.space_before = Pt(0)
    ph2.paragraph_format.space_after = Pt(2)
    rh_title = ph2.add_run("How MedReminder AI Was Built & Sold to Consumers")
    rh_title.bold = True
    rh_title.font.name = FONT_PRIMARY
    rh_title.font.size = Pt(15)
    rh_title.font.color.rgb = RGBColor(255, 255, 255)

    ph3 = c_hero.add_paragraph()
    ph3.alignment = WD_ALIGN_PARAGRAPH.LEFT
    ph3.paragraph_format.space_before = Pt(0)
    ph3.paragraph_format.space_after = Pt(0)
    rh_sub = ph3.add_run(
        "A 15-step technical and commercial roadmap written exclusively in the Passive Voice using 15 distinct verbs."
    )
    rh_sub.font.name = FONT_PRIMARY
    rh_sub.font.size = Pt(8.5)
    rh_sub.font.color.rgb = RGB_LIGHT

    kpis = [
        ("15 STEPS", "Sequential Roadmap"),
        ("PASSIVE VOICE", "100% Grammatical Compliance"),
        ("ZERO REPETITION", "15 Unique Action Verbs"),
        ("CONSUMER PITCH", "Accessible Technical Value"),
    ]
    for idx, (k_big, k_sm) in enumerate(kpis):
        ck = tbl_top.cell(1, idx)
        set_explicit_cell_dxa(ck, 1.825)
        set_cell_background(ck, HEX_SURFACE_SOFT)
        set_hairline_box_borders(ck, border_color=HEX_BORDER_LIGHT, bottom_accent=HEX_ACCENT_NEUT)
        set_cell_margins(ck, top=40, bottom=40, left=60, right=60)
        pk = ck.paragraphs[0]
        pk.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pk.paragraph_format.space_before = Pt(0)
        pk.paragraph_format.space_after = Pt(0)
        rk1 = pk.add_run(k_big + "\n")
        rk1.bold = True
        rk1.font.name = FONT_PRIMARY
        rk1.font.size = Pt(8)
        rk1.font.color.rgb = RGB_DARK
        rk2 = pk.add_run(k_sm)
        rk2.font.name = FONT_PRIMARY
        rk2.font.size = Pt(7)
        rk2.font.color.rgb = RGB_MUTED

    # Row 2: Neutral Pipeline Flow Image inside unified table
    c_flow = tbl_top.cell(2, 0).merge(tbl_top.cell(2, 3))
    set_explicit_cell_dxa(c_flow, 7.30)
    set_cell_background(c_flow, "FFFFFF")
    set_hairline_box_borders(c_flow, border_color=HEX_BORDER_LIGHT)
    set_cell_margins(c_flow, top=30, bottom=20, left=20, right=20)
    p_flow = c_flow.paragraphs[0]
    p_flow.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_flow.paragraph_format.space_before = Pt(0)
    p_flow.paragraph_format.space_after = Pt(0)
    if os.path.exists(flow_path):
        p_flow.add_run().add_picture(flow_path, width=Inches(7.15))

    # Row 3: Neutral App Showcase Banner inside unified table
    c_show = tbl_top.cell(3, 0).merge(tbl_top.cell(3, 3))
    set_explicit_cell_dxa(c_show, 7.30)
    set_cell_background(c_show, "FFFFFF")
    set_hairline_box_borders(c_show, border_color=HEX_BORDER_LIGHT)
    set_cell_margins(c_show, top=20, bottom=30, left=20, right=20)
    p_show = c_show.paragraphs[0]
    p_show.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_show.paragraph_format.space_before = Pt(0)
    p_show.paragraph_format.space_after = Pt(0)
    if os.path.exists(showcase_path):
        p_show.add_run().add_picture(showcase_path, width=Inches(7.15))

    add_micro_spacer(doc, pt_size=5)

    # ==========================================================================
    # PHASE 01, PHASE 02, PHASE 03 (UNIFIED TABLES — ZERO MANUAL PAGE BREAKS!)
    # ==========================================================================
    p1_steps = [s for s in STEPS_DATA if s["phase"] == 1]
    add_unified_phase_block(
        doc,
        "PHASE 01",
        "ARCHITECTURE, CLOUD & DATA SECURITY (STEPS 01–05)",
        "Establishing Consumer Trust, Privacy & 24/7 Availability",
        p1_steps,
    )

    add_micro_spacer(doc, pt_size=6)

    p2_steps = [s for s in STEPS_DATA if s["phase"] == 2]
    add_unified_phase_block(
        doc,
        "PHASE 02",
        "SMART BACKEND & CLINICAL PRECISION (STEPS 06–10)",
        "Delivering Speed, Automated Schedules & Medical-Legal Accuracy",
        p2_steps,
    )

    add_micro_spacer(doc, pt_size=6)

    p3_steps = [s for s in STEPS_DATA if s["phase"] == 3]
    add_unified_phase_block(
        doc,
        "PHASE 03",
        "NATIVE ANDROID UX, OFFLINE ALARMS & AI GRAPH SEARCH (STEPS 11–15)",
        "Closing the Consumer Sale with Offline Dependability & Preventive Alerts",
        p3_steps,
    )

    add_micro_spacer(doc, pt_size=8)

    # ==========================================================================
    # UNIFIED GRAMMAR VERIFICATION MATRIX + EXECUTIVE SYNTHESIS TABLE
    # ==========================================================================
    tbl_audit = doc.add_table(rows=18, cols=5)
    force_table_col_widths(tbl_audit, [0.70, 1.15, 1.25, 1.50, 2.70])
    set_minimal_table_borders(tbl_audit)
    for r in tbl_audit.rows:
        prevent_row_split(r)

    # Row 0: Merged Index Banner
    c_idx = tbl_audit.cell(0, 0).merge(tbl_audit.cell(0, 4))
    set_explicit_cell_dxa(c_idx, 7.30)
    set_cell_background(c_idx, HEX_SURFACE_ALT)
    set_hairline_box_borders(c_idx, border_color=HEX_BORDER_LIGHT, bottom_accent=HEX_PRIMARY_DARK)
    set_cell_margins(c_idx, top=45, bottom=45, left=95, right=95)
    pi = c_idx.paragraphs[0]
    pi.paragraph_format.space_before = Pt(0)
    pi.paragraph_format.space_after = Pt(0)
    pi.paragraph_format.keep_with_next = True
    ri0 = pi.add_run("INDEX   /   ")
    ri0.bold = True
    ri0.font.name = FONT_PRIMARY
    ri0.font.size = Pt(8.5)
    ri0.font.color.rgb = RGB_MUTED
    ri1 = pi.add_run("GRAMMAR VERIFICATION MATRIX: 15 UNIQUE VERBS IN PASSIVE VOICE")
    ri1.bold = True
    ri1.font.name = FONT_PRIMARY
    ri1.font.size = Pt(9)
    ri1.font.color.rgb = RGB_DARK
    ri2 = pi.add_run("   —   Audit Reference Confirming Zero Repeated Verbs (be + Past Participle)")
    ri2.font.name = FONT_PRIMARY
    ri2.font.size = Pt(8)
    ri2.font.color.rgb = RGB_MUTED

    # Row 1: Column Headers
    headers = ["STEP", "INFINITIVE VERB", "PAST PARTICIPLE", "PASSIVE STRUCTURE", "TECHNICAL & COMMERCIAL SCOPE"]
    col_w = [0.70, 1.15, 1.25, 1.50, 2.70]
    for c_i, h_text in enumerate(headers):
        cell = tbl_audit.cell(1, c_i)
        set_explicit_cell_dxa(cell, col_w[c_i])
        set_cell_background(cell, HEX_PRIMARY_DARK)
        set_cell_margins(cell, top=50, bottom=50, left=70, right=70)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = FONT_PRIMARY
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)

    # Rows 2..16: The 15 Unique Verbs
    for idx, step in enumerate(STEPS_DATA, start=2):
        row = tbl_audit.rows[idx]
        bg = HEX_SURFACE_SOFT if idx % 2 == 0 else "FFFFFF"
        vals = [
            f"Step {step['num']}",
            f"to {step['base_verb']}",
            step["participle"],
            step["passive_phrase"],
            f"{step['title']}  ({step['tech_tag']})",
        ]
        for c_i, val in enumerate(vals):
            cell = row.cells[c_i]
            set_explicit_cell_dxa(cell, col_w[c_i])
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=38, bottom=38, left=70, right=70)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = FONT_PRIMARY
            r.font.size = Pt(8)
            if c_i in (0, 3):
                r.bold = True
            if c_i == 3:
                r.font.color.rgb = RGB_DARK
            elif c_i == 4:
                r.font.color.rgb = RGB_MUTED
            else:
                r.font.color.rgb = RGB_BODY

    # Row 17: Merged Executive Summary Footer inside same table
    c_sum = tbl_audit.cell(17, 0).merge(tbl_audit.cell(17, 4))
    set_explicit_cell_dxa(c_sum, 7.30)
    set_cell_background(c_sum, HEX_SURFACE_ALT)
    set_minimal_card_borders(c_sum, left_accent_hex=HEX_PRIMARY_DARK, border_color=HEX_BORDER_LIGHT)
    set_cell_margins(c_sum, top=65, bottom=65, left=95, right=95)

    ps = c_sum.paragraphs[0]
    ps.paragraph_format.space_before = Pt(0)
    ps.paragraph_format.space_after = Pt(0)
    ps.paragraph_format.line_spacing = 1.12
    rs1 = ps.add_run("EXECUTIVE COMMERCIAL SYNTHESIS — ")
    rs1.bold = True
    rs1.font.name = FONT_PRIMARY
    rs1.font.size = Pt(8.5)
    rs1.font.color.rgb = RGB_DARK

    rs2 = ps.add_run(
        "MedReminder AI bridges clinical software engineering and everyday consumer usability. Through 56-dp accessible touch targets, Docker-backed 24/7 availability, encrypted JWT privacy, automated UTC calculation, offline native Android alarms, and DFS state-space verification, complex technology is transformed into effortless daily peace of mind."
    )
    rs2.font.name = FONT_PRIMARY
    rs2.font.size = Pt(8.5)
    rs2.font.color.rgb = RGB_BODY

    os.makedirs(os.path.dirname(out_docx_path), exist_ok=True)
    doc.save(out_docx_path)
    print(f"Unified Neutral Minimalist Infographic Word document saved to: {out_docx_path}")


def main():
    screenshots_dir = "/Users/4strob0y/Downloads/MedReminderAI/docs/screenshots"
    dev_screenshots_dir = "/Users/4strob0y/Developer/MedReminderAI/docs/screenshots"
    if os.path.exists(screenshots_dir) and not os.path.exists(dev_screenshots_dir):
        shutil.copytree(screenshots_dir, dev_screenshots_dir)

    assets_dir = "/Users/4strob0y/Developer/MedReminderAI/docs/infographic_assets"
    showcase_path, flow_path = generate_visual_assets(screenshots_dir, assets_dir)

    out_dev = "/Users/4strob0y/Developer/MedReminderAI/docs/MedReminderAI_Infographic_15_Steps_Passive_Voice.docx"
    out_dl = "/Users/4strob0y/Downloads/MedReminderAI/docs/MedReminderAI_Infographic_15_Steps_Passive_Voice.docx"

    build_infographic_docx(showcase_path, flow_path, out_dev)
    shutil.copy2(out_dev, out_dl)
    print(f"Also copied to: {out_dl}")


if __name__ == "__main__":
    main()
