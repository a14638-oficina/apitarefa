from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta
from con_sql_alchemy import bd
from resources.user import userRegister, userLogin
from resources.tarefa import Tarefas, Tarefa
from models.user import UserModel

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tarefas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "my_secret_long_key_very_secret_aaaaaaa_bbbbb"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=10)

@jwt.token_in_blocklist_loader
def verify_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST



@jwt.revoked_token_loader
def token_invalid(jwt_header, jwt_payload):
    return {"mensagem": "Logout efetuado! Faça login para aceder novamente"}, 401



api.add_resource(userRegister, "/registo")
api.add_resource(userLogin, "/login")
api.add_resource(Tarefas, "/tarefas")
api.add_resource(Tarefa, "/tarefas/<int:tarefa_id>")

if __name__ == "__main__":
    bd.init_app(app)
    with app.app_context():
        bd.create_all()
        # Cria o administrador inicial, se ainda não existir.
        if UserModel.find_user_by_email("admin@tarefas.local") is None:
            admin = UserModel("admin", "admin@tarefas.local", "admin123", "admin")
            admin.save_user()
    app.run(debug=True)
