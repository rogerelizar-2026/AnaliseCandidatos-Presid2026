# -*- coding: utf-8 -*-
"""Gera o e-book PDF A5 e o flipbook HTML5 a partir do index.html (fonte única).

Saídas:
  downloads/Analise-2026-Ebook-A5.pdf   (A5, capa especificada pelo curador)
  downloads/Analise-2026-Flipbook.html  (arquivo único; páginas do PDF viradas em 3D)
Executar da raiz do repositório:  python3 ferramentas/gerar_ebook_flipbook.py
"""
import base64, io, json, math, os, pathlib, re, subprocess, sys
from xml.sax.saxutils import escape

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
import fitz  # pymupdf
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
from bs4 import BeautifulSoup, NavigableString, Tag

from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                PageBreak, NextPageTemplate, Image as RLImage, Table, TableStyle,
                                KeepTogether, CondPageBreak, HRFlowable)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

RAIZ = pathlib.Path.cwd()
TMP = pathlib.Path("/tmp/ebook_assets"); TMP.mkdir(exist_ok=True)
SRC = (RAIZ / "index.html").read_text(encoding="utf-8")
LULA, FLAV = "#b91c1c", "#1d4ed8"
NOMES = {"A": "Lula (PT)", "B": "Flávio Bolsonaro (PL)"}
CORES = {"A": LULA, "B": FLAV}
CURTO = {"Economia e impostos": "Economia", "Segurança pública": "Segurança", "Saúde (SUS)": "Saúde",
         "Educação": "Educação", "Social e trabalho": "Social", "Mulheres e cuidados": "Mulheres/cuidados",
         "Habitação e cidades": "Habitação", "Infraestrutura e energia": "Infra/energia",
         "Agro e alimentos": "Agro", "Meio ambiente e clima": "Ambiente",
         "Democracia e Estado": "Democracia", "Exterior e defesa": "Exterior/defesa"}

# ---------------- fontes ----------------
_FD = pathlib.Path(matplotlib.__file__).parent / "mpl-data" / "fonts" / "ttf"
for nome, arq in [("DVSerif", "DejaVuSerif.ttf"), ("DVSerif-B", "DejaVuSerif-Bold.ttf"),
                  ("DVSerif-I", "DejaVuSerif-Italic.ttf"), ("DVSans", "DejaVuSans.ttf"),
                  ("DVSans-B", "DejaVuSans-Bold.ttf"), ("DVSans-I", "DejaVuSans-Oblique.ttf")]:
    pdfmetrics.registerFont(TTFont(nome, str(_FD / arq)))
pdfmetrics.registerFontFamily("DVSerif", normal="DVSerif", bold="DVSerif-B", italic="DVSerif-I", boldItalic="DVSerif-B")
pdfmetrics.registerFontFamily("DVSans", normal="DVSans", bold="DVSans-B", italic="DVSans-I", boldItalic="DVSans-B")
SERIF, SANS = "DVSerif", "DVSans"
def pilfont(nome, tam): return ImageFont.truetype(str(_FD / nome), tam)

# ---------------- dados (mesma fonte do site) ----------------
_node = ('const fs=require("fs"),vm=require("vm");const s=fs.readFileSync("index.html","utf8");'
         'const a=s.indexOf("const POLICY_DATA");const b=s.indexOf("];",a);const c={};vm.createContext(c);'
         'vm.runInContext(s.slice(a,b+2)+";this.x=POLICY_DATA",c);console.log(JSON.stringify(c.x));')
POLICY = json.loads(subprocess.check_output(["node", "-e", _node], text=True))
AREAS = list(dict.fromkeys(d["area"] for d in POLICY))
_ini = SRC.index('getElementById("chart_votes_canvas")')
_seg = SRC[_ini:_ini + 1600]
VOT_ROT = re.findall(r'"([^"]+)"', re.search(r"labels: \[(.*?)\]", _seg).group(1))
VOT_VAL = [int(x) for x in re.search(r"data: \[([\d,\s]+)\]", _seg).group(1).split(",")]
VOT_COR = re.findall(r'"(#[0-9a-fA-F]{6})"', re.search(r"backgroundColor: \[(.*?)\]", _seg).group(1))
print(f"POLICY_DATA: {len(POLICY)} linhas · votos: {list(zip(VOT_ROT, VOT_VAL))[:2]}…")

# ---------------- gráficos estáticos ----------------
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": "#20242b", "axes.edgecolor": "#8a8f98",
                     "axes.labelcolor": "#20242b", "xtick.color": "#3c414b", "ytick.color": "#3c414b", "font.size": 8})
def salvar(fig, nome):
    pth = TMP / nome; fig.savefig(pth, dpi=210, bbox_inches="tight", pad_inches=0.08); plt.close(fig); return pth

def g_votos():
    fig, ax = plt.subplots(figsize=(5.2, 2.9))
    pos = range(len(VOT_ROT))[::-1]
    ax.barh(list(pos), VOT_VAL, color=VOT_COR, height=0.62)
    ax.set_yticks(list(pos)); ax.set_yticklabels(VOT_ROT, fontsize=7.6)
    for y, v in zip(pos, VOT_VAL):
        ax.text(v + 6e5, y, f"{v:,}".replace(",", "."), va="center", fontsize=7.4)
    ax.set_xlim(0, max(VOT_VAL) * 1.22); ax.set_xlabel("Votos"); ax.grid(axis="x", alpha=0.25); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.xaxis.set_major_formatter(lambda v, _: f"{v/1e6:.0f} mi")
    ax.set_title("Votos para Presidente — 1º turno, 4/10/2026", fontsize=9.5, loc="left", weight="bold")
    return salvar(fig, "votos.png")

