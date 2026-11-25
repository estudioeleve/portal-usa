# PASSO A PASSO — CRIAR O ROBÔ DO PORTAL USA PELA API DA META
Custo total: R$ 0 (API da Meta, GitHub e Claude que você já usa).
Dependências externas: Meta (Instagram + Facebook + developers.facebook.com) e GitHub.
Tempo: uns 40 minutos. Dá para fazer no PC (recomendado) — algumas telas da Meta não abrem bem no celular.

Para o Claude que receber este zip: leia LEIA-ME-PRIMEIRO.md, robo/REGRAS-FONTES.md e este arquivo. Guie o Israel UMA ETAPA POR VEZ, em português, com o link direto e o caminho completo de cada tela. Nunca peça para ele colar token, senha ou chave na conversa.

---------------------------------------------------------------------
## ETAPA 1 — Deixar o @portalusanews como conta Profissional (no celular)
1. Abra o Instagram já logado no @portalusanews.
2. Toque na sua foto (canto de baixo, à direita) → nas 3 linhas ☰ (canto de cima, à direita).
3. Vá em "Tipo de conta e ferramentas" (ou "Para profissionais") → "Mudar para conta profissional".
4. Escolha a categoria "Site de notícias e mídia" (ou "Empresa de mídia/notícias").
5. Escolha "Empresa" (não "Criador" — Empresa libera tudo, inclusive Stories pela API).
Pronto quando: aparecer "Painel profissional" no seu perfil.

## ETAPA 2 — Criar a Página do Facebook do Portal USA
1. No PC, abra: https://www.facebook.com/pages/create
2. Nome: Portal USA News. Categoria: "Site de notícias e mídia".
3. Coloque a foto de perfil (identidade/foto-perfil.png) e a capa, se quiser. Salve.

## ETAPA 3 — Criar (ou usar) o portfólio empresarial (Business Manager)
1. Abra: https://business.facebook.com/settings
2. Se você já tem o portfólio da ELEVE / Portal ONE News, pode usar o mesmo. Se não, clique em "Criar portfólio empresarial" e preencha nome e e-mail.
3. Em "Contas" → "Páginas" → "Adicionar" → escolha a Página "Portal USA News".
4. Em "Contas" → "Contas do Instagram" → "Adicionar" → entre com o @portalusanews e autorize.
   Isso também liga o Instagram à Página.
Pronto quando: a Página e o @portalusanews aparecem dentro do portfólio.

## ETAPA 4 — Criar o app gratuito na Meta
1. Abra: https://developers.facebook.com/apps
   (Se for a primeira vez, clique em "Começar" e confirme sua conta de desenvolvedor com o e-mail/celular.)
2. Clique em "Criar app".
3. Nome do app: "Robo Portal USA". E-mail: o seu.
4. Caso de uso: escolha "Gerenciar mensagens e conteúdo no Instagram" (se não aparecer, escolha "Outro" → tipo "Empresa").
5. Portfólio empresarial: escolha o da ETAPA 3. Clique em "Criar app".
6. Dentro do app, no menu da esquerda: "Casos de uso" → "Personalizar" (no do Instagram) → "API do Instagram com login do Facebook" (Instagram API with Facebook Login).
7. Em "Permissões", adicione:
   instagram_basic, instagram_content_publish, pages_show_list, pages_read_engagement, business_management
   (opcional para responder comentários depois: instagram_manage_comments)
8. Deixe o app no "Modo de desenvolvimento". Não precisa enviar para análise da Meta, porque só você (administrador) vai usar nas suas próprias contas.

## ETAPA 5 — Gerar a chave que não expira (usuário do sistema)
1. Abra: https://business.facebook.com/settings/system-users
2. Clique em "Adicionar" → nome "robo-portal-usa" → função "Administrador" → Criar.
3. Clique no usuário criado → "Atribuir ativos":
   - Apps → "Robo Portal USA" → controle total.
   - Páginas → "Portal USA News" → controle total.
   - Contas do Instagram → @portalusanews → controle total.
   Salve.
