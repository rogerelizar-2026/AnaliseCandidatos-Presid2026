# AnaliseCandidatos-Presid2026

Relatório analítico em **português brasileiro** sobre os programas de governo dos dois finalistas da eleição presidencial brasileira de 2026 — **Lula (PT, 13)** e **Flávio Bolsonaro (PL, 22)** — com data de corte em 23 de outubro de 2026.

## Como abrir

Abra o arquivo **`index.html`** em qualquer navegador moderno: ele é a **tela inicial de escolha** (leve e rápida), com dois caminhos — **📖 Ler no flipbook** (edição digital em fonte ampliada) ou **📊 Ir para a página principal** (`analise.html`, o relatório interativo completo; os gráficos usam Chart.js via CDN e requerem conexão na primeira carga). A tela de abertura também oferece o download direto do e-book PDF A5 para impressão.

## Conteúdo

- Perfis eleitorais e institucionais com votos exatos do 1º turno (TSE);
- Matriz comparativa lado a lado em 12 áreas de política, com páginas dos PDFs;
- Modelagem de viabilidade em gráficos interativos (tempo × custo, impacto × dependências, risco × tempo) com base de dados auditável;
- Sumário investigativo: convergências, vieses ideológicos nomeados, mapa de vetos institucionais e promessas sob alerta jurídico-fiscal (CF, Lei 8.213/1991, Lei 13.260/2016, LGPD, BCB, IBGE, INPE e Tesouro Nacional);
- Temas sensíveis e evolução das propostas entre o 1º e o 2º turno;
- Notas de rodapé com links para verificação direta nas fontes oficiais.

## Fontes primárias

Os dois PDFs registrados no TSE (DivulgaCandContas) estão arquivados em `fontes-primarias/`:

- `fontes-primarias/PropostasLula.pdf` (84 páginas)
- `fontes-primarias/PropostasFlavio.pdf` (76 páginas)

As citações "p. X" no relatório referem-se à paginação impressa de cada PDF.

## Idiomas, acessibilidade e downloads

- **Português brasileiro é o idioma principal** (autoritativo); o **inglês é o secundário**. Alternância no **botão flutuante ☰ Menu**.
- O **botão flutuante único ☰ Menu** (hambúrguer, canto inferior direito) concentra **todas** as opções — índice de seções, idioma, tema, estilo, acessibilidade e downloads: idioma, **tema claro/escuro/automático**, **acessibilidade** (tamanho do texto, alto contraste, links sublinhados, redução de movimento) e **downloads em PDF**.
- **Downloads (☰ Menu):** análise completa em **e-book PDF A5** (`downloads/Analise-2026-Ebook-A5.pdf`, 52 pp., capa com bandeira desfocada + urna “2026” + “by rogerelizar” + subtítulo “2º Turno 2026 - Criado por IA”), **flipbook HTML5 em fonte ampliada** (`downloads/Analise-2026-Flipbook.html`, 138 pp., ≈16 MB, arquivo único e offline; edição digital rediagramada com **corpo de 16 pt** e tabelas em blocos para leitura confortável na tela; no desktop abre em 2 páginas centradas e no celular em página única, imagens WebP 190 dpi; botão “⌂ Página principal” de volta ao relatório), os programas oficiais (`fontes-primarias/PropostasLula.pdf`, `fontes-primarias/PropostasFlavio.pdf`) e o **prompt da análise A5** (`downloads/Prompt-Analise-A5.pdf`). Geradores: `ferramentas/gerar_ebook_flipbook.py` e `ferramentas/gerar_prompt_pdf.py` (rodar da raiz).
- **Prompts divididos em dois:** o **para download** é o que gera a análise em PDF A5 (fonte: `prompt/prompt-analise-a5.md`); o **prompt completo** do site e de todos os complementos fica **só no repositório** (`prompt/PROMPT-COMPLETO-SITE.md`, com o prompt original e o histórico de refinamentos em anexo), **sem download** na página.
- Os candidatos são citados **sempre pelo nome** (sem codinomes por letra); os alertas do sumário investigativo são numerados por candidato (“Lula, alerta n” / “Flávio Bolsonaro, alerta n”).
- As preferências ficam salvas no navegador (`localStorage`). Na versão em inglês, citações literais, páginas dos PDFs e títulos de fontes permanecem em português para preservar a auditabilidade.
- **Tema claro por padrão** (estilo Jornal diurno); o tema escuro (edição noturna) é opcional no ☰ Menu. **Estilo principal: 📰 Jornal — claro por padrão (edição noturna no tema escuro)**, com diagramação editorial (manchete, fios duplos, capitular, colunas) e tipografia fluida responsiva para celulares pequenos. Alternativos no ☰ Menu: **Padrão** (limpo) e **🎮 Gamer** (neon escuro). Mudam só a apresentação — conteúdo, dados e notas são idênticos. No celular (≤820px) o sumário superior some e a navegação fica no menu. Inclui barra de progresso de leitura e “voltar ao topo” dentro do menu.
- **Rótulos simétricos (regra editorial):** “bolsonarismo” e “lulismo” (e derivados bolsonarista/lulista) só aparecem emparelhados, com o mesmo destaque e estatuto de fonte. “Extrema-direita/esquerda” não são aplicados a nenhum lado: exigiriam citação direta (página) dos programas originais, que não contêm esses termos (busca integral verificada nos PDFs do TSE).
