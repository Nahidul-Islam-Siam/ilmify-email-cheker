from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Flowable,
    HRFlowable,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "EMAIL_CHECKER_WIDE_RESEARCH_REPORT.pdf"
REPORT_DATE = "April 2, 2026"
AUTHOR_NAME = "Nahidul Islam Siam"
AUTHOR_ROLE = "Full Stack Developer"
AUTHOR_FB = "https://www.facebook.com/nahidulislam.siam.39"
AUTHOR_GITHUB = "https://github.com/Nahidul-Islam-Siam"


NAVY = colors.HexColor("#0F172A")
SLATE = colors.HexColor("#334155")
MUTED = colors.HexColor("#64748B")
LINE = colors.HexColor("#CBD5E1")
PANEL = colors.HexColor("#F8FAFC")
BLUE = colors.HexColor("#2563EB")
BLUE_SOFT = colors.HexColor("#DBEAFE")
TEAL = colors.HexColor("#0F766E")
TEAL_SOFT = colors.HexColor("#CCFBF1")
GOLD = colors.HexColor("#B45309")
GOLD_SOFT = colors.HexColor("#FEF3C7")
ROSE = colors.HexColor("#BE123C")
ROSE_SOFT = colors.HexColor("#FFE4E6")
GREEN = colors.HexColor("#166534")
GREEN_SOFT = colors.HexColor("#DCFCE7")


SOURCES = [
    (
        "S1",
        "RFC 5322: Internet Message Format",
        "https://datatracker.ietf.org/doc/html/rfc5322",
        "Defines the core addr-spec grammar: local-part@domain.",
    ),
    (
        "S2",
        "RFC 5321: Simple Mail Transfer Protocol",
        "https://datatracker.ietf.org/doc/rfc5321/",
        "Defines SMTP behavior, local-part handling, implicit MX fallback, and recipient-verification caveats.",
    ),
    (
        "S3",
        'RFC 7505: A "Null MX" No Service Resource Record for Domains That Accept No Mail',
        "https://datatracker.ietf.org/doc/html/rfc7505",
        "Defines the MX 0 . pattern that explicitly signals a domain does not accept mail.",
    ),
    (
        "S4",
        "RFC 6531: SMTP Extension for Internationalized Email",
        "https://datatracker.ietf.org/doc/rfc6531/",
        "Defines SMTPUTF8 support for internationalized mailbox addresses.",
    ),
    (
        "S5",
        'MDN: <input type="email">',
        "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/email",
        "Documents browser-level email formatting validation.",
    ),
    (
        "S6",
        "Node.js DNS API",
        "https://nodejs.org/api/dns.html",
        "Documents resolveMx and related DNS lookups used in Node implementations.",
    ),
    (
        "S7",
        "validator.js",
        "https://github.com/validatorjs/validator.js",
        "Documents isEmail and normalizeEmail, including provider-specific normalization options and RFC caveats.",
    ),
    (
        "S8",
        "disposable-email-domains",
        "https://github.com/disposable-email-domains/disposable-email-domains",
        "Maintained public disposable-domain list used by production systems such as PyPI.",
    ),
    (
        "S9",
        "Google Workspace Admin Help: Email sender guidelines",
        "https://support.google.com/a/answer/81126",
        "Current Gmail delivery requirements, including authentication and DNS expectations.",
    ),
]


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            fontName="Helvetica-Bold",
            fontSize=26,
            leading=30,
            textColor=NAVY,
            alignment=TA_LEFT,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReportSubtitle",
            fontName="Helvetica",
            fontSize=12.5,
            leading=18,
            textColor=SLATE,
            spaceAfter=14,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=22,
            textColor=NAVY,
            spaceBefore=8,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubTitle",
            fontName="Helvetica-Bold",
            fontSize=11.5,
            leading=15,
            textColor=NAVY,
            spaceBefore=4,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            fontName="Helvetica",
            fontSize=9.6,
            leading=14,
            textColor=SLATE,
            spaceAfter=7,
        )
    )
    styles.add(ParagraphStyle(name="BodyTight", parent=styles["Body"], spaceAfter=4))
    styles.add(
        ParagraphStyle(
            name="Small",
            fontName="Helvetica",
            fontSize=8.1,
            leading=11,
            textColor=MUTED,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CalloutTitle",
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=13,
            textColor=NAVY,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Source",
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            textColor=SLATE,
            leftIndent=10,
            bulletIndent=0,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CodeBlock",
            fontName="Courier",
            fontSize=8.2,
            leading=11,
            backColor=colors.white,
            borderColor=LINE,
            borderPadding=6,
            borderWidth=0.5,
            borderRadius=4,
            textColor=NAVY,
        )
    )
    return styles


