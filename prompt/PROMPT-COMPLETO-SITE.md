# Prompt completo — Site “Análise Comparativa 2026” e todos os complementos

> ⚠️ **Arquivo interno do repositório. NÃO é disponibilizado para download no site.**
> O download oferecido aos leitores é outro documento: `prompt/prompt-analise-a5.md`
> (renderizado em `downloads/Prompt-Analise-A5.pdf`), que gera apenas a análise em PDF A5.
> **Este** é o prompt consolidado que origina **o site inteiro e seus complementos**
> (página bilíngue, menu flutuante, estilos visuais, e-book A5, flipbook e a divisão de prompts).
> Os Anexos preservam o histórico fiel dos pedidos do curador **by rogerelizar**.

---

# PARTE I — O PROMPT COMPLETO (consolidado)

## 1. Papel

Atue como desenvolvedor full-stack sênior, engenheiro de prompt e cientista político (economia política, relações internacionais, jornalismo investigativo). Rigor epistemológico, consciência institucional e **neutralidade estrita** — sem endosso e sem recomendação de voto; a mesma régua jurídico-fiscal para os dois lados.

## 2. Entradas

Dois PDFs oficiais registrados no TSE (2º turno presidencial de 2026), arquivados em `fontes-primarias/`:

- **Luiz Inácio Lula da Silva (PT, nº 13)** — `PropostasLula.pdf` (84 pp.; vice Geraldo Alckmin, PSB; coligação “Brasil Pronto pra Mais”);
- **Flávio Bolsonaro (PL, nº 22)** — `PropostasFlavio.pdf` (76 pp.; vice Alfredo Gaspar, PL; partido isolado).

Cite os candidatos **sempre pelo nome** (nunca por letras/códigos). Ordem: número de urna (13 antes de 22).

## 3. Fontes oficiais obrigatórias para dados em tempo real

TSE (DivulgaCandContas; Resultados) · Constituição Federal · Lei nº 8.213/1991 (auxílio-reclusão) · Lei nº 13.260/2016 (terrorismo) · LGPD (inclusive saúde/biometria) · BCB · IBGE · INPE/TerraBrasilis (PRODES) · Tesouro Transparente/Nacional (e IFI para dívida). Jornalismo apenas para declarações públicas de campanha, identificado como tal. **Nunca inventar dados:** sem verificação, escrever literalmente “Data pending verification from TSE”. Toda afirmação pesquisada com nota de rodapé/referência numerada.

## 4. Método em três camadas (nunca misturar)

(i) texto dos PDFs, com página; (ii) declarações públicas posteriores, com fonte; (iii) avaliação analítica do autor (notas de viabilidade), declarada e auditável.

## 5. Conteúdo analítico (idêntico em site, e-book e flipbook)

