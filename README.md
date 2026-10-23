# AnaliseCandidatos-Presid2026

Relatório analítico em **português brasileiro** sobre os programas de governo dos dois finalistas da eleição presidencial brasileira de 2026 — **Lula (PT, 13)** e **Flávio Bolsonaro (PL, 22)** — com data de corte em 23 de outubro de 2026.

## Como abrir

Abra o arquivo **`index.html`** em qualquer navegador moderno (documento HTML5 único e autocontido; os gráficos interativos usam Chart.js via CDN e requerem conexão na primeira carga).

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

- **Português brasileiro é o idioma principal** (autoritativo); o **inglês é o secundário**. Alternância nos botões `PT | EN` do topo ou em **⚙ Opções**.
- O botão **⚙ Opções** concentra: idioma, **tema claro/escuro/automático**, **acessibilidade** (tamanho do texto, alto contraste, links sublinhados, redução de movimento) e **downloads em PDF**.
- Downloads: `fontes-primarias/PropostasLula.pdf`, `fontes-primarias/PropostasFlavio.pdf` e `downloads/Prompt-Gerador-da-Pagina.pdf` (prompt integral do curador **by rogerelizar**; gerador em `ferramentas/gerar_prompt_pdf.py`).
- As preferências ficam salvas no navegador (`localStorage`). Na versão em inglês, citações literais, páginas dos PDFs e títulos de fontes permanecem em português para preservar a auditabilidade.
