import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://auto_trips_db_user:FHmSPSsC7fGN1N5bGdILCYsEJrP7wz5R@dpg-cu0lc4rqf0us73b0p61g-a.oregon-postgres.render.com/auto_trips_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para a tabela Viagem
class Viagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destino = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)  # Categoria da viagem
    agencia = db.Column(db.String(100), nullable=False)   # Nome da agência

    def __repr__(self):
        return f"<Viagem {self.destino}>"

# Criar o banco de dados
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Bem-vindo à API de Viagens!"

# Rota para cadastrar uma nova viagem
@app.route('/viagens', methods=['POST'])
def cadastrar_viagem():
    dados = request.json

    # Verificar se todos os campos obrigatórios estão presentes
    campos_obrigatorios = {"destino", "data", "preco", "descricao", "categoria", "agencia"}
    if not campos_obrigatorios.issubset(dados):
        return jsonify({"erro": f"Os campos {', '.join(campos_obrigatorios)} são obrigatórios!"}), 400

    # Criar a nova viagem
    nova_viagem = Viagem(
        destino=dados["destino"],
        data=dados["data"],
        preco=dados["preco"],
        descricao=dados["descricao"],
        categoria=dados["categoria"],
        agencia=dados["agencia"]
    )
    db.session.add(nova_viagem)
    db.session.commit()

    return jsonify({
        "id": nova_viagem.id,
        "destino": nova_viagem.destino,
        "data": nova_viagem.data,
        "preco": nova_viagem.preco,
        "descricao": nova_viagem.descricao,
        "categoria": nova_viagem.categoria,
        "agencia": nova_viagem.agencia
    }), 201

@app.route('/viagens', methods=['GET'])
def listar_viagens():
    categoria = request.args.get('categoria')
    index = request.args.get('index', type=int)  # Novo parâmetro opcional para índice específico
    
    if categoria:
        viagens = Viagem.query.filter_by(categoria=categoria).all()
    else:
        viagens = Viagem.query.all()

    if not viagens:
        return jsonify({"erro": "Nenhuma viagem encontrada!"}), 404

    if index is not None:  # Se um índice for fornecido
        if 0 <= index < len(viagens):  # Valida o índice
            viagem = viagens[index]
            return jsonify({
                "agencia": viagem.agencia,
                "categoria": viagem.categoria,
                "data": viagem.data,
                "descricao": viagem.descricao,
                "destino": viagem.destino,
                "id": viagem.id,
                "preco": viagem.preco
            }), 200
        else:
            return jsonify({"erro": "Índice fora do intervalo!"}), 400

    # Caso contrário, retorna todas as viagens
    trips = [{"agencia": v.agencia, "categoria": v.categoria, "data": v.data, 
              "descricao": v.descricao, "destino": v.destino, "id": v.id, 
              "preco": v.preco} for v in viagens]

    return jsonify({"quantidade_trips": len(trips), "trips": trips}), 200


# Rota para deletar uma viagem pelo ID
@app.route('/viagens/<int:id>', methods=['DELETE'])
def deletar_viagem(id):
    viagem = Viagem.query.get(id)
    if not viagem:
        return jsonify({"erro": "Viagem não encontrada!"}), 404

    db.session.delete(viagem)
    db.session.commit()

    return jsonify({"mensagem": "Viagem deletada com sucesso!"}), 200

# Executar a aplicação
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
