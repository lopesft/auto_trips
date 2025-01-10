from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista para armazenar as viagens em memória
viagens = []

# Rota para cadastrar uma nova viagem
@app.route('/viagens', methods=['POST'])
def cadastrar_viagem():
    dados = request.json  # Dados enviados na requisição
    # Verificar se todos os campos obrigatórios estão presentes
    if not all(k in dados for k in ("destino", "data", "preco", "descricao")):
        return jsonify({"erro": "Os campos 'destino', 'data', 'preco' e 'descricao' são obrigatórios!"}), 400

    # Criar a nova viagem
    nova_viagem = {
        "id": len(viagens) + 1,
        "destino": dados["destino"],
        "data": dados["data"],
        "preco": dados["preco"],
        "descricao": dados["descricao"],
    }
    viagens.append(nova_viagem)  # Adicionar à lista
    return jsonify(nova_viagem), 201  # Retornar a viagem cadastrada com status 201 (Criado)

# Rota para listar todas as viagens
@app.route('/viagens', methods=['GET'])
def listar_viagens():
    return jsonify(viagens), 200  # Retorna a lista de viagens com status 200 (OK)

# Rota para excluir uma viagem por ID
@app.route('/viagens/<int:viagem_id>', methods=['DELETE'])
def excluir_viagem(viagem_id):
    global viagens
    # Procurar a viagem pelo ID
    viagem = next((v for v in viagens if v["id"] == viagem_id), None)
    if viagem is None:
        return jsonify({"erro": "Viagem não encontrada!"}), 404
    
    viagens = [v for v in viagens if v["id"] != viagem_id]  # Remover a viagem da lista
    return jsonify({"mensagem": "Viagem excluída com sucesso!"}), 200

# Executar a aplicação
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
