# RODADA DE NOTÍCIAS — Portal USA (@portalusanews)

Siga também `LEIA-ME-PRIMEIRO.md` e `robo/REGRAS-FONTES.md` (fontes, colônias, voz e segurança do imigrante).
Tudo em português. Público: imigrantes brasileiros nos EUA, principalmente os sem documento.

## Em cada rodada
1. Leia `dados/postados.json` (o que já foi publicado). Nunca repita notícia nem assunto já postado nas últimas 48 h.
2. Procure notícias NOVAS (últimas ~6 h, no máximo 24 h) com a busca na web, nas fontes da `REGRAS-FONTES.md`
   (portais brasileiros nos EUA, ice.gov/uscis.gov/consulados, AP, Reuters, BBC Brasil, g1, Folha, UOL).
   Foco: imigração, deportação, ICE, documentos, consulados, trabalho, custo de vida, segurança, clima extremo
   e fatos das colônias (MA, NJ, NY, CT, FL, PA e outras).
3. Escolha NO MÁXIMO 1 notícia por rodada — a que mais afeta brasileiros nos EUA.
   Se não houver nada novo e relevante, NÃO publique nada e só termine.
4. Confira o fato em pelo menos 2 fontes confiáveis (ou 1 fonte oficial). Operação do ICE só com fonte confirmada.
   Sem pânico, sem boato. Na dúvida, não publique.
5. Arte: `python3 robo/arte_card.py "EDITORIA" "Título" "Fonte: NOME" dados/feed/AAAA-MM-DD-HHMM-slug.jpg`
   - EDITORIA curta: IMIGRAÇÃO, CONSULADO, TRABALHO, SEGURANÇA, CLIMA, COMUNIDADE, DIREITOS, ECONOMIA.
   - Título forte, verdadeiro, até ~90 caracteres, sem ponto final.
   - Sem foto (o ambiente não baixa imagens de outros sites). Nunca escrever "imagem ilustrativa"/"imagem conceitual".
   - Se o Pillow faltar: pip install pillow --break-system-packages
6. Legenda (nesta ordem):
   - Título com 1 emoji no início (🚨 só para urgente; 🇺🇸 📍 ⚠️ 📄 💼 conforme o tema)
   - 2 a 4 linhas com os fatos e a atribuição ("segundo o ICE", "de acordo com o Brazilian Times")
   - "👉 O que isso muda pra você:" + o que fazer, a quem procurar (consulado, advogado de imigração, entidade de apoio), prazos
   - Pergunta à comunidade citando a cidade/estado quando houver
   - "Fonte: NOME"
   - Hashtags: #imigrantes #brasileirosnoseua #portalusanews + cidade/estado (ex.: #boston #newark)
   - NUNCA expor nome ou rosto de imigrante sem documento. Menores: nunca identificar.
7. Publicar:
   - `git add` a arte e faça commit/push na main (git -c user.name="Robo Portal USA" -c user.email="noreply@anthropic.com").
   - Pegue o hash do commit: `git rev-parse HEAD`.
   - `python3 robo/publicar_meta.py foto "https://raw.githubusercontent.com/estudioeleve/portal-usa/<HASH>/dados/feed/<arquivo>.jpg" "<legenda>"`
   - A chave está no cofre do ambiente (Network secrets, graph.facebook.com). Nunca peça, imprima ou grave a chave.
   - Erro da Meta: tente mais 1 vez. Persistindo, escreva o erro em `dados/erros.log` (sem chave), faça commit e pare.
8. Registre em `dados/postados.json`: {"id","titulo","editoria","fonte","link_fonte","media_id","link","data_utc"}. Commit e push.
9. Não mande notificação para ninguém.