def g_bolha(ykey, skey, titulo, ylabel, nome):
    fig, ax = plt.subplots(figsize=(5.2, 3.7))
    for cand in ("A", "B"):
        ds = [d for d in POLICY if d["cand"] == cand]
        ax.scatter([d["tempo"] for d in ds], [d[ykey] for d in ds], s=[d[skey] * 42 for d in ds],
                   c=CORES[cand], alpha=0.55, edgecolors=CORES[cand], linewidths=0.9, label=NOMES[cand])
        for d in ds:
            ax.annotate(CURTO[d["area"]], (d["tempo"], d[ykey]), fontsize=5.3, alpha=0.9,
                        xytext=(3, 3), textcoords="offset points")
    ax.set_xlim(0, 54); ax.set_ylim(0, 10.6); ax.set_xlabel("Tempo até a entrega plena (meses) →")
    ax.set_ylabel(ylabel); ax.grid(alpha=0.25); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.legend(fontsize=7.5, frameon=False, loc="upper left")
    ax.set_title(titulo, fontsize=9.3, loc="left", weight="bold")
    return salvar(fig, nome)

def g_radar():
    cats = ["Impacto\npositivo", "Dependência\ndo Estado", "Dependência\nda sociedade", "Custo\nfiscal", "Tempo\n(normalizado)", "Risco\nnegativo"]
    def medias(cand):
        ls = [d for d in POLICY if d["cand"] == cand]
        m = lambda k: sum(d[k] for d in ls) / len(ls)
        return [round(v, 1) for v in (m("impacto"), m("depE"), m("depS"), m("custo"), m("tempo") / 48 * 10, m("risco"))]
    ang = [i / 6 * 2 * math.pi for i in range(6)] + [0]
    fig, ax = plt.subplots(figsize=(4.7, 3.9), subplot_kw=dict(polar=True))
    for cand in ("A", "B"):
        vals = medias(cand) + [medias(cand)[0]]
        ax.plot(ang, vals, color=CORES[cand], linewidth=1.6, label=NOMES[cand])
        ax.fill(ang, vals, color=CORES[cand], alpha=0.16)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(cats, fontsize=6.8)
    ax.set_ylim(0, 10); ax.set_yticks([2, 4, 6, 8, 10]); ax.set_yticklabels(["2", "4", "6", "8", "10"], fontsize=6)
    ax.legend(fontsize=7.5, frameon=False, loc="upper right", bbox_to_anchor=(1.18, 1.12))
    ax.set_title("Perfil médio nas 12 áreas (0–10)", fontsize=9.3, weight="bold", pad=18)
    return salvar(fig, "radar.png")

def g_deps(cand):
    ls = [next(d for d in POLICY if d["area"] == a and d["cand"] == cand) for a in AREAS]
    x = range(len(AREAS)); w = 0.27
    fig, ax = plt.subplots(figsize=(5.2, 3.5))
    ax.bar([i - w for i in x], [d["impacto"] for d in ls], w, label="Impacto positivo", color="#137547")
    ax.bar(list(x), [d["depE"] for d in ls], w, label="Dependência do Estado", color="#14273d")
    ax.bar([i + w for i in x], [d["depS"] for d in ls], w, label="Dependência da sociedade", color="#c9a227")
    ax.set_xticks(list(x)); ax.set_xticklabels([CURTO[a] for a in AREAS], rotation=38, ha="right", fontsize=6.4)
    ax.set_ylim(0, 10.6); ax.set_ylabel("Nota (0–10)"); ax.grid(axis="y", alpha=0.25); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.legend(fontsize=7.2, frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.14))
    ax.set_title(f"Impacto × Dependências — {NOMES[cand]}", fontsize=9.3, loc="left", weight="bold")
    return salvar(fig, f"deps_{cand}.png")

GRAF = {
    "chart_votes_canvas": [(g_votos(), "Votos nominais — 1º turno (TSE, totalização final).")],
    "chart_time_cost_canvas": [(g_bolha("custo", "impacto", "Tempo × Custo fiscal (bolha = impacto)", "Custo fiscal à União (0–10) →", "bolha_tc.png"), "Tempo de implementação × custo fiscal; tamanho da bolha = impacto positivo.")],
    "chart_radar_canvas": [(g_radar(), "Perfil médio nas 12 áreas (0–10; tempo de 48 meses = 10).")],
    "chart_dependencies_canvas": [(g_deps("A"), "Impacto × dependências por área (0–10) — Lula (PT)."),
                                  (g_deps("B"), "Impacto × dependências por área (0–10) — Flávio Bolsonaro (PL).")],
    "chart_risk_time_canvas": [(g_bolha("risco", "custo", "Risco × Tempo (bolha = custo fiscal)", "Potencial negativo / risco (0–10) →", "bolha_rt.png"), "Risco negativo × tempo; tamanho da bolha = custo fiscal.")],
}
print("gráficos gerados:", [p.name for v in GRAF.values() for p, _ in v])

