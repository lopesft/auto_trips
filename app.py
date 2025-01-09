from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista para armazenar as viagens em memória
viagens = []

# Rota para cadastrar uma nova viagem
@app.route('/viagens', methods=['POST'])
def cadastrar_viagem():
    dados = request.json  # Dados enviados na requisição
    # Verificar se todos os campos obrigatórios estão presentes
    if not all(k in dados for k in ("destino", "data", "preco")):
        return jsonify({"erro": "Os campos 'destino', 'data' e 'preco' são obrigatórios!"}), 400

    # Criar a nova viagem
    nova_viagem = {
        "id": len(viagens) + 1,
        "destino": dados["destino"],
        "data": dados["data"],
        "preco": dados["preco"]
    }
    viagens.append(nova_viagem)  # Adicionar à lista
    return jsonify(nova_viagem), 201  # Retornar a viagem cadastrada com status 201 (Criado)

# Rota para listar todas as viagens
@app.route('/viagens', methods=['GET'])
def listar_viagens():
    return jsonify(viagens), 200  # Retorna a lista de viagens com status 200 (OK)

# Executar a aplicação
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

    
