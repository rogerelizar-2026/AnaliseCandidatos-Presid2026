# Complete Prompt — “Two Competing Projects for Brazil” Website, Analyses and Complements

> **Repository-only document. This complete prompt must not be offered for download anywhere on the website.**
>
> It replaces the previous consolidated prompt in Portuguese. This recreated version is written in **English** and reflects the latest finished version of the project: opening choice screen, bilingual interactive report, 54-page A5 e-book, 148-page large-print flipbook, updated downloadable A5-analysis prompt, fullscreen side controls, button-free mobile fullscreen, and strict paragraph separation between material attributed to Lula and material attributed to Flávio Bolsonaro.
>
> The public downloadable prompt is a different document: `prompt/prompt-analise-a5.md`, rendered as `downloads/Prompt-Analise-A5.pdf`. It generates **only the analysis as a printable A5 PDF**. This file, kept at the legacy path `prompt/PROMPT-COMPLETO-SITE.md` so repository references remain stable, is the complete build specification for the **entire website and all complements**.
>
> If this document is pasted into an AI system or handed to a development/editorial team, use the text between **BEGIN COMPLETE PROMPT** and **END COMPLETE PROMPT**. The provenance appendix after the end marker is repository documentation, not part of the prompt.

---

## BEGIN COMPLETE PROMPT

### 0. Mission

Build, validate and publish the complete project **“Dois projetos de Brasil em disputa”** (“Two competing projects for Brazil”): a strictly neutral, source-auditable comparison of the two government programmes filed for Brazil’s 2026 presidential runoff.

The finished project must contain all of the following, with the same analytical content and evidence base throughout:

1. a lightweight opening page, `index.html`, where the reader chooses between the flipbook and the main interactive report;
2. the complete bilingual interactive report, `analise.html`, in Brazilian Portuguese first and English second;
3. the two official programme PDFs archived under `fontes-primarias/`;
4. a printable A5 e-book, `downloads/Analise-2026-Ebook-A5.pdf`;
5. a separate large-print, single-file HTML5 flipbook, `downloads/Analise-2026-Flipbook.html`;
6. a downloadable Portuguese prompt that generates only the A5 analysis, with source at `prompt/prompt-analise-a5.md` and rendered output at `downloads/Prompt-Analise-A5.pdf`;
7. this complete English prompt, stored only in the repository at `prompt/PROMPT-COMPLETO-SITE.md`, with **no download link** anywhere on the public pages;
8. the two generators, `ferramentas/gerar_ebook_flipbook.py` and `ferramentas/gerar_prompt_pdf.py`;
9. a `README.md` explaining how to open, read, download, regenerate and audit everything.

Do not deliver a partial website and describe the missing artifacts as future work. Do not invent a different architecture unless a requirement below is technically impossible; if a substitution is unavoidable, preserve the user-visible behavior and record the deviation in the final build report.

### 1. Roles, neutrality and epistemic discipline

Work simultaneously as:

- a senior full-stack developer;
- a prompt engineer and technical editor;
- a political scientist with expertise in political economy, international relations and investigative political journalism;
- a publication designer/typesetter;
- an accessibility and quality-assurance reviewer.

Maintain **strict neutrality**:

- no endorsement and no voting recommendation;
- the same legal, fiscal and evidentiary ruler for both candidates;
- no loaded labels without a direct, cited basis;
- no asymmetry in typography, source status, order of scrutiny or burden of proof that is not explicitly justified by the evidence;
- distinguish facts, later campaign statements, and the author’s analytical judgments at all times.

The curator is **by rogerelizar**. The assembling AI must be credited exactly as **Arena.ai — Agent Mode**. Never invent or disclose an underlying model name. The curator supplied the prompts and the two official PDFs only; the curator did not draft or pre-approve the analysis line by line and does not necessarily endorse it.

### 2. Inputs, candidates, chronology and frozen publication facts

#### 2.1 Primary programme PDFs

Place the two official TSE-filed programmes in `fontes-primarias/`:

- `fontes-primarias/PropostasLula.pdf` — Luiz Inácio Lula da Silva, PT, ballot number 13, 84 pages;
- `fontes-primarias/PropostasFlavio.pdf` — Flávio Bolsonaro, PL, ballot number 22, 76 pages.

Extract searchable text while preserving printed-page mapping. Every programme claim in the comparative matrix must carry the relevant PDF page reference.

#### 2.2 Candidates and tickets

Refer to candidates **by name in all visible text**. Never use letter codenames for them in prose, headings, chart labels, alerts, tables or captions. Historical internal HTML ids and internal data codes may remain only where required for stable code/generator compatibility; they must never be presented to the reader as candidate names.

Use these fixed colors, always together with names:

- Lula: `#b91c1c`;
- Flávio Bolsonaro: `#1d4ed8`.

The narrative order is ballot-number order (Lula/13 before Flávio Bolsonaro/22), except election-result rankings, which are ordered by votes.

Verified ticket facts for the frozen edition:

- **Luiz Inácio Lula da Silva (PT, 13)** — incumbent president (2003–2010 and 2023–present), seeking an unprecedented fourth term; born in Caetés, Pernambuco. Running mate: **Geraldo Alckmin (PSB)**. Coalition: **Brasil Pronto pra Mais** — Federação Brasil da Esperança (PT, PCdoB, PV), PSB, PDT and Federação PSOL–REDE (PSOL, REDE).
- **Flávio Bolsonaro (PL, 22)** — senator for Rio de Janeiro since 2019, lawyer, eldest son of former president Jair Bolsonaro; born in Resende, Rio de Janeiro; first presidential run. Running mate: **Alfredo Gaspar (PL-AL)**. The PL runs alone, without a formal coalition.

Programme structures to reproduce in separate candidate cards:

- Lula: government-balance introduction on pp. 6–14, followed by 13 programmatic guidelines on pp. 15–83: Democracy and the State; Fighting inequality; Integrated security; Education; Health; Culture and sport; Right to the city; Sustainable, productive and digital economy; Food security and farming; Energy and low carbon; Environment and climate; Labour; Sovereignty and international protagonism.
- Flávio Bolsonaro: a “citizen journey” in 9 axes: *Brasil sem Medo* (security, p. 13); *Brasil por Elas* (women, p. 17); *Brasil sem Fila* (digital State, p. 23); *Brasil Mais Barato* (prices/taxes, p. 29); *Brasil que Prepara* (education/health, p. 34); *Brasil que Prospera* (work/credit/housing, p. 42); *Brasil que Cresce* (infrastructure/energy/farming/world, p. 49); *Brasil que Cumpre a Constituição* (Judiciary/freedom, p. 65); *Brasil que Não Volta Atrás* (fiscal “Tesouraço”, p. 68).

#### 2.3 Election chronology and first-round result

Freeze the editorial cut-off at **23 October 2026**. The first round was held on 4 October 2026; the runoff is on **25 October 2026, 08:00–17:00 Brasília time**. If executing after that date, preserve the pre-runoff historical framing unless the curator explicitly commissions a new edition.

Reverify and reproduce the final TSE tally:

- Flávio Bolsonaro (PL): **56,104,503 votes**, **47.03%** of valid votes;
- Lula (PT): **53,879,538 votes**, **45.16%**;
- margin: **2,224,965 votes** (1.87 percentage points);
- Augusto Cury: 3,448,569 (2.89%);
- Renan Santos: 2,675,887 (2.24%);
- all other candidacies combined: approximately 3.19 million (2.68%);
- blank ballots: 2,300,798 (1.84%);
- null ballots: 3,674,249 (2.93%);
- abstentions: 33,469,244 (21.08% of eligible voters).