1. **Apresentação (introdução):** boas-vindas e finalidade; *disclaimer* de isenção do curador **by rogerelizar** (forneceu apenas o prompt e os dois PDFs; não redigiu/revisou previamente nem endossa necessariamente a análise) informando que **um prompt em PDF (versão que gera a análise em e-book A5) está para download no ☰ Menu** e que **o prompt completo fica arquivado no repositório, sem download**; chamado à cidadania responsável (fontes oficiais, voto correto e consciente em 25/10/2026, 8h–17h de Brasília); **fechar com data e hora da publicação** em `America/Sao_Paulo` (elemento `<time>` com `datetime` ISO + créditos).
2. **Como ler (metodologia):** fontes primárias; fontes oficiais de checagem; o que são as notas; convenções (nomes; idiomas — PT principal/autoritativo, EN secundário com evidências literais preservadas em PT; estilos visuais só mudam apresentação; **rótulos simétricos** — ver § 7).
3. **Perfis e votos:** cartões dos candidatos (quem é, vice, posicionamento, coligação, votos exatos do 1º turno e leitura institucional); gráfico de barras dos votos nominais; tabela de totalização final (TSE); **espectro ideológico das alianças formais** (partido/federação, posição convencional, traço dominante — PT com “(lulismo)” e PL com “(bolsonarismo)”, mesmo formato) com nota de base comum; estrutura dos dois programas.
4. **Matriz comparativa (12 áreas):** economia/impostos; segurança/justiça penal; saúde (SUS); educação; proteção social/trabalho/renda; mulheres/igualdade/cuidados; habitação/cidades/saneamento; infraestrutura/logística/energia; agro/alimentos/terra; meio ambiente/clima; democracia/Estado/digital; política externa/defesa/soberania. Proposta central de cada PDF (páginas) + relação (idêntica, similar divergente, oposta…) com selo.
5. **Modelagem de viabilidade (Chart.js):** conjunto único auditável `POLICY_DATA` (12 áreas × 2; tempo em meses; custo fiscal, impacto +, dependência Estado, dependência sociedade, risco −, tudo 0–10; justificativa breve) alimentando: bolhas tempo × custo (raio = impacto), radar de médias (tempo/48×10), barras agrupadas impacto × dependências com alternância de candidato, bolhas risco × tempo (raio = custo), filtro por área, tabela completa dos dados e régua de codificação publicada.
6. **Sumário investigativo:** 6.1 idênticas/equivalentes; 6.2 similares com vieses nomeados; 6.3 mapa de fricção institucional (Legislativo/Judiciário/subnacionais + instrumento); 6.4 promessas sinalizadas (populismo fiscal/incompatibilidade/inexequibilidade) **só** com fundamento em fonte oficial, agrupadas sob o nome de cada candidato (“Lula, alerta n” / “Flávio Bolsonaro, alerta n”) + alerta comum.
7. **Temas sensíveis:** posição × posição e motivação provável (interpretação declarada).
8. **Evolução 1º → 2º turno:** sem novo plano registrado (Lei nº 9.504/1997, art. 11, § 1º, IX); acréscimos, viradas e ambiguidades com fontes datadas.
9. **Contexto oficial + veredito:** fotografia BCB/Tesouro-IFI/IBGE/INPE na data de corte (23/10/2026); veredito comparativo sem recomendação (“Se vencer Lula, espere… / Se vencer Flávio Bolsonaro, espere…”).
10. **Fontes e notas:** referências numeradas (oficiais primeiro), notas de neutralidade e de impressão.

## 6. Entrega web — `index.html` (documento único)

- HTML5 válido, autocontido (única dependência externa: Chart.js 4.4.1 via CDN no `<head>`); `lang="pt-BR"`; ids semânticos estáveis: `introduction, methodology, electoral_profiles, candidate_A_profile, candidate_B_profile, candidate_A_proposals, candidate_B_proposals, comparative_matrix, feasibility_modeling, investigative_summary, sensitive_themes, proposal_evolution, official_context, references` (ids são internos; o texto visível usa sempre os **nomes**).
- **Créditos no subtítulo (byline):** “Curadoria: **by rogerelizar** · Pesquisa, redação, gráficos e montagem por inteligência artificial: **Arena.ai — Agent Mode**” (nunca nomear modelo subjacente).
- **Bilíngue:** PT principal (padrão) e EN secundário — interface, títulos, aberturas, cabeçalhos, gráficos (rótulos/títulos/tooltips), controles e textos novos traduzidos; evidências literais, páginas e títulos de fontes permanecem em PT com aviso de transparência em EN.
- **Botão flutuante único ☰ Menu** (hambúrguer, canto inferior direito, com `safe-area`): é a **única** porta de opções. O painel (`<dialog>` acessível: Esc fecha, foco retorna) contém: 🧭 Índice das 10 seções (clicar fecha e rola) · idioma PT/EN · tema claro/escuro/automático · estilo visual · acessibilidade (tamanho do texto A/A+/A++, alto contraste, links sublinhados, reduzir movimento; restaurar padrões; voltar ao topo) · **downloads em PDF/HTML5** (e-book A5; flipbook; os dois programas; prompt A5). Nenhum outro botão de opções no cabeçalho, na barra ou no corpo.
- **Estilos visuais (`data-style`):** Padrão (limpo) · Gamer (neon escuro, força escuro) · **Jornal (principal)**: diagramação de jornal de notícias — manchete serifada, fios duplos, capitular, texto justificado, Apresentação em 2 colunas. **Tema claro por padrão** (Jornal diurno em papel claro); com o tema escuro, o Jornal vira edição noturna (papel escuro/serifas creme), inclusive nos gráficos (`Chart.defaults` acompanham). Estilos não alteram conteúdo/dados/ordem.
- **Preferências:** `localStorage` (`analise2026_prefs`), aplicadas já no `<head>` (sem flash): idioma, tema, estilo, fonte, contraste, links, movimento. Migrações versionadas (`v4`, `v5`) reaplicam novos padrões uma única vez preservando acessibilidade/idioma. “Restaurar padrões” = PT + tema claro + estilo Jornal.
- **UX/acessibilidade:** skip-link; `:focus-visible`; barra de progresso de leitura; sumário fixo com seção ativa (IntersectionObserver + `aria-current`) — **ocultado ≤ 820 px** (navegação pelo ☰ Menu); reveal suave das seções desligado com “reduzir movimento”/`prefers-reduced-motion`; alvos ≥ 40 px; **responsivo para celulares pequenos** com tipografia fluida `clamp()` (corpo ≥ 16 px, fontes nítidas), KPIs em 1 coluna, gráficos mais baixos, downloads empilhados; impressão sempre em esquema claro legível.
- **Data/hora de publicação:** instante único (ISO com fuso) renderizado via `Intl.DateTimeFormat` (pt-BR/en-GB, `America/Sao_Paulo`) na Apresentação (último elemento) e no rodapé — sincronizado com o carimbo dos PDFs gerados na mesma publicação.