# ---------------- capa e contracapa (PIL) ----------------
W, H = 1240, 1754
def bandeira_desfocada(brilho=0.82):
    S = 2; w, h = W * S, H * S
    img = Image.new("RGB", (w, h), (0, 155, 58)); d = ImageDraw.Draw(img)
    d.polygon([(w/2, h*0.07), (w*0.95, h/2), (w/2, h*0.93), (w*0.05, h/2)], fill=(254, 223, 0))
    cx, cy, r = w/2, h/2, int(w*0.215)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(0, 39, 118))
    import random; rnd = random.Random(2026)
    for _ in range(27):
        a, rr = rnd.uniform(0, 6.283), rnd.uniform(0, r*0.82)
        sx, sy, sr = cx+rr*math.cos(a), cy+rr*math.sin(a), rnd.uniform(5, 10)
        d.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=(255, 255, 255))
    d.line([(cx-r, cy+r*0.38), (cx+r, cy-r*0.58)], fill=(255, 255, 255), width=int(r*0.20))
    img = img.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(15))
    img = ImageEnhance.Brightness(img).enhance(brilho)
    grad = Image.new("L", (1, H))
    for y in range(H):
        t = y / H; grad.putpixel((0, y), int(120 - 80 * math.sin(math.pi * min(1, max(0, t)))))
    preto = Image.new("RGB", (W, H), (0, 0, 0))
    img = Image.composite(preto, img, grad.resize((W, H)))
    return img.convert("RGBA")

def texto(d, xy, s, fonte, fill, ancora="mm", sombra=True):
    if sombra: d.text((xy[0]+3, xy[1]+3), s, font=fonte, fill=(0, 0, 0, 150), anchor=ancora)
    d.text(xy, s, font=fonte, fill=fill, anchor=ancora)