The chart data series for the votes chart is `[56104503, 53879538, 3448569, 2675887, 3190000]`, in that order. A 99.99% TSE news tally is superseded by the final tally wherever they differ.

#### 2.4 Official-context snapshot

Reverify, in the official sources, the October 2026 baseline used in the final section:

- Selic: **13.75% per year** (Copom, 16 September 2026);
- 12-month IPCA inflation: **4.58%**, against a 3% ± 1.5 p.p. target;
- BCB Focus, 13 October: projected 2026 IPCA 5.22%, year-end Selic 13.25%, GDP growth 1.85%;
- Federal Public Debt: **R$9.293 trillion** in August 2026;
- general-government gross debt: 82.5% of GDP in July and **82.9% of GDP (about R$11.1 trillion)** in August;
- unemployment: **5.3%** in the June–August 2026 moving quarter (IBGE/PNAD Contínua);
- PRODES 2025/26 deforestation: Amazon **3,335 km²** (down 41.8%, lowest since 1988); Cerrado **5,516.69 km²** (down 23.8%).

#### 2.5 Publication timestamp

Use one frozen report-publication instant everywhere in the report and book front matter:

- ISO value: `2026-10-23T14:33:57.033064-03:00`;
- time zone: `America/Sao_Paulo`;
- render it with `Intl.DateTimeFormat` in `pt-BR` and `en-GB` on the web page;
- place it at the end of the Introduction and in the footer.

The downloadable prompt PDF may carry its own later edition-generation stamp in its wrapper/footer; do not let that later stamp overwrite the frozen publication timestamp of the analysis itself.

### 3. Mandatory sources and research protocol

#### 3.1 Official-source hierarchy

For factual claims outside the two programme PDFs, prioritize and cross-reference only these official sources:

- **TSE — DivulgaCandContas**: tickets, coalitions and filed programmes;
- **TSE — Electoral Results**: exact nominal votes and percentages;
- **Federal Constitution**;
- **Law No. 9,504/1997** and **Law No. 14,208/2021** where electoral/federation rules matter;
- **Law No. 8,213/1991** for imprisonment aid (*auxílio-reclusão*);
- **Law No. 13,260/2016** for terrorism;
- **LGPD, Law No. 13,709/2018**, including health and biometric data;
- **Complementary Law No. 200/2023**, **Complementary Law No. 101/2000**, and **Complementary Law No. 179/2021** where fiscal rules and Central Bank autonomy matter;
- **Central Bank of Brazil (BCB)**, **IBGE**, **INPE/TerraBrasilis (PRODES)**, **National Treasury/Tesouro Transparente**, and **IFI/Senate** for monetary, fiscal, employment, social and deforestation data.

Journalism may be used only to document dated public campaign statements after the PDFs were filed. Identify the outlet and date. Journalism alone must never justify a legal or fiscal warning.

#### 3.2 Evidence ledger

Before writing final prose, build an internal evidence ledger. For every material claim, record:

- claim;
- candidate or common context;
- policy area;
- layer: filed PDF, later public statement, or analytical assessment;
- programme page or external source;
- source date and URL;
- exact quotation or faithful paraphrase;
- how the claim will be cited in the output.

Open and inspect the primary official document whenever possible. Do not treat a search snippet as final proof. Put official sources before journalistic items in the reference list. Every materially researched claim must have a numbered footnote/reference link.

Full-text-search both programme PDFs for the movement labels discussed in Section 4.3 and for any strong qualifier before using it. Do not claim a term appears in a programme unless the search and page inspection prove it.

#### 3.3 Anti-hallucination rule

Never invent data. If exact real-time data cannot be verified in the required sources, write literally:

> Data pending verification from TSE

Do not replace that fallback with an unlabeled estimate. In the final build report, list every remaining fallback and its location.

### 4. Method, attribution and terminology

#### 4.1 Three layers that must never be blurred

1. **What the filed PDF says** — always with PDF page.
2. **What was said afterwards** — runoff television, debates, interviews and campaign/government acts, always dated and sourced.
3. **The author’s analytical assessment** — feasibility scores, named ideological biases, likely motivations and comparative verdicts, always labeled as assessment and governed by one ruler for both candidates.

The comparative matrix belongs to layer 1 only. Later statements belong in the evolution section and must not retroactively rewrite the matrix.

#### 4.2 Candidate-attribution and paragraph-separation rule

This is a structural requirement in the website-to-book conversion and in all editorial writing:

- Never flatten one candidate’s profile, programme structure, proposal list, alert, evolution card or verdict into the other candidate’s running paragraph.
- In each matrix area, use this sequence: area heading; a separate subheading for **Lula (PT)**; Lula’s items; a separate subheading for **Flávio Bolsonaro (PL)**; Flávio Bolsonaro’s items; then a separate “Relationship between the proposals” block.
- A column heading must become its own subheading when a wide table is converted to sequential blocks; it must not be merely a bold prefix inside the first paragraph.
- Each list item inside a table cell becomes its own bullet/paragraph in block layout.
- Each feasibility data block repeats **candidate name + policy area**, so it remains attributable even when it starts on a new page.
- If a comparative synthesis contains a shared sentence followed by candidate-specific clauses, split it: shared sentence first; then a new paragraph beginning “Lula:”; then a new paragraph beginning “Flávio Bolsonaro:”. Apply the same rule inside list items, callouts, chart readings and converted table cells.
- A genuinely common official-context paragraph may remain common only if no passage attributable to one candidate runs directly into a passage attributable to the other.
- In HTML-to-book conversion, treat both `div.card` and `article.card` as cards. Never buffer an `article.card` as inline text. Keep a card’s colored rule and heading with at least the first lines of its body; do not leave the rule orphaned at a page bottom.
- Audit generated book flowables for candidate-subject transitions inside the same paragraph (patterns equivalent to “; Flávio…”, “.(p. X) Lula…”, a footnote marker followed by the other candidate as subject, or “; on Lula’s side…”). Split every applicable case without changing the underlying wording or evidence.

#### 4.3 Symmetric movement terminology

The terms **Bolsonarismo** and **Lulismo**, and their derivatives **bolsonarista** and **lulista**, may appear only as a matched pair with:

- identical typographic emphasis;
- identical source status: conventional usage in political-science literature and public debate;
- an explicit note that neither filed programme uses the terms.

Include this explanation near their first paired use, in both languages on the web and in Portuguese in the books: both candidates equally merit the “-ism” suffix because the facts and aspects generating one label are the same as those generating the other — each leads a nationwide political movement organized around the leader’s own name (leader’s name + “-ism”), with a loyal electoral base, its own vocabulary and a programmatic identity associated with the leader.

Use only conventional, symmetric spectrum positions — left, centre-left and right — when they are sourced and methodologically explained. Do not introduce a stronger qualifier without direct evidence and equal treatment.

#### 4.4 Language policy

- Brazilian Portuguese is the primary and authoritative language of the report.
- English is the secondary language on the opening page and main report.
- Translate the interface, headings, leads, table headers and key structural prose, candidate-profile labels, controls, chart titles/labels/tooltips, modeling notes and newly authored explanatory text.
- Verbatim quotations, PDF page references, source titles and evidence passages may remain in Portuguese in the English view, with a clear transparency note, so that auditability against the primary sources is preserved.
- The A5 e-book and flipbook are generated from the Portuguese report only: strip English duplicate blocks during book generation.
- The downloadable A5 prompt remains in Brazilian Portuguese. This complete repository prompt is in English.

### 5. Required analytical content

Create the following ten report sections, in this order, with these stable section ids in `analise.html`:

