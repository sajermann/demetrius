# Instruções para o Claude

Landing page estática (HTML, CSS e JS puros) de um prestador de serviço de conserto de eletrodomésticos. O `README.md` explica a estrutura, as seções, as imagens e os breakpoints. Leia-o antes de mexer.

## Como trabalhar aqui

- Converse em português.
- **Servidor:** o usuário roda o Live Server do VS Code em `http://127.0.0.1:5500/index.html`. Use esse. Não suba outro servidor; se for realmente necessário, avise e derrube ao terminar.
- **Testes no navegador:** use o Playwright MCP.
  - Trabalhe numa aba só. Não chame `page.close()` no meio dos testes (isso gera várias abas `about:blank`).
  - Quando o usuário estiver acompanhando, traga a aba para a frente (`page.bringToFront()`).
  - Ao terminar, feche o navegador uma vez com `browser_close`.
  - Prefira medir com script e devolver um JSON curto (posições, larguras, `currentSrc`, overflow). Abra screenshots só quando precisar ver o visual, juntando vários numa imagem reduzida.
- **Tamanhos para testar:** 1440, 1025 e 1024, 768, 761 e 760, e 390. Os breakpoints são `max-width: 1024px` (tablet) e `max-width: 760px` (celular).

## Imagens

- Os originais ficam em `source-images/`, com nome em inglês. Tudo em `assets/images/` é gerado por `python scripts/build-images.py`. Nunca edite essa pasta à mão.
- Toda imagem usa `srcset` + `sizes`. Aparelhos grandes são descritos pela largura da caixa (`400w`, `800w`), porque o CSS define o tamanho exibido.
- A imagem do formulário "O que aconteceu?" muda conforme o aparelho escolhido. O mapeamento está em `APARELHOS` e `largeImage()` no `main.js`.

## Créditos (decisão do usuário)

- O rodapé tem um crédito único "Imagens: FreePNGImg" e o crédito da foto do multímetro (CC BY 2.0, a licença exige).
- Ao trocar uma imagem, mantenha o rodapé do `index.html` e o `assets/credits.json` batendo com o que é usado. Se uma imagem nova exigir crédito pela licença, avise o usuário.

## Conteúdo

- Textos em primeira pessoa (o profissional falando: "Eu encontro a causa", "Por que me chamar").
- TV é a especialidade, com busca na casa do cliente. Máquina de lavar e micro-ondas são consertados na casa do cliente. Placas eletrônicas e aparelhos menores são atendidos na bancada.
- O `README.md` não cita o nome do profissional. Mantenha assim.

## Linguagem e padrão de comunicação

- **Conversas e interações com usuário** Sempre converse com o usuário em  **Português Brasileiro (`pt-BR`)**.
- **Código fonte e documentação:** **100% in English**.
  - Todas variáveis, funções, classes, e nomes de constantes DEVEM estar em inglês.
  - Todos comentáriosm de código, docstrings (JSDoc), e mensagems de commit DEVEM estar em Inglês.
  - Exemplos:
    ```javascript
    // Bom:
    const activeWords = [];
    // Compute total placed cells
    function calculateGridCoverage() { ... }

    // Ruim:
    const palavrasAtivas = [];
    // Calcula celulas
    function calculaCobertura() { ... }
    ```

## Armadilhas já encontradas

- O lado esquerdo do "Sobre" usa `display: contents` no tablet. Por isso o `main.js` observa também os filhos de cada `[data-rise]`: um elemento sem caixa nunca dispara o IntersectionObserver.
- O personagem do topo se centraliza sozinho (`left: 50%` + `translate: -50% 4%`). A animação de entrada precisa manter o `-50%` horizontal.