def capa():
    img = bandeira_desfocada()
    camada = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(camada)
    cx = W // 2
    # urna eletrônica (ilustração plana)
    topo, larg, alt = 548, 540, 568
    d.ellipse([cx-300, topo+alt-6, cx+300, topo+alt+52], fill=(0, 0, 0, 110))
    d.rounded_rectangle([cx-larg//2, topo, cx+larg//2, topo+alt], radius=38, fill=(233, 233, 236, 255), outline=(115, 118, 125, 255), width=5)
    d.rounded_rectangle([cx-222, topo+42, cx+222, topo+292], radius=22, fill=(14, 30, 62, 255), outline=(95, 105, 125, 255), width=4)
    texto(d, (cx, topo+74), "JUSTIÇA ELEITORAL", pilfont("DejaVuSans-Bold.ttf", 27), (200, 215, 240, 255), sombra=False)
    texto(d, (cx, topo+158), "2026", pilfont("DejaVuSans-Bold.ttf", 150), (255, 255, 255, 255), sombra=False)
    texto(d, (cx, topo+255), "by rogerelizar", pilfont("DejaVuSans-Bold.ttf", 42), (255, 223, 0, 255), sombra=False)  # sob o número
    gx, gy = cx-208, topo+322
    for lin in range(4):
        for col in range(3):
            x, y = gx + col*58, gy + lin*46
            d.rounded_rectangle([x, y, x+46, y+34], radius=7, fill=(201, 205, 212, 255), outline=(130, 134, 142, 255), width=2)
    for i, (rot, cor, tc) in enumerate([("BRANCO", (245, 245, 245), (60, 60, 60)), ("CORRIGE", (240, 140, 40), (40, 30, 10)), ("CONFIRMA", (30, 160, 80), (255, 255, 255))]):
        y = gy + i*58
        d.rounded_rectangle([cx+28, y, cx+208, y+46], radius=9, fill=cor + (255,), outline=(105, 108, 115, 255), width=2)
        texto(d, (cx+118, y+24), rot, pilfont("DejaVuSans-Bold.ttf", 26), tc + (255,), sombra=False)
    texto(d, (cx, topo+alt-30), "URNA ELETRÔNICA", pilfont("DejaVuSans-Bold.ttf", 27), (95, 98, 105, 255), sombra=False)
    img.alpha_composite(camada); d = ImageDraw.Draw(img)
    # título no alto
    texto(d, (cx, 108), "E L E I Ç Õ E S   P R E S I D E N C I A I S   2 0 2 6", pilfont("DejaVuSans-Bold.ttf", 39), (255, 223, 0, 255))
    texto(d, (cx, 196), "Dois projetos de Brasil", pilfont("DejaVuSerif-Bold.ttf", 77), (255, 255, 255, 255))
    texto(d, (cx, 280), "em disputa", pilfont("DejaVuSerif-Bold.ttf", 77), (255, 255, 255, 255))
    texto(d, (cx, 356), "Análise comparativa completa dos programas de governo", pilfont("DejaVuSerif-Italic.ttf", 35), (242, 242, 242, 255))
    texto(d, (cx, 404), "Lula (PT) × Flávio Bolsonaro (PL)", pilfont("DejaVuSans-Bold.ttf", 34), (255, 255, 255, 255))
    d.line([(cx-320, 448), (cx+320, 448)], fill=(255, 223, 0, 255), width=5)
    # base: subtítulo exato
    d.line([(cx-340, 1478), (cx+340, 1478)], fill=(255, 223, 0, 255), width=5)
    texto(d, (cx, 1548), "2º Turno 2026 - Criado por IA", pilfont("DejaVuSans-Bold.ttf", 54), (255, 255, 255, 255))
    texto(d, (cx, 1632), "E-book A5 · Edição para leitura e impressão", pilfont("DejaVuSans.ttf", 31), (232, 232, 232, 255))
    texto(d, (cx, 1682), "Curadoria: by rogerelizar · Montagem: Arena.ai — Agent Mode", pilfont("DejaVuSans.ttf", 27), (220, 220, 220, 255))
    pth = TMP / "capa.png"; img.convert("RGB").save(pth, quality=92); return pth

def contracapa():
    img = bandeira_desfocada(brilho=0.55); d = ImageDraw.Draw(img); cx = W // 2
    texto(d, (cx, 640), "Vote de forma correta", pilfont("DejaVuSerif-Bold.ttf", 62), (255, 255, 255, 255))
    texto(d, (cx, 716), "e consciente.", pilfont("DejaVuSerif-Bold.ttf", 62), (255, 255, 255, 255))
    texto(d, (cx, 800), "2º turno — 25 de outubro de 2026", pilfont("DejaVuSans-Bold.ttf", 38), (255, 223, 0, 255))
    texto(d, (cx, 850), "das 8h às 17h (horário de Brasília)", pilfont("DejaVuSans.ttf", 34), (240, 240, 240, 255))
    d.line([(cx-300, 930), (cx+300, 930)], fill=(255, 223, 0, 255), width=4)
    texto(d, (cx, 1010), "Leia os programas oficiais. Confira no TSE, no Banco Central,", pilfont("DejaVuSans.ttf", 30), (235, 235, 235, 255))
    texto(d, (cx, 1052), "no IBGE e no Tesouro Nacional. Nenhum relatório vota por você.", pilfont("DejaVuSans.ttf", 30), (235, 235, 235, 255))
    texto(d, (cx, 1560), "2º Turno 2026 - Criado por IA", pilfont("DejaVuSans-Bold.ttf", 36), (255, 255, 255, 255))
    texto(d, (cx, 1624), "Curadoria: by rogerelizar (apenas os prompts e os PDFs oficiais)", pilfont("DejaVuSans.ttf", 27), (225, 225, 225, 255))
    texto(d, (cx, 1668), "Montagem por IA: Arena.ai — Agent Mode · Fontes primárias: TSE", pilfont("DejaVuSans.ttf", 27), (225, 225, 225, 255))
    pth = TMP / "contracapa.png"; img.convert("RGB").save(pth, quality=92); return pth

CAPA, CONTRA = capa(), contracapa()
print("capas geradas")

# ---------------- estilos do livro ----------------
NAVY, OURO, CINZA = HexColor("#14273d"), HexColor("#b8860b"), HexColor("#5b6470")
FW = A5[0] - 26 * mm
Capitulo = ParagraphStyle("Capitulo", fontName=SERIF, fontSize=16.5, leading=20.5, textColor=NAVY, spaceAfter=4, keepWithNext=1)
H3e = ParagraphStyle("H3e", fontName=SERIF, fontSize=11.8, leading=14.8, textColor=NAVY, spaceBefore=11, spaceAfter=4, keepWithNext=1)
H4e = ParagraphStyle("H4e", fontName=SANS, fontSize=9.8, leading=12.6, textColor=NAVY, spaceBefore=9, spaceAfter=3, keepWithNext=1)
Corpo = ParagraphStyle("Corpo", fontName=SERIF, fontSize=9.3, leading=13.6, alignment=TA_JUSTIFY, spaceAfter=5, splitLongWords=1)
Lead = ParagraphStyle("Lead", parent=Corpo, fontName="DVSerif-I", fontSize=9.7, leading=14.2, textColor=HexColor("#3f4652"))
Pequeno = ParagraphStyle("Pequeno", fontName=SANS, fontSize=7.8, leading=10.6, textColor=CINZA, spaceAfter=4, splitLongWords=1)
Lista = ParagraphStyle("Lista", parent=Corpo, alignment=TA_LEFT, leftIndent=11, bulletIndent=2, spaceAfter=3.2)
Cel = ParagraphStyle("Cel", fontName=SANS, fontSize=7.3, leading=9.6, spaceAfter=0, splitLongWords=1)
CelH = ParagraphStyle("CelH", fontName=SANS, fontSize=7.3, leading=9.4, textColor=white, spaceAfter=0)
Legenda = ParagraphStyle("Legenda", fontName=SANS, fontSize=7.7, leading=10.2, textColor=CINZA, alignment=TA_CENTER, spaceBefore=2, spaceAfter=7)
DadosBloco = ParagraphStyle("DadosBloco", fontName=SANS, fontSize=7.9, leading=11, spaceAfter=4.5, backColor=HexColor("#f7f2e4"),
                            borderColor=HexColor("#d8c9a3"), borderWidth=0.5, borderPadding=5, splitLongWords=1)
Refe = ParagraphStyle("Refe", parent=Pequeno, fontSize=7.7, leading=10.6, leftIndent=9, firstLineIndent=-9, spaceAfter=3.5, alignment=TA_LEFT)

EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u26FF\u2700-\u27BF\u2B00-\u2BFF]")
BADGE_COR = {"a": "#b91c1c", "b": "#1d4ed8", "ok": "#0c5b36", "warn": "#6b4e00", "bad": "#7a0f2e", "neut": "#33475c"}

def limpa(t): return EMOJI.sub("", t)
def inline(no, refs=False):
    if isinstance(no, NavigableString):
        return escape(limpa(str(no)))
    if not isinstance(no, Tag):
        return ""
    if no.name == "br": return "<br/>"
    classes = no.get("class") or []
    if no.name in ("ul", "ol"):
        return "<br/>".join("• " + inline(li, refs) for li in no.find_all("li", recursive=False))
    inner = "".join(inline(c, refs) for c in no.children)
    if no.name in ("strong", "b"): return f"<b>{inner}</b>"
    if no.name in ("em", "i"): return f"<i>{inner}</i>"
    if no.name == "sup": return f"<super>{inner}</super>"
    if no.name == "a":
        href = no.get("href") or ""
        if refs and href.startswith("http"):
            return inner + f' <font size="6.2" color="#555f6b">({escape(href)})</font>'
        return inner
    if no.name == "span" and "badge" in classes:
        cor = next((BADGE_COR[c] for c in classes if c in BADGE_COR), "#33475c")
        return f'<b><font color="{cor}">[{inner}]</font></b>'
    if no.name == "span" and "kicker" in classes: return f"<b>{inner}</b>"
    if no.name == "code": return f'<font name="{SANS}" size="7.6">{inner}</font>'
    return inner

def figura(canvas_id, story):
    for arq, leg in GRAF.get(canvas_id, []):
        with Image.open(arq) as im: iw, ih = im.size
        img = RLImage(str(arq), width=FW, height=FW * ih / iw)
        story.append(KeepTogether([img, Paragraph(leg, Legenda)]))

def grade_tabela(tbl):
    linhas = tbl.find_all("tr")
    grade, spans, ocup = [], [], set()
    cabec = []
    for r, tr in enumerate(linhas):
        while len(grade) <= r: grade.append([])
        c = 0
        for cel in tr.find_all(["th", "td"], recursive=False):
            while (r, c) in ocup: c += 1
            rs, cs = int(cel.get("rowspan", 1)), int(cel.get("colspan", 1))
            while len(grade[r]) <= c: grade[r].append("")
            grade[r][c] = cel
            if cel.name == "th" and r == 0: cabec.append(cel.get_text(" ", strip=True))
            if rs > 1 or cs > 1:
                spans.append(("SPAN", (c, r), (c + cs - 1, r + rs - 1)))
                for rr in range(r, r + rs):
                    for cc in range(c, c + cs):
                        if (rr, cc) != (r, c): ocup.add((rr, cc))
            c += cs
    ncol = max(len(g) for g in grade)
    for g in grade: g += [""] * (ncol - len(g))
    return grade, spans, cabec

def tabela(tbl, story, secao):
    tbody = tbl.find("tbody")
    if tbody is not None and tbody.get("id") == "policy_data_body":
        for cand in ("A", "B"):
            story.append(Paragraph(f"{NOMES[cand]} — notas por área", H4e))
            for d in [x for x in POLICY if x["cand"] == cand]:
                story.append(CondPageBreak(52))
                story.append(Paragraph(
                    f"<b>{escape(d['area'])}</b> — Tempo {d['tempo']} meses · Custo fiscal {d['custo']} · Impacto + {d['impacto']} · "
                    f"Dep. Estado {d['depE']} · Dep. sociedade {d['depS']} · Risco − {d['risco']}<br/><i>{escape(d['nota'])}</i>", DadosBloco))
        return
    grade, spans, cabec = grade_tabela(tbl)
    if not grade: return
    textos = [[(c.get_text(" ", strip=True) if isinstance(c, Tag) else "") for c in linha] for linha in grade]
    n = len(grade[0])
    media = sum(len(t) for linha in textos[1:] for t in linha) / max(1, (len(textos) - 1) * n)
    if n >= 4 and media > 105:  # tabela larga de texto longo → blocos legíveis por linha
        for linha, tlinha in zip(grade[1:], textos[1:]):
            story.append(CondPageBreak(110))
            story.append(Paragraph(inline(linha[0]) if isinstance(linha[0], Tag) else escape(tlinha[0]), H4e))
            for j in range(1, n):
                if isinstance(linha[j], Tag) and tlinha[j]:
                    rot = f"<b>{escape(cabec[j])}:</b> " if j < len(cabec) and cabec[j] else ""
                    story.append(Paragraph(rot + inline(linha[j]), Corpo))
        return
    dados = []
    for r, linha in enumerate(grade):
        dados.append([Paragraph(inline(c), CelH if r == 0 else Cel) if isinstance(c, Tag) else "" for c in linha])
    pesos = [max(6.0, math.sqrt(max(len(textos[r][c]) for r in range(len(textos))))) for c in range(n)]
    soma = sum(pesos); larguras = [FW * p / soma for p in pesos]
    estilo = [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#b8ab8c")),
              ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 3.2), ("RIGHTPADDING", (0, 0), (-1, -1), 3.2),
              ("TOPPADDING", (0, 0), (-1, -1), 2.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
              ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf6ea")])] + spans
    story.append(Table(dados, colWidths=larguras, repeatRows=1, style=TableStyle(estilo)))
    story.append(Spacer(1, 5))

CAIXA = {"info": ("#eef6ff", "#0b5fa5"), "warn": ("#fff8e1", "#9a6b00"), "danger": ("#fff0f3", "#a4133c"), "good": ("#eaf7ef", "#137547")}
BLOCOS = {"p", "ul", "ol", "div", "table", "h3", "h4", "hr", "canvas"}

def emite_filhos(el, story, secao):
    buf = []
    def flush():
        t = "".join(buf).strip(); buf.clear()
        if t: story.append(Paragraph(t, Corpo))
    for filho in el.children:
        if isinstance(filho, NavigableString):
            if str(filho).strip(): buf.append(inline(filho))
            continue
        if not isinstance(filho, Tag): continue
        if filho.name in BLOCOS or filho.name == "section":
            flush(); despacha(filho, story, secao)
        else:
            buf.append(inline(filho))
    flush()

def despacha(el, story, secao):
    nome, classes = el.name, el.get("class") or []
    if nome == "h2": return
    if nome == "h3": story.append(Paragraph(inline(el), H3e)); return
    if nome == "h4": story.append(Paragraph(inline(el), H4e)); return
    if nome == "p":
        estilo = Lead if "lead" in classes else (Pequeno if "small" in classes else Corpo)
        if el.get_text(strip=True): story.append(Paragraph(inline(el), estilo))
        return
    if nome in ("ul", "ol"):
        for i, li in enumerate(el.find_all("li", recursive=False), 1):
            if secao == "references":
                story.append(Paragraph(inline(li, refs=True), Refe))
            else:
                story.append(Paragraph(inline(li), Lista, bulletText=f"{i}." if nome == "ol" else "•"))
        story.append(Spacer(1, 2)); return
    if nome == "hr": story.append(HRFlowable(width="100%", thickness=0.6, color=HexColor("#b8ab8c"), spaceBefore=5, spaceAfter=5)); return
    if nome == "canvas": figura(el.get("id"), story); return
    if nome == "table": tabela(el, story, secao); return
    if nome == "div":
        if "controls" in classes: return
        if "tablebox" in classes:
            t = el.find("table")
            if t: tabela(t, story, secao)
            return
        if "chartbox" in classes:
            cv = el.find("canvas")
            if cv: figura(cv.get("id"), story)
            return
        if "callout" in classes:
            tipo = next((c for c in classes if c in CAIXA), "info"); fundo, borda = CAIXA[tipo]
            dentro = []; emite_filhos(el, dentro, secao)
            tb = Table([[dentro]], colWidths=[FW], style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), HexColor(fundo)), ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#b8ab8c")),
                ("LINEBEFORE", (0, 0), (0, 0), 2.4, HexColor(borda)), ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
            story.append(KeepTogether(tb)); story.append(Spacer(1, 6)); return
        if "card" in classes:
            cor = LULA if "a" in classes else (FLAV if "b" in classes else "#14273d")
            story.append(HRFlowable(width="100%", thickness=2.0, color=HexColor(cor), spaceBefore=7, spaceAfter=4))
            emite_filhos(el, story, secao); story.append(Spacer(1, 4)); return
        if "timeline" in classes:
            for f in el.find_all("div", recursive=False):
                story.append(Paragraph(inline(f), Lista, bulletText="▸"))
            return
        emite_filhos(el, story, secao); return
    emite_filhos(el, story, secao)

# ---------------- monta o livro ----------------
soup = BeautifulSoup(SRC, "html.parser")
pub_texto = soup.select_one(".pub-datetime")
PUB = pub_texto.get_text(" ", strip=True) if pub_texto else "23 de outubro de 2026 às 14h33 (horário de São Paulo)"
KPIS = [(k.find("b").get_text(" ", strip=True), k.find("span").get_text(" ", strip=True)) for k in soup.select(".kpi")]
for sel in [".i18n-en", "script", "style", "nav", "footer", "dialog", ".controls", "button", "select", "noscript"]:
    for t in soup.select(sel): t.decompose()
for t in list(soup.find_all(attrs={"hidden": True})): t.decompose()
secoes = soup.find_all("section")
print("seções:", [s.get("id") for s in secoes])

TOC_CURTOS = ["Apresentação", "Como ler (metodologia)", "1. Perfis, votos e alianças", "2. Matriz comparativa",
              "3. Modelagem de viabilidade", "4. Sumário investigativo", "5. Temas sensíveis",
              "6. Evolução 1º → 2º turno", "7. Contexto oficial e veredito", "Fontes e notas"]

class LivroDoc(BaseDocTemplate):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw); self.capitulos = []
    def afterFlowable(self, fl):
        if getattr(fl, "style", None) is not None and fl.style.name == "Capitulo":
            self.capitulos.append(self.page)
            chave = f"cap{len(self.capitulos)}"
            self.canv.bookmarkPage(chave)
            self.canv.addOutlineEntry(fl.getPlainText(), chave, 0, 0)

