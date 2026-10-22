// The message builder, the entrances and the slow crossfade.

const WHATSAPP = 'https://wa.me/5511950202979';
const OPENING = 'Olá, Demetrius! Vim pelo site e quero um orçamento.';

// Each appliance: the picture shown beside the form (a name from assets/images, see largeImage),
// how it is said in a sentence, and its common defects.
const APARELHOS = [
  { nome: 'TV', imagem: 'tv', frase: 'Minha TV', defeitos: ['Não liga', 'Sem imagem', 'Linhas na tela', 'Sem som', 'Desliga sozinha'] },
  { nome: 'Máquina de lavar', imagem: 'washing-machine', frase: 'Minha máquina de lavar', defeitos: ['Não liga', 'Não centrifuga', 'Não puxa água', 'Não solta água', 'Vaza água', 'Faz barulho', 'Mostra erro'] },
  { nome: 'Placa eletrônica', imagem: 'circuit-board', frase: 'Minha placa eletrônica', defeitos: ['Não liga', 'Componente queimado', 'Em curto', 'Não aciona comandos', 'Mostra erro'] },
  { nome: 'Micro-ondas', imagem: 'microwave', frase: 'Meu micro-ondas', defeitos: ['Não esquenta', 'Não liga', 'Solta faísca', 'Prato não gira', 'Painel não responde'] },
  { nome: 'Air fryer', imagem: 'air-fryer', frase: 'Minha air fryer', defeitos: ['Não liga', 'Não esquenta', 'Desliga sozinha', 'Timer não funciona'] },
  { nome: 'Forninho', imagem: 'toaster-oven', frase: 'Meu forninho elétrico', defeitos: ['Não esquenta', 'Temperatura errada', 'Não desliga', 'Não liga'] },
  { nome: 'Cooktop', imagem: 'cooktop', frase: 'Meu cooktop', defeitos: ['Não esquenta', 'Painel não responde', 'Mostra erro', 'Desliga sozinho'] },
  { nome: 'Outro', imagem: 'character', frase: 'Meu aparelho', defeitos: ['Não liga', 'Faz barulho', 'Parou no meio do uso', 'Outro defeito'] },
];
// The form picture in its two sizes; "character" (for Outro) is Demetrius himself.
const largeImage = (name) => {
  if (name === 'character') {
    const base = 'assets/images/character/character';
    return { src: `${base}-540.webp`, srcset: `${base}-360.webp 360w, ${base}-540.webp 540w, ${base}-720.webp 720w` };
  }
  const base = `assets/images/appliances/large/${name}`;
  return { src: `${base}-800.webp`, srcset: `${base}-400.webp 400w, ${base}-800.webp 800w` };
};
const FRASES = {
  'Mostra erro': 'mostra um código de erro',
  'Sem imagem': 'tem som mas está sem imagem',
  'Linhas na tela': 'está com linhas na tela',
  'Sem som': 'está sem som',
  'Componente queimado': 'está com componente queimado',
  'Em curto': 'está em curto',
  'Não aciona comandos': 'não está acionando os comandos',
  'Temperatura errada': 'não chega na temperatura certa',
  'Prato não gira': 'liga mas o prato não gira',
  'Timer não funciona': 'está com o timer sem funcionar',
  'Outro defeito': 'está com defeito',
};

