from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("inicio.html")

@app.route("/institucional")
def institucional():
    return render_template("institucional.html")

@app.route("/trabalhe-conosco")
def trabalhe_conosco():
    return render_template("trabalhe.html")

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/loja")
def loja():
    return render_template("loja.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    if not data or not data.get("mensagem"):
        return jsonify({"erro": "Mensagem não fornecida."}), 400

    resposta = processar_mensagem(data["mensagem"])
    return jsonify({"resposta": resposta})


@app.route("/api/proposta", methods=["POST"])
def proposta():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"erro": "Dados inválidos."}), 400

    campos_obrigatorios = ["nome", "email", "interesse"]
    for campo in campos_obrigatorios:
        if not data.get(campo, "").strip():
            return jsonify({"erro": f"Campo obrigatório: {campo}"}), 400

    resultado = enviar_email(data)
    status = 200 if resultado["sucesso"] else 500
    return jsonify(resultado), status


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "versao": "1.0.0"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