1. `introduction`
2. `methodology`
3. `electoral_profiles`
4. `comparative_matrix`
5. `feasibility_modeling`
6. `investigative_summary`
7. `sensitive_themes`
8. `proposal_evolution`
9. `official_context`
10. `references`

The Portuguese report is the single content source for the website, e-book and flipbook.

#### 5.1 Introduction — transparency, curator disclaimer and responsible voting

Write a welcoming introduction in Portuguese and a parallel English block. It must:

- explain the purpose: a document-based comparison, not slogans or social-media clips;
- promise page-level or official-source verification for material claims;
- include the curator disclaimer: **by rogerelizar** supplied only the prompts and the two official PDFs; did not draft, line-edit in advance, or necessarily endorse the interpretations, scores, warnings or verdicts; all research, writing, charts and assembly were performed by AI, credited as **Arena.ai — Agent Mode**;
- explain the prompt split exactly: the downloadable PDF prompt generates the analysis as an A5 e-book; the complete prompt that originated the whole site and complements is archived in the repository and is **not downloadable from the page**;
- urge responsible citizenship: read the official programmes, check TSE/BCB/IBGE/INPE/Treasury sources, and vote correctly and consciously on 25 October 2026, 08:00–17:00 Brasília time;
- end, as its last substantive element, with the frozen publication date and time, curator credit and AI-assembly credit.

#### 5.2 How to read — method, limits and anti-fabrication guarantees

Explain:

- primary sources: the two TSE PDFs and printed-page citations;
- official checking sources and hierarchy;
- the three evidence layers;
- what feasibility scores are and are not;
- reading conventions: candidate names, colors, language policy, symmetric terminology, visual styles changing presentation only, and the literal fallback for unverifiable real-time data.

#### 5.3 Profiles, votes and alliances

Include:

- two separate semantic `<article class="card …">` candidate cards with stable internal ids `candidate_A_profile` for Lula and `candidate_B_profile` for Flávio Bolsonaro (visible headings use names only). Each card covers who he is, running mate, coalition or standalone status, positioning, exact first-round votes and institutional reading;
- a bar chart with canvas id `chart_votes_canvas`;
- the final first-round result table, including blank/null/abstention context and a note that the final tally supersedes the 99.99% news tally;
- the ideological spectrum of formal alliances: ticket, party/federation, conventional position and dominant programmatic trait. Include PT and PL parenthetical movement labels in identical format and the symmetric “-ism” explanation;
- a note that party federations must act as one for at least four years under Law No. 14,208/2021, and discuss what formal breadth or narrowness means institutionally without treating it as a merit score.

#### 5.4 Comparative policy matrix

Begin with two separate programme-structure cards, internal ids `candidate_A_proposals` and `candidate_B_proposals`, then compare the filed PDFs faithfully in exactly these 12 areas:

1. Economy, public accounts and taxes
2. Public security and criminal justice
3. Health (SUS)
4. Education
5. Social protection, labour and income
6. Women, equality and care
7. Housing, cities and sanitation
8. Infrastructure, logistics and energy
9. Farming, food and land
10. Environment and climate
11. Democracy, the State and the digital world
12. Foreign policy, defence and sovereignty

For every area:

- synthesize each programme’s central proposal in bullets with PDF pages;
- do not import runoff statements;
- classify the relationship precisely (identical, functionally equivalent, similar but divergent, opposite, or a more exact mixed label);
- when a relationship is summarized, put genuinely shared claims first and candidate-specific interpretations in separate named paragraphs.

Write cell prose so that it can survive conversion to sequential book blocks without ambiguity.

#### 5.5 Feasibility and impact modeling

Publish the coding ruler, four modeled chart groups and the complete 24-row dataset described in Section 6. State clearly that scores are the author’s auditable analytical coding, not official data or predictions.

Each chart must have:

- a descriptive heading;
- accessible canvas label;
- a caption;
- an adjacent reading paragraph explaining what the reader should and should not infer;
- candidate-specific clauses split into separate paragraphs whenever the subject changes.

#### 5.6 Investigative summary

Create four subsections with stable ids `identical_proposals`, `similar_divergent`, `institutional_friction` and `misleading_flags`.

**5.6.1 Identical or functionally equivalent proposals.** Reverify and present the six strong functional equivalences in the reference edition:

1. single health record, digital health with AI/telehealth and use of idle private capacity;
2. mass subsidized popular housing and land regularization;
3. maintaining income transfers to the poorest;
4. domestic fertilizer autonomy (gas/potash/phosphate);
5. Payment for Environmental Services and satellite traceability of supply chains;
6. critical minerals with domestic value added and clean-energy data centers.

State that no passage is literally identical in both PDFs; the equivalence is functional. For item 1 and any similar case, split Lula’s and Flávio Bolsonaro’s formulations into separate paragraphs/sub-bullets.

**5.6.2 Similar proposals, divergent named ideological biases.** Use a shared-problem table with separate candidate instrument/bias cells. Cover expensive food; childcare and care; teaching quality; organized crime; high interest rates; app-based work; disinformation; external insertion. Name each bias explicitly (for example distributive developmentalism vs. supply-side liberalism; universalist progressivism vs. pro-market targeting; integrated *garantismo* vs. conservative-security punitivism) and ground the label in the instruments, not in rhetoric.

**5.6.3 Institutional-friction map.** For each friction cluster, state proposal, veto/implementation actor, required legal instrument and expected friction. Cover constitutional amendments and the 3/5 congressional threshold; fiscal-framework and budget-amendment politics; state/municipal execution of policing, prisons, schools, childcare and transport; Supreme Court review; autonomous Central Bank limits; regulators and decentralized litigation under LGPD/environmental and sectoral law.

**5.6.4 Flagged promises.** Flag a promise as fiscally populist/incompatible or legally unfeasible only when an official constitutional, statutory or fiscal source demonstrates the collision or missing funding/design. Apply the same test to both sides. Organize alerts under the candidate’s name and number them in visible text as “Lula, alert n” / “Flávio Bolsonaro, alert n”, followed by any genuinely common alert. Reverify the reference-edition alert topics before reproducing them:

- Flávio Bolsonaro: declaring factions “narcoterrorists”; lowering criminal majority to 16 and penal punishment from 14; redirecting resources connected with prisoners’ families to victims; the fiscal trilemma of doubling security and adding 500,000 prison places while cutting taxes and running a surplus; automatic environmental licensing by administrative silence; a one-million-camera facial-recognition “Brazilian Wall”; chemical castration, full-sentence/no-progression rules and universal ankle monitors in protective measures.
- Lula: weekend zero-fare transport financed through mandatory budget amendments (runoff addition); expanding everything while preserving the fiscal framework; ending the 6×1 schedule as a future promise; runoff health superlatives without a baseline; Petrobras as simultaneous price reducer, investor and green champion; democratic platform regulation without a precise sanctioning design.
- Common alert: government purchase/freezing of household and firm debts, with each candidate’s formulation in a separate paragraph before the shared fiscal/moral-hazard conclusion.

“Flagged” does not mean “false”; it means the promise as phrased cannot stand without a rule change, identified funding or a redesign not yet presented.

#### 5.7 Sensitive contemporary themes

For each issue, present Lula’s public position, Flávio Bolsonaro’s public position and a separate “likely political-economic motivation” interpretation. Cover:

1. amnesty for 8 January;
2. the Supreme Court, abortion and drugs;
3. guns and ammunition;
4. the 6×1 working schedule;
5. Bolsa Família;
6. tax reform;
7. oil and the Equatorial Margin;
8. external anchor;
9. online betting;
10. secrecy and corruption as debated in the runoff.