4. Clique em "Gerar novo token" → escolha o app "Robo Portal USA" → validade "Nunca" →
   marque as mesmas permissões da ETAPA 4 → "Gerar token".
5. COPIE o token e guarde num lugar seguro (bloco de notas no seu PC ou gerenciador de senhas).
   NÃO cole na conversa com o Claude. NÃO coloque no GitHub.

## ETAPA 6 — Descobrir o ID da conta do Instagram
1. Abra: https://developers.facebook.com/tools/explorer
2. Em "Aplicativo da Meta" escolha "Robo Portal USA". Em "Token de acesso" cole o token da ETAPA 5 (essa ferramenta é da própria Meta, pode colar lá).
3. No campo de consulta, escreva:  me/accounts?fields=name,instagram_business_account
   e clique em "Enviar".
4. Vai aparecer a Página "Portal USA News" e, dentro de "instagram_business_account", um "id" que começa com 1784...
   Esse número é o IG_USER_ID. Guarde junto com o token (esse número não é segredo).

## ETAPA 7 — Guardar a chave no COFRE do Claude (Network secrets)
A chave NÃO vai na conversa, NÃO vai no GitHub e NÃO vai em "Environment variables" (lá qualquer um que usa o ambiente lê).
O lugar certo é "Network secrets": o Claude coloca a chave sozinho em cada chamada para a Meta e o robô nunca vê a chave.
Faça no PC:
1. Abra: https://claude.ai/code
2. Logo acima da caixa de mensagem, clique no botão com o ícone de nuvem e o nome do ambiente (ex.: "Default").
3. No menu que abre, em "Cloud":
   - Recomendado: clique em "Add cloud environment" e crie um ambiente só do robô, nome "Portal USA" (Network access: Trusted). Assim a chave do Portal USA não mistura com a do Portal ONE News.
   - Depois passe o mouse em cima do ambiente "Portal USA" e clique na engrenagem que aparece à direita.
4. Na janela "Edit cloud environment", clique na linha "Network secrets" → "Add secret".
5. Preencha:
   - Secret type: Bearer (deixe o padrão)
   - Allowed websites: graph.facebook.com
   - Custom headers: Header name = Authorization | Prefix = Bearer | Value = COLE AQUI A CHAVE do Bloco de Notas
6. Clique em "Add". Pronto — depois de salvo, nem você consegue ver o valor de novo (é normal).
7. Ainda nessa janela, em "Environment variables", escreva uma linha (esse número não é segredo):
   IG_USER_ID=1784xxxxxxxxxxx
   e clique em "Save changes".
8. Na tarefa agendada do robô do Portal USA, escolha o ambiente "Portal USA".
9. Teste: o Claude roda, dentro desse ambiente,  python3 robo/publicar_meta.py limite
   Se responder com "quota_usage", a chave está funcionando. Se a lista de segredos mostrar "Not sent", ler a nota embaixo.

## ETAPA 8 — Repositório público para as mídias
1. O Claude cria o repositório público "estudioeleve/portal-usa" no GitHub (mesmo esquema do Portal ONE News).
2. Pastas: dados/feed, dados/reels, dados/carrossel, entrada/ (o que o Israel mandar), modelos/, robo/.
3. Cada mídia vai por commit e o robô usa a URL raw.githubusercontent.com/estudioeleve/portal-usa/<commit>/dados/...
   (jsDelivr não serve acima de 20 MB; usar raw).
4. Vídeo final abaixo de 100 MB (crf 21, maxrate 6M).

## ETAPA 9 — Teste
1. O Claude monta um post de teste de feed com a moldura e manda a prévia ao Israel.
2. Com o OK do Israel, roda:  python3 robo/publicar_meta.py foto URL "legenda"
3. Confere no @portalusanews. Depois testa um Reels:  python3 robo/publicar_meta.py reels URL_VIDEO "legenda"