def on_capa(canv, doc):
    canv.saveState(); canv.drawImage(str(CAPA), 0, 0, width=A5[0], height=A5[1]); canv.restoreState()
def on_contra(canv, doc):
    canv.saveState(); canv.drawImage(str(CONTRA), 0, 0, width=A5[0], height=A5[1]); canv.restoreState()
def on_miolo(canv, doc):
    canv.saveState()
    canv.setStrokeColor(OURO); canv.setLineWidth(0.8); canv.line(13*mm, 12.5*mm, A5[0]-13*mm, 12.5*mm)
    canv.setFont(SANS, 6.6); canv.setFillColor(CINZA)
    canv.drawString(13*mm, 8.5*mm, "Eleições Presidenciais 2026 — Análise Comparativa · by rogerelizar")
    canv.drawRightString(A5[0]-13*mm, 8.5*mm, str(doc.page))
    canv.drawRightString(A5[0]-13*mm, A5[1]-10*mm, "2º Turno 2026 - Criado por IA")
    canv.restoreState()

def criar_doc(caminho):
    doc = LivroDoc(str(caminho), pagesize=A5, leftMargin=13*mm, rightMargin=13*mm, topMargin=15*mm, bottomMargin=16*mm,
                   title="Eleições Presidenciais 2026 — Análise Comparativa dos Programas de Governo (e-book A5)",
                   author="by rogerelizar (curadoria) / Arena.ai — Agent Mode (montagem por IA)")
    doc.addPageTemplates([
        PageTemplate(id="capa", frames=[Frame(0, 0, A5[0], A5[1])], onPage=on_capa),
        PageTemplate(id="miolo", frames=[Frame(13*mm, 16*mm, FW, A5[1]-31*mm)], onPage=on_miolo),
        PageTemplate(id="contracapa", frames=[Frame(0, 0, A5[0], A5[1])], onPage=on_contra),
    ])
    return doc