Never present inferred motivation as a mind-reading fact.

#### 5.8 Proposal evolution from the filed PDFs to the runoff

Open with the legal clarification: there is no newly filed runoff programme; the August PDFs remain the official proposals under Law No. 9,504/1997, art. 11, §1, IX. The evolution occurred through free TV time, interviews, the 18 October Band debate and campaign/government acts from 5 to 22 October 2026.

Use two separate candidate cards. For the reference edition, reverify and cover:

- Lula: weekend zero-fare transport through a constitutional amendment using 26.8% of mandatory amendments; sanctioned MEI debt relief and revenue-ceiling changes; expanded “Desenrola” debt purchase plus restart credit; new health targets; continuity on ending 6×1, real minimum wage, fiscal framework and tax reform.
- Flávio Bolsonaro: newly announced Ministry of Prosperity; reversal to a favorable vote on ending 6×1 while continuing to discuss hourly payment; naming and promising to raise Bolsa Família with two-year permanence; debt purchase/freezing; return of Perse for events/tourism; “Einstein-standard” health and “Health Real Plan” statements; and the ambiguity between not delinking pensions from the minimum wage and correcting BPC/pensions only for inflation.

Every evolution item must be dated and sourced as layer 2.

#### 5.9 The Brazil the winner inherits and final verdict

Present the official baseline in three cards: interest/inflation (BCB); public accounts/debt (Treasury/IFI/BCB); employment and environment (IBGE/INPE). Translate the constraints into plain language: debt above 80% of GDP, high real interest and rigid spending mean a menu of promises cannot all be implemented simultaneously.

Close with two separate verdict blocks:

- **If Lula wins, expect…** — main governing path, greatest strength and greatest vulnerability.
- **If Flávio Bolsonaro wins, expect…** — main governing path, greatest strength and greatest vulnerability.

Follow with three common deciding variables: real congressional composition and the price of budget amendments; the interest-rate/growth path; state and municipal execution capacity. Make **no voting recommendation**.

#### 5.10 Sources and notes

Provide numbered, linked references, official sources first. Include notes on neutrality, the 23 October 2026 cut-off, the two-prompt split and print/screen editions. Preserve stable reference anchor ids used by in-text citations.

### 6. Feasibility dataset and charts

#### 6.1 Coding ruler

Use exactly six dimensions:

- **Time**: months to full material delivery, not announcement. Anchors: 6 ≈ administrative act; 12 ≈ simple law; 24 ≈ law + federative network; 36 ≈ constitutional amendment/medium works; 48 ≈ structural change over a term or more.
- **Fiscal cost (0–10)**: annual pressure on the federal budget through spending, forgone revenue or implicit subsidy. Anchors: 1–2 under R$2bn/year; 3–4 R$2–10bn; 5–6 R$10–30bn; 7–8 R$30–80bn; 9–10 above R$80bn. Private investment counts less here and more as society dependency.
- **Positive impact (0–10)**: reach × depth × prior evidence; universal systems with installed networks score above untested pilots.
- **State/Union dependency (0–10)**: need for federal budget, bureaucracy and regulation; 10 means only the Union can deliver.
- **Society/local-entity dependency (0–10)**: need for firms, households, civil society, states and municipalities; 10 means nothing happens without their money, adherence or execution.
- **Negative risk (0–10)**: probability × severity of fiscal, legal, distributive, environmental or institutional harm, including constitutional collision, litigation and documented side effects.

#### 6.2 Frozen reference dataset

For exact reproduction of the latest edition, encode the following 24 observations. Values are **months / fiscal cost / impact / State dependency / society dependency / risk**. Write a brief, evidence-based coding note for every row in Portuguese and translate its substance for the English view. Do not silently change a value; a genuine rescoring is a new edition and requires all charts, readings, books and references to be regenerated and the change disclosed.

| Candidate | Policy area | Values | Coding-note substance |
|---|---|---:|---|
| Lula | Economy & taxes | 36/8/7/9/5/6 | Fiscal framework + NIB/PAC: public credit/investment as drivers; implicit subsidy cost. |
| Flávio Bolsonaro | Economy & taxes | 30/7/7/6/8/7 | “Big scissors” + tax-reform review: forgone revenue/transition; depends on private and state response. |
| Lula | Public security | 24/6/6/8/6/5 | Security amendment/SUSP + funding; policing is state-level, so delivery is federative. |
| Flávio Bolsonaro | Public security | 36/9/6/9/4/9 | 500k prison places, TREVA and 1m cameras: permanent capex/running cost; highest constitutional/LGPD risk. |
| Lula | Health (SUS) | 24/8/8/9/5/4 | Installed SUS network lowers risk; high recurring specialist/medicine cost. |
| Flávio Bolsonaro | Health (SUS) | 24/7/7/7/7/5 | Record + real-cost payment + idle private capacity; depends on philanthropic providers and municipalities. |
| Lula | Education | 36/8/8/9/6/4 | Fundeb/full-time schooling/federal institutes: federal funding, local delivery, long maturation. |
| Flávio Bolsonaro | Education | 30/6/6/6/7/6 | Results, vouchers and civic-military schools: lower federal cost; greater federative/equity variance. |
| Lula | Social protection & labour | 18/9/8/10/4/6 | Real minimum wage drags pensions/BPC; shorter hours without pay cuts shift cost to employers. |
| Flávio Bolsonaro | Social protection & labour | 18/6/6/6/8/5 | PDF says keep + autonomy; disclose that runoff additions raise estimated cost to about 8. |
| Lula | Women & care | 30/7/7/9/6/4 | Public care network as diffuse social infrastructure; low legal risk. |
| Flávio Bolsonaro | Women & care | 24/6/7/7/7/5 | Digital platform + vouchers: faster launch; connectivity, take-up and LGPD scoring risks. |
| Lula | Housing & cities | 36/9/8/9/6/5 | MCMV/PAC subsidy and directed credit; sensitive to FGTS/savings and interest rates. |
| Flávio Bolsonaro | Housing & cities | 36/8/7/6/8/5 | 2.5m Casa Verde e Amarela homes + concessions; depends on mortgage rates and markets. |
| Lula | Infrastructure & energy | 48/9/8/9/6/6 | PAC/Petrobras/local content: high public/state-company capex and administered-price risk. |
| Flávio Bolsonaro | Infrastructure & energy | 48/6/8/5/10/7 | Mostly private R$900bn: lower fiscal cost only if capital arrives despite a 13.75% Selic. |
| Lula | Farming & food | 24/7/7/8/7/5 | Family-farming credit, interest subsidy and public purchases; weather/exchange-rate exposure. |
| Flávio Bolsonaro | Farming & food | 24/6/7/6/9/6 | Insurance, securitization and titling; market/producer leverage with land-environment risk. |
| Lula | Environment & climate | 48/6/8/9/6/4 | Enforcement + public-land allocation; 2026 PRODES trajectory supports feasibility. |
| Flávio Bolsonaro | Environment & climate | 36/5/6/6/8/8 | Strong 2029 target, but tacit licensing and 20-year stability raise legal/environmental risk. |
| Lula | Democracy & the State | 30/5/6/9/5/6 | Participation + platform/amendment regulation: low budget cost, high political-legal conflict. |
| Flávio Bolsonaro | Democracy & the State | 30/4/6/7/5/8 | Supreme-Court reform/end of re-election: low budget cost, high inter-branch friction. |
| Lula | Foreign policy & defence | 36/6/7/9/4/5 | State diplomacy/defence base; moderate tariff and supply-chain risk. |
| Flávio Bolsonaro | Foreign policy & defence | 36/5/6/7/7/7 | OECD/opening path: efficiency gains with sectoral import/alignment risks. |