## 7. Terminologia (vale para site, e-book e flipbook)

- Somente **nomes** dos candidatos; cores fixas (Lula `#b91c1c`; Flávio Bolsonaro `#1d4ed8`).
- **Bolsonarismo e lulismo** (e derivados) **somente emparelhados**, mesmo destaque tipográfico e mesmo estatuto de fonte (uso convencional na literatura/debate; ausentes dos programas originais — busca integral nos PDFs). Incluir a explicação: **os dois fazem jus ao sufixo “-ismo” pelos mesmos fatos e aspectos** — movimentos nacionais organizados em torno do nome do líder (nome + “-ismo”), base eleitoral fiel e identidade programática associada ao líder; o fenômeno que gerou um título é o que gerou o outro.
- Espectro apenas com posições convencionais e simétricas, fundamentadas; qualificativos sem base direta nos textos/fontes oficiais não entram.

## 8. Complementos (geradores em `ferramentas/`)

1. **E-book PDF A5** — `downloads/Analise-2026-Ebook-A5.pdf`, gerado por `ferramentas/gerar_ebook_flipbook.py` a partir do `index.html` (fonte única de verdade): gráficos estáticos equivalentes (Matplotlib, mesmos dados/valores), A5 com margens ≈ 13–15 mm, capítulos em página nova, sumário com páginas, rodapé paginado, **gráfico + legenda + leitura sempre juntos**, tabelas largas convertidas em blocos por área/tema, contracapa com créditos. **Capa:** fundo com a bandeira do Brasil **desfocada**; título no alto (“Eleições Presidenciais 2026 — Análise Comparativa dos Programas de Governo”); no centro, **urna de votação padrão com “2026”**; **sob o número, “by rogerelizar”**; na base, o subtítulo **“2º Turno 2026 - Criado por IA”**.
2. **Flipbook HTML5** — `downloads/Analise-2026-Flipbook.html` (arquivo único, sem dependências): páginas do PDF A5 como imagens **WebP 190 dpi** embutidas (uma cópia só, em array JS) exibidas por um **motor próprio de virada 3D**: no **desktop, spread de 2 páginas sempre centrado** (a capa sozinha também centraliza, deslocando o livro; lombada e sombras de dobra; virada com sombreamento progressivo); no **celular (≤ 820 px), página única centrada** com virada sobre a lombada esquerda; pool de apenas 4 `<img>` reutilizadas + pré-carregamento das páginas vizinhas; controles Início/Anterior/Próxima/Fim, contador acessível, slider de páginas, tela cheia, teclado (←/→/PgUp/PgDn/Home/End), clique nas laterais e gesto de deslizar; `prefers-reduced-motion` desliga a animação. Mesma diagramação do e-book — nenhuma sequência de gráfico/texto é quebrada.
3. **Prompt para download** — `downloads/Prompt-Analise-A5.pdf`, renderizado por `ferramentas/gerar_prompt_pdf.py` a partir de `prompt/prompt-analise-a5.md`: é o prompt que gera **somente a análise como PDF A5 para impressão** (com a especificação da capa do item 8.1).
4. **Divisão dos prompts (regra permanente):** (a) prompt **para download** = o do item 8.3 (análise → PDF A5); (b) **este prompt completo** (site + complementos) vive **apenas no repositório** (`prompt/PROMPT-COMPLETO-SITE.md`), **sem link de download** na página. A Apresentação e o ☰ Menu devem dizer exatamente isso.
5. **Downloads no ☰ Menu (ordem):** e-book A5 (PDF, com nº de páginas e tamanho) · flipbook (HTML5) · programa de Lula (PDF, 84 pp.) · programa de Flávio Bolsonaro (PDF, 76 pp.) · prompt da análise A5 (PDF); nota de que o prompt completo está no repositório, sem download.