def montar(paginas_caps):
    story = [Spacer(1, 1), NextPageTemplate("miolo"), PageBreak()]
    story.append(Paragraph("ELEIÇÕES PRESIDENCIAIS 2026 · 2º TURNO", ParagraphStyle("k", fontName=SANS, fontSize=8.2, leading=11, textColor=OURO, alignment=TA_CENTER)))
    story.append(Paragraph("Dois projetos de Brasil em disputa", ParagraphStyle("tt", fontName=SERIF, fontSize=19, leading=23, textColor=NAVY, alignment=TA_CENTER, spaceBefore=6, spaceAfter=3)))
    story.append(Paragraph("Análise comparativa completa dos programas de governo — Lula (PT) × Flávio Bolsonaro (PL)", ParagraphStyle("ts", fontName="DVSerif-I", fontSize=10.3, leading=14, textColor=CINZA, alignment=TA_CENTER, spaceAfter=6)))
    story.append(HRFlowable(width="42%", thickness=1.4, color=OURO, hAlign="CENTER", spaceBefore=3, spaceAfter=8))
    story.append(Paragraph("<b>Curadoria:</b> by rogerelizar (forneceu apenas os prompts e os dois PDFs oficiais registrados no TSE).<br/><b>Pesquisa, redação, gráficos e montagem:</b> inteligência artificial — Arena.ai (Agent Mode).<br/><b>Publicação:</b> " + escape(PUB) + ".<br/><b>Edição:</b> e-book A5 para leitura e impressão, gerado a partir da página interativa do projeto (mesmo conteúdo, mesma data de corte: 23 de outubro de 2026).", ParagraphStyle("cr", fontName=SANS, fontSize=8.4, leading=12.4, alignment=TA_CENTER, textColor=HexColor("#2c333d"), spaceAfter=7)))
    story.append(Paragraph("<b>Isenção do curador.</b> O curador limitou-se a formular os prompts e a anexar os programas oficiais. Não redigiu, não revisou previamente linha a linha e não endossa necessariamente interpretações, notas de viabilidade ou alertas deste relatório — responsabilidade editorial da montagem por IA, sujeita a conferência nas fontes citadas. Um prompt em PDF (a versão que gera esta análise em formato A5) está disponível para download no menu da página; o prompt completo do site fica arquivado no repositório do projeto.", Corpo))
    story.append(Paragraph("<b>Como usar este e-book.</b> Cada capítulo começa em página nova e os gráficos viajam com suas legendas e textos de leitura. No site, a mesma análise é interativa (filtros, dois idiomas, temas e acessibilidade) e há um flipbook HTML5 com esta diagramação. Imprima em A5 ou leia na tela — e, antes de votar, confira os números nas fontes oficiais indicadas.", Corpo))
    if KPIS:
        story.append(Paragraph("A eleição em números", H3e))
        for b, s in KPIS:
            story.append(Paragraph(f"<b>{escape(b)}</b> — {escape(s)}", Lista, bulletText="▸"))
    story.append(PageBreak())
    story.append(Paragraph("Sumário", ParagraphStyle("Sumario", parent=Capitulo)))
    story.append(HRFlowable(width="100%", thickness=0.8, color=OURO, spaceBefore=2, spaceAfter=7))
    tocT = ParagraphStyle("tocT", fontName=SERIF, fontSize=10.2, leading=13, textColor=NAVY)
    tocN = ParagraphStyle("tocN", fontName=SANS, fontSize=9.6, leading=13, textColor=NAVY, alignment=2)
    linhas = []
    for i, titulo in enumerate(TOC_CURTOS):
        num = str(paginas_caps[i]) if paginas_caps and i < len(paginas_caps) else "00"
        linhas.append([Paragraph(escape(titulo), tocT), Paragraph(num, tocN)])
    story.append(Table(linhas, colWidths=[FW - 14*mm, 14*mm], style=TableStyle([
        ("LINEBELOW", (0, 0), (-1, -2), 0.35, HexColor("#d8c9a3")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 1), ("RIGHTPADDING", (0, 0), (-1, -1), 1),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4)])))
    for sec in secoes:
        h2 = sec.find("h2", recursive=False) or sec.find("h2")
        titulo = limpa(h2.get_text(" ", strip=True)) if h2 else (sec.get("id") or "Capítulo")
        story.append(PageBreak())
        story.append(Paragraph(escape(titulo), Capitulo))
        story.append(HRFlowable(width="100%", thickness=0.9, color=OURO, spaceBefore=2, spaceAfter=7))
        emite_filhos(sec, story, sec.get("id") or "")
    story += [NextPageTemplate("contracapa"), PageBreak(), Spacer(1, 1)]
    return story

