import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://auto_trips_db_user:FHmSPSsC7fGN1N5bGdILCYsEJrP7wz5R@dpg-cu0lc4rqf0us73b0p61g-a.oregon-postgres.render.com/auto_trips_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desabilitar o rastreamento de modificações
db = SQLAlchemy(app)

# Modelo para a tabela Viagem
class Viagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destino = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Viagem {self.destino}>"

# Criar o banco de dados (vai criar o arquivo viagens.db se não existir)
with app.app_context():
    db.create_all()  # Criação das tabelas, se ainda não existirem

# Rota para cadastrar uma nova viagem
@app.route('/viagens', methods=['POST'])
def cadastrar_viagem():
    dados = request.json  # Dados enviados na requisição

    # Verificar se todos os campos obrigatórios estão presentes
    if not all(k in dados for k in ("destino", "data", "preco", "descricao")):
        return jsonify({"erro": "Os campos 'destino', 'data', 'preco' e 'descricao' são obrigatórios!"}), 400

    # Criar a nova viagem
    nova_viagem = Viagem(
        destino=dados["destino"],
        data=dados["data"],
        preco=dados["preco"],
        descricao=dados["descricao"]
    )
    
    db.session.add(nova_viagem)  # Adicionar a viagem ao banco
    db.session.commit()  # Salvar as alterações no banco de dados

    return jsonify({
        "id": nova_viagem.id,
        "destino": nova_viagem.destino,
        "data": nova_viagem.data,
        "preco": nova_viagem.preco,
        "descricao": nova_viagem.descricao
    }), 201  # Retorna os dados da viagem cadastrada com status 201 (Criado)

# Rota para listar todas as viagens
@app.route('/viagens', methods=['GET'])
def listar_viagens():
    viagens = Viagem.query.all()  # Recuperar todas as viagens do banco
    # Retorna a lista de viagens
    return jsonify([{
        "id": v.id,
        "destino": v.destino,
        "data": v.data,
        "preco": v.preco,
        "descricao": v.descricao
    } for v in viagens]), 200  # Retorna a lista de viagens com status 200 (OK)

# Rota para deletar uma viagem pelo ID
@app.route('/viagens/<int:id>', methods=['DELETE'])
def deletar_viagem(id):
    viagem = Viagem.query.get(id)  # Buscar a viagem pelo ID
    if not viagem:
        return jsonify({"erro": "Viagem não encontrada!"}), 404

    db.session.delete(viagem)  # Deletar a viagem do banco
    db.session.commit()  # Salvar as alterações

    return jsonify({"mensagem": "Viagem deletada com sucesso!"}), 200  # Resposta de sucesso

# Executar a aplicação
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

@app.route('/')
def home():
    return "Bem-vindo à API de Viagens!"