Keep the web `POLICY_DATA` order stable and the 12 area labels consistent across charts, table and generators. Internal candidate codes, if used, must map visibly to full names everywhere.

#### 6.3 Interactive charts in `analise.html`

Use Chart.js **4.4.1** from the jsDelivr CDN in the `<head>`. The five canvas ids are:

- `chart_votes_canvas`;
- `chart_time_cost_canvas`;
- `chart_radar_canvas`;
- `chart_dependency_canvas` (singular “dependency” — do not rename it in only one place);
- `chart_risk_time_canvas`.

Build:

1. nominal-votes bar chart;
2. time × fiscal-cost bubbles, bubble size = positive impact;
3. average-profile radar across the 12 areas, with time normalized as `months / 48 × 10`;
4. grouped bars for positive impact × State dependency × society dependency by area, with a candidate toggle;
5. risk × time bubbles, bubble size = fiscal cost;
6. an area filter where applicable and a complete auditable data table (`tbody` id `policy_data_body`).

Chart titles, axis labels, legends, datasets and tooltips must update between Portuguese and English and must use candidate names, not internal codes. Chart default text/grid colors must follow light/dark theme and visual style. Preserve candidate colors in every theme.

### 7. Opening page — `index.html`

The repository root is a **lightweight choice screen**, not the report and not an automatic flipbook loader. It must not preload the 16 MB flipbook.

Requirements:

- valid HTML5, `lang="pt-BR"` by default, responsive and accessible;
- title/headline **“Dois projetos de Brasil em disputa”** in Portuguese and “Two competing projects for Brazil” in English;
- candidate chips showing the runoff pair and valid-vote percentages;
- two large, clearly differentiated choices:
  - **Read the flipbook** → `downloads/Analise-2026-Flipbook.html`, with live page count, HTML5/single-file note, approximate size and a warning that it may take a few seconds on mobile;
  - **Go to the main page** → `analise.html`, described as the complete interactive report;
- a secondary direct download for the 54-page A5 e-book;
- a runoff-date/responsible-voting footer;
- credits: curator **by rogerelizar** and AI assembly **Arena.ai — Agent Mode**, plus “2º Turno 2026 - Criado por IA”;
- PT/EN toggle using the same localStorage key as the main page, `analise2026_prefs`. Read the existing preference object, update only `lang`, and write the whole object back so theme/style/accessibility preferences from the main page are not erased;
- skip link, visible focus, at least 40 px language targets, large card actions, safe-area padding and `prefers-reduced-motion` handling;
- one-column choices on small phones without horizontal scrolling.

Update all page counts and approximate file sizes on this screen after final artifacts are generated. Never perform a blind global replacement of a bare number such as “138” or “148”; replace only full label contexts, because unrelated strings such as CSS colors and law URLs may contain the same digits.

### 8. Main interactive report — `analise.html`

#### 8.1 Document and hero

`analise.html` is one self-contained HTML5 document except for the Chart.js CDN script and relative links to local downloads/opening page. Keep all CSS and report JavaScript in the document; no build step or framework is required to open it.

The hero must contain:

- eyebrow identifying the 2026 presidential runoff and independent analytical report;
- H1: “Dois projetos de Brasil em disputa: análise comparativa completa dos programas de governo”;
- a subtitle naming **Luiz Inácio Lula da Silva (PT, nº 13)** and **Flávio Bolsonaro (PL, nº 22)**;
- byline with exactly **by rogerelizar** and **Arena.ai — Agent Mode** in both languages;
- metadata pills for the 23 October 2026 cut-off, TSE primary sources, PT-primary/EN-secondary languages and strict neutrality/no voting recommendation;
- four KPI cards summarizing the first-round margin, 84 × 76 programme pages/structures, 12 modeled areas and the main runoff convergence/fiscal warning.

The sticky table of contents begins with **“⌂ Abertura” / “⌂ Start”** linking back to `index.html`, followed by the ten report sections. Use the stable section ids in Section 5 and the candidate-card ids in Sections 5.3–5.4.

#### 8.2 Single floating menu

There must be exactly one options entry point: a single floating bottom-right **☰ Menu** button (`id="menuFab"`), respecting safe-area insets. Do not add separate options buttons in the hero or table of contents.

It opens an accessible `<dialog id="optionsDialog">` containing, in this order:

1. contents links to all ten sections; clicking one closes the dialog and goes to the section;
2. language PT/EN;
3. theme light/dark/automatic;
4. visual style standard/gamer/news;
5. accessibility: text size normal/large/extra-large, high contrast, underline all links, reduce motion, reset defaults and back to top;
6. downloads, in this order: A5 e-book; HTML5 flipbook; Lula programme PDF; Flávio Bolsonaro programme PDF; downloadable A5-analysis prompt PDF;
7. the explicit note that the complete site prompt is archived only in the repository and has no download on the page.

Dialog behavior: use `showModal()` where available; Esc closes; clicking the backdrop closes; focus moves into the dialog and returns to the invoking button on close; all controls are keyboard reachable and expose pressed/checked state.

#### 8.3 Preferences, themes and visual styles

Persist preferences in localStorage under `analise2026_prefs`. Apply them in a small script in the `<head>` before first paint to avoid a theme/language flash.

Preference fields:

- `lang`: `pt` (default) or `en`;
- `theme`: `light` (default), `dark` or `auto`;
- `style`: `standard`, `gamer` or `news` (default);
- `font`: `normal`, `large` or `xlarge`;
- `contrast`: `normal` or `high`;
- `links`: `default` or `underlined`;
- `motion`: `full` or `reduce`;
- migration flags `v4` and `v5`.

The v5 migration applies the light Newspaper default once while preserving language/accessibility choices. Reset means PT + light theme + Newspaper style + normal accessibility settings.

Visual rules:

- **Light theme is the default.**
- `news` is the lead style: an editorial newspaper design with serif headline, double rules, drop cap, justified text and two-column Introduction on wide screens. In light theme it is a daytime paper edition; in dark theme it becomes a night edition with dark paper and cream serif text.
- `standard` is a clean institutional design.
- `gamer` is a dark neon design and forces dark chart/UI treatment while selected.
- Styles and themes change presentation only — never content, data, ordering or conclusions.
- Print CSS always falls back to a legible light scheme and hides interactive controls/dialogs.

#### 8.4 UX, responsiveness and accessibility

Implement:

- skip-to-content link;
- visible `:focus-visible` outlines;
- reading-progress bar;
- sticky TOC with IntersectionObserver active-section highlighting and `aria-current`; hide the sticky TOC at widths up to 820 px and rely on the floating menu;
- gentle reveal-on-scroll only when motion is allowed;
- touch targets of at least 40 px (44 px preferred for primary controls);
- fluid `clamp()` typography; body text remains genuinely readable on small phones (about 16 px or more);
- one-column KPI/download stacks, shorter charts and horizontally contained tables on narrow screens;
- `prefers-reduced-motion` and the in-page reduce-motion preference disabling smooth scroll, reveal and unnecessary transitions;
- chart containers with text alternatives/adjacent readings, not color-only meaning.

### 9. Downloads and the permanent two-prompt rule

Maintain exactly two prompt concepts:

