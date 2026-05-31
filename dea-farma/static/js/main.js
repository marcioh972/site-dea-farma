/* ─────────────────────────────────────────────
   Navbar scroll + hamburger + chat flutuante + modal proposta
───────────────────────────────────────────── */

// ── Navbar scroll shadow ──────────────────────
/*const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 10);
});*/

// Navbar transparente no topo, cor original ao rolar
const navbar = document.getElementById('mainNavbar');

// Função que verifica a posição do scroll da tela
function handleScroll() {
  // Se rolou mais do que 50px do topo da página
  if (window.scrollY > 50) {
    navbar.classList.add('scrolled'); // Ativa o fundo escuro/borrado
  } else {
    navbar.classList.remove('scrolled'); // Volta a ficar transparente
  }
}

// Ouvinte de evento: monitora sempre que o usuário rolar a tela
window.addEventListener('scroll', handleScroll);

// ── Hamburger ─────────────────────────────────
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');

if (hamburger) {
  hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('open');
  });
}

// Fecha menu ao clicar em link
navLinks?.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', () => navLinks.classList.remove('open'));
});

// ── Chat flutuante ────────────────────────────
const chatFab = document.getElementById('chatFab');
const chatWidget = document.getElementById('chatWidget');
const cwClose = document.getElementById('cwClose');
const fabBadge = document.getElementById('fabBadge');
const fabIconOpen = chatFab?.querySelector('.fab-icon-open');
const fabIconClose = chatFab?.querySelector('.fab-icon-close');

if (chatFab) {
  chatFab.addEventListener('click', () => {
    const isOpen = chatWidget.classList.toggle('open');
    fabIconOpen.classList.toggle('hidden', isOpen);
    fabIconClose.classList.toggle('hidden', !isOpen);
    if (isOpen && fabBadge) fabBadge.style.display = 'none';
    if (isOpen) document.getElementById('cwInput')?.focus();
  });
}

if (cwClose) {
  cwClose.addEventListener('click', () => {
    chatWidget.classList.remove('open');
    fabIconOpen?.classList.remove('hidden');
    fabIconClose?.classList.add('hidden');
  });
}

// ── Chat — enviar mensagem ─────────────────────
const cwInput = document.getElementById('cwInput');
const cwSend = document.getElementById('cwSend');
const cwMsgs = document.getElementById('cwMessages');

function cwAppend(html, role = 'bot') {
  const div = document.createElement('div');
  div.className = `cw-msg ${role}`;
  div.innerHTML = `<div class="cw-bubble">${html}</div>`;
  cwMsgs.appendChild(div);
  cwMsgs.scrollTop = cwMsgs.scrollHeight;
}

function cwShowTyping() {
  const div = document.createElement('div');
  div.className = 'cw-msg bot cw-typing';
  div.id = 'cwTyping';
  div.innerHTML = `<div class="cw-bubble">
    <span class="cw-typing-dot"></span>
    <span class="cw-typing-dot"></span>
    <span class="cw-typing-dot"></span>
  </div>`;
  cwMsgs.appendChild(div);
  cwMsgs.scrollTop = cwMsgs.scrollHeight;
}

function cwHideTyping() {
  document.getElementById('cwTyping')?.remove();
}

async function cwSendMsg(texto) {
  const msg = (texto || cwInput?.value || '').trim();
  if (!msg) return;
  if (cwInput) cwInput.value = '';

  cwAppend(msg, 'user');
  cwShowTyping();

  // Esconde atalhos rápidos após primeiro uso
  const topicsEl = document.getElementById('cwTopics');
  if (topicsEl) topicsEl.style.display = 'none';

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mensagem: msg }),
    });
    const data = await res.json();
    cwHideTyping();
    cwAppend(res.ok ? data.resposta : '⚠️ Erro ao processar. Tente novamente.', 'bot');
  } catch {
    cwHideTyping();
    cwAppend('⚠️ Sem conexão com o servidor Flask.', 'bot');
  }
}

cwSend?.addEventListener('click', () => cwSendMsg());
cwInput?.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); cwSendMsg(); }
});

// Atalhos de tópico rápido
document.querySelectorAll('.cw-topic').forEach(btn => {
  btn.addEventListener('click', () => cwSendMsg(btn.dataset.msg));
});

// ── Modal proposta ─────────────────────────────
const modalOverlay = document.getElementById('modalOverlay');
const closeModal = document.getElementById('closeModal');
const cwOpenProposal = document.getElementById('cwOpenProposal');
const submitBtn = document.getElementById('submitBtn');
const submitLabel = document.getElementById('submitLabel');
const submitSpinner = document.getElementById('submitSpinner');
const formFeedback = document.getElementById('formFeedback');

function openModal() { modalOverlay?.classList.add('active'); }
function closeModalFn() {
  modalOverlay?.classList.remove('active');
  if (formFeedback) { formFeedback.className = 'form-feedback'; formFeedback.textContent = ''; }
}

cwOpenProposal?.addEventListener('click', openModal);
closeModal?.addEventListener('click', closeModalFn);
modalOverlay?.addEventListener('click', e => { if (e.target === modalOverlay) closeModalFn(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModalFn(); });

// Botão "Solicitar Proposta" do header (se existir na página)
document.getElementById('openProposal')?.addEventListener('click', openModal);

submitBtn?.addEventListener('click', async () => {
  formFeedback.className = 'form-feedback';

  const dados = {
    nome: document.getElementById('f_nome')?.value.trim(),
    email: document.getElementById('f_email')?.value.trim(),
    telefone: document.getElementById('f_telefone')?.value.trim(),
    cnpj: document.getElementById('f_cnpj')?.value.trim(),
    segmento: document.getElementById('f_segmento')?.value,
    interesse: document.getElementById('f_interesse')?.value.trim(),
  };

  if (!dados.nome) return showFb('Informe seu nome.');
  if (!dados.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(dados.email)) return showFb('E-mail inválido.');
  if (!dados.interesse) return showFb('Descreva seu interesse.');

  submitBtn.disabled = true;
  submitLabel.textContent = 'Enviando...';
  submitSpinner?.classList.remove('hidden');

  try {
    const res = await fetch('/api/proposta', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dados),
    });
    const data = await res.json();

    if (res.ok && data.sucesso) {
      showFb(`✅ Proposta enviada para ${dados.email}!`, 'success');
      // Mensagem no chat (se widget estiver visível)
      if (cwMsgs) cwAppend(`📩 Proposta enviada! Nossa equipe retorna em até 24h úteis.`, 'bot');
      setTimeout(() => {
        closeModalFn();
        resetSubmitBtn();
        ['f_nome', 'f_email', 'f_telefone', 'f_cnpj', 'f_interesse'].forEach(id => {
          const el = document.getElementById(id);
          if (el) el.value = '';
        });
        const seg = document.getElementById('f_segmento');
        if (seg) seg.value = '';
      }, 2500);
    } else {
      showFb(data.mensagem || 'Erro ao enviar proposta.');
      resetSubmitBtn();
    }
  } catch {
    showFb('Sem conexão com o servidor.');
    resetSubmitBtn();
  }
});

function showFb(msg, tipo = 'error') {
  if (!formFeedback) return;
  formFeedback.textContent = msg;
  formFeedback.className = `form-feedback ${tipo}`;
}

function resetSubmitBtn() {
  if (!submitBtn) return;
  submitBtn.disabled = false;
  if (submitLabel) submitLabel.textContent = 'Enviar proposta por e-mail';
  submitSpinner?.classList.add('hidden');
}