sai_pdf = RAIZ / "downloads" / "Analise-2026-Ebook-A5.pdf"
_doc1 = criar_doc("/tmp/ebook_pass1.pdf"); _doc1.build(montar(None))
_caps = list(_doc1.capitulos)
print("capítulos (páginas):", _caps)
_doc2 = criar_doc(sai_pdf); _doc2.build(montar(_caps))
assert list(_doc2.capitulos) == _caps, "paginação do sumário divergiu entre passes"
d = fitz.open(sai_pdf); npag = len(d)
print(f"EBOOK pages={npag} bytes={sai_pdf.stat().st_size}")

# ---------------- flipbook HTML5 (arquivo único) ----------------
folhas = []
for i in range(0, npag, 2):
    def face(pg, lado):
        if pg >= npag:
            return f'<div class="face {lado} fim"><div>Fim<br><small>by rogerelizar</small></div></div>'
        pix = d[pg].get_pixmap(dpi=115)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=66, optimize=True)
        uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
        return f'<div class="face {lado}"><img src="{uri}" alt="Página {pg+1}"></div>'
    folhas.append(f'<div class="leaf">{face(i, "front")}{face(i+1, "back")}</div>')

FLIP = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Eleições Presidenciais 2026 — Flipbook A5 | Lula (PT) × Flávio Bolsonaro (PL)</title>
<meta name="description" content="Flipbook HTML5 da análise comparativa dos programas de governo — 2º turno 2026. Curadoria: by rogerelizar. Criado por IA (Arena.ai — Agent Mode).">
<style>
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:Georgia,'Times New Roman',serif;background:#17130c radial-gradient(900px 500px at 50% -5%,rgba(216,162,74,.14),transparent 62%);color:#f2e9d8;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:14px 10px 26px}
header{text-align:center;max-width:760px}
.k{font-family:Verdana,sans-serif;letter-spacing:.18em;font-size:.68rem;color:#d8a24a;text-transform:uppercase}
h1{font-size:clamp(1.25rem,4.6vw,1.8rem);margin:.35rem 0 .2rem;line-height:1.2}
.sub{opacity:.85;font-style:italic;font-size:clamp(.85rem,3vw,.98rem);margin:0 0 4px}
.credits{font-family:Verdana,sans-serif;font-size:.72rem;opacity:.75}
#palco{perspective:2400px;margin:16px 0 10px;width:min(94vw,500px)}
#livro{position:relative;width:100%;aspect-ratio:148/210;transform-style:preserve-3d;filter:drop-shadow(0 22px 44px rgba(0,0,0,.55))}
.leaf{position:absolute;inset:0;transform-origin:left center;transform-style:preserve-3d;transition:transform .75s cubic-bezier(.25,.7,.3,1)}
.leaf.flipped{transform:rotateY(-180deg)}
.face{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden;background:#fbf7ec;overflow:hidden;border-radius:3px 8px 8px 3px}
.face.back{transform:rotateY(180deg);border-radius:8px 3px 3px 8px}
.face img{width:100%;height:100%;object-fit:cover;display:block;user-select:none;-webkit-user-drag:none}
.face.fim{display:flex;align-items:center;justify-content:center;text-align:center;color:#5b5546;font-size:1.3rem;background:#efe8d8}
.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:center;font-family:Verdana,sans-serif}
button,a.btn{min-height:44px;padding:10px 18px;border-radius:6px;border:2px solid #d8a24a;background:#d8a24a;color:#17130c;font:inherit;font-weight:700;font-size:.92rem;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center}
button.ghost{background:transparent;color:#f2e9d8;border-color:#a08c5f}
button:disabled{opacity:.38;cursor:default}
#contador{font-size:.88rem;min-width:128px;text-align:center}
.dica{font-family:Verdana,sans-serif;font-size:.72rem;opacity:.7;text-align:center;margin-top:8px}
:focus-visible{outline:3px solid #f0c169;outline-offset:2px}
@media (prefers-reduced-motion: reduce){.leaf{transition:none}}
</style>
</head>
<body>
<header>
<div class="k">Eleições Presidenciais 2026 · 2º turno · Flipbook A5</div>
<h1>Dois projetos de Brasil em disputa</h1>
<p class="sub">Análise comparativa completa dos programas de governo — Lula (PT) × Flávio Bolsonaro (PL)</p>
<div class="credits">Curadoria: <strong>by rogerelizar</strong> · Montagem por IA: <strong>Arena.ai — Agent Mode</strong> · 2º Turno 2026 - Criado por IA</div>
</header>
<div id="palco"><div id="livro">__FOLHAS__</div></div>
<div class="controls">
<button type="button" id="ant">◀ Anterior</button>
<span id="contador" aria-live="polite"></span>
<button type="button" id="prox">Próxima ▶</button>
<a class="btn ghost" href="Analise-2026-Ebook-A5.pdf" download>⬇ PDF A5</a>
</div>
<p class="dica">Toque nas laterais do livro, deslize o dedo ou use ← → no teclado para virar as páginas. Funciona sem internet.</p>
<script>
(function(){
"use strict";
var leaves=[].slice.call(document.querySelectorAll(".leaf"));
var total=__NPAG__, atual=0;
var contador=document.getElementById("contador"), ant=document.getElementById("ant"), prox=document.getElementById("prox");
function render(){
  leaves.forEach(function(l,i){
    var virada=i<atual;
    l.classList.toggle("flipped",virada);
    l.style.zIndex=virada?String(i+1):String(leaves.length-i);
  });
  var visivel=Math.min(atual*2+1,total);
  contador.textContent="Página "+visivel+" de "+total;
  ant.disabled=atual<=0; prox.disabled=atual>=leaves.length;
}
function proxPagina(){ if(atual<leaves.length){atual++;render();} }
function antPagina(){ if(atual>0){atual--;render();} }
prox.addEventListener("click",proxPagina);
ant.addEventListener("click",antPagina);
document.addEventListener("keydown",function(e){ if(e.key==="ArrowRight")proxPagina(); if(e.key==="ArrowLeft")antPagina(); });
var livro=document.getElementById("livro");
livro.addEventListener("click",function(e){
  var r=livro.getBoundingClientRect(), x=(e.clientX-r.left)/r.width;
  if(x>0.55)proxPagina(); else if(x<0.45)antPagina();
});
var tx=null;
livro.addEventListener("touchstart",function(e){tx=e.changedTouches[0].clientX;},{passive:true});
livro.addEventListener("touchend",function(e){
  if(tx===null)return; var dx=e.changedTouches[0].clientX-tx; tx=null;
  if(dx<-42)proxPagina(); else if(dx>42)antPagina();
},{passive:true});
render();
})();
</script>
</body>
</html>
"""
sai_flip = RAIZ / "downloads" / "Analise-2026-Flipbook.html"
sai_flip.write_text(FLIP.replace("__FOLHAS__", "\n".join(folhas)).replace("__NPAG__", str(npag)), encoding="utf-8")
print(f"FLIPBOOK bytes={sai_flip.stat().st_size} folhas={len(folhas)}")