## ETAPA 10 — Ligar os robôs (tarefas agendadas)
A) ROBÔ DE MATÉRIA (o Israel manda vídeos e fotos)
   - O Israel manda os vídeos/fotos na conversa do Portal USA (ou na pasta entrada/ do repositório).
   - O robô segue LEIA-ME-PRIMEIRO.md, seção "A": assiste, confere, escreve, monta e POSTA com publicar_meta.py.
B) ROBÔ DE NOTÍCIAS (rodadas automáticas)
   - Tarefa agendada, sugestão: de hora em hora entre 7h e 23h (horário de Nova York), minuto quebrado (ex.: :13).
   - Prompt da tarefa (colar inteiro ao criar):

"""
Você é o robô do Portal USA (@portalusanews), notícias para imigrantes brasileiros nos EUA.
Sempre em português. Clone o repositório público estudioeleve/portal-usa e leia LEIA-ME-PRIMEIRO.md e robo/REGRAS-FONTES.md — siga tudo.
1. Varra as fontes da REGRAS-FONTES.md e escolha até 2 notícias novas que afetam brasileiros nos EUA (não repetir o que já está em dados/postados.json).
2. Confira cada fato em pelo menos uma fonte confiável. Operação do ICE só com fonte confirmada.
3. Escreva na voz do Portal USA: de "você", com o bloco "O que isso muda pra você" e pergunta à comunidade citando a cidade.
4. Monte a arte com modelos/ (moldura de feed, ou Reels vertical com a bandeira 3D se houver vídeo próprio/liberado). Margens de segurança, texto fora de rosto, logo oficial.
5. Faça commit da mídia em dados/ e publique com: python3 robo/publicar_meta.py (foto|carrossel|reels) ...
   A chave está no cofre do Claude (Network secrets, graph.facebook.com) e o IG_USER_ID nas variáveis do ambiente "Portal USA" — nunca peça, escreva ou grave a chave.
6. Registre em dados/postados.json (título, fonte, link, data). Não mande notificação ao Israel.
7. Se der erro da Meta, tente 1 vez de novo; se persistir, registre o erro em dados/erros.log e pare.
"""

---------------------------------------------------------------------
## INFORMAÇÕES DA API (para o Claude)
- Publicação em 2 passos: POST /{IG_USER_ID}/media (cria o container) → POST /{IG_USER_ID}/media_publish (publica).
- Foto: image_url (JPEG). Reels: media_type=REELS, video_url, share_to_feed=true, cover_url opcional.
- Carrossel: até 10 itens (fotos e vídeos), cada item com is_carousel_item=true, depois media_type=CAROUSEL + children.
- Vídeo: esperar status_code = FINISHED antes de publicar (GET /{container}?fields=status_code).
- Collab: parâmetro collaborators (até 3 @), funciona em foto, carrossel e Reels.
- Limite: 50 posts por 24 h por conta (carrossel conta 1). Ver uso: GET /{IG_USER_ID}/content_publishing_limit.
- Containers expiram em 24 h.
- Reels: MP4 (H.264 + AAC), vertical 1080x1920, até 15 min (ideal até 90 s), até 300 MB pela URL.
- Documentação oficial: https://developers.facebook.com/docs/instagram-platform/content-publishing
- O mesmo esquema serve depois para o Portal ONE News (resolve a collab nos Reels).

## SE DER ERRO
- "Invalid OAuth access token": token errado ou sem permissão → refazer ETAPA 5 marcando todas as permissões.
- "Application does not have permission": falta instagram_content_publish → ETAPA 4, item 7.
- "The user is not an Instagram Business": refazer ETAPA 1 e 3 (conta Profissional e ligada à Página).
- "Media download has failed": a URL da mídia não é pública ou o arquivo é grande demais → usar raw.githubusercontent.
- Código 2207042: passou do limite de 50 posts em 24 h → esperar.