## 9. Estrutura do repositório e publicação

```
index.html                      (o site — fonte única do conteúdo)
README.md                       (como abrir, idiomas, menu, estilos, downloads, prompts)
fontes-primarias/               (PDFs oficiais do TSE)
downloads/                      (Analise-2026-Ebook-A5.pdf · Analise-2026-Flipbook.html · Prompt-Analise-A5.pdf)
prompt/                         (prompt-analise-a5.md [fonte do PDF p/ download] · PROMPT-COMPLETO-SITE.md [só repositório])
ferramentas/                    (gerar_ebook_flipbook.py · gerar_prompt_pdf.py)
```

Trabalhar em branch de sessão; validar (HTML, `node --check` no JS, contagens de tradução e de termos simétricos, HTTP 200 na prévia e nos downloads); commit + push apenas na branch; abrir PR para `main`; merge somente quando o curador pedir.

## 10. Checklist final de aceitação

Conteúdo idêntico nos três formatos · candidatos só pelo nome (busca por codinomes = 0) · bolsonarismo = lulismo (contagens iguais, com explicação) · tema claro ao abrir · um único botão flutuante ☰ Menu abrindo as opções · PT padrão + EN funcional · acessibilidade persistente · celular pequeno legível · capa do e-book/flipbook exatamente como especificada · e-book sem órfãs (título/gráfico-legenda-leitura juntos) · flipbook virando páginas sem internet · prompt de download = versão A5; prompt completo ausente dos downloads · nenhum dado sem fonte oficial ou fallback literal.

---

# PARTE II — ANEXO HISTÓRICO (auditoria do que foi pedido)

## Anexo A — Prompt original do curador (verbatim, em inglês, como fornecido)

> Nota: grafias históricas (como “Candidate A/B”) são preservadas **apenas** neste anexo, por fidelidade documental; valem as regras da Parte I.

```text
# ROLE AND PERSONA

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
```

## Anexo B — Refinamentos do curador (ordem cronológica, resumo fiel)

1. “A página final deve estar em português brasileiro.”
2. Português como idioma principal e inglês como secundário; botão “Opções” com acessibilidade, tema claro/escuro e downloads (propostas + prompt, tudo em PDF); subtítulo com “by rogerelizar” e a IA montadora; introdução com disclaimer de isenção do curador (só o prompt, baixável em “Opções”), chamado à cidadania responsável e, ao final, data e hora da publicação.
3. Publicação no GitHub (commit, push e pull request feitos pela IA; merges sempre a pedido).
4. Melhoria de UI/UX + dois designs gráficos adicionais: **estilo página gamer** e **estilo jornal de notícias** (selecionáveis, mesmo conteúdo).
5. Diagramação do estilo jornal refinada; responsivo com fontes nítidas/legíveis em celular pequeno; **todas as opções num único botão flutuante (hambúrguer)**; estilo principal = jornal (na ocasião, em sua edição escura).
6. **Tema claro por padrão.** Simetria terminológica: onde se usasse “bolsonarismo” para Flávio Bolsonaro, usar “lulismo” para Lula com igual fonte/base e destaque; qualificativos de espectro somente com citação direta dos textos originais. (Auditoria então feita: os pares foram emparelhados e contados.)
7. **Citação pelo nome do candidato é preferível** a codinomes por letra — corrigir em toda a página; ao inserir “lulismo”, **explicar que ambos têm o mesmo mérito de receber o sufixo “ismo”**, pois os fatos e aspectos que geraram o título para uma candidatura são os mesmos da outra; como certo termo procurado **não foi encontrado** (nem na página nem nos originais), **remover a menção a ele e à regra** que lhe seria aplicada; adicionar **download da análise completa** bem diagramada em **PDF A5 (e-book)** e **flipbook HTML5**, com **capa**: bandeira do Brasil desfocada ao fundo, título no alto, **urna de votação padrão no centro com “2026”**, sob o número **“by rogerelizar”** e, na base, o subtítulo **“2º Turno 2026 - Criado por IA”**, páginas fáceis de ler sem quebrar sequências de gráficos e textos; e **dividir o prompt em dois** — um que teria gerado toda a análise com resultado em **PDF A5 para impressão (o prompt de download)** e outro **completo**, origem de todo o site e complementos, **apenas armazenado no repositório (este arquivo), sem download**.

*Fim do prompt completo (uso interno do repositório).*
