import os                                              # para ler a password do adminfrom flask import Flask

from flask_restful import Api
from con_sql_alchemy import bd
from flask_jwt_extended import JWTManager
from datetime import timedelta
from blocklist import BLOCKLIST
from models.user import Utilizador                     # necessário para criar o admin
from models.tarefa import Tarefa                       # SEM este import o create_all() não cria a tabela tarefas
from resources.auth import Registo, Login, Logout     # resources/user.py renomeado para auth.py
from resources.tarefa import Tarefas, TarefaId

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app) #Inicializa o JWT para tratar da autenticação das páginas

#Configurações
#SQLITE não se utiliza em base de dados
#Foi utilizada agora por ser apenas um teste
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tarefas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "my_secret_long_key_very_secret_aaaaaaa_bbbbb"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=10)

@jwt.token_in_blocklist_loader

def verify_blocklist(jwt_header,jwt_payload):
    jti = jwt_payload["jti"]
    return jti in BLOCKLIST

@jwt.revoked_token_loader

def token_invalid(jwt_header,jwt_payload):
    return {"mensagem": "Logout efetuado! Faça login para aceder novamente"}, 401

api.add_resource(Register,"/registar")
api.add_resource(Login,"/login")
api.add_resource(Logout, "/logout")
api.add_resource(Tarefas, "/tarefas")                  # POST criar | GET listar
api.add_resource(TarefaId, "/tarefas/<int:id>")        # GET | PUT | DELETE



if __name__ == "__main__":
    bd.init_app(app)

    with app.app_context():
        bd.create_all()  # Cria todas as tabelas dos modelos SQLAlchemy

        if not Utilizador.query.filter_by(
            email="admin@oficina.pt"
        ).first():
            admin = Utilizador(
                username="admin",
                email="admin@oficina.pt",
                password=os.environ.get("ADMIN_PASSWORD", "admin123"),
                tipo="admin",
            )

            admin.save_user()

    app.run(debug=True)