# -*- coding: utf-8 -*-
"""Gera o PDF do prompt PARA DOWNLOAD (versão que gera a análise em e-book A5).

Fonte: prompt/prompt-analise-a5.md → Saída: downloads/Prompt-Analise-A5.pdf
O prompt COMPLETO (site + complementos) NÃO vira PDF: fica só no repositório
em prompt/PROMPT-COMPLETO-SITE.md, sem download — conforme a divisão de prompts.
Executar a partir da raiz do repositório:  python3 ferramentas/gerar_prompt_pdf.py
"""
from datetime import datetime
from zoneinfo import ZoneInfo
from xml.sax.saxutils import escape
import os, re

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

try:
    import matplotlib, pathlib
    _fd = pathlib.Path(matplotlib.__file__).parent / "mpl-data" / "fonts" / "ttf"
    pdfmetrics.registerFont(TTFont("DVSerif", str(_fd / "DejaVuSerif.ttf")))
    pdfmetrics.registerFont(TTFont("DVSerif-B", str(_fd / "DejaVuSerif-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("DVSerif-I", str(_fd / "DejaVuSerif-Italic.ttf")))
    pdfmetrics.registerFont(TTFont("DVSans", str(_fd / "DejaVuSans.ttf")))
    pdfmetrics.registerFontFamily("DVSerif", normal="DVSerif", bold="DVSerif-B", italic="DVSerif-I", boldItalic="DVSerif-B")
    SERIF, SANS = "DVSerif", "DVSans"
except Exception:
    SERIF, SANS = "Times-Roman", "Helvetica"

TZ = ZoneInfo("America/Sao_Paulo")
agora = datetime.now(TZ)
stamp = agora.strftime("%d/%m/%Y às %H:%M")

FONTE_MD = "prompt/prompt-analise-a5.md"
OUT = "downloads/Prompt-Analise-A5.pdf"

navy = HexColor("#14273d"); gold = HexColor("#b8860b"); cinza = HexColor("#5b6b7b")
sTitulo = ParagraphStyle("t", fontName=SERIF, fontSize=23, leading=28, textColor=navy, alignment=TA_CENTER, spaceAfter=6)
sSub = ParagraphStyle("s", fontName=SERIF, fontSize=11.5, leading=16.5, alignment=TA_CENTER, textColor=cinza, spaceAfter=4)
sH1 = ParagraphStyle("h1", fontName=SERIF, fontSize=13.5, leading=17, textColor=navy, spaceBefore=14, spaceAfter=5, keepWithNext=1)
sH2 = ParagraphStyle("h2", fontName=SERIF, fontSize=11.5, leading=15, textColor=navy, spaceBefore=10, spaceAfter=4, keepWithNext=1)
sCorpo = ParagraphStyle("c", fontName=SERIF, fontSize=10.3, leading=15.2, alignment=TA_JUSTIFY, spaceAfter=6)
sItem = ParagraphStyle("i", parent=sCorpo, leftIndent=12, bulletIndent=3, spaceAfter=3.5, alignment=TA_LEFT)
sCit = ParagraphStyle("q", parent=sCorpo, textColor=cinza, leftIndent=10, rightIndent=10)

def inline(t):
    t = escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\w)\*([^*]+?)\*(?!\w)", r"<i>\1</i>", t)
    t = re.sub(r"`([^`]+)`", r'<font name="%s" size="8.2">\1</font>' % SANS, t)
    return t

def rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont(SANS, 7.2); canvas.setFillColor(cinza)
    canvas.drawCentredString(A4[0]/2, 13*mm, f"Prompt da análise em PDF A5 (download) • Curadoria: by rogerelizar • Montagem por IA (Arena.ai — Agent Mode) • {stamp} (America/Sao_Paulo) • p. {doc.page}")
    canvas.setStrokeColor(gold); canvas.setLineWidth(1.1)
    canvas.line(15*mm, 16*mm, A4[0]-15*mm, 16*mm)
    canvas.restoreState()

md = open(FONTE_MD, encoding="utf-8").read().splitlines()
ini = next(i for i, l in enumerate(md) if l.strip() == "## O PROMPT")
corpo_md = md[ini+1:]

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=18*mm, bottomMargin=20*mm,
                        title="Prompt — Análise Eleitoral em PDF A5 (by rogerelizar)",
                        author="by rogerelizar (curadoria) / Arena.ai — Agent Mode (montagem por IA)")
story = []
story.append(Spacer(1, 20*mm))
story.append(Paragraph("Eleições Presidenciais 2026 · 2º turno", ParagraphStyle("k", parent=sSub, textColor=gold, fontSize=11)))
story.append(Paragraph("Prompt — Análise em PDF A5", sTitulo))
story.append(Paragraph("O prompt que gera <b>toda a análise comparativa como e-book A5 para impressão</b>,<br/>disponibilizado para download e auditoria pública do método.", sSub))
story.append(Spacer(1, 5*mm)); story.append(HRFlowable(width="38%", thickness=1.6, color=gold, hAlign="CENTER")); story.append(Spacer(1, 5*mm))
story.append(Paragraph("<b>Curadoria (forneceu apenas os prompts e os dois PDFs oficiais):</b> by rogerelizar", sSub))
story.append(Paragraph("<b>Pesquisa, redação, gráficos, site, e-book e flipbook:</b> inteligência artificial — Arena.ai (Agent Mode)", sSub))
story.append(Paragraph(f"<b>Esta edição do prompt:</b> {stamp} — horário de São Paulo (America/Sao_Paulo)", sSub))
story.append(Spacer(1, 7*mm))
story.append(Paragraph("Sobre os dois prompts (leia primeiro)", sH1))
story.append(Paragraph("O projeto tem <b>dois prompts</b>. <b>Este</b> (para download) é a versão atualizada que gera <b>somente a análise</b>, com resultado em <b>PDF A5 diagramado para leitura e impressão</b> — incluindo conteúdo, modelagem, capa e a separação tipográfica entre os blocos de cada candidato. O <b>prompt completo</b>, que origina o site interativo inteiro e todos os seus complementos (tela inicial, menu flutuante, estilos visuais, e-book, flipbook e geradores), foi <b>recriado em inglês</b> a partir da versão final e <b>não está disponível para download</b>: fica arquivado somente no repositório do projeto (<i>prompt/PROMPT-COMPLETO-SITE.md</i>), como especificação integral de construção e registro resumido das decisões do curador.", sCorpo))
story.append(Paragraph("<b>Isenção do curador:</b> by rogerelizar limitou-se a formular os prompts e a anexar os programas oficiais registrados no TSE. Não redigiu, não aprovou previamente linha a linha e não endossa necessariamente análises, notas de viabilidade ou alertas jurídico-fiscais produzidos pela IA. Divergências entre o pedido e o resultado devem ser cobradas da montagem — e conferidas sempre nas fontes primárias antes do voto.", sCorpo))
story.append(PageBreak())
story.append(Paragraph("O PROMPT", ParagraphStyle("kk", parent=sH1, alignment=TA_CENTER, fontSize=15, spaceBefore=2)))
story.append(HRFlowable(width="100%", thickness=0.7, color=gold, spaceAfter=6))
for raw in corpo_md:
    l = raw.strip()
    if not l:
        continue
    if l == "---":
        story.append(HRFlowable(width="100%", thickness=0.6, color=cinza, spaceBefore=5, spaceAfter=5)); continue
    if l.startswith("### "):
        story.append(Paragraph(inline(l[4:]), sH1)); continue
    if l.startswith("## "):
        story.append(Paragraph(inline(l[3:]), sH1)); continue
    if l.startswith("# "):
        story.append(Paragraph(inline(l[2:]), sH1)); continue
    if l.startswith("> "):
        story.append(Paragraph(inline(l[2:]), sCit)); continue
    if l.startswith("- "):
        story.append(Paragraph(inline(l[2:]), sItem, bulletText="•")); continue
    m = re.match(r"(\d+)\.\s+(.*)", l)
    if m:
        story.append(Paragraph(inline(m.group(2)), sItem, bulletText=m.group(1) + ".")); continue
    story.append(Paragraph(inline(l), sCorpo))
doc.build(story, onFirstPage=rodape, onLaterPages=rodape)
print(OUT, os.path.getsize(OUT), "bytes | stamp:", stamp, "| iso:", agora.isoformat())
