# Landing page para prestador de serviço

Página única de divulgação para um profissional autônomo de serviços técnicos. Neste caso, conserto de eletrodomésticos e TVs. O objetivo é **levar o visitante a pedir um orçamento pelo WhatsApp**. Todas as seções existem para apoiar essa ação.

É um site estático: HTML, CSS e JavaScript puros, sem framework e sem build obrigatório. Basta abrir o `index.html` num servidor local (por exemplo, a extensão Live Server do VS Code) ou publicar a pasta em qualquer hospedagem estática.

## Estrutura da página

| Seção | Papel na página |
| --- | --- |
| Topo (hero) | Diz o que é o serviço, mostra o profissional e oferece o botão de orçamento e o telefone |
| O que eu conserto | Lista os aparelhos atendidos, com os defeitos mais comuns e onde o conserto é feito |
| Faixa de destaque | Põe em evidência a especialidade principal e o serviço de busca em casa |
| Do defeito ao conserto | Explica o processo em três passos, deixando claro que o preço vem antes do serviço |
| Quem conserta | Formação técnica e motivos para confiar no profissional |
| Dúvidas comuns | Responde às objeções mais frequentes (preço, garantia, atendimento em casa, região) |
| O que aconteceu? | Formulário interativo que monta a mensagem e abre o WhatsApp com o texto pronto |
| Rodapé | Navegação, contato e créditos das imagens |

## Arquivos

```
index.html              a página
styles.css              todo o visual (tokens de cor e tipografia no topo)
main.js                 formulário do WhatsApp, animações de entrada, troca de imagens, botões flutuantes
assets/
  fonts/                fonte Chillax (servida localmente, sem depender de CDN)
  icons/                favicon e ícone do WhatsApp
  images/               GERADA pelo script; não editar à mão
    appliances/thumb/   miniaturas dos aparelhos: 96px e 192px
    appliances/large/   aparelhos grandes: cabem em 400px e 800px
    character/          ilustração do profissional: 360, 540, 720 e 980px de largura
    photos/             fotos: 400px e 800px
    og-image.jpg        imagem da prévia de link (WhatsApp, Facebook), 1200x630
    manifest.json       tamanho real de cada arquivo gerado
  credits.json          origem e licença de cada imagem e da fonte
source-images/          originais em alta resolução, não carregados pela página
scripts/
  build-images.py       gera assets/images/ a partir de source-images/
```

## Imagens responsivas

Cada imagem é gerada em mais de um tamanho, e o HTML usa `srcset` e `sizes` para o navegador baixar só o tamanho necessário. Um celular comum baixa a miniatura de 96px, e uma tela de alta densidade baixa a de 192px. Tudo sai em WebP.

Para trocar ou adicionar uma imagem:

1. Coloque o original em `source-images/` com o nome em inglês (por exemplo, `source-images/appliances/refrigerator.png`). Aparelhos devem ter fundo transparente.
2. Se for um aparelho novo, inclua o nome em `APPLIANCES` no topo de `scripts/build-images.py`.
3. Rode `python scripts/build-images.py` (precisa do Pillow: `pip install pillow`).
4. Aponte o HTML (ou o `main.js`, para o formulário) para os arquivos gerados.

## Tamanhos de tela (breakpoints)

| Largura | Comportamento |
| --- | --- |
| acima de 1024px | Desktop: topo dividido ao meio, seções em colunas |
| até 1024px | Tablet: topo empilhado, "Quem conserta" e formulário em uma coluna |
| até 760px | Celular: tudo em uma coluna, imagem do formulário oculta, botão flutuante do WhatsApp |

Para testar: 1440, 1025 e 1024, 768, 761 e 760, e 390.

## Para adaptar a outro prestador de serviço

- **Contato:** o número de WhatsApp aparece nos links `wa.me` do `index.html` e na constante `WHATSAPP` do `main.js`.
- **Serviços e defeitos do formulário:** lista `APARELHOS` no `main.js`.
- **Cores e tipografia:** variáveis em `:root`, no topo do `styles.css`.
- **Créditos:** o rodapé do `index.html` e o `assets/credits.json` precisam continuar batendo com as imagens usadas.
