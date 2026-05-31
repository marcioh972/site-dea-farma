import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from datetime import datetime


# ─────────────────────────────────────────────
# CONFIGURAÇÕES DE E-MAIL
# Altere para suas credenciais SMTP
# ─────────────────────────────────────────────
EMAIL_CONFIG = {
    "host": "smtp.gmail.com",
    "port": 587,
    "user": os.environ.get("EMAIL_USER", "seuemail@gmail.com"),
    "password": os.environ.get("EMAIL_PASS", "sua_senha_app"),
    "from_name": "DeA Farma — Atendimento",
}

# ─────────────────────────────────────────────
# BASE DE CONHECIMENTO DO BOT
# ─────────────────────────────────────────────
FAQ = {
    "entrega": {
        "keywords": ["entrega", "prazo", "frete", "envio", "shipping", "chegada", "tempo"],
        "resposta": (
            "🚚 <strong>Prazo de entrega:</strong><br>"
            "• <strong>Capitais:</strong> 1 a 2 dias úteis<br>"
            "• <strong>Interior:</strong> 3 a 5 dias úteis<br>"
            "• <strong>Regiões remotas:</strong> até 8 dias úteis<br><br>"
            "Trabalhamos com transportadoras parceiras certificadas pela ANVISA. "
            "O rastreamento é enviado por e-mail após a expedição."
        ),
    },
    "minimo": {
        "keywords": ["mínimo", "minimo", "pedido mínimo", "quantidade", "compra mínima", "valor mínimo"],
        "resposta": (
            "📦 <strong>Pedido mínimo:</strong><br>"
            "• Pedido mínimo: <strong>R$ 1.500,00</strong><br>"
            "• Para novos clientes, exigimos cadastro com CNPJ ativo e alvará sanitário vigente.<br><br>"
            "Quer solicitar uma proposta personalizada? Clique em <em>\"Solicitar Proposta\"</em> abaixo."
        ),
    },
    "pagamento": {
        "keywords": ["pagamento", "forma", "boleto", "pix", "cartão", "prazo pagamento", "crédito", "financiamento"],
        "resposta": (
            "💳 <strong>Formas de pagamento:</strong><br>"
            "• <strong>PIX:</strong> desconto de 2%<br>"
            "• <strong>Boleto bancário:</strong> 28 dias<br>"
            "• <strong>Cartão de crédito:</strong> até 6x sem juros<br>"
            "• <strong>Faturamento:</strong> disponível para clientes com 6+ meses de relacionamento<br><br>"
            "Condições especiais para pedidos acima de R$ 10.000."
        ),
    },
    "anvisa": {
        "keywords": ["anvisa", "registro", "autorização", "regulatório", "regularização", "licença", "sanitário"],
        "resposta": (
            "🏛️ <strong>Conformidade ANVISA:</strong><br>"
            "Todos os nossos produtos possuem registro vigente na ANVISA. "
            "Comercializamos apenas para:<br>"
            "• Farmácias e drogarias com alvará sanitário<br>"
            "• Clínicas e hospitais<br>"
            "• Distribuidoras autorizadas<br><br>"
            "Documentação técnica disponível mediante solicitação formal."
        ),
    },
    "catalogo": {
        "keywords": ["catálogo", "catalogo", "produto", "medicamento", "linha", "disponível", "estoque", "genérico", "referência"],
        "resposta": (
            "💊 <strong>Nossa linha de produtos:</strong><br>"
            "• Medicamentos genéricos e de referência<br>"
            "• Fitoterápicos e suplementos<br>"
            "• Produtos OTC (sem prescrição)<br>"
            "• Linha hospitalar e oncológica<br><br>"
            "Nosso catálogo completo com mais de <strong>8.000 SKUs</strong> é enviado junto à proposta comercial."
        ),
    },
    "cadastro": {
        "keywords": ["cadastro", "cadastrar", "cliente", "conta", "documentos", "cnpj", "abertura"],
        "resposta": (
            "📋 <strong>Cadastro de cliente:</strong><br>"
            "Documentos necessários:<br>"
            "• CNPJ ativo<br>"
            "• Alvará sanitário vigente<br>"
            "• Responsável técnico (CRF)<br>"
            "• Contrato social<br><br>"
            "Após envio da proposta, nossa equipe entra em contato em até <strong>24 horas úteis</strong>."
        ),
    },
    "temperatura": {
        "keywords": ["temperatura", "refrigerado", "cadeia do frio", "termolábil", "armazenamento", "conservação"],
        "resposta": (
            "🌡️ <strong>Cadeia do frio:</strong><br>"
            "Possuímos infraestrutura completa para produtos termolábeis:<br>"
            "• Câmaras frias com monitoramento 24/7<br>"
            "• Transporte refrigerado com datalogger<br>"
            "• Certificação de boas práticas de armazenamento (CBPAF)<br><br>"
            "Consulte disponibilidade de produtos refrigerados na proposta."
        ),
    },
}

SAUDACOES = ["olá", "ola", "oi", "bom dia", "boa tarde", "boa noite", "hey", "hello"]
AGRADECIMENTOS = ["obrigado", "obrigada", "valeu", "thanks", "grato", "grata", "agradeço"]


