# -*- coding: utf-8 -*-
"""Gera o PDF do prompt que originou a página (transparência ao leitor)."""
from datetime import datetime
from zoneinfo import ZoneInfo
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable, Preformatted
from reportlab.lib.fonts import tt2ps
import textwrap, os

TZ = ZoneInfo("America/Sao_Paulo")
agora = datetime.now(TZ)
stamp = agora.strftime("%d/%m/%Y às %H:%M")
stamp_en = agora.strftime("%B %d, %Y at %H:%M")

OUT = "downloads/Prompt-Gerador-da-Pagina.pdf"

PROMPT_ORIGINAL = """# ROLE AND PERSONA

Act as an expert Full-Stack Developer, Senior Prompt Engineer, and Political Scientist with post-doctoral expertise in Political Economy, Foreign Relations, and Investigative Political Journalism. Your analysis must demonstrate epistemological rigor, institutional awareness, and strict neutrality.

# CONTEXT

You will be provided with two PDF documents containing the official government proposals of two candidates for the Presidency of Brazil (hereafter "Candidate A" and "Candidate B"). You must analyze these documents and cross-reference them with real-time data from official Brazilian institutional sources.

# OBJECTIVES & DIRECTIVES

## 1. Comparative Policy Matrix

Extract and categorize all proposals from both PDFs into distinct policy areas (e.g., Economy, Health, Education, Foreign Policy, Security, Environment). Create a comprehensive HTML table comparing the proposals side-by-side.

## 2. Feasibility & Impact Modeling (Chart.js)

For each feasible policy area, generate interactive charts using Chart.js (embedded in the HTML). Map the following dimensions:

- Estimated Implementation Time vs. Financial/Fiscal Cost.

- Positive Impact vs. State Dependency vs. Civil Society/People Dependency.

- Negative Potential/Risks vs. Implementation Time.

(Note: Choose the most appropriate Chart.js chart type for each multidimensional relationship, such as Bubble, Radar, or Stacked Bar charts).

## 3. Investigative Analytical Summary

Provide a rigorous summary covering:

- Identical proposals between both candidates.

- Similar proposals with divergent ideological biases (explicitly name the bias: e.g., neoliberal, developmentalist, progressive, conservative).

- Proposals requiring institutional friction/approval from other branches (specify: Legislative, Judicial, or subnational entities).

- Potentially Misleading Proposals: Flag proposals that are populist, fiscally incompatible, or legally unfeasible. Constraint: You must justify these flags using data from the official sources listed below (e.g., citing fiscal rules from Tesouro Transparente or constitutional limits).

## 4. Real-Time Web Research & Contextualization

Use your web browsing tools to query the specific sources listed in the "Data Sources" section to find:

- Each candidate's public stance on sensitive contemporary themes, highlighting disagreements and underlying political/economic motivations.

- Proposal Evolution: Compare current proposals with their 1st-round platforms. Detail any alterations, additions, or retractions.

- Electoral & Institutional Data: Exact nominal votes in the 1st round, political party, ideological-political positioning, VP candidate, formal coalitions, and the ideological positioning of these allied parties.

# DATA SOURCES (Strict Web Search Targets)

When searching for real-time data, you MUST prioritize and cross-reference the following official channels:

- TSE (DivulgaCandContas): Legal composition of tickets and proposals submitted to Electoral Justice.

- TSE (Electoral Results): Exact nominal votes for the selected round and office.

- Federal Constitution: Fundamental rights, penal age, environment, and amendment process.

- Law nº 8.213/1991: Social security requirements for imprisonment aid.

- Law nº 13.260/2016: Legal framework of terrorism.

- LGPD (General Data Protection Law): Data processing, including health data.

- Central Bank (BCB), IBGE, INPE/TerraBrasilis, and Tesouro Transparente: Interest rates, inflation, social indicators, deforestation, and public accounts.

# OUTPUT FORMAT SPECIFICATIONS (HTML)

- Deliver the final output strictly as a single, valid, self-contained HTML5 document.

- Use semantic id attributes for each candidate's sections (e.g., id="candidate_A_profile", id="candidate_B_proposals").

- Include the Chart.js library via CDN in the <head>.

- Write the JavaScript required to initialize and render the charts using the data extracted from your analysis.

- Apply clean, professional CSS styling for readability.

- CRITICAL CONSTRAINT: Do not hallucinate data. If exact real-time data (like exact 1st round votes) cannot be verified via web search, explicitly state "Data pending verification from TSE" in the HTML. Cite sources for all web-researched claims using footnotes or tooltips.

[Arquivos anexados pelo curador: PropostasFlavio.pdf e PropostasLula.pdf]
"""

REFINAMENTOS = """Refinamentos posteriores fornecidos pelo curador (resumo fiel):

1) "a página final deve estar em português brasileiro" — a página foi entregue integralmente em português brasileiro.

2) "adicione o idioma português brasileiro como principal e inglês como secundário, também adicione um botão 'Opções' contendo: opções de acessibilidade, de tema claro/escuro, de download das propostas e do prompt que gerou esta página (tudo em pdf). no subtítulo deve conter o nome do curador 'by rogerelizar' e da IA que montou tudo. A introdução deve haver um disclaimer sobre a isenção do curador que proveu apenas o prompt que pode ser baixado no botão 'Opções' e um chamado à cidadania responsável, votando corretamente e conscientemente, finalizando com a data e hora desta publicação"

Nota de transparência: este PDF reproduz o prompt original em inglês exatamente como fornecido, para que qualquer leitor possa auditar o que foi pedido à IA — e distinguir o pedido (responsabilidade do curador) da execução analítica (responsabilidade editorial da montagem por IA, sujeita a verificação nas fontes citadas).
"""

