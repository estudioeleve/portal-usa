# PORTAL USA (@portalusanews) — PACOTE COMPLETO
Leia este arquivo primeiro. Responda sempre em português, de forma curta, com custo e dependências ditos antes.

## O que tem no pacote
- identidade/ — logo "Portal [bandeira 3D] usa news" (Poppins, linhas da mesma largura, centralizadas), bandeira animada, paleta, foto de perfil.
  Cores: azul-marinho #0B1E4A, azul #132F6E, vermelho #C8202F (só no chip da editoria), branco.
- molduras/ — feed (1080x1350), Reels vertical (principal, 1080x1920), Reels horizontal; exemplo de Reels com a bandeira 3D se mexendo.
  Degradê forte no rodapé, sumindo até o meio.
- modelos/ — HTML/CSS/JS das molduras (flag3d.js = bandeira 3D; logo_usa.js = logo), rv.py (Reels com bandeira animada: rv_fixa.png + 45 quadros lf/%03d.png em loop com ffmpeg -stream_loop -1), shot.py (print com Playwright/Chrome).
- robo/REGRAS-FONTES.md — fontes, colônias e a voz do robô (conversar com o imigrante).
- robo/publicar_meta.py — publica foto, carrossel e Reels (com collab) pela API oficial da Meta.
- PASSO-A-PASSO-CRIAR-O-ROBO.md — caminho completo, etapa por etapa, para ligar o robô.

## COMO O ROBÔ TRABALHA
### A) Matéria a partir do que o Israel envia (vídeos e fotos)
1. O Israel manda vídeos e/ou fotos (pode vir com áudio, texto curto ou nada).
2. O robô assiste tudo: transcreve as falas (faster-whisper), olha os quadros, entende o fato.
3. Confere na web nomes, cidades e dados (REGRAS-FONTES.md, seção 2). Sem confirmação, não afirma.
4. Escreve a matéria em português, de "você" para o imigrante:
   título forte, lide com os fatos e atribuição, e o bloco "O que isso muda pra você" (o que fazer, a quem ligar, prazos).
5. Monta o post:
   - Vídeo → Reels vertical com a moldura e a bandeira 3D se mexendo. Vídeo horizontal: zoom no assunto principal, preenchendo o quadro.
   - Fotos → post de feed ou carrossel com a moldura do feed.
   - Edição de fala: deixar a pessoa terminar a frase, nunca cortar no meio; vários vídeos → editar pelas falas principais.
6. Legenda: título, resumo, "O que isso muda pra você", pergunta à comunidade (citando a cidade), hashtags (#imigrantes #brasileirosnoseua + cidade).
7. POSTA no @portalusanews.

### B) Rodadas automáticas de notícia
- Varre as fontes da REGRAS-FONTES.md, escolhe o que afeta brasileiros nos EUA, escreve na mesma voz e posta com a moldura.
- Sem notificação automática para o Israel avisando que postou.

## REGRAS VISUAIS (sempre)
- Logo oficial do Portal USA, sem esticar nem montar com pedaços.
- Margem de segurança: nada encostado nas bordas; Reels: esquerda 100, direita 170, topo abaixo de 190, nada importante abaixo de ~1500.
- Texto nunca em cima de rosto/cabeça. Texto centralizado, linhas equilibradas, poucas fontes (Poppins), poucas cores (só a paleta).
- Mostrar sempre o assunto principal da imagem. Nunca usar foto ruim, nem aparecer repórter de outro veículo.
- Nunca "imagem ilustrativa"/"imagem conceitual" na arte.
- Sem efeito sonoro que o Israel não tenha mandado.

## SEGURANÇA DO IMIGRANTE
- Nunca mostrar rosto ou nome de imigrante sem documento sem autorização dele (risco de deportação). Na dúvida, desfocar.
- Operação do ICE só com fonte confirmada. Sem pânico, sem boato.
- Menores: nunca identificar.

## POSTAGEM — como ligar o robô na conta
Opção 1 (recomendada, R$ 0): API oficial da Meta (Instagram Graph API, "Content Publishing").
- Conta @portalusanews precisa ser Profissional (Empresa ou Criador) e ligada a uma Página do Facebook.
- Criar um app em developers.facebook.com (gratuito), modo desenvolvimento, com o Israel como administrador.
- Permissões: instagram_basic, instagram_content_publish, pages_show_list, pages_read_engagement.
- Gerar token de longa duração (ou token de "usuário do sistema" no Business Manager, que não expira).
- Publicar: POST /{ig-user-id}/media (image_url / video_url com media_type=REELS / carrossel) → POST /{ig-user-id}/media_publish.
- O arquivo precisa estar numa URL pública (ex.: repositório GitHub público, raw.githubusercontent).
- Limite: 50 posts por 24 h por conta.
Opção 2: Windsor.ai (create_image_post / create_carousel_post / create_video_post) — o plano grátis só tem 1 conta, já usada pelo Portal ONE News.

## SEGURANÇA DAS CHAVES
- NUNCA gravar token/chave no repositório (é público) nem colar em conversa. Guardar no cofre do Claude: claude.ai/code → ambiente → engrenagem → Network secrets (ver ETAPA 7 do passo a passo).


## MATERIAL QUE O ISRAEL MANDA (regra dele, 24/11/2026)
- Quando o Israel mandar vídeo, foto e/ou print de outra matéria: ler o print/assistir o vídeo e fazer a notícia a partir disso (título, texto, "O que isso muda pra você", legenda). Conferir os fatos na web antes de publicar.
- Vídeo VERTICAL: vai na moldura de Reels vertical INTEIRO, sem cortar nenhuma parte, aumentado o máximo possível dentro da moldura (sem esticar/deformar).
- Vídeo HORIZONTAL: usa a moldura horizontal (portal-usa-moldura-reelsh).
- Foto ou vídeo com pessoa: a pessoa principal fica CENTRALIZADA no quadro. Texto nunca em cima do rosto.