def processar_mensagem(texto: str) -> str:
    texto_lower = texto.lower().strip()

    # Saudação
    if any(s in texto_lower for s in SAUDACOES):
        return (
            "👋 Olá! Bem-vindo à <strong>PharmaDistrib</strong>.<br><br>"
            "Sou o assistente virtual e posso te ajudar com:<br>"
            "• Prazos de entrega e frete<br>"
            "• Pedido mínimo e catálogo<br>"
            "• Formas de pagamento<br>"
            "• Conformidade ANVISA<br>"
            "• Cadastro de novos clientes<br><br>"
            "Como posso te ajudar hoje?"
        )

    # Agradecimento
    if any(a in texto_lower for a in AGRADECIMENTOS):
        return (
            "😊 Fico feliz em ajudar! Se precisar de mais informações ou quiser "
            "receber uma proposta comercial, é só falar. Estamos à disposição!"
        )

    # Busca na base de conhecimento
    for tema, dados in FAQ.items():
        if any(kw in texto_lower for kw in dados["keywords"]):
            return dados["resposta"]

    # Fallback
    return (
        "🤔 Não encontrei uma resposta específica para sua pergunta.<br><br>"
        "Posso te ajudar com: <strong>entrega, pagamento, pedido mínimo, "
        "ANVISA, catálogo, cadastro ou cadeia do frio</strong>.<br><br>"
        "Ou, se preferir, solicite uma <strong>proposta personalizada</strong> "
        "e nossa equipe comercial entrará em contato!"
    )


def gerar_email_proposta(dados: dict) -> str:
    return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"></head>
<body style="font-family: 'Segoe UI', sans-serif; background:#f4f6f8; margin:0; padding:20px;">
  <div style="max-width:620px; margin:0 auto; background:#fff; border-radius:12px; overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.08);">
    
    <div style="background: linear-gradient(135deg, #0a3d62, #1e6fa0); padding:32px; text-align:center;">
      <h1 style="color:#fff; margin:0; font-size:22px; font-weight:700; letter-spacing:1px;">
        💊 PHARMA<span style="color:#5dade2;">DISTRIB</span>
      </h1>
      <p style="color:#a9cce3; margin:6px 0 0; font-size:13px;">Distribuição Farmacêutica com Excelência</p>
    </div>

    <div style="padding:32px;">
      <h2 style="color:#0a3d62; font-size:18px; margin:0 0 4px;">Proposta Comercial</h2>
      <p style="color:#7f8c8d; font-size:13px; margin:0 0 24px;">
        Gerada em {datetime.now().strftime('%d/%m/%Y às %H:%M')}
      </p>

      <div style="background:#eaf4fb; border-left:4px solid #1e6fa0; border-radius:0 8px 8px 0; padding:16px 20px; margin-bottom:24px;">
        <p style="margin:0 0 8px; font-size:13px; color:#555;"><strong>Cliente</strong></p>
        <p style="margin:0; font-size:16px; color:#0a3d62; font-weight:600;">{dados.get('nome', '')}</p>
        <p style="margin:4px 0 0; font-size:13px; color:#555;">
          📧 {dados.get('email', '')} &nbsp;|&nbsp; 📞 {dados.get('telefone', 'Não informado')}
        </p>
        {f'<p style="margin:4px 0 0; font-size:13px; color:#555;">🏢 CNPJ: {dados.get("cnpj", "")}</p>' if dados.get("cnpj") else ''}
      </div>

      <div style="margin-bottom:24px;">
        <p style="font-size:13px; font-weight:600; color:#555; text-transform:uppercase; letter-spacing:.5px; margin:0 0 8px;">Interesse / Mensagem</p>
        <p style="font-size:15px; color:#333; background:#f9f9f9; border-radius:8px; padding:14px; margin:0; line-height:1.6;">
          {dados.get('interesse', 'Não informado')}
        </p>
      </div>

      <div style="background:#0a3d62; border-radius:8px; padding:20px; text-align:center;">
        <p style="color:#a9cce3; font-size:12px; margin:0 0 4px;">Nossa equipe comercial responderá em até</p>
        <p style="color:#fff; font-size:22px; font-weight:700; margin:0;">24 horas úteis</p>
      </div>
    </div>

    <div style="background:#f4f6f8; padding:16px; text-align:center;">
      <p style="color:#aaa; font-size:11px; margin:0;">
        PharmaDistrib — Todos os produtos com registro ANVISA vigente<br>
        Este e-mail foi gerado automaticamente pelo sistema de atendimento.
      </p>
    </div>
  </div>
</body>
</html>
"""


def enviar_email(dados: dict) -> dict:
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[PharmaDistrib] Nova proposta — {dados.get('nome', 'Cliente')}"
        msg["From"] = f"{EMAIL_CONFIG['from_name']} <{EMAIL_CONFIG['user']}>"
        msg["To"] = dados.get("email")

        html_body = gerar_email_proposta(dados)
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        with smtplib.SMTP(EMAIL_CONFIG["host"], EMAIL_CONFIG["port"]) as server:
            server.ehlo()
            server.starttls()
            server.login(EMAIL_CONFIG["user"], EMAIL_CONFIG["password"])
            # Envia para o cliente E para o comercial interno
            destinatarios = [dados.get("email"), EMAIL_CONFIG["user"]]
            server.sendmail(EMAIL_CONFIG["user"], destinatarios, msg.as_string())

        return {"sucesso": True, "mensagem": "Proposta enviada com sucesso!"}

    except smtplib.SMTPAuthenticationError:
        return {"sucesso": False, "mensagem": "Erro de autenticação no servidor de e-mail."}
    except smtplib.SMTPException as e:
        return {"sucesso": False, "mensagem": f"Erro SMTP: {str(e)}"}
    except Exception as e:
        return {"sucesso": False, "mensagem": f"Erro inesperado: {str(e)}"}


