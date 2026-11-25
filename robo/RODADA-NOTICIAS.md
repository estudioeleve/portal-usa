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
   - Título na arte: no máximo 3 linhas, todas do MESMO tamanho (padrão do Israel). Nunca linha cheia em cima
     e 1 ou 2 palavras embaixo. O script recusa título desequilibrado: aí reescreva o título e rode de novo.
   - A arte segue a MOLDURA OFICIAL do feed (molduras/portal-usa-moldura-feed.png): foto cheia, logo no canto superior
     esquerdo, degradê no rodapé, chip vermelho, título e @portalusanews. Nunca outro layout.
   - FOTO DA FONTE (regra do Israel, 25/11/2026 — igual ao robô do Portal ONE News). Nunca postar só com a bandeira.
     a) `python3 robo/coletar.py LINK_DA_MATERIA` → baixa a foto principal (og:image) em dados/feed/fotos/,
        apara as bordas (robo/aparar.py) e grava o crédito da figcaption em dados/feed/fotos/coleta.json.
     b) ABRA e OLHE a foto. Só serve se: for do fato (nada de foto de arquivo antiga ou genérica); nítida, boa
        resolução, sem estar escura/tremida/borrada; assunto principal no centro, sem cabeça cortada; sem marca
        d'água nem logo de outro veículo (se tiver, cubra ou desfoque); sem rosto de imigrante sem documento.
     c) Não serviu → outra matéria do mesmo fato: `python3 robo/coletar.py OUTRO_LINK --anexar`.
        Nenhuma serviu → NÃO publique. Nunca invente imagem, nunca use foto ruim.
     d) A foto preenche o quadro inteiro da moldura (zoom se precisar); texto nunca em cima de rosto ou cabeça.
     e) Crédito na legenda e na arte: "Foto: NOME / VEÍCULO" (sem nome: "Foto: reprodução / VEÍCULO").
     f) Erro de rede no download (403/bloqueado; o coletar.py sai com "ERRO DE REDE"): PARE, escreva em
        dados/erros.log e avise o Israel. Não tente outro caminho.
     - Dependências: pip install requests trafilatura beautifulsoup4 ftfy pillow --break-system-packages
   - TAPAR O ROSTO: antes de usar, rode `python3 robo/tapar_rosto.py foto.jpg foto_tapada.jpg` e OLHE o resultado.
     Todo rosto de imigrante (e de menor) tem que estar irreconhecível. Se sobrou rosto, tape com
     `--caixa x,y,largura,altura` (pode repetir). Rosto de autoridade pública (agente identificado, político) pode ficar.
   - Depois: acrescente no fim do comando da arte o arquivo da foto tapada e o crédito "Foto: NOME / VEÍCULO".
   - Nunca escrever "imagem ilustrativa"/"imagem conceitual".
   - Dependências: pip install pillow "opencv-python-headless<5" --break-system-packages
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