1. **Downloadable A5-analysis prompt**
   - source: `prompt/prompt-analise-a5.md`;
   - rendered download: `downloads/Prompt-Analise-A5.pdf`;
   - language: Brazilian Portuguese;
   - purpose: generate only the complete analysis as a printable A5 PDF;
   - contents: role and neutrality; inputs and verified 23 Oct 2026 snapshot; official sources and anti-hallucination fallback; three-layer method; all required chapters; symmetric terminology; the coding ruler and frozen 24 values in Section 6.2; candidate paragraph-separation rules; exact cover; A5 layout; acceptance checklist and build-report requirement;
   - explicitly state that it does not generate the opening page, interactive website, menu, visual styles, flipbook or generators.

2. **Complete site prompt**
   - file: `prompt/PROMPT-COMPLETO-SITE.md` (legacy filename retained);
   - language: English;
   - purpose: generate the entire website, analyses and complements specified here;
   - availability: **repository only; no website download link, no rendered PDF download, and no copy placed under `downloads/`**.

The Introduction, main-page downloads area and README must state this split accurately. After rendering `Prompt-Analise-A5.pdf`, measure its real page count and update the main-page download label. In the latest reference generation it has **8 pages**; do not hard-code that number in generators or prose where a fresh render could change it.

### 10. Generator architecture — `ferramentas/gerar_ebook_flipbook.py`

Write one Python generator, run from the repository root, that reads `analise.html` as the single content source and produces both the standard A5 e-book and the large-print source PDF used by the flipbook.

Use a proven local stack equivalent to BeautifulSoup + ReportLab Platypus + Matplotlib + Pillow + PyMuPDF. Do not depend on a browser print pipeline.

#### 10.1 Data extraction

- Extract `POLICY_DATA` from `analise.html` by executing/slicing the actual JavaScript array safely (for example through Node’s VM), rather than duplicating a second hand-maintained dataset.
- Extract vote labels, values and colors by slicing from `getElementById("chart_votes_canvas")`, not from the first textual occurrence of the canvas id (which is the HTML tag).
- Assert 24 modeling rows and the expected vote series before building.

#### 10.2 Two book profiles from one source

Define two profiles:

- **`padrao` (standard print e-book)**
  - output: `downloads/Analise-2026-Ebook-A5.pdf`;
  - A5, about 13 mm side margins, 15 mm top and 16 mm bottom;
  - serif body about 9.3 pt with leading about 13.6 pt, justified body text, table cells about 7.3 pt;
  - latest reference output: **54 pages**.

- **`ampliada` (large-print screen edition)**
  - intermediate PDF only, used as the flipbook page source;
  - same A5 page geometry/content, but 10.5 mm side margins, 13.5 mm top and 14.5 mm bottom;
  - serif body **16 pt** with 23.5 pt leading, left-aligned;
  - no ordinary content set at a functionally tiny size: headings, data blocks, captions and references are scaled for comfortable screen reading (reference URLs may be 11.5 pt in this profile);
  - latest reference output: **148 pages**.

Both profiles share cover, chapters, references and evidence. Never generate flipbook pages by merely enlarging raster images of the standard print PDF; reflow the large-print profile.

#### 10.3 Cover and back cover

Generate the cover programmatically (Pillow or equivalent), exactly to this brief:

- blurred Brazilian-flag background;
- report title at the top: “Eleições Presidenciais 2026 — Análise Comparativa dos Programas de Governo”;
- a standard Brazilian electronic ballot box centered, visibly inscribed **“2026”**;
- directly under the number: **“by rogerelizar”**;
- near the base: **“2º Turno 2026 - Criado por IA”**, edition identification and curator/AI-assembly credits.

The back cover carries credits, curator disclaimer in short form, primary-source note and a responsible-voting call. These printed-book credits remain even though the flipbook’s web-interface header has no subtitle/credits line.

#### 10.4 Front matter, manual table of contents and pagination

Each book contains:

1. cover;
2. title page with report title, subtitle, credits, frozen publication timestamp, edition note and curator disclaimer;
3. “how to use this edition” text appropriate to standard or large-print profile;
4. election-in-numbers KPI list;
5. table of contents with final chapter page numbers;
6. the ten report sections, each starting on a new page;
7. back cover.

Use a **manual two-pass table of contents**: build once to collect chapter start pages, rebuild with those numbers, and assert that chapter pages are unchanged in the second pass. Do not rely on ReportLab `TableOfContents` + `multiBuild` for this book; that approach failed to converge in the reference implementation.

Running pages have a gold rule, footer “Eleições Presidenciais 2026 — Análise Comparativa · by rogerelizar”, page number and top-right running head “2º Turno 2026 - Criado por IA”. Add PDF metadata and chapter bookmarks/outline where supported.

#### 10.5 HTML-to-book conversion rules

Parse `analise.html` and remove English duplicates (`.i18n-en`), scripts, styles, navigation, footer, dialogs, controls, buttons, selects, noscript blocks and hidden elements before book conversion.

Implement block dispatch for paragraphs, lists, headings, rules, canvases, tables, callouts, timelines, `div` containers and **`article` elements**. In particular:

- `article` is a block element;
- `div.card` and `article.card` both become candidate cards with a colored rule and separate heading/paragraph/list flowables;
- protect a card rule from being orphaned (conditional page break of about 150 pt in large print and 72 pt in standard profile before the rule);
- chart boxes map canvas ids to static chart images and captions;
- callouts become boxed flows with semantic background/border colors and are kept together as far as practical;
- references keep numbered labels and print URLs in a legible auxiliary style.

#### 10.6 Tables, spans and candidate separation

For ordinary compact tables, compute sensible column widths and repeat the header row when splitting.

Convert a table to sequential blocks when it is wide or has long average cell text. In the large-print profile, also force block conversion for tables with row/col spans, because a long spanned segment can exceed a page frame and make the table unsplittable. Down-fill the merged value into following rows before emitting blocks.

For each converted row:

- emit the first-column value as the block heading;
- for each remaining non-empty cell, emit the column label as its own subheading;
- color the subheading red when it begins with Lula’s name and blue when it begins with Flávio Bolsonaro’s name, while retaining the full text label;
- recursively emit the cell’s paragraphs and list items as separate flowables.

For the special modeling table (`policy_data_body`), do not render a cramped grid. Emit a candidate heading and then one data block per area beginning with **“Candidate name · Policy area”**, followed by all six values and the coding note.

Implement a conservative candidate-transition splitter for book paragraphs generated from ordinary paragraphs, list items, buffered inline content and block-converted cells:

- split only when both candidates occur and the second becomes the subject after sentence/semicolon punctuation, a colon label, a footnote marker or an equivalent explicit transition;
- preserve comparative syntheses with no candidate-subject transition;
- when splitting inside inline HTML, close open inline tags at the end of each new paragraph and reopen them at the start of the next so ReportLab markup remains valid;
- in ordered/unordered lists, only the first resulting paragraph carries the original bullet/number.

#### 10.7 Static charts

Regenerate static Matplotlib equivalents from the same extracted web data:

- votes;
- time × fiscal cost;
- average radar;
- impact/dependencies for Lula;
- impact/dependencies for Flávio Bolsonaro;
- risk × time.

In the standard profile, each bubble chart may combine both candidates with named point labels. In the large-print profile:

- split each bubble chart by candidate;
- enlarge chart fonts by about 55% and figure height by about 38%;
- number the 12 areas inside bubbles 1–12 in `POLICY_DATA` order;
- combine exact-coordinate duplicates into one label such as `1·4` instead of stacking illegible text;
- print the full number→area map in every bubble caption;
- position radar and dependency legends/titles so they cannot collide.

Map `chart_dependency_canvas` exactly; a pluralized/incorrect id silently drops both dependency charts and must be caught by tests. Keep each chart image and caption together, and keep the following reading text with them as closely as Platypus allows.

