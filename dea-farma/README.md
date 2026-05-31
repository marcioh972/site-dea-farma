# 💊 DeA Farma — Assistente de Atendimento

Bot de atendimento + envio de propostas por e-mail para distribuidora de medicamentos.

## Estrutura do projeto

```
dea-farma/
├── app.py                  ← Backend Flask (rotas, bot, e-mail)
├── requirements.txt
├── templates/
│   └── index.html          ← Interface principal
└── static/
    ├── css/style.css
    └── js/app.js
```

## Como rodar

### 1. Instale as dependências
```bash
pip install -r requirements.txt
```

### 2. Configure as variáveis de e-mail

**Opção A — Variáveis de ambiente (recomendado):**
```bash
export EMAIL_USER="seuemail@gmail.com"
export EMAIL_PASS="sua_senha_de_app_gmail"
```

**Opção B — Direto no `app.py`** (linha ~18):
```python
"user": "seuemail@gmail.com",
"password": "sua_senha_app",
```

> ⚠️ Para Gmail, use uma **Senha de App** (não a senha normal).
> Acesse: Google Account → Segurança → Verificação em 2 etapas → Senhas de app

### 3. Execute
```bash
python app.py
```

Acesse: **http://localhost:5000**

---

## Funcionalidades

### Bot de atendimento
Responde automaticamente dúvidas sobre:
- Prazo de entrega
- Pedido mínimo
- Formas de pagamento
- Conformidade ANVISA
- Catálogo de produtos
- Cadastro de clientes
- Cadeia do frio

Para adicionar novos tópicos, edite o dicionário `FAQ` em `app.py`.

### Envio de proposta
- Formulário com nome, e-mail, telefone, CNPJ, segmento e interesse
- E-mail HTML estilizado enviado para o cliente E para o comercial interno
- Feedback visual de sucesso/erro

---

## Rotas da API

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Interface web |
| POST | `/api/chat` | Responde mensagem do bot |
| POST | `/api/proposta` | Envia proposta por e-mail |
| GET | `/api/health` | Status da aplicação |

### Exemplo de uso da API

**Chat:**
```json
POST /api/chat
{ "mensagem": "Qual o prazo de entrega?" }
```

**Proposta:**
```json
POST /api/proposta
{
  "nome": "Farmácia Central",
  "email": "compras@farmacia.com.br",
  "telefone": "(11) 99999-9999",
  "cnpj": "00.000.000/0001-00",
  "segmento": "Farmácia / Drogaria",
  "interesse": "Genéricos linha cardiovascular"
}
```