class PipelineGraphic(Flowable):
    def __init__(self, width=170 * mm, height=62 * mm):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw_box(self, c, x, y, w, h, title, subtitle, fill, stroke):
        c.setFillColor(fill)
        c.setStrokeColor(stroke)
        c.roundRect(x, y, w, h, 9, fill=1, stroke=1)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + 8, y + h - 16, title)
        c.setFillColor(SLATE)
        c.setFont("Helvetica", 7.7)
        c.drawString(x + 8, y + h - 29, subtitle)

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(PANEL)
        c.roundRect(0, 0, self.width, self.height, 12, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(10, self.height - 18, "What a modern email checker actually does")

        y = 18
        box_w = 30 * mm
        box_h = 24 * mm
        xs = [6 * mm, 40 * mm, 74 * mm, 108 * mm, 142 * mm]
        steps = [
            ("Normalize", "trim, split, IDNA", BLUE_SOFT, BLUE),
            ("Syntax", "format only", TEAL_SOFT, TEAL),
            ("DNS", "MX, A/AAAA, Null MX", GOLD_SOFT, GOLD),
            ("Policy", "disposable, role, rules", ROSE_SOFT, ROSE),
            ("Verify", "OTP or magic link", GREEN_SOFT, GREEN),
        ]
        for i, (title, subtitle, fill, stroke) in enumerate(steps):
            self.draw_box(c, xs[i], y, box_w, box_h, title, subtitle, fill, stroke)
            if i < len(steps) - 1:
                arrow_x1 = xs[i] + box_w + 2
                arrow_x2 = xs[i + 1] - 2
                arrow_y = y + box_h / 2
                c.setStrokeColor(MUTED)
                c.setLineWidth(1.3)
                c.line(arrow_x1, arrow_y, arrow_x2, arrow_y)
                c.line(arrow_x2 - 4, arrow_y + 3, arrow_x2, arrow_y)
                c.line(arrow_x2 - 4, arrow_y - 3, arrow_x2, arrow_y)

        c.setFillColor(MUTED)
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(
            10,
            6,
            "Synthesis: syntax stops obvious garbage; OTP is what proves inbox control.",
        )
        c.restoreState()


class DNSDecisionGraphic(Flowable):
    def __init__(self, width=170 * mm, height=78 * mm):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def node(self, c, x, y, w, h, title, fill):
        c.setFillColor(fill)
        c.setStrokeColor(LINE)
        c.roundRect(x, y, w, h, 8, fill=1, stroke=1)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 9.2)
        c.drawCentredString(x + w / 2, y + h / 2 - 4, title)

    def arrow(self, c, x1, y1, x2, y2, label=None):
        c.setStrokeColor(SLATE)
        c.setLineWidth(1.2)
        c.line(x1, y1, x2, y2)
        c.line(x2 - 4, y2 + 3, x2, y2)
        c.line(x2 - 4, y2 - 3, x2, y2)
        if label:
            c.setFillColor(MUTED)
            c.setFont("Helvetica", 7.5)
            c.drawString((x1 + x2) / 2 - 12, (y1 + y2) / 2 + 5, label)

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(PANEL)
        c.roundRect(0, 0, self.width, self.height, 12, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(NAVY)
        c.drawString(10, self.height - 18, "DNS mail-route decision flow")

        self.node(c, 54 * mm, 58 * mm, 62 * mm, 12 * mm, "Check domain syntax", BLUE_SOFT)
        self.node(c, 54 * mm, 40 * mm, 62 * mm, 12 * mm, "Query MX records", TEAL_SOFT)
        self.node(c, 12 * mm, 18 * mm, 42 * mm, 12 * mm, "Null MX?", GOLD_SOFT)
        self.node(c, 64 * mm, 18 * mm, 42 * mm, 12 * mm, "Usable MX?", GOLD_SOFT)
        self.node(c, 116 * mm, 18 * mm, 42 * mm, 12 * mm, "A/AAAA fallback", GOLD_SOFT)
        self.node(c, 10 * mm, 2 * mm, 45 * mm, 10 * mm, "invalid for mail", ROSE_SOFT)
        self.node(c, 62 * mm, 2 * mm, 45 * mm, 10 * mm, "mail route exists", GREEN_SOFT)
        self.node(c, 114 * mm, 2 * mm, 45 * mm, 10 * mm, "no mail route", ROSE_SOFT)

        self.arrow(c, 85 * mm, 58 * mm, 85 * mm, 52 * mm)
        self.arrow(c, 85 * mm, 40 * mm, 33 * mm, 30 * mm, "check")
        self.arrow(c, 85 * mm, 40 * mm, 85 * mm, 30 * mm, "MX")
        self.arrow(c, 85 * mm, 40 * mm, 137 * mm, 30 * mm, "if none")
        self.arrow(c, 33 * mm, 18 * mm, 33 * mm, 12 * mm, "yes")
        self.arrow(c, 85 * mm, 18 * mm, 85 * mm, 12 * mm, "yes")
        self.arrow(c, 137 * mm, 18 * mm, 137 * mm, 12 * mm, "none")

        c.setFillColor(MUTED)
        c.setFont("Helvetica-Oblique", 7.8)
        c.drawString(
            10,
            74,
            "RFC 5321 says an empty MX result can still imply delivery via A/AAAA. RFC 7505 adds explicit no-mail signaling.",
        )
        c.restoreState()


class EvidenceGraphic(Flowable):
    def __init__(self, width=170 * mm, height=70 * mm):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw_bar(self, c, y, label, score, bar_color, note):
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(8, y + 5, label)
        c.setFillColor(colors.white)
        c.setStrokeColor(LINE)
        c.roundRect(52, y, 300, 12, 6, fill=1, stroke=1)
        c.setFillColor(bar_color)
        c.roundRect(52, y, 300 * score, 12, 6, fill=1, stroke=0)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 7.5)
        c.drawString(360, y + 3, note)

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(PANEL)
        c.roundRect(0, 0, self.width, self.height, 12, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(10, self.height - 18, "Evidence strength by validation method")

        self.draw_bar(c, 42, "Syntax", 0.25, BLUE, "proves formatting only")
        self.draw_bar(c, 28, "DNS route", 0.55, TEAL, "proves domain can likely receive mail")
        self.draw_bar(c, 14, "SMTP probe", 0.62, GOLD, "probabilistic; provider behavior varies")
        self.draw_bar(c, 0, "OTP / magic link", 0.96, GREEN, "proves user controlled the inbox")

        c.setFillColor(MUTED)
        c.setFont("Helvetica-Oblique", 7.8)
        c.drawString(
            10,
            57,
            "Analyst synthesis: higher confidence methods usually cost more latency or user effort.",
        )
        c.restoreState()


class ArchitectureGraphic(Flowable):
    def __init__(self, width=170 * mm, height=82 * mm):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def card(self, c, x, y, w, h, title, fill, lines):
        c.setFillColor(fill)
        c.setStrokeColor(LINE)
        c.roundRect(x, y, w, h, 8, fill=1, stroke=1)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x + 8, y + h - 14, title)
        c.setFont("Helvetica", 7.4)
        draw_y = y + h - 26
        for line in lines:
            c.setFillColor(SLATE)
            c.drawString(x + 8, draw_y, line)
            draw_y -= 10

    def connect(self, c, x1, y1, x2, y2):
        c.setStrokeColor(MUTED)
        c.setLineWidth(1.1)
        c.line(x1, y1, x2, y2)
        c.line(x2 - 3, y2 + 2, x2, y2)
        c.line(x2 - 3, y2 - 2, x2, y2)

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(PANEL)
        c.roundRect(0, 0, self.width, self.height, 12, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(10, self.height - 18, "Recommended service architecture")

        self.card(c, 8 * mm, 44 * mm, 35 * mm, 18 * mm, "UI", BLUE_SOFT, ["live feedback", "verify prompt"])
        self.card(c, 52 * mm, 44 * mm, 38 * mm, 18 * mm, "Check API", TEAL_SOFT, ["normalize", "syntax", "status JSON"])
        self.card(c, 98 * mm, 44 * mm, 32 * mm, 18 * mm, "DNS layer", GOLD_SOFT, ["MX", "A/AAAA", "Null MX"])
        self.card(c, 136 * mm, 44 * mm, 28 * mm, 18 * mm, "Policy", ROSE_SOFT, ["disposable", "role", "rules"])

        self.card(c, 30 * mm, 12 * mm, 35 * mm, 18 * mm, "Cache + DB", GREEN_SOFT, ["results", "attempts", "verification state"])
        self.card(c, 74 * mm, 12 * mm, 35 * mm, 18 * mm, "Mailer", BLUE_SOFT, ["OTP", "magic link", "templates"])
        self.card(c, 118 * mm, 12 * mm, 35 * mm, 18 * mm, "Queue", TEAL_SOFT, ["async retries", "optional SMTP probe"])

        self.connect(c, 43 * mm, 53 * mm, 52 * mm, 53 * mm)
        self.connect(c, 90 * mm, 53 * mm, 98 * mm, 53 * mm)
        self.connect(c, 130 * mm, 53 * mm, 136 * mm, 53 * mm)
        self.connect(c, 71 * mm, 44 * mm, 48 * mm, 30 * mm)
        self.connect(c, 82 * mm, 44 * mm, 91 * mm, 30 * mm)
        self.connect(c, 116 * mm, 44 * mm, 135 * mm, 30 * mm)

        c.setFillColor(MUTED)
        c.setFont("Helvetica-Oblique", 7.8)
        c.drawString(
            10,
            6,
            "Design principle: keep signup latency on syntax + DNS, and move slower checks to async workflows.",
        )
        c.restoreState()


class RoadmapGraphic(Flowable):
    def __init__(self, width=170 * mm, height=42 * mm):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(PANEL)
        c.roundRect(0, 0, self.width, self.height, 12, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(10, self.height - 18, "Suggested build roadmap")

        phases = [
            ("Phase 1", "Syntax + DNS", BLUE_SOFT, BLUE),
            ("Phase 2", "Disposable + role policy", TEAL_SOFT, TEAL),
            ("Phase 3", "OTP / magic link", GOLD_SOFT, GOLD),
            ("Phase 4", "Async SMTP and risk scoring", ROSE_SOFT, ROSE),
        ]
        x = 10
        y = 8
        for idx, (phase, text, fill, stroke) in enumerate(phases):
            box_w = 120
            box_h = 14
            c.setFillColor(fill)
            c.setStrokeColor(stroke)
            c.roundRect(x, y, box_w, box_h, 7, fill=1, stroke=1)
            c.setFillColor(NAVY)
            c.setFont("Helvetica-Bold", 8.2)
            c.drawString(x + 6, y + 4, phase)
            c.setFont("Helvetica", 8.2)
            c.drawString(x + 40, y + 4, text)
            if idx < len(phases) - 1:
                c.setStrokeColor(MUTED)
                c.line(x + box_w, y + 7, x + box_w + 12, y + 7)
                c.line(x + box_w + 9, y + 9, x + box_w + 12, y + 7)
                c.line(x + box_w + 9, y + 5, x + box_w + 12, y + 7)
            x += 132
        c.restoreState()


def paragraph(text, styles, style_name="Body"):
    return Paragraph(text, styles[style_name])


def bullets(items, styles):
    return ListFlowable(
        [ListItem(Paragraph(item, styles["BodyTight"]), leftIndent=8) for item in items],
        bulletType="bullet",
        bulletFontName="Helvetica",
        bulletFontSize=8,
        leftIndent=15,
    )


def callout(title, body, styles, fill=PANEL, accent=BLUE):
    table = Table(
        [[Paragraph(title, styles["CalloutTitle"])], [Paragraph(body, styles["Body"])]],
        colWidths=[170 * mm],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), fill),
                ("BOX", (0, 0), (-1, -1), 0.7, LINE),
                ("LINEBEFORE", (0, 0), (0, -1), 4, accent),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def author_card(styles):
    fb = f'<link href="{escape(AUTHOR_FB)}" color="blue">{escape(AUTHOR_FB)}</link>'
    github = f'<link href="{escape(AUTHOR_GITHUB)}" color="blue">{escape(AUTHOR_GITHUB)}</link>'
    body = (
        f"<b>Research by {escape(AUTHOR_NAME)}</b><br/>"
        f"{escape(AUTHOR_ROLE)}<br/>"
        f"Facebook: {fb}<br/>"
        f"GitHub: {github}"
    )
    table = Table(
        [
            [Paragraph("Author Branding", styles["CalloutTitle"])],
            [Paragraph(body, styles["Body"])],
        ],
        colWidths=[170 * mm],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PANEL),
                ("BOX", (0, 0), (-1, -1), 0.7, LINE),
                ("LINEBEFORE", (0, 0), (0, -1), 4, GREEN),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def build_cover(styles):
    meta = Table(
        [
            ["Prepared", REPORT_DATE],
            ["Scope", "Protocol standards, DNS and SMTP behavior, product design, deliverability, build strategy"],
            ["Output", "Wide research PDF with original diagrams and implementation guidance"],
        ],
        colWidths=[28 * mm, 130 * mm],
    )
    meta.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PANEL),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("TEXTCOLOR", (0, 0), (-1, -1), SLATE),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    return [
        Spacer(1, 16 * mm),
        Paragraph("Email Checker", styles["ReportTitle"]),
        Paragraph("Wide Research Report", styles["ReportTitle"]),
        Paragraph(
            "How email validation really works, what it can and cannot prove, and what to build first if you want a practical production system.",
            styles["ReportSubtitle"],
        ),
        Spacer(1, 4 * mm),
        PipelineGraphic(),
        Spacer(1, 5 * mm),
        paragraph(
            "Bottom line: the most reliable architecture is layered. Syntax and HTML input validation catch formatting issues. DNS checks establish whether the domain can likely receive mail. Policy checks catch disposable or risky domains. OTP or magic-link verification is what actually proves the user controls the inbox. SMTP probing can add signal, but it should be treated as optional and probabilistic rather than as the foundation of the product. [S1][S2][S3][S5]",
            styles,
        ),
        Spacer(1, 3 * mm),
        meta,
        Spacer(1, 4 * mm),
        callout(
            "Research note",
            "This report uses official standards and primary documentation where possible. Places where the report goes beyond the standards into implementation strategy are explicitly presented as analyst synthesis rather than protocol fact.",
            styles,
            fill=BLUE_SOFT,
            accent=BLUE,
        ),
        Spacer(1, 3 * mm),
        author_card(styles),
        PageBreak(),
    ]