styles = getSampleStyleSheet()
navy = HexColor("#0e2233"); gold = HexColor("#c9a227"); cinza = HexColor("#5b6b7b")
sTitulo = ParagraphStyle("t", parent=styles["Title"], fontSize=24, leading=29, textColor=navy, alignment=TA_CENTER, spaceAfter=6)
sSub = ParagraphStyle("s", parent=styles["Normal"], fontSize=12, leading=17, alignment=TA_CENTER, textColor=cinza, spaceAfter=4)
sH = ParagraphStyle("h", parent=styles["Heading2"], fontSize=13, leading=17, textColor=navy, spaceBefore=12, spaceAfter=5)
sCorpo = ParagraphStyle("c", parent=styles["Normal"], fontSize=10.5, leading=15.5, alignment=TA_JUSTIFY, spaceAfter=7)
sMono = ParagraphStyle("m", parent=styles["Code"], fontSize=8.6, leading=11.8, fontName="Courier", alignment=TA_LEFT)

def rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5); canvas.setFillColor(cinza)
    canvas.drawCentredString(A4[0]/2, 13*mm, f"Prompt que gerou a página • Curadoria: by rogerelizar • Montagem por IA (Arena.ai — Agent Mode) • {stamp} (America/Sao_Paulo) • p. {doc.page}")
    canvas.setStrokeColor(gold); canvas.setLineWidth(1.2)
    canvas.line(15*mm, 16*mm, A4[0]-15*mm, 16*mm)
    canvas.restoreState()

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=18*mm, bottomMargin=20*mm,
                        title="Prompt que gerou a página — Análise Presidencial 2026 (by rogerelizar)",
                        author="by rogerelizar (curadoria) / Arena.ai — Agent Mode (montagem por IA)")
story = []
story.append(Spacer(1, 22*mm))
story.append(Paragraph("Eleições Presidenciais 2026", ParagraphStyle("k", parent=sSub, textColor=gold, fontSize=11)))
story.append(Paragraph("Prompt que gerou esta página", sTitulo))
story.append(Paragraph("Documento de transparência: o pedido original do curador à inteligência artificial,<br/>na íntegra, para auditoria pública do método.", sSub))
story.append(Spacer(1, 5*mm)); story.append(HRFlowable(width="38%", thickness=1.6, color=gold, hAlign="CENTER")); story.append(Spacer(1, 5*mm))
story.append(Paragraph("<b>Curadoria (forneceu apenas o prompt e os dois PDFs):</b> by rogerelizar", sSub))
story.append(Paragraph("<b>Pesquisa, redação, gráficos e montagem HTML:</b> inteligência artificial — Arena.ai (Agent Mode)", sSub))
story.append(Paragraph(f"<b>Publicação desta versão:</b> {stamp} — horário de São Paulo (America/Sao_Paulo) &nbsp;•&nbsp; {stamp_en} (São Paulo time)", sSub))
story.append(Spacer(1, 8*mm))
story.append(Paragraph("Como usar este documento", sH))
story.append(Paragraph("Este PDF <b>não</b> é uma proposta de governo nem endossa candidato. Ele reproduz, sem edição de conteúdo, as instruções que o curador enviou à IA, acompanhadas dos dois arquivos <i>PropostasLula.pdf</i> e <i>PropostasFlavio.pdf</i> (disponíveis para download no botão “Opções” da página). A finalidade é permitir que qualquer cidadã ou cidadão verifique: (1) o que foi pedido; (2) quais fontes oficiais foram exigidas (TSE, Constituição, Leis nº 8.213/1991 e nº 13.260/2016, LGPD, BCB, IBGE, INPE e Tesouro Transparente); e (3) a restrição expressa contra inventar dados. Divergências entre o pedido e a página final devem ser cobradas da montagem — não presumidas como posição do curador.", sCorpo))
story.append(Paragraph("Isenção do curador: o curador limitou-se a formular o prompt e a anexar os programas oficiais registrados no TSE. Não redigiu, não aprovou previamente e não endossa necessariamente análises, notas de viabilidade ou alertas jurídico-fiscais produzidos pela IA. A leitura crítica e a conferência nas fontes primárias são indispensáveis antes do voto.", sCorpo))
story.append(Paragraph("Parte I — Prompt original (em inglês, como fornecido)", sH))
# Preformatted com quebra manual para não estourar a margem
linhas = []
for par in PROMPT_ORIGINAL.split("\n"):
    if len(par) > 108:
        linhas.extend(textwrap.wrap(par, width=108, replace_whitespace=False, drop_whitespace=False) or [""])
    else:
        linhas.append(par)
story.append(Preformatted("\n".join(linhas), sMono))
story.append(PageBreak())
story.append(Paragraph("Parte II — Refinamentos posteriores", sH))
for par in REFINAMENTOS.split("\n\n"):
    story.append(Paragraph(par.replace("\n", " "), sCorpo))
story.append(Paragraph("Chamado à cidadania responsável", sH))
story.append(Paragraph("Nenhum relatório — humano ou gerado com apoio de IA — substitui o juízo do eleitor. Leia os programas oficiais, confira os números no TSE, desconfie de promessas sem custo nem caminho institucional e vote de forma correta e consciente. Democracia se faz com informação verificável.", sCorpo))
story.append(Paragraph(f"Documento gerado em {stamp} (America/Sao_Paulo). Curadoria: by rogerelizar. Montagem: Arena.ai — Agent Mode.", sSub))
doc.build(story, onFirstPage=rodape, onLaterPages=rodape)
print(OUT, os.path.getsize(OUT), "bytes | stamp:", stamp, "| iso:", agora.isoformat())
print(agora.isoformat())
