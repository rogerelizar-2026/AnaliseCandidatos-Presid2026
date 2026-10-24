# -*- coding: utf-8 -*-
"""Gera o e-book PDF A5 e o flipbook HTML5 a partir do analise.html (fonte única).

Saídas:
  downloads/Analise-2026-Ebook-A5.pdf   (A5 padrão para impressão, capa especificada)
  downloads/Analise-2026-Flipbook.html  (arquivo único; edição digital em FONTE AMPLIADA
                                         — corpo de 16 pt — paginada só para leitura na tela)
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
SRC = (RAIZ / "analise.html").read_text(encoding="utf-8")
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
_node = ('const fs=require("fs"),vm=require("vm");const s=fs.readFileSync("analise.html","utf8");'
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
PERFIL_ATUAL = "padrao"
GF = 1.0   # escala das fontes dos gráficos (perfil ampliado: 1,55)
GH = 1.0   # escala da altura das figuras (perfil ampliado: 1,38)
def salvar(fig, nome):
    pth = TMP / nome; fig.savefig(pth, dpi=210, bbox_inches="tight", pad_inches=0.08); plt.close(fig); return pth

def g_votos():
    fig, ax = plt.subplots(figsize=(5.2, 2.9*GH))
    pos = range(len(VOT_ROT))[::-1]
    ax.barh(list(pos), VOT_VAL, color=VOT_COR, height=0.62)
    ax.set_yticks(list(pos)); ax.set_yticklabels(VOT_ROT, fontsize=7.6*GF)
    for y, v in zip(pos, VOT_VAL):
        ax.text(v + 6e5, y, f"{v:,}".replace(",", "."), va="center", fontsize=7.4*GF)
    ax.set_xlim(0, max(VOT_VAL) * 1.22); ax.set_xlabel("Votos"); ax.grid(axis="x", alpha=0.25); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.xaxis.set_major_formatter(lambda v, _: f"{v/1e6:.0f} mi")
    ax.set_title("Votos para Presidente — 1º turno, 4/10/2026", fontsize=9.5*GF, loc="left", weight="bold")
    return salvar(fig, "votos.png")

def g_bolha(ykey, skey, titulo, ylabel, nome, cands=("A", "B")):
    fig, ax = plt.subplots(figsize=(5.2, 3.7*GH))
    desloc = [(4, 4), (-4, 7), (4, -11), (-4, -14)]
    for ci, cand in enumerate(cands):
        ds = [d for d in POLICY if d["cand"] == cand]
        fator = 34 if len(cands) == 1 else 42
        ax.scatter([d["tempo"] for d in ds], [d[ykey] for d in ds], s=[d[skey] * fator for d in ds],
                   c=CORES[cand], alpha=0.55, edgecolors=CORES[cand], linewidths=0.9, label=NOMES[cand])
        for j, d in enumerate(ds):
            if PERFIL_ATUAL == "ampliada" and len(cands) == 1:
                # Muitos pontos dividem a mesma coordenada: número dentro da bolha
                # (o mapa número→área vai na legenda, em fonte grande) evita colisões;
                # coordenadas idênticas viram um rótulo só ("1·4").
                grupo = [str(AREAS.index(x["area"]) + 1) for x in ds if x["tempo"] == d["tempo"] and x[ykey] == d[ykey]]
                if grupo[0] == str(AREAS.index(d["area"]) + 1):
                    ax.annotate("·".join(grupo), (d["tempo"], d[ykey]), fontsize=(6.8 if len(grupo) == 1 else 5.4)*GF,
                                color="white", weight="bold", ha="center", va="center")
            else:
                dx, dy = desloc[(j + ci) % len(desloc)]
                ax.annotate(CURTO[d["area"]], (d["tempo"], d[ykey]), fontsize=(6.4 if len(cands) == 1 else 5.3)*GF, alpha=0.95,
                            xytext=(dx, dy), textcoords="offset points",
                            ha="left" if dx >= 0 else "right", va="bottom" if dy >= 0 else "top",
                            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.68))
    ax.set_xlim(0, 54); ax.set_ylim(0, 10.6); ax.set_xlabel("Tempo até a entrega plena (meses) →")
    ax.set_ylabel(ylabel); ax.grid(alpha=0.25); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    if len(cands) > 1:
        ax.legend(fontsize=7.5*GF, frameon=False, loc="upper left")
    ax.set_title(titulo, fontsize=9.3*GF, loc="left", weight="bold")
    return salvar(fig, nome)

def g_radar():
    cats = ["Impacto\npositivo", "Dependência\ndo Estado", "Dependência\nda sociedade", "Custo\nfiscal", "Tempo\n(normalizado)", "Risco\nnegativo"]
    def medias(cand):
        ls = [d for d in POLICY if d["cand"] == cand]
        m = lambda k: sum(d[k] for d in ls) / len(ls)
        return [round(v, 1) for v in (m("impacto"), m("depE"), m("depS"), m("custo"), m("tempo") / 48 * 10, m("risco"))]
    ang = [i / 6 * 2 * math.pi for i in range(6)] + [0]
    fig, ax = plt.subplots(figsize=(4.7, 3.9*GH), subplot_kw=dict(polar=True))
    for cand in ("A", "B"):
        vals = medias(cand) + [medias(cand)[0]]
        ax.plot(ang, vals, color=CORES[cand], linewidth=1.6, label=NOMES[cand])
        ax.fill(ang, vals, color=CORES[cand], alpha=0.16)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(cats, fontsize=6.8*GF)
    ax.set_ylim(0, 10); ax.set_yticks([2, 4, 6, 8, 10]); ax.set_yticklabels(["2", "4", "6", "8", "10"], fontsize=6*GF)
    if PERFIL_ATUAL == "ampliada":
        ax.legend(fontsize=7.5*GF, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.24), ncol=2)
        ax.set_title("Perfil médio nas 12 áreas (0–10)", fontsize=9.3*GF, weight="bold", pad=52)
    else:
        ax.legend(fontsize=7.5*GF, frameon=False, loc="upper right", bbox_to_anchor=(1.18, 1.12))
        ax.set_title("Perfil médio nas 12 áreas (0–10)", fontsize=9.3*GF, weight="bold", pad=18)
    return salvar(fig, "radar.png")

def g_deps(cand):
    ls = [next(d for d in POLICY if d["area"] == a and d["cand"] == cand) for a in AREAS]
    x = range(len(AREAS)); w = 0.27
    fig, ax = plt.subplots(figsize=(5.2, 3.5*GH))
    rot = ("Impacto +", "Dep. Estado", "Dep. sociedade") if PERFIL_ATUAL == "ampliada" else ("Impacto positivo", "Dependência do Estado", "Dependência da sociedade")
    ax.bar([i - w for i in x], [d["impacto"] for d in ls], w, label=rot[0], color="#137547")
    ax.bar(list(x), [d["depE"] for d in ls], w, label=rot[1], color="#14273d")
    ax.bar([i + w for i in x], [d["depS"] for d in ls], w, label=rot[2], color="#c9a227")
    ax.set_xticks(list(x)); ax.set_xticklabels([CURTO[a] for a in AREAS], rotation=38, ha="right", fontsize=6.4*GF)
    ax.set_ylim(0, 10.6); ax.set_ylabel("Nota (0–10)"); ax.grid(axis="y", alpha=0.25); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    if PERFIL_ATUAL == "ampliada":
        ax.legend(fontsize=6.7*GF, frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.09))
        ax.set_title(f"Impacto × Dependências — {NOMES[cand]}", fontsize=9.3*GF, loc="left", weight="bold", pad=30)
    else:
        ax.legend(fontsize=7.2*GF, frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.14))
        ax.set_title(f"Impacto × Dependências — {NOMES[cand]}", fontsize=9.3*GF, loc="left", weight="bold")
    return salvar(fig, f"deps_{cand}.png")

def gerar_graficos():
    global GF, GH
    GF = 1.55 if PERFIL_ATUAL == "ampliada" else 1.0
    GH = 1.38 if PERFIL_ATUAL == "ampliada" else 1.0
    plt.rcParams.update({"font.size": 8 * GF})
    if PERFIL_ATUAL == "ampliada":
        mapa_areas = " Áreas: " + " · ".join(f"{i+1} {CURTO[a]}" for i, a in enumerate(AREAS)) + "."
        bolha_tc = [(g_bolha("custo", "impacto", "Tempo × Custo fiscal — Lula (PT)", "Custo fiscal à União (0–10) →", "bolha_tc_A.png", cands=("A",)), "Tempo de implementação × custo fiscal — Lula (PT); tamanho da bolha = impacto positivo." + mapa_areas),
                    (g_bolha("custo", "impacto", "Tempo × Custo fiscal — Flávio Bolsonaro (PL)", "Custo fiscal à União (0–10) →", "bolha_tc_B.png", cands=("B",)), "Tempo de implementação × custo fiscal — Flávio Bolsonaro (PL); tamanho da bolha = impacto positivo." + mapa_areas)]
        bolha_rt = [(g_bolha("risco", "custo", "Risco × Tempo — Lula (PT)", "Potencial negativo / risco (0–10) →", "bolha_rt_A.png", cands=("A",)), "Risco negativo × tempo — Lula (PT); tamanho da bolha = custo fiscal." + mapa_areas),
                    (g_bolha("risco", "custo", "Risco × Tempo — Flávio Bolsonaro (PL)", "Potencial negativo / risco (0–10) →", "bolha_rt_B.png", cands=("B",)), "Risco negativo × tempo — Flávio Bolsonaro (PL); tamanho da bolha = custo fiscal." + mapa_areas)]
    else:
        bolha_tc = [(g_bolha("custo", "impacto", "Tempo × Custo fiscal (bolha = impacto)", "Custo fiscal à União (0–10) →", "bolha_tc.png"), "Tempo de implementação × custo fiscal; tamanho da bolha = impacto positivo.")]
        bolha_rt = [(g_bolha("risco", "custo", "Risco × Tempo (bolha = custo fiscal)", "Potencial negativo / risco (0–10) →", "bolha_rt.png"), "Risco negativo × tempo; tamanho da bolha = custo fiscal.")]
    return {
    "chart_votes_canvas": [(g_votos(), "Votos nominais — 1º turno (TSE, totalização final).")],
    "chart_time_cost_canvas": bolha_tc,
    "chart_radar_canvas": [(g_radar(), "Perfil médio nas 12 áreas (0–10; tempo de 48 meses = 10).")],
    "chart_dependency_canvas": [(g_deps("A"), "Impacto × dependências por área (0–10) — Lula (PT)."),
                                  (g_deps("B"), "Impacto × dependências por área (0–10) — Flávio Bolsonaro (PL).")],
    "chart_risk_time_canvas": bolha_rt,
    }
GRAF = {}

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
MARGEM_X, MARGEM_TOPO, MARGEM_BASE = 13 * mm, 15 * mm, 16 * mm
FW = A5[0] - 2 * MARGEM_X
TAM = {}
REF_INLINE, CODE_INLINE = 6.2, 7.6
COND_DADOS, COND_LINHA = 52, 110
TABELA_BLOCOS_COLS, TABELA_BLOCOS_MEDIA = 4, 105
CEL_PAD_X, CEL_PAD_Y = 3.2, 2.6
RODAPE_FONTE = 6.6
EDICAO_TXT = COMO_USAR_TXT = ""

def aplicar_perfil(perfil):
    """'padrao' = e-book A5 p/ impressão · 'ampliada' = flipbook em fonte grande (tela)."""
    global PERFIL_ATUAL, MARGEM_X, MARGEM_TOPO, MARGEM_BASE, FW, TAM
    global Capitulo, H3e, H4e, Corpo, Lead, Pequeno, Lista, Cel, CelH, Legenda, DadosBloco, Refe
    global REF_INLINE, CODE_INLINE, COND_DADOS, COND_LINHA, TABELA_BLOCOS_COLS, TABELA_BLOCOS_MEDIA
    global CEL_PAD_X, CEL_PAD_Y, RODAPE_FONTE, EDICAO_TXT, COMO_USAR_TXT
    PERFIL_ATUAL = perfil
    amp = perfil == "ampliada"
    MARGEM_X = 10.5 * mm if amp else 13 * mm
    MARGEM_TOPO = 13.5 * mm if amp else 15 * mm
    MARGEM_BASE = 14.5 * mm if amp else 16 * mm
    FW = A5[0] - 2 * MARGEM_X
    Capitulo = ParagraphStyle("Capitulo", fontName=SERIF, fontSize=25 if amp else 16.5, leading=30 if amp else 20.5, textColor=NAVY, spaceAfter=6 if amp else 4, keepWithNext=1)
    H3e = ParagraphStyle("H3e", fontName=SERIF, fontSize=19 if amp else 11.8, leading=24 if amp else 14.8, textColor=NAVY, spaceBefore=16 if amp else 11, spaceAfter=6 if amp else 4, keepWithNext=1)
    H4e = ParagraphStyle("H4e", fontName=SANS, fontSize=16 if amp else 9.8, leading=21 if amp else 12.6, textColor=NAVY, spaceBefore=13 if amp else 9, spaceAfter=4 if amp else 3, keepWithNext=1)
    Corpo = ParagraphStyle("Corpo", fontName=SERIF, fontSize=16 if amp else 9.3, leading=23.5 if amp else 13.6, alignment=TA_LEFT if amp else TA_JUSTIFY, spaceAfter=8 if amp else 5, splitLongWords=1)
    Lead = ParagraphStyle("Lead", parent=Corpo, fontName="DVSerif-I", fontSize=16.5 if amp else 9.7, leading=24 if amp else 14.2, textColor=HexColor("#3f4652"))
    Pequeno = ParagraphStyle("Pequeno", fontName=SANS, fontSize=13 if amp else 7.8, leading=18.5 if amp else 10.6, textColor=CINZA, spaceAfter=6 if amp else 4, splitLongWords=1)
    Lista = ParagraphStyle("Lista", parent=Corpo, alignment=TA_LEFT, leftIndent=20 if amp else 11, bulletIndent=5 if amp else 2, spaceAfter=5 if amp else 3.2)
    Cel = ParagraphStyle("Cel", fontName=SANS, fontSize=12 if amp else 7.3, leading=16.5 if amp else 9.6, spaceAfter=0, splitLongWords=1)
    CelH = ParagraphStyle("CelH", fontName=SANS, fontSize=12 if amp else 7.3, leading=16 if amp else 9.4, textColor=white, spaceAfter=0)
    Legenda = ParagraphStyle("Legenda", fontName=SANS, fontSize=12.5 if amp else 7.7, leading=17 if amp else 10.2, textColor=CINZA, alignment=TA_CENTER, spaceBefore=4 if amp else 2, spaceAfter=10 if amp else 7)
    DadosBloco = ParagraphStyle("DadosBloco", fontName=SANS, fontSize=13.5 if amp else 7.9, leading=19.5 if amp else 11, spaceAfter=7 if amp else 4.5, backColor=HexColor("#f7f2e4"),
                                borderColor=HexColor("#d8c9a3"), borderWidth=0.5, borderPadding=8 if amp else 5, splitLongWords=1)
    Refe = ParagraphStyle("Refe", parent=Pequeno, fontSize=12.5 if amp else 7.7, leading=17.5 if amp else 10.6, leftIndent=14 if amp else 9, firstLineIndent=-14 if amp else -9, spaceAfter=6 if amp else 3.5, alignment=TA_LEFT)
    TAM = {"kicker": (11, 15) if amp else (8.2, 11), "titulo": (26, 31) if amp else (19, 23),
           "subtitulo": (15, 20) if amp else (10.3, 14), "creditos": (12.5, 18) if amp else (8.4, 12.4),
           "toc_titulo": (15, 19) if amp else (10.2, 13), "toc_num": (14, 19) if amp else (9.6, 13)}
    REF_INLINE = 11.5 if amp else 6.2
    CODE_INLINE = 12 if amp else 7.6
    COND_DADOS = 190 if amp else 52
    COND_LINHA = 230 if amp else 110
    TABELA_BLOCOS_COLS = 3 if amp else 4
    TABELA_BLOCOS_MEDIA = 55 if amp else 105
    CEL_PAD_X = 5 if amp else 3.2
    CEL_PAD_Y = 4 if amp else 2.6
    RODAPE_FONTE = 8.4 if amp else 6.6
    EDICAO_TXT = ("edição digital em <b>fonte ampliada</b>, rediagramada para leitura confortável na tela "
                  "(corpo de 16 pt e tabelas convertidas em blocos; mesmo conteúdo e mesma data de corte: 23 de outubro de 2026). "
                  "Para imprimir, baixe o e-book A5 padrão no botão “PDF A5” do flipbook." if amp else
                  "e-book A5 para leitura e impressão, gerado a partir da página interativa do projeto "
                  "(mesmo conteúdo, mesma data de corte: 23 de outubro de 2026).")
    COMO_USAR_TXT = ("<b>Como usar esta edição ampliada.</b> Ela existe para ser lida na tela sem esforço: o texto foi "
                     "rediagramado em corpo grande e as tabelas largas viraram blocos sequenciais — por isso o número de páginas é "
                     "bem maior que o do e-book impresso. Vire as páginas pelas laterais, pelo controle deslizante ou pelas setas do "
                     "teclado, e use a tela cheia no computador. Cada capítulo começa em página nova e os gráficos viajam com suas "
                     "legendas. Antes de votar, confira os números nas fontes oficiais indicadas." if amp else
                     "<b>Como usar este e-book.</b> Cada capítulo começa em página nova e os gráficos viajam com suas legendas e textos de leitura. "
                     "No site, a mesma análise é interativa (filtros, dois idiomas, temas e acessibilidade) e há um flipbook HTML5 em fonte ampliada "
                     "para leitura na tela. Imprima em A5 ou leia na tela — e, antes de votar, confira os números nas fontes oficiais indicadas.")

aplicar_perfil("padrao")

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
            return inner + f' <font size="{REF_INLINE}" color="#555f6b">({escape(href)})</font>'
        return inner
    if no.name == "span" and "badge" in classes:
        cor = next((BADGE_COR[c] for c in classes if c in BADGE_COR), "#33475c")
        return f'<b><font color="{cor}">[{inner}]</font></b>'
    if no.name == "span" and "kicker" in classes: return f"<b>{inner}</b>"
    if no.name == "code": return f'<font name="{SANS}" size="{CODE_INLINE}">{inner}</font>'
    return inner

# Transição de candidato dentro do mesmo parágrafo: "…(p. 19); Flávio compromete-se…",
# "…risco (p. 35, 38). Flávio: …", "…custo.[8] Lula detalhou…", "; do lado de Lula, …".
_SPLIT_CAND = re.compile(
    r"(?<=[.;])\s+(?=(?:<b>)?(?:Lula|Flávio(?: Bolsonaro)?)(?::|,| é\b| nomeia\b| compromete-se\b| prometeu\b| detalhou\b| regula\b| prioriza\b| expande\b| aposta\b| enfatiza\b| desmonta\b))"
    r"|(?<=</super>)\s+(?=(?:Lula|Flávio)(?: detalhou\b| prometeu\b))"
    r"|(?<=;)\s+(?=do lado de (?:Lula|Flávio)\b)")

def _rebalanceia(partes):
    """Fecha no fim de cada trecho as tags inline abertas e as reabre no trecho seguinte."""
    pilha, out = [], []
    for parte in partes:
        ini = "".join(tag for _, tag in pilha)
        atual = list(pilha)
        for m in re.finditer(r"</?([a-zA-Z]+)(?:\s[^>]*)?>", parte):
            nome, s = m.group(1).lower(), m.group(0)
            if s.startswith("</"):
                for k in range(len(atual) - 1, -1, -1):
                    if atual[k][0] == nome:
                        del atual[k]; break
            elif nome not in ("br", "hr"):
                atual.append((nome, s))
        out.append(ini + parte + "".join(f"</{n}>" for n, _ in reversed(atual)))
        pilha = atual
    return out

def divide_candidatos(html_txt):
    """Separa em parágrafos os trechos de cada candidato quando os dois são sujeitos
    emendados no mesmo parágrafo. Sínteses comparativas sem transição de sujeito ficam intactas."""
    limpo = re.sub(r"<[^>]+>", " ", html_txt)
    if not (re.search(r"\bLula\b", limpo) and re.search(r"\bFlávio\b", limpo)):
        return [html_txt]
    partes = [x.strip() for x in _SPLIT_CAND.split(html_txt) if x.strip()]
    return _rebalanceia(partes) if len(partes) > 1 else [html_txt]

def anexa_paragrafos(story, html_txt, estilo, bulletText=None):
    for i, parte in enumerate(divide_candidatos(html_txt)):
        if bulletText is not None:
            story.append(Paragraph(parte, estilo, bulletText=bulletText if i == 0 else None))
        else:
            story.append(Paragraph(parte, estilo))

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
                story.append(CondPageBreak(COND_DADOS))
                story.append(Paragraph(
                    f"<b>{NOMES[cand]} · {escape(d['area'])}</b> — Tempo {d['tempo']} meses · Custo fiscal {d['custo']} · Impacto + {d['impacto']} · "
                    f"Dep. Estado {d['depE']} · Dep. sociedade {d['depS']} · Risco − {d['risco']}<br/><i>{escape(d['nota'])}</i>", DadosBloco))
        return
    grade, spans, cabec = grade_tabela(tbl)
    if not grade: return
    textos = [[(c.get_text(" ", strip=True) if isinstance(c, Tag) else "") for c in linha] for linha in grade]
    n = len(grade[0])
    media = sum(len(t) for linha in textos[1:] for t in linha) / max(1, (len(textos) - 1) * n)
    # Na edição ampliada, células mescladas (rowspan) impedem a quebra da tabela entre
    # páginas: repetimos o valor mesclado nas linhas seguintes e emitimos blocos.
    forcar_blocos = PERFIL_ATUAL == "ampliada" and bool(spans)
    if forcar_blocos:
        for c in range(n):
            ult, ult_txt = None, ""
            for r in range(len(grade)):
                if isinstance(grade[r][c], Tag):
                    ult, ult_txt = grade[r][c], textos[r][c]
                elif ult is not None:
                    grade[r][c], textos[r][c] = ult, ult_txt
    if forcar_blocos or (n >= TABELA_BLOCOS_COLS and media > TABELA_BLOCOS_MEDIA):  # tabela larga/mesclada → blocos legíveis por linha
        for linha, tlinha in zip(grade[1:], textos[1:]):
            story.append(CondPageBreak(COND_LINHA))
            story.append(Paragraph(inline(linha[0]) if isinstance(linha[0], Tag) else escape(tlinha[0]), H4e))
            for j in range(1, n):
                if isinstance(linha[j], Tag) and tlinha[j]:
                    rotulo = cabec[j] if j < len(cabec) and cabec[j] else ""
                    if rotulo:
                        cor_rot = LULA if rotulo.startswith("Lula") else (FLAV if rotulo.startswith("Flávio") else None)
                        txt_rot = f'<font color="{cor_rot}">{escape(rotulo)}</font>' if cor_rot else escape(rotulo)
                        story.append(Paragraph(txt_rot, H4e))
                    emite_filhos(linha[j], story, secao)
        return
    dados = []
    for r, linha in enumerate(grade):
        dados.append([Paragraph(inline(c), CelH if r == 0 else Cel) if isinstance(c, Tag) else "" for c in linha])
    pesos = [max(6.0, math.sqrt(max(len(textos[r][c]) for r in range(len(textos))))) for c in range(n)]
    soma = sum(pesos); larguras = [FW * p / soma for p in pesos]
    estilo = [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#b8ab8c")),
              ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), CEL_PAD_X), ("RIGHTPADDING", (0, 0), (-1, -1), CEL_PAD_X),
              ("TOPPADDING", (0, 0), (-1, -1), CEL_PAD_Y), ("BOTTOMPADDING", (0, 0), (-1, -1), CEL_PAD_Y),
              ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf6ea")])] + spans
    story.append(Table(dados, colWidths=larguras, repeatRows=1, style=TableStyle(estilo)))
    story.append(Spacer(1, 5))

CAIXA = {"info": ("#eef6ff", "#0b5fa5"), "warn": ("#fff8e1", "#9a6b00"), "danger": ("#fff0f3", "#a4133c"), "good": ("#eaf7ef", "#137547")}
BLOCOS = {"p", "ul", "ol", "div", "article", "table", "h3", "h4", "hr", "canvas"}

def emite_filhos(el, story, secao):
    buf = []
    def flush():
        t = "".join(buf).strip(); buf.clear()
        if t: anexa_paragrafos(story, t, Corpo)
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
        if el.get_text(strip=True): anexa_paragrafos(story, inline(el), estilo)
        return
    if nome in ("ul", "ol"):
        for i, li in enumerate(el.find_all("li", recursive=False), 1):
            if secao == "references":
                story.append(Paragraph(inline(li, refs=True), Refe))
            else:
                anexa_paragrafos(story, inline(li), Lista, bulletText=f"{i}." if nome == "ol" else "•")
        story.append(Spacer(1, 2)); return
    if nome == "hr": story.append(HRFlowable(width="100%", thickness=0.6, color=HexColor("#b8ab8c"), spaceBefore=5, spaceAfter=5)); return
    if nome == "canvas": figura(el.get("id"), story); return
    if nome == "table": tabela(el, story, secao); return
    if nome in ("div", "article"):
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
            story.append(CondPageBreak(150 if PERFIL_ATUAL == "ampliada" else 72))
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
    canv.setStrokeColor(OURO); canv.setLineWidth(0.8); canv.line(MARGEM_X, MARGEM_BASE-3.5*mm, A5[0]-MARGEM_X, MARGEM_BASE-3.5*mm)
    canv.setFont(SANS, RODAPE_FONTE); canv.setFillColor(CINZA)
    canv.drawString(MARGEM_X, MARGEM_BASE-7.5*mm, "Eleições Presidenciais 2026 — Análise Comparativa · by rogerelizar")
    canv.drawRightString(A5[0]-MARGEM_X, MARGEM_BASE-7.5*mm, str(doc.page))
    canv.drawRightString(A5[0]-MARGEM_X, A5[1]-(MARGEM_TOPO-5*mm), "2º Turno 2026 - Criado por IA")
    canv.restoreState()

def criar_doc(caminho, titulo):
    doc = LivroDoc(str(caminho), pagesize=A5, leftMargin=MARGEM_X, rightMargin=MARGEM_X, topMargin=MARGEM_TOPO, bottomMargin=MARGEM_BASE,
                   title=titulo,
                   author="by rogerelizar (curadoria) / Arena.ai — Agent Mode (montagem por IA)")
    doc.addPageTemplates([
        PageTemplate(id="capa", frames=[Frame(0, 0, A5[0], A5[1])], onPage=on_capa),
        PageTemplate(id="miolo", frames=[Frame(MARGEM_X, MARGEM_BASE, FW, A5[1]-MARGEM_TOPO-MARGEM_BASE)], onPage=on_miolo),
        PageTemplate(id="contracapa", frames=[Frame(0, 0, A5[0], A5[1])], onPage=on_contra),
    ])
    return doc

def montar(paginas_caps):
    story = [Spacer(1, 1), NextPageTemplate("miolo"), PageBreak()]
    story.append(Paragraph("ELEIÇÕES PRESIDENCIAIS 2026 · 2º TURNO", ParagraphStyle("k", fontName=SANS, fontSize=TAM["kicker"][0], leading=TAM["kicker"][1], textColor=OURO, alignment=TA_CENTER)))
    story.append(Paragraph("Dois projetos de Brasil em disputa", ParagraphStyle("tt", fontName=SERIF, fontSize=TAM["titulo"][0], leading=TAM["titulo"][1], textColor=NAVY, alignment=TA_CENTER, spaceBefore=6, spaceAfter=3)))
    story.append(Paragraph("Análise comparativa completa dos programas de governo — Lula (PT) × Flávio Bolsonaro (PL)", ParagraphStyle("ts", fontName="DVSerif-I", fontSize=TAM["subtitulo"][0], leading=TAM["subtitulo"][1], textColor=CINZA, alignment=TA_CENTER, spaceAfter=6)))
    story.append(HRFlowable(width="42%", thickness=1.4, color=OURO, hAlign="CENTER", spaceBefore=3, spaceAfter=8))
    story.append(Paragraph("<b>Curadoria:</b> by rogerelizar (forneceu apenas os prompts e os dois PDFs oficiais registrados no TSE).<br/><b>Pesquisa, redação, gráficos e montagem:</b> inteligência artificial — Arena.ai (Agent Mode).<br/><b>Publicação:</b> " + escape(PUB) + ".<br/><b>Edição:</b> " + EDICAO_TXT + "", ParagraphStyle("cr", fontName=SANS, fontSize=TAM["creditos"][0], leading=TAM["creditos"][1], alignment=TA_CENTER, textColor=HexColor("#2c333d"), spaceAfter=7)))
    story.append(Paragraph("<b>Isenção do curador.</b> O curador limitou-se a formular os prompts e a anexar os programas oficiais. Não redigiu, não revisou previamente linha a linha e não endossa necessariamente interpretações, notas de viabilidade ou alertas deste relatório — responsabilidade editorial da montagem por IA, sujeita a conferência nas fontes citadas. Um prompt em PDF (a versão que gera esta análise em formato A5) está disponível para download no menu da página; o prompt completo do site fica arquivado no repositório do projeto.", Corpo))
    story.append(Paragraph(COMO_USAR_TXT, Corpo))
    if KPIS:
        story.append(Paragraph("A eleição em números", H3e))
        for b, s in KPIS:
            story.append(Paragraph(f"<b>{escape(b)}</b> — {escape(s)}", Lista, bulletText="▸"))
    story.append(PageBreak())
    story.append(Paragraph("Sumário", ParagraphStyle("Sumario", parent=Capitulo)))
    story.append(HRFlowable(width="100%", thickness=0.8, color=OURO, spaceBefore=2, spaceAfter=7))
    tocT = ParagraphStyle("tocT", fontName=SERIF, fontSize=TAM["toc_titulo"][0], leading=TAM["toc_titulo"][1], textColor=NAVY)
    tocN = ParagraphStyle("tocN", fontName=SANS, fontSize=TAM["toc_num"][0], leading=TAM["toc_num"][1], textColor=NAVY, alignment=2)
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

def gerar_pdf(perfil, caminho, titulo):
    global GRAF
    aplicar_perfil(perfil)
    GRAF = gerar_graficos()
    print(f"[{perfil}] gráficos:", [p.name for v in GRAF.values() for p, _ in v])
    doc1 = criar_doc(f"/tmp/ebook_{perfil}_pass1.pdf", titulo); doc1.build(montar(None))
    caps = list(doc1.capitulos)
    print(f"[{perfil}] capítulos (páginas):", caps)
    doc2 = criar_doc(caminho, titulo); doc2.build(montar(caps))
    assert list(doc2.capitulos) == caps, "paginação do sumário divergiu entre passes"
    with fitz.open(caminho) as dd:
        total = len(dd)
    print(f"[{perfil}] PDF pages={total} bytes={pathlib.Path(caminho).stat().st_size} -> {caminho}")
    return caps, total

sai_pdf = RAIZ / "downloads" / "Analise-2026-Ebook-A5.pdf"
_caps_std, npag_ebook = gerar_pdf("padrao", sai_pdf,
    "Eleições Presidenciais 2026 — Análise Comparativa dos Programas de Governo (e-book A5)")
pdf_ampliado = TMP / "Analise-2026-Flipbook-Fonte-Ampliada.pdf"
_caps_amp, npag = gerar_pdf("ampliada", pdf_ampliado,
    "Eleições Presidenciais 2026 — Análise Comparativa dos Programas de Governo (flipbook em fonte ampliada)")
d = fitz.open(pdf_ampliado)

# ---------------- flipbook HTML5 (arquivo único) ----------------
# Motor v2: desktop = spread de 2 páginas centrado (capa centraliza sozinha);
# mobile = página única centrada, virada sobre a lombada; pool de 4 <img>
# reutilizadas (decode preguiçoso), imagens WebP 190 dpi (fallback JPEG).
# Fonte das páginas: PDF "ampliado" (corpo 16 pt) — NÃO o e-book de impressão.
from PIL import features as _pil_features
_USA_WEBP = bool(_pil_features.check("webp"))
_FMT, _MIME = ("WEBP", "image/webp") if _USA_WEBP else ("JPEG", "image/jpeg")
paginas_uri = []
for pg in range(npag):
    pix = d[pg].get_pixmap(dpi=190, alpha=False)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    buf = io.BytesIO()
    if _USA_WEBP:
        im.save(buf, "WEBP", quality=74, method=6)
    else:
        im.save(buf, "JPEG", quality=75, optimize=True)
    paginas_uri.append(f"data:{_MIME};base64," + base64.b64encode(buf.getvalue()).decode())
print(f"flipbook: {npag} páginas em {_FMT} 190dpi")

FLIP = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#17130c">
<title>Eleições Presidenciais 2026 — Flipbook em fonte ampliada | Lula (PT) × Flávio Bolsonaro (PL)</title>
<meta name="description" content="Flipbook HTML5 em fonte ampliada da análise comparativa dos programas de governo — 2º turno 2026. Curadoria: by rogerelizar. Criado por IA (Arena.ai — Agent Mode).">
<style>
:root{--dur:860ms;--ease:cubic-bezier(.22,.68,.26,1);--ouro:#d8a24a;--papel:#fbf7ec}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;min-height:100dvh;display:flex;flex-direction:column;align-items:center;overflow-x:hidden;padding:12px 12px calc(16px + env(safe-area-inset-bottom,0px));font-family:Georgia,'Times New Roman',serif;color:#f2e9d8;background:#17130c radial-gradient(1000px 540px at 50% -6%,rgba(216,162,74,.15),transparent 62%)}
header{width:min(100%,920px);margin-inline:auto;text-align:center}
.k{font-family:Verdana,Geneva,sans-serif;letter-spacing:.18em;font-size:.66rem;color:var(--ouro);text-transform:uppercase}
h1{font-size:clamp(1.22rem,3.6vw,1.85rem);line-height:1.15;margin:.32rem 0 .18rem}
#palco{width:100%;flex:1 1 auto;min-height:0;display:grid;place-items:center;padding:12px 0 8px;perspective:2800px;perspective-origin:50% 48%}
#livro{position:relative;margin-inline:auto;transform-style:preserve-3d;transition:transform var(--dur) var(--ease),width .35s ease;touch-action:pan-y;user-select:none;-webkit-user-select:none;cursor:pointer;border-radius:6px}
#livro.spread{width:min(97vw,1400px,max(300px,calc((100vh - 190px)*1.4095238)));width:min(97vw,1400px,max(300px,calc((100dvh - 190px)*1.4095238)));aspect-ratio:296/210}
#livro.single{width:min(97vw,720px,max(270px,calc((100vh - 190px)*.7047619)));width:min(97vw,720px,max(270px,calc((100dvh - 190px)*.7047619)));aspect-ratio:148/210}
#livro.spread.closed-front{transform:translateX(-25%)}
#livro.spread.closed-back{transform:translateX(25%)}
#livro:focus-visible{outline:3px solid #f0c169;outline-offset:5px}
.page,.face{position:absolute;top:0;height:100%;overflow:hidden;background:var(--papel)}
.page{z-index:1}
#livro.spread .page.left{box-shadow:-14px 22px 38px rgba(0,0,0,.38)}
#livro.spread .page.right{box-shadow:14px 22px 38px rgba(0,0,0,.38)}
#livro.single .page.right{box-shadow:0 24px 48px rgba(0,0,0,.50)}
.face{box-shadow:0 10px 28px rgba(0,0,0,.25)}
#livro.spread .page.left{left:0;width:50%;border-radius:9px 2px 2px 9px}
#livro.spread .page.right{left:50%;width:50%;border-radius:2px 9px 9px 2px}
#livro.single .page.left{display:none}
#livro.single .page.right{left:0;width:100%;border-radius:7px}
#livro.spread.closed-front .page.left{visibility:hidden}
#livro.spread.closed-back .page.right{visibility:hidden}
.page img,.face img{width:100%;height:100%;display:block;object-fit:contain;background:var(--papel);-webkit-user-drag:none}
.page.blank img,.face.paper img{display:none}
.page.blank{background:linear-gradient(135deg,#efe7d2,#e2d5b4)}
.blank-label,.paper-back{position:absolute;inset:0;display:none;align-items:center;justify-content:center;text-align:center;padding:18px;color:#7a6f57;font-style:italic;font-size:clamp(.8rem,2.2vw,1rem)}
.page.blank .blank-label{display:flex}
.shade,.face-shade{position:absolute;inset:0;pointer-events:none}
#livro.spread .page.left .shade{background:linear-gradient(90deg,rgba(0,0,0,.06),transparent 13%,transparent 76%,rgba(0,0,0,.24) 96%,rgba(0,0,0,.40))}
#livro.spread .page.right .shade{background:linear-gradient(270deg,rgba(0,0,0,.06),transparent 13%,transparent 76%,rgba(0,0,0,.24) 96%,rgba(0,0,0,.40))}
#livro.single .page.right .shade{background:linear-gradient(90deg,rgba(0,0,0,.20),transparent 7%,transparent 94%,rgba(0,0,0,.10))}
.spine{position:absolute;top:0;bottom:0;left:calc(50% - 1px);width:2px;z-index:20;pointer-events:none;background:linear-gradient(180deg,rgba(90,70,30,.05),rgba(90,70,30,.38),rgba(90,70,30,.05))}
#livro.single .spine{display:none}
#turning{position:absolute;top:0;height:100%;z-index:30;display:none;pointer-events:none;transform-style:preserve-3d;will-change:transform;transform:rotateY(0deg)}
#livro.spread #turning{left:50%;width:50%;transform-origin:left center}
#livro.single #turning{left:0;width:100%;transform-origin:left center}
#turning.on{display:block}
#turning.animate{transition:transform var(--dur) var(--ease)}
#turning.flipped{transform:rotateY(-180deg)}
.face{inset:0;width:100%;backface-visibility:hidden;-webkit-backface-visibility:hidden}
.face.front{transform:translateZ(.7px);border-radius:2px 9px 9px 2px}
.face.back{transform:rotateY(180deg) translateZ(.7px);border-radius:9px 2px 2px 9px}
#livro.single .face.front,#livro.single .face.back{border-radius:7px}
.face.paper{background:linear-gradient(135deg,#f3ecd9,#e6dab9)}
.face.paper .paper-back{display:flex}
.face-shade{opacity:0;background:linear-gradient(90deg,rgba(0,0,0,.46),rgba(0,0,0,.10) 42%,rgba(255,255,255,.12) 58%,rgba(0,0,0,.20))}
#turning.animating .face.front .face-shade{animation:sombraFrente var(--dur) ease-in-out both}
#turning.animating .face.back .face-shade{animation:sombraVerso var(--dur) ease-in-out both}
@keyframes sombraFrente{0%{opacity:0}45%{opacity:.62}100%{opacity:.30}}
@keyframes sombraVerso{0%{opacity:.68}55%{opacity:.34}100%{opacity:0}}
.hint{position:absolute;top:50%;z-index:25;width:44px;height:44px;margin-top:-22px;border-radius:50%;display:grid;place-items:center;background:rgba(23,19,12,.55);color:#fff;font-family:Verdana,sans-serif;font-size:1.35rem;opacity:0;transition:opacity .25s;pointer-events:none}
.hint.prev{left:10px}.hint.next{right:10px}
@media(hover:hover){#livro:hover .hint{opacity:.88}}
.controls,.progresso{width:min(96vw,900px);margin-inline:auto;font-family:Verdana,Geneva,sans-serif}
.controls{display:flex;gap:8px;align-items:center;justify-content:center;flex-wrap:wrap}
button,a.btn{min-height:44px;padding:10px 15px;border-radius:7px;border:2px solid var(--ouro);background:var(--ouro);color:#17130c;font:inherit;font-weight:700;font-size:.9rem;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;justify-content:center}
button.ghost,a.btn.ghost{background:transparent;color:#f2e9d8;border-color:#a08c5f}
button:disabled{opacity:.36;cursor:default}
#contador{font-size:.89rem;min-width:158px;text-align:center}
.progresso{display:flex;align-items:center;gap:10px;margin-top:9px;font-size:.74rem;opacity:.92}
.progresso input[type=range]{flex:1;accent-color:var(--ouro);height:28px;cursor:pointer}
.dica{font-family:Verdana,Geneva,sans-serif;font-size:.71rem;opacity:.72;text-align:center;margin:7px auto 0;max-width:900px}
:focus-visible{outline:3px solid #f0c169;outline-offset:2px}
@media(max-width:820px){
 body{padding:9px 7px calc(12px + env(safe-area-inset-bottom,0px))}
 #palco{padding:8px 0 6px}
 #livro.single{width:min(97.5vw,720px,max(270px,calc((100vh - 190px)*.7047619)));width:min(97.5vw,720px,max(270px,calc((100dvh - 190px)*.7047619)))}
 button,a.btn{padding:9px 12px;font-size:.86rem}
 #contador{min-width:132px;font-size:.84rem}
}
/* ---------- TELA CHEIA ---------- */
body.fs{height:100dvh;overflow:hidden;padding:8px 0 calc(8px + env(safe-area-inset-bottom,0px))}
body.fs .k,body.fs .progresso,body.fs .dica{display:none}
body.fs header{flex:0 0 auto}
body.fs h1{margin:0}
body.fs #palco{padding:6px 0 2px}
body.fs .controls{flex:0 0 auto;width:100%;margin:4px 0 0}
body.fs #contador{font-weight:700;font-size:.95rem}
body.fs .controls>button,body.fs .controls>a.btn{box-shadow:0 10px 24px rgba(0,0,0,.45)}
@media(min-width:821px){
 body.fs #livro.spread{width:min(1520px,calc(100vw - 252px),max(320px,calc((100dvh - 118px)*1.4095238)))}
 body.fs #livro.single{width:min(760px,calc(100vw - 252px),max(270px,calc((100dvh - 118px)*.7047619)))}
 body.fs .controls>button,body.fs .controls>a.btn{position:fixed;z-index:60;max-width:112px;white-space:normal;text-align:center;line-height:1.18}
 body.fs a.principal{left:14px;top:58px}
 body.fs #tela{right:14px;top:58px}
 body.fs #inicio{left:14px;top:calc(50% - 122px)}
 body.fs #ant{left:14px;top:calc(50% - 58px)}
 body.fs #fim{right:14px;top:calc(50% - 122px)}
 body.fs #prox{right:14px;top:calc(50% - 58px)}
 body.fs a.pdf{left:14px;bottom:58px}
}
@media(max-width:820px){
 body.fs .controls>button,body.fs .controls>a.btn{display:none!important}
 body.fs #livro.single{width:min(98vw,max(270px,calc((100dvh - 106px)*.7047619)))}
 body.fs h1{font-size:clamp(.98rem,4.6vw,1.2rem);padding-inline:8px}
}
@media(prefers-reduced-motion:reduce){:root{--dur:1ms}#turning.animating .face-shade{animation:none}}
</style>
</head>
<body>
<header>
<div class="k">Eleições Presidenciais 2026 · 2º turno · Flipbook em fonte ampliada</div>
<h1>Dois projetos de Brasil em disputa</h1>
</header>
<section id="palco" aria-label="Livro digital">
  <div id="livro" class="spread closed-front" tabindex="0" role="application" aria-label="Flipbook. Use as setas esquerda e direita para virar as páginas.">
    <div class="page static left blank"><img id="imgLeft" alt=""><div class="blank-label"></div><div class="shade"></div></div>
    <div class="page static right"><img id="imgRight" alt=""><div class="blank-label"></div><div class="shade"></div></div>
    <div id="turning" aria-hidden="true">
      <div class="face front"><img id="imgFront" alt=""><div class="face-shade"></div></div>
      <div class="face back" id="faceBack"><img id="imgBack" alt=""><div class="paper-back">by rogerelizar</div><div class="face-shade"></div></div>
    </div>
    <div class="spine"></div>
    <div class="hint prev" aria-hidden="true">‹</div>
    <div class="hint next" aria-hidden="true">›</div>
  </div>
</section>
<div class="controls">
  <button type="button" id="inicio" class="ghost" aria-label="Ir para o início">⏮ Início</button>
  <button type="button" id="ant">◀ Anterior</button>
  <span id="contador" aria-live="polite"></span>
  <button type="button" id="prox">Próxima ▶</button>
  <button type="button" id="fim" class="ghost" aria-label="Ir para o fim">Fim ⏭</button>
  <button type="button" id="tela" class="ghost">Tela cheia</button>
  <a class="btn principal" href="../analise.html">⌂ Página principal</a>
  <a class="btn ghost pdf" href="Analise-2026-Ebook-A5.pdf" download>⬇ PDF A5</a>
</div>
<div class="progresso"><span>1</span><input id="slider" type="range" min="1" step="1" value="1" aria-label="Ir para a página"><span id="totalPag"></span></div>
<p class="dica">Edição digital em <strong>fonte ampliada</strong>, feita para ler na tela sem esforço. No computador, o livro abre em duas páginas centradas; no celular, em página única. Toque nas laterais, deslize o dedo ou use ← →. Funciona sem internet.</p>
<noscript><p class="dica">Ative o JavaScript para folhear — ou baixe o PDF A5 acima.</p></noscript>
<script>const PAGES=__PAGES_JSON__;</script>
<script>
(function(){
"use strict";
var total=PAGES.length;
var livro=document.getElementById("livro"), turn=document.getElementById("turning"), faceBack=document.getElementById("faceBack");
var imgL=document.getElementById("imgLeft"), imgR=document.getElementById("imgRight"), imgF=document.getElementById("imgFront"), imgB=document.getElementById("imgBack");
var elL=imgL.parentElement, elR=imgR.parentElement;
var contador=document.getElementById("contador"), slider=document.getElementById("slider");
var bIni=document.getElementById("inicio"), bAnt=document.getElementById("ant"), bProx=document.getElementById("prox"), bFim=document.getElementById("fim"), bTela=document.getElementById("tela");
var mq=window.matchMedia("(max-width: 820px)");
var reduz=window.matchMedia("(prefers-reduced-motion: reduce)");
var mode=mq.matches?"single":"spread";
var anchor=0, spread=0, page=0, animating=false, finishFn=null, finishTimer=0, tokenSeq=0, suppressClick=0;
var maxSpread=Math.ceil((total-1)/2);
var preloaded={};
slider.max=String(total); document.getElementById("totalPag").textContent=String(total);

function duracao(){ return reduz.matches?30:(mode==="single"?680:860); }
function spreadPages(s){
  if(s<=0) return [null,0];
  var l=2*s-1, r=2*s;
  return [l<total?l:null, r<total?r:null];
}
function preload(centro){
  for(var i=centro-2;i<=centro+5;i++){
    if(i>=0&&i<total&&!preloaded[i]){ preloaded[i]=1; var im=new Image(); im.src=PAGES[i]; }
  }
}
function setImg(img, idx){
  var cont=img.parentElement;
  if(idx===null||idx===undefined){
    img.removeAttribute("src"); img.alt=""; delete img.dataset.page;
    if(cont.classList.contains("page")) cont.classList.add("blank");
    return;
  }
  cont.classList.remove("blank");
  if(img.dataset.page!==String(idx)){ img.src=PAGES[idx]; img.dataset.page=String(idx); }
  img.alt="Página "+(idx+1)+" de "+total;
}
function limites(){
  return {
    podeAnt: !animating && (mode==="single" ? page>0 : spread>0),
    podeProx: !animating && (mode==="single" ? page<total-1 : spread<maxSpread)
  };
}
function botoes(){
  var l=limites();
  bAnt.disabled=!l.podeAnt; bIni.disabled=!l.podeAnt;
  bProx.disabled=!l.podeProx; bFim.disabled=!l.podeProx;
  slider.disabled=animating;
}
function sincroniza(){
  anchor=Math.max(0,Math.min(total-1,anchor));
  page=anchor;
  spread=page===0?0:Math.min(maxSpread,Math.ceil(page/2));
  if(mode==="spread") anchor=spread===0?0:Math.min(2*spread-1,total-1);
}
function render(){
  sincroniza();
  livro.style.setProperty("--dur", duracao()+"ms");
  livro.classList.toggle("single",mode==="single");
  livro.classList.toggle("spread",mode==="spread");
  if(mode==="single"){
    livro.classList.remove("closed-front","closed-back");
    setImg(imgL,null); setImg(imgR,page);
    contador.textContent="Página "+(page+1)+" de "+total;
    slider.value=String(page+1);
  }else{
    var pr=spreadPages(spread), l=pr[0], r=pr[1];
    livro.classList.toggle("closed-front",l===null&&r!==null);
    livro.classList.toggle("closed-back",r===null&&l!==null);
    setImg(imgL,l); setImg(imgR,r);
    contador.textContent = l===null ? ("Capa · Página "+(r+1)+" de "+total)
      : (r===null ? ("Página "+(l+1)+" de "+total) : ("Páginas "+(l+1)+"–"+(r+1)+" de "+total));
    slider.value=String(anchor+1);
  }
  livro.setAttribute("aria-label","Flipbook, "+contador.textContent+". Use as setas esquerda e direita para virar as páginas.");
  botoes(); preload(anchor);
}
function concluir(novoAnchor, token){
  if(token!==tokenSeq) return;
  window.clearTimeout(finishTimer); finishFn=null; animating=false;
  turn.classList.remove("on","animate","animating","flipped");
  anchor=novoAnchor; render();
}
function virar(op){
  if(animating) return;
  animating=true; botoes();
  if(mode==="spread"){
    var destino=op.targetSpread;
    var dp=spreadPages(destino);
    livro.classList.toggle("closed-front",dp[0]===null&&dp[1]!==null);
    livro.classList.toggle("closed-back",dp[1]===null&&dp[0]!==null);
    setImg(imgL,op.underLeft); setImg(imgR,op.underRight);
  }else{
    setImg(imgR,op.underRight);
  }
  faceBack.classList.toggle("paper",!!op.paper);
  setImg(imgF,op.front);
  if(op.paper){ imgB.removeAttribute("src"); imgB.alt=""; delete imgB.dataset.page; }
  else setImg(imgB,op.back);
  turn.classList.remove("animate","animating","flipped");
  turn.classList.add("on");
  if(op.fromFlipped) turn.classList.add("flipped");
  void turn.offsetWidth;
  var token=++tokenSeq;
  finishFn=function(){ concluir(op.newAnchor,token); };
  finishTimer=window.setTimeout(function(){ if(finishFn){ var f=finishFn; finishFn=null; f(); } }, duracao()+90);
  window.requestAnimationFrame(function(){
    window.requestAnimationFrame(function(){
      turn.classList.add("animate","animating");
      turn.classList.toggle("flipped",!!op.toFlipped);
    });
  });
}
turn.addEventListener("transitionend",function(e){
  if(e.propertyName==="transform"&&finishFn){ var f=finishFn; finishFn=null; window.clearTimeout(finishTimer); f(); }
});
function proxima(){
  if(animating) return;
  if(mode==="single"){
    if(page>=total-1) return;
    virar({front:page,paper:true,fromFlipped:false,toFlipped:true,newAnchor:page+1,underRight:page+1});
  }else{
    if(spread>=maxSpread) return;
    var atual=spreadPages(spread), dest=spreadPages(spread+1);
    virar({front:atual[1],back:dest[0],fromFlipped:false,toFlipped:true,
           newAnchor:dest[0]!==null?dest[0]:dest[1],underLeft:atual[0],underRight:dest[1],targetSpread:spread+1});
  }
}
function anterior(){
  if(animating) return;
  if(mode==="single"){
    if(page<=0) return;
    virar({front:page-1,paper:true,fromFlipped:true,toFlipped:false,newAnchor:page-1,underRight:page});
  }else{
    if(spread<=0) return;
    var atual=spreadPages(spread), dest=spreadPages(spread-1);
    virar({front:dest[1],back:atual[0],fromFlipped:true,toFlipped:false,
           newAnchor:dest[0]!==null?dest[0]:dest[1],underLeft:dest[0],underRight:atual[1],targetSpread:spread-1});
  }
}
function irPara(novoAnchor){
  if(animating) return;
  anchor=novoAnchor; render();
}
bProx.addEventListener("click",proxima);
bAnt.addEventListener("click",anterior);
bIni.addEventListener("click",function(){irPara(0);});
bFim.addEventListener("click",function(){irPara(total-1);});
slider.addEventListener("input",function(){ irPara(Number(slider.value)-1); });
function sincronizarTela(){
  var fs=!!(document.fullscreenElement||document.webkitFullscreenElement);
  document.body.classList.toggle("fs",fs);
  bTela.textContent=fs?"Sair da tela cheia":"Tela cheia";
}
document.addEventListener("fullscreenchange",sincronizarTela);
document.addEventListener("webkitfullscreenchange",sincronizarTela);
bTela.addEventListener("click",function(){
  if(document.fullscreenElement||document.webkitFullscreenElement){ (document.exitFullscreen||document.webkitExitFullscreen).call(document); }
  else if(document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
  else if(document.documentElement.webkitRequestFullscreen) document.documentElement.webkitRequestFullscreen();
});
livro.addEventListener("click",function(e){
  if(Date.now()<suppressClick) return;
  var r=livro.getBoundingClientRect(), x=(e.clientX-r.left)/r.width;
  if(mode==="spread"){ if(x<0.5)anterior(); else proxima(); }
  else{ if(x<0.30)anterior(); else if(x>0.70)proxima(); }
});
var ta=null, tx=0, ty=0;
livro.addEventListener("touchstart",function(e){ var t=e.changedTouches[0]; tx=t.clientX; ty=t.clientY; },{passive:true});
livro.addEventListener("touchend",function(e){
  var t=e.changedTouches[0], dx=t.clientX-tx, dy=t.clientY-ty;
  if(Math.abs(dx)>44&&Math.abs(dx)>Math.abs(dy)*1.25){
    suppressClick=Date.now()+350;
    if(dx<0)proxima(); else anterior();
  }
},{passive:true});
document.addEventListener("keydown",function(e){
  var tag=(e.target&&e.target.tagName)||"";
  if(tag==="INPUT"||tag==="TEXTAREA"||tag==="SELECT") return;
  if(e.key==="ArrowRight"||e.key==="PageDown"){ e.preventDefault(); proxima(); }
  else if(e.key==="ArrowLeft"||e.key==="PageUp"){ e.preventDefault(); anterior(); }
  else if(e.key==="Home"){ e.preventDefault(); irPara(0); }
  else if(e.key==="End"){ e.preventDefault(); irPara(total-1); }
});
function trocarModo(){
  var novo=mq.matches?"single":"spread";
  if(novo===mode) return;
  if(finishFn){ var f=finishFn; finishFn=null; window.clearTimeout(finishTimer); f(); }
  mode=novo; render();
}
if(mq.addEventListener) mq.addEventListener("change",trocarModo);
else if(mq.addListener) mq.addListener(trocarModo);
render();
})();
</script>
</body>
</html>
"""

sai_flip = RAIZ / "downloads" / "Analise-2026-Flipbook.html"
sai_flip.write_text(FLIP.replace("__PAGES_JSON__", json.dumps(paginas_uri, separators=(",", ":"))), encoding="utf-8")
print(f"FLIPBOOK bytes={sai_flip.stat().st_size} paginas={npag} formato={_FMT}")