def build_summary(styles):
    comparison = Table(
        [
            ["Method", "What it proves", "Strength", "Primary weakness"],
            ["HTML / regex", "Looks like an email", "Fastest UX filter", "No deliverability proof"],
            ["Syntax library", "Server-side format check", "Reliable baseline guardrail", "Still no mailbox proof"],
            ["DNS route check", "Domain likely accepts mail", "Best low-friction protocol signal", "Cannot prove inbox ownership"],
            ["SMTP probe", "Mailbox may exist", "Sometimes catches dead inboxes", "Provider behavior is inconsistent"],
            ["OTP / magic link", "User controlled the inbox", "Highest confidence", "Adds user friction"],
        ],
        colWidths=[30 * mm, 55 * mm, 42 * mm, 43 * mm],
        repeatRows=1,
    )
    comparison.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.4),
                ("LEADING", (0, 0), (-1, -1), 10.5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PANEL]),
                ("GRID", (0, 0), (-1, -1), 0.45, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    return [
        Paragraph("Executive Summary", styles["SectionTitle"]),
        bullets(
            [
                "An email checker is not one thing. It is a stack of checks that answer different questions at different confidence levels.",
                "RFC 5322 defines the core email shape, while RFC 5321 governs how SMTP systems treat local parts, domains, delivery routing, and recipient handling. [S1][S2]",
                "DNS is the best technical midpoint for an MVP. MX lookup, A or AAAA fallback, and Null MX detection give strong routing signal without SMTP latency or anti-abuse friction. [S2][S3][S6]",
                "SMTP probing is useful only as a secondary signal because servers can refuse VRFY, defer decisions, accept mail for later rejection, or behave like catch-all domains. [S2]",
                "If the product goal is to confirm the user owns the inbox, OTP or magic-link verification is the decisive control. The rest of the checker only narrows risk. [S2][S9]",
                "Teams that send verification emails must think beyond validation. Deliverability now depends on SPF or DKIM for all Gmail-bound senders, and SPF plus DKIM plus DMARC for high-volume Gmail senders, with valid DNS and TLS requirements called out by Google. [S9]",
            ],
            styles,
        ),
        Spacer(1, 3 * mm),
        comparison,
        Spacer(1, 4 * mm),
        EvidenceGraphic(),
        Spacer(1, 3 * mm),
        callout(
            "Decision framing",
            "There are really three different products people call an email checker: a formatter, a deliverability pre-checker, and an ownership verifier. Conflating them leads to incorrect promises in the UI and unnecessary engineering complexity.",
            styles,
            fill=TEAL_SOFT,
            accent=TEAL,
        ),
        PageBreak(),
    ]


def build_deep_dive(styles):
    smtp_table = Table(
        [
            ["SMTP reality", "What it means for your checker"],
            ["252 Cannot VRFY user", "The server will accept mail but will not confirm the recipient in advance."],
            ["VRFY or EXPN disabled", "Many servers deliberately avoid easy recipient enumeration for security reasons."],
            ["Catch-all domains", "RCPT acceptance can look valid even when the mailbox may not exist as an individual account."],
            ["Delayed rejection", "Some systems decide only after message body or internal policy checks, so signup-time probing can mislead."],
        ],
        colWidths=[46 * mm, 124 * mm],
        repeatRows=1,
    )
    smtp_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PANEL]),
                ("GRID", (0, 0), (-1, -1), 0.45, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    sender_table = Table(
        [
            ["Gmail requirement snapshot", "Current official guidance"],
            ["All senders", "Starting February 1, 2024, Gmail requires SPF or DKIM, valid forward and reverse DNS, TLS, RFC 5322 formatting, and acceptable spam rates. [S9]"],
            ["5,000+ messages per day", "Starting February 1, 2024, Gmail additionally requires SPF and DKIM, DMARC, alignment, and one-click unsubscribe for marketing or subscribed messages. [S9]"],
            ["Operational implication", "An email checker that sends OTPs at scale must be paired with solid sender-domain operations, not just address validation logic."],
        ],
        colWidths=[50 * mm, 120 * mm],
        repeatRows=1,
    )
    sender_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PANEL]),
                ("GRID", (0, 0), (-1, -1), 0.45, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    return [
        Paragraph("Standards and Technical Deep Dive", styles["SectionTitle"]),
        Paragraph("1. Syntax and normalization", styles["SubTitle"]),
        paragraph(
            'RFC 5322 defines the core address form as <font name="Courier">local-part@domain</font>. The local part may be more permissive than many developers expect, and RFC 5321 adds an important operational detail: mailbox local parts must be preserved as case-sensitive even though many providers are case-insensitive in practice. [S1][S2]',
            styles,
        ),
        paragraph(
            'This is why practical implementations should avoid home-grown mega-regexes and should be careful with canonicalization. Browser validation via <font name="Courier">input type=email</font> is useful for fast UX, but MDN is clear that it only checks formatting. On the server side, a library such as validator.js provides a safer baseline and exposes normalization options that reflect real provider behavior. The validator.js documentation also warns that lowercasing every local part may violate RFC 5321. [S5][S7]',
            styles,
        ),
        Paragraph("2. DNS routing matters more than most teams think", styles["SubTitle"]),
        paragraph(
            "RFC 5321 specifies the core MX lookup behavior. A domain with usable MX records can likely receive mail through those targets. A less obvious rule is the implicit MX fallback: if an MX lookup returns an empty list, SMTP clients are supposed to treat the address as if it had an implicit MX pointing back to the host itself, then rely on A or AAAA records. That means no MX is not always equivalent to no mail route. [S2]",
            styles,
        ),
        paragraph(
            'RFC 7505 refines this story with Null MX. A domain that publishes a single MX record with preference 0 and exchange "." is explicitly saying that it does not accept mail. That is a much stronger signal than simply not finding MX records. [S3]',
            styles,
        ),
        Spacer(1, 2 * mm),
        DNSDecisionGraphic(),
        Spacer(1, 3 * mm),
        Paragraph("3. Internationalized mailboxes", styles["SubTitle"]),
        paragraph(
            "If you need to support non-ASCII mailbox names or internationalized domains beyond basic IDNA handling, RFC 6531 introduces SMTPUTF8. This matters because some teams assume Unicode email is just a UI problem, when in reality it can change downstream SMTP compatibility and vendor choices. A pragmatic MVP may start with ASCII local parts and IDNA-converted domains, then add SMTPUTF8 if the market requires it. [S4]",
            styles,
        ),
        Paragraph("4. SMTP probing is real, but not decisive", styles["SubTitle"]),
        paragraph(
            "SMTP probing typically uses EHLO, MAIL FROM, and RCPT TO against the domain's chosen mail exchanger. In theory it answers a compelling question: does this mailbox exist? In practice the protocol and modern provider behavior make the answer unreliable. RFC 5321 defines the 252 response as a case where the server will accept mail but will not confirm the recipient in advance, and it allows sites to disable VRFY or EXPN for security reasons rather than reveal valid recipients. [S2]",
            styles,
        ),
        smtp_table,
        Spacer(1, 3 * mm),
        callout(
            "Analyst synthesis",
            "SMTP probing should be treated as a background signal, not as the product's promise to the user. The checker can say deliverable likely or high risk more honestly than it can say mailbox definitely exists.",
            styles,
            fill=GOLD_SOFT,
            accent=GOLD,
        ),
        Spacer(1, 4 * mm),
        Paragraph("5. Disposable domains and policy layers", styles["SubTitle"]),
        paragraph(
            "Temporary or throwaway mail detection is not part of SMTP or RFC syntax. It is a policy choice. Public projects such as disposable-email-domains maintain blocklists specifically for domains that are often used for spam, dummy registrations, or abuse, and the repo notes real production use cases such as PyPI account protection. [S8]",
            styles,
        ),
        paragraph(
            'The same policy layer is where role accounts such as <font name="Courier">admin@</font>, <font name="Courier">info@</font>, or <font name="Courier">support@</font> belong. They are not invalid by protocol, but they may be lower-quality leads or higher-risk registrations depending on the product.',
            styles,
        ),
        Spacer(1, 4 * mm),
        Paragraph("6. Deliverability of your own verification email", styles["SubTitle"]),
        paragraph(
            "Once you choose OTP or magic-link verification, your checker becomes a sender. At that point the engineering problem expands from validation to sender reputation, DNS hygiene, and authentication. Google's current sender guidance is especially important because verification and onboarding flows frequently target Gmail inboxes. [S9]",
            styles,
        ),
        sender_table,
        PageBreak(),
    ]


def build_architecture_section(styles):
    build_buy = Table(
        [
            ["Option", "Best when", "Upside", "Tradeoff"],
            ["Self-built MVP", "You need core validation only", "Low cost, fully controllable, easy to fit to product rules", "You own DNS quirks, sender setup, and ongoing maintenance"],
            ["Self-built + async probe", "You need extra signal but not a vendor dependency", "Can improve ranking and risk scoring", "Higher complexity and false-confidence risk"],
            ["Third-party verification API", "You need speed, vendor data, or enterprise workflows", "Fastest path to broad coverage", "Recurring cost, vendor lock-in, opaque heuristics"],
            ["Hybrid", "You want control on core checks and external enrichment only when needed", "Balanced cost and capability", "Requires thoughtful orchestration"],
        ],
        colWidths=[30 * mm, 45 * mm, 48 * mm, 47 * mm],
        repeatRows=1,
    )
    build_buy.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.4),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PANEL]),
                ("GRID", (0, 0), (-1, -1), 0.45, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    statuses = Preformatted(
        """{
  "normalizedEmail": "user@example.com",
  "status": "deliverable_likely",
  "signals": {
    "syntaxValid": true,
    "domainResolvable": true,
    "mxFound": true,
    "nullMx": false,
    "disposable": false,
    "roleBased": false
  },
  "nextAction": "send_verification_link"
}""",
        styles["CodeBlock"],
    )

    return [
        Paragraph("Implementation Guidance", styles["SectionTitle"]),
        paragraph(
            "For most products, the strongest first milestone is a layered MVP with these responsibilities: client formatting feedback, server-side syntax validation, DNS mail-route checks, disposable-domain and role-account policy checks, and OTP or magic-link verification. Keep SMTP probes out of the signup critical path unless the business case is unusually strong.",
            styles,
        ),
        ArchitectureGraphic(),
        Spacer(1, 3 * mm),
        Paragraph("Recommended API shape", styles["SubTitle"]),
        paragraph(
            'A useful API should return structured states rather than a single boolean. This makes the front end more honest and gives you room to add new checks without changing the contract. Example statuses include <font name="Courier">invalid_syntax</font>, <font name="Courier">null_mx</font>, <font name="Courier">disposable_domain</font>, <font name="Courier">deliverable_likely</font>, and <font name="Courier">verified</font>.',
            styles,
        ),
        statuses,
        Spacer(1, 3 * mm),
        Paragraph("Practical build notes", styles["SubTitle"]),
        bullets(
            [
                'Use <font name="Courier">validator.js</font> or a similarly mature library for server-side validation rather than hand-written regexes. [S7]',
                'In Node.js, <font name="Courier">dns.promises.resolveMx()</font> is the natural MX lookup primitive, and the Node docs show the returned object shape with <font name="Courier">priority</font> and <font name="Courier">exchange</font>. [S6]',
                "Respect DNS uncertainty. Cache results, but do not assume permanent truth from one lookup; mail routing can change.",
                "Treat disposable-domain checks as configurable policy, not immutable protocol truth. False positives are possible, and allowlists matter. [S8]",
                "Protect the endpoint against abuse. Email-checker APIs are attractive for account enumeration and dictionary attacks.",
            ],
            styles,
        ),
        Spacer(1, 3 * mm),
        RoadmapGraphic(),
        Spacer(1, 4 * mm),
        Paragraph("Build vs buy", styles["SubTitle"]),
        paragraph(
            "If the need is straightforward signup validation, a self-built DNS-plus-verification stack is often enough. If the product needs high-volume sales enrichment, bounce forecasting, mailbox scoring, or historical provider reputation data, a third-party verifier can be justified. That is not because the RFC basics are too hard, but because some of the highest-value signals are proprietary and operational rather than purely protocol-based.",
            styles,
        ),
        build_buy,
        Spacer(1, 4 * mm),
        callout(
            "Final recommendation",
            "Build the checker in this order: syntax, DNS route validation, disposable-domain policy, then verification email flow. Add SMTP probing only as an asynchronous enrichment layer. This delivers the best accuracy-to-complexity ratio for most products.",
            styles,
            fill=GREEN_SOFT,
            accent=GREEN,
        ),
        PageBreak(),
    ]


def build_sources(styles):
    story = [
        Paragraph("Source Notes", styles["SectionTitle"]),
        paragraph(
            "All links below were reviewed during report preparation on April 2, 2026. Official standards and vendor documentation can change, so regenerating this report later is the right way to refresh the conclusions.",
            styles,
        ),
    ]

    for code, title, url, note in SOURCES:
        link = f'<link href="{escape(url)}" color="blue">{escape(url)}</link>'
        text = f"<b>{code}.</b> {escape(title)}<br/>{link}<br/>{escape(note)}"
        story.append(Paragraph(text, styles["Source"]))

    story.extend(
        [
            Spacer(1, 4 * mm),
            HRFlowable(width="100%", thickness=0.6, color=LINE),
            Spacer(1, 2 * mm),
            paragraph(
                "Original visuals in this PDF were generated locally for this report and are based on the cited standards and documentation rather than copied screenshots.",
                styles,
                "Small",
            ),
            Spacer(1, 3 * mm),
            author_card(styles),
        ]
    )
    return story


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(doc.pagesize[0] - doc.rightMargin, 12 * mm, f"Page {doc.page}")
    canvas.drawString(
        doc.leftMargin,
        12 * mm,
        f"Research by {AUTHOR_NAME} | {AUTHOR_ROLE}",
    )
    canvas.restoreState()


def build():
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="Email Checker Wide Research Report",
        author=AUTHOR_NAME,
    )

    story = []
    story.extend(build_cover(styles))
    story.extend(build_summary(styles))
    story.extend(build_deep_dive(styles))
    story.extend(build_architecture_section(styles))
    story.extend(build_sources(styles))

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


if __name__ == "__main__":
    build()
    print(f"Generated: {OUTPUT}")