const builder = document.getElementById('builder');
if (builder) {
  const aparelhosEl = document.getElementById('aparelhos-chips');
  const defeitosEl = document.getElementById('defeitos-chips');
  const preview = document.getElementById('preview');
  const hidden = document.getElementById('text');

  const chip = (name, value, checked) => {
    const label = document.createElement('label');
    label.className = 'chip';
    label.innerHTML = `<input type="radio" name="${name}" value="${value}"${checked ? ' checked' : ''}><span>${value}</span>`;
    return label;
  };

  const message = () => {
    const data = new FormData(builder);
    const aparelho = APARELHOS.find((a) => a.nome === data.get('aparelho'));
    const defeito = data.get('defeito');
    const modelo = (data.get('modelo') || '').trim();
    const bairro = (data.get('bairro') || '').trim();
    let text = 'Olá, Demetrius! Vim pelo site.';
    if (aparelho && defeito) {
      text += ` ${aparelho.frase} ${FRASES[defeito] || defeito.toLowerCase()}.`;
    } else if (aparelho) {
      text += ` ${aparelho.frase} está com defeito.`;
    } else {
      text = OPENING;
    }
    if (modelo) text += ` Marca e modelo: ${modelo}.`;
    if (bairro) text += ` Estou no bairro ${bairro}.`;
    if (aparelho && aparelho.nome === 'TV') text += ' Você consegue buscar a TV aqui?';
    if (aparelho) text += ' Posso mandar foto ou vídeo. Qual seria o orçamento?';
    return text;
  };

  const update = () => {
    const text = message();
    preview.textContent = text;
    hidden.value = text;
  };

  // The picture beside the form follows the chosen appliance: fade out, swap, fade back in once loaded.
  const picture = document.getElementById('cta-img');
  const showImagem = (nome) => {
    const aparelho = APARELHOS.find((a) => a.nome === nome);
    const next = largeImage(aparelho.imagem);
    if (!picture || picture.getAttribute('src') === next.src) return;
    picture.classList.add('is-swapping');
    setTimeout(() => {
      picture.onload = () => picture.classList.remove('is-swapping');
      picture.srcset = next.srcset;
      picture.src = next.src;
    }, 200);
  };
  // Warm the cache the first time the visitor reaches for the form, so swaps are instant.
  // The browser picks the same size it would pick for the picture itself.
  builder.addEventListener('pointerenter', () => {
    if (!picture || !picture.offsetParent) return;
    APARELHOS.forEach((a) => {
      const img = new Image();
      img.sizes = picture.sizes;
      img.srcset = largeImage(a.imagem).srcset;
    });
  }, { once: true });

  const showDefeitos = (nome) => {
    const aparelho = APARELHOS.find((a) => a.nome === nome);
    defeitosEl.replaceChildren(...aparelho.defeitos.map((d) => chip('defeito', d, false)));
  };

  aparelhosEl.replaceChildren(...APARELHOS.map((a, i) => chip('aparelho', a.nome, i === 0)));
  showDefeitos(APARELHOS[0].nome);
  update();

  builder.addEventListener('change', (event) => {
    if (event.target.name === 'aparelho') {
      showDefeitos(event.target.value);
      showImagem(event.target.value);
    }
    update();
  });
  builder.addEventListener('input', update);
  builder.addEventListener('submit', (event) => {
    event.preventDefault();
    window.open(`${WHATSAPP}?text=${encodeURIComponent(message())}`, '_blank', 'noopener');
  });
}

// Entrances: each group rises once as it comes into view.
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const targets = document.querySelectorAll('[data-rise], .blocks, .hero');
if ('IntersectionObserver' in window && !reduce) {
  // A group can lose its own box (display: contents on tablets), so its children are watched too
  // and whichever comes into view first starts the group.
  const owner = new Map();
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        owner.get(entry.target).classList.add('is-in');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -5% 0px' });
  targets.forEach((el) => {
    [el, ...el.children].forEach((node) => {
      owner.set(node, el);
      io.observe(node);
    });
  });
} else {
  targets.forEach((el) => el.classList.add('is-in'));
}

// The about photograph changes slowly, like light in a room.
const fade = document.querySelector('[data-fade]');
if (fade && !reduce) {
  const imgs = [...fade.querySelectorAll('img')];
  let i = 0;
  let timer = null;
  const start = () => {
    timer = setInterval(() => {
      imgs[i].classList.remove('is-on');
      i = (i + 1) % imgs.length;
      imgs[i].classList.add('is-on');
    }, 5500);
  };
  start();
  document.addEventListener('visibilitychange', () => {
    clearInterval(timer);
    if (!document.hidden) start();
  });
}

// The floating WhatsApp button appears on phones once the hero has scrolled away.
const float = document.querySelector('.float');
const hero = document.querySelector('.hero');
if (float && hero && 'IntersectionObserver' in window) {
  new IntersectionObserver(([entry]) => {
    float.classList.toggle('is-on', !entry.isIntersecting);
  }).observe(hero);
}

// The back-to-top arrow shows up as soon as the visitor has scrolled a little.
const totop = document.querySelector('.totop');
if (totop) {
  const toggleTotop = () => totop.classList.toggle('is-on', window.scrollY > 300);
  window.addEventListener('scroll', toggleTotop, { passive: true });
  toggleTotop();
}

document.getElementById('ano').textContent = new Date().getFullYear();