### 11. Flipbook — `downloads/Analise-2026-Flipbook.html`

Generate a single self-contained HTML5 flipbook from the **large-print intermediate PDF**, not from the standard e-book.

#### 11.1 Page images and file construction

- Rasterize every large-print PDF page at **190 dpi**.
- Prefer WebP (about quality 74, method 6); fall back to optimized JPEG (about quality 75) only if WebP is unavailable.
- Embed each page once as a base64 data URI in one JavaScript `PAGES` array.
- No external CSS, JavaScript, fonts or page images. Relative links to `../analise.html` and the A5 PDF are allowed because they apply when the file is served from the repository layout.
- Latest reference output: **148 pages**, about 16 MB. Page count and labels must be refreshed from the actual generated file.

#### 11.2 Normal (non-fullscreen) interface

Use a dark, book-like page with gold accents and cream paper. The interface header contains:

- a small kicker;
- H1 **“Dois projetos de Brasil em disputa”**;
- **no analytical subtitle** and **no curator/AI credits line** in the web-interface header.

Below the book in normal mode, show: First, Previous, accessible page counter, Next, Last, Fullscreen, “⌂ Página principal” linking to `../analise.html`, and “⬇ PDF A5” download. Under them show a page slider and a short usage hint.

Maximize the useful book size:

- desktop spread: up to **1400 px** wide, also constrained by 97vw and by viewport height with about 190 px reserved for chrome;
- single page: up to **720 px** wide with the same height logic;
- use dynamic viewport units with a safe fallback.

#### 11.3 Book geometry and turning engine

Use a custom CSS-3D/JavaScript engine with a reusable pool of four `<img>` elements (static left, static right, turning front and turning back), plus preloading of nearby pages. Do not create 148 permanent image elements.

Desktop mode (viewport wider than 820 px):

- show a centered two-page spread;
- model the book box as two A5 pages side by side (aspect ratio 296/210);
- center a lone front cover by translating the spread box −25% and a lone back cover by +25%, with the empty side hidden;
- for an even total page count, the correct final state is one centered back-cover page, not a forced pair;
- include spine and page-edge shading;
- animate the turning leaf around the center spine.

Mobile mode (viewport up to 820 px):

- show one centered A5 page (aspect ratio 148/210);
- hide the left static page/spine;
- animate the turning sheet around the left hinge with a paper back.

Common behavior:

- buttons First/Previous/Next/Last with correct disabled states;
- slider jump;
- click/tap zones: left/right halves in spread mode; outer 30% zones in single mode;
- horizontal touch swipe with click suppression after a real swipe;
- keyboard ArrowLeft/ArrowRight, PageUp/PageDown, Home and End;
- `aria-live` page counter and a book `aria-label` that includes the counter;
- image alt text identifying page number out of total;
- mode switching at the 820 px breakpoint while preserving the current anchor page as closely as possible;
- transition-end plus timeout fallback so a missed CSS event cannot lock the book;
- `prefers-reduced-motion` effectively removes the turning animation;
- do not put a CSS `filter` on the 3D book container if it would flatten `preserve-3d`; put shadows on pages/faces instead.

#### 11.4 Fullscreen interface

Request fullscreen on `document.documentElement`. Synchronize a `body.fs` class with `fullscreenchange` and `webkitfullscreenchange`; change the button label between “Tela cheia” and “Sair da tela cheia”. Support standard and WebKit-prefixed request/exit methods where present.

In fullscreen, the visual hierarchy is mandatory:

- **Above the book:** only **“Dois projetos de Brasil em disputa”**. Hide the kicker.
- **Below the book:** only the numeric page indicator/counter. Hide the slider and usage hint.
- The book remains centered and as large as the viewport safely allows.

On desktop fullscreen (min-width 821 px), distribute all other controls intelligently along the sides as fixed, legible buttons:

- upper left: “⌂ Página principal”;
- upper right: “Sair da tela cheia”;
- left center: “Início” above “Anterior”;
- right center: “Fim” above “Próxima”;
- lower left: “⬇ PDF A5”.

Reserve approximately **252 px** of total horizontal space for those side rails in the book-width calculation (spread up to 1520 px; height constrained with about 118 px reserved for title/counter/chrome). Buttons must wrap within about 112 px, remain at least 44 px high, carry a shadow and never cover the visible page area.

On mobile fullscreen (max-width 820 px):

- show **no buttons or download links at all**;
- keep only the H1 above and the page counter below;
- size the single page up to 98vw, height-constrained with about 106 px reserved;
- page changes are by horizontal swipe, with edge taps retained as an invisible gesture fallback;
- respect safe-area insets.

Leaving fullscreen restores the normal header kicker, bottom controls, slider and hint.

### 12. Prompt PDF generator — `ferramentas/gerar_prompt_pdf.py`

Write a small Python renderer, run from the repository root:

- input: `prompt/prompt-analise-a5.md`;
- output: `downloads/Prompt-Analise-A5.pdf`;
- page size: A4 (this is a readable prompt handout; the prompt it contains specifies an A5 output);
- locate the exact heading `## O PROMPT` in the Markdown and render the prompt body after a generated title/explanatory first page;
- render headings, paragraphs, bullets, numbered items, quotations, bold/italic and inline code in a restrained serif/sans design;
- first page explains the two-prompt split in Portuguese, gives curator/AI credits and includes the curator disclaimer;
- state that the complete prompt was recreated in English and is repository-only at `prompt/PROMPT-COMPLETO-SITE.md`;
- footer on every page: downloadable-prompt identification, **by rogerelizar**, **Arena.ai — Agent Mode**, the actual generation date/time in `America/Sao_Paulo`, and page number;
- PDF metadata identifies the downloadable A5 prompt and credits.

Keep the Markdown source compatible with this deliberately simple line-oriented renderer: one paragraph or list item per line; no Markdown tables or fenced code blocks inside the downloadable prompt body unless the renderer is upgraded to handle them properly.

After every prompt-PDF render, measure the actual page count and file size and update user-facing labels and README values contextually.

### 13. Repository structure and README

Maintain this structure:

```text
index.html
analise.html
README.md
fontes-primarias/
  PropostasLula.pdf
  PropostasFlavio.pdf
downloads/
  Analise-2026-Ebook-A5.pdf
  Analise-2026-Flipbook.html
  Prompt-Analise-A5.pdf
prompt/
  prompt-analise-a5.md
  PROMPT-COMPLETO-SITE.md
ferramentas/
  gerar_ebook_flipbook.py
  gerar_prompt_pdf.py
```

The README must explain:

- open `index.html` first;
- what the opening screen, main report, flipbook and e-book are;
- content/sections and primary sources;
- PT-primary/EN-secondary policy;
- the single floating menu, styles/themes/accessibility and preferences;
- all downloads with current page counts/sizes;
- the two-prompt split, including that the complete prompt is in English, replaces the former consolidated Portuguese prompt at the same repository path, and is not downloadable;
- generator commands and the fact that `analise.html` is the single content source for both book profiles;
- candidate-name and symmetric-terminology rules.

Do not publish this complete prompt under `downloads/`, and do not link to it with a `download` attribute from any page.

### 14. Build sequence

Execute in this order:

1. Inspect the repository and preserve unrelated user work.
2. Archive and extract the two official PDFs; build the evidence/source ledgers.
3. Verify tickets, final votes, runoff chronology and the official baseline.
4. Draft the Portuguese analysis and structured modeling dataset.
5. Build `analise.html`, including i18n, charts, menu, preferences, styles and accessibility.
6. Build `index.html` and verify that it does not load the flipbook automatically.
7. Write/update the Portuguese downloadable A5 prompt so it mirrors the final A5 analysis specification.
8. Write this complete English prompt, replacing the prior repository prompt.
9. Implement `ferramentas/gerar_prompt_pdf.py`; render the downloadable prompt PDF.
10. Implement `ferramentas/gerar_ebook_flipbook.py`; generate the standard e-book and large-print flipbook.
11. Measure actual page counts and file sizes; update opening-page labels, main-page download labels, README and any prompt references with targeted replacements only.
12. Run the full QA suite in Section 15; inspect real rendered pages, not only source text.
13. Commit only intended files, push only to the authorized working/session branch and open a pull request to `main`. Merge only if the curator explicitly asks.

Generated artifacts that are part of the published project (the HTML pages, three files under `downloads/`, prompts, generators, README and primary PDFs) belong in Git according to the repository’s established convention. Keep caches, temporary page images and intermediate PDFs out of Git.

### 15. Validation and quality gates

Do not claim browser screenshot QA unless it was actually performed. At minimum, run and report:

#### 15.1 Static/source checks

- HTML structure and duplicate-id checks for `index.html` and `analise.html`;
- all relative links resolve inside the repository;
- no `download` link points to `PROMPT-COMPLETO-SITE.md` or any copy of the complete prompt;
- visible-text search shows no letter codenames for candidates;
- paired movement-term counts are equal for each pair used, including derivatives, and the “-ism” explanation is present;
- `node --check` passes for every extracted inline report script and for the extracted flipbook engine;
- Python generators compile with `python3 -m py_compile`; remove `__pycache__` artifacts before commit;
- targeted page-count updates did not corrupt unrelated strings such as the hex color `#137547` or the LGPD law path containing `l13709`.

#### 15.2 Data and content checks

- exactly 12 areas and 24 modeling observations;
- row values equal Section 6.2 in web, e-book and flipbook data;
- radar means and time normalization recomputed independently;
- vote series and candidate order match the final tally;
- every canvas id referenced by web code and by the book generator exists exactly once, especially `chart_dependency_canvas`;
- reference anchors cited in prose exist and reference entries are not orphaned in a misleading way.

#### 15.3 Interactive simulation

Use a DOM/browser test capable of running the scripts. For the main report, verify language switching and persistence, light default, theme/style changes, accessibility toggles, dialog open/close/focus return, contents navigation and chart creation without JavaScript errors.

For the flipbook, verify at least:

- desktop starts as a centered lone cover;
- Next reaches pages 2–3;
- Last reaches the single centered final page for the current even page count and disables Next;
- Previous/First and slider work;
- main-page and A5-PDF links are correct;
- mobile starts in single-page mode and advances/returns by swipe;
- a simulated fullscreen change adds `body.fs` and changes the exit label;
- fullscreen CSS hides kicker/slider/hint, puts desktop controls on the sides and hides all mobile buttons;
- mobile fullscreen still turns pages by swipe;
- zero JavaScript errors.

#### 15.4 PDF and visual checks

For both generated book profiles:

- page size is A5;
- standard e-book page count is measured and matches every label (54 in the reference build);
- large-print/flipbook page count is measured and matches every label (148 in the reference build);
- fonts are embedded and body text is selectable/searchable;
- inspect cover, title page, table of contents, candidate profiles, programme structures, at least one complete matrix area, every chart type, data blocks, identical proposals, one alert cluster, evolution cards, verdict, references and back cover;
- confirm candidate cards and matrix candidate blocks are visibly separated by headings/rules/paragraph breaks;
- text-search alone is not sufficient: visually confirm that Flávio Bolsonaro’s material does not begin mid-paragraph after Lula’s, or vice versa;
- check for blank unintended pages, clipped text, overlapping labels, orphan headings/rules and chart/caption separation.

For the downloadable prompt PDF:

- confirm the text is selectable and contains the fallback sentence, the 54-page A5 reference, the frozen modeling values and the candidate-separation rule;
- visually inspect first, middle and last pages;
- measure its actual page count (8 in the latest reference render) and update the website label.

Serve the repository over local HTTP bound to `0.0.0.0` and confirm HTTP 200 and expected byte sizes for `/`, `/analise.html`, the flipbook, the A5 e-book, both programme PDFs and the prompt PDF. Where practical, byte-compare the served flipbook with the repository file.

### 16. Final acceptance checklist

The work is complete only when all statements below are true:

- the root opening screen is light, bilingual and offers flipbook versus main page without preloading the flipbook;
- the main report opens in Portuguese, light theme and Newspaper style;
- there is one floating ☰ Menu and no competing options entry point;
- all ten analytical sections and five charts are present and functional;
- candidates are named everywhere in visible text;
- Bolsonarismo/Lulismo terminology is paired, equally emphasized and explained;
- the same 24-row dataset drives web charts, book charts and printed data;
- the standard A5 e-book and large-print flipbook contain the same Portuguese analysis, differently typeset;
- the printed cover matches the exact flag/ballot-box/“2026”/byline/subtitle brief;
- no candidate’s attributed passage runs into the other’s without a paragraph/block separation;
- the flipbook is larger in normal view, has no subtitle/credits in its interface header, and follows the exact fullscreen title/counter rule;
- desktop fullscreen controls are on the sides; mobile fullscreen has no buttons and works by swipe;
- the downloadable prompt is the Portuguese A5-only prompt;
- this complete English prompt is repository-only and absent from every download list;
- page counts and file sizes in all labels/docs match the generated artifacts;
- all factual claims are officially sourced or carry the exact TSE fallback;
- accessibility preferences persist and the report is readable on a small phone;
- the final response gives a concise build report with files changed, generated page counts/sizes, validation performed, remaining fallbacks (if any), commit and pull-request status.

## END COMPLETE PROMPT

---

## Appendix — Provenance and curator decisions incorporated

This appendix is an audit summary, not part of the prompt above.

The project began with an English request for a senior full-stack developer and political scientist to compare two official Brazilian presidential programmes in one HTML5 document, including a policy matrix, Chart.js feasibility modeling, an investigative summary and real-time research restricted to official sources. The curator then refined the work through a sequence of decisions that this recreated prompt consolidates:

1. final page in Brazilian Portuguese, later expanded to Portuguese primary and English secondary;
2. visible curator/AI credits, curator disclaimer, responsible-citizenship call and frozen publication date/time;
3. improved UI/UX with Standard, Gamer and Newspaper visual styles;
4. one floating hamburger menu for all options and responsive typography for small phones;
5. light theme by default, with the Newspaper night edition only in dark theme;
6. strict symmetric treatment of *bolsonarismo/lulismo* and their derivatives;
7. candidates cited by name rather than by letter, with an equal-status explanation for the “-ism” suffix;
8. downloadable A5 e-book and HTML5 flipbook with the specified flag/ballot-box cover;
9. permanent split between the downloadable A5-analysis prompt and the repository-only complete prompt;
10. centered desktop two-page flipbook spread, centered lone covers and a mobile single-page hinge engine;
11. root opening choice screen and a dedicated 16 pt large-print flipbook, prioritizing legibility over low page count;
12. lean flipbook header, larger normal and fullscreen book sizes, desktop fullscreen side controls, button-free mobile fullscreen navigation by swipe, and strict paragraph separation between candidate-attributed passages;
13. updating the downloadable A5 prompt from the latest edition and recreating this complete prompt in English as the repository-only replacement for the previous consolidated Portuguese version.

Where an early request used an internal shorthand or a layout later superseded by the curator, the consolidated prompt above is authoritative.
