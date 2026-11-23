from flask_restful import Resource, reqparse
from hmac import compare_digest
from flask_jwt_extended import create_access_token
from models.user import UserModel

class userRegister(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("username", type=str, required=True, help="O username é obrigatório")
    argumentos.add_argument("email", type=str, required=True, help="O email é obrigatório")
    argumentos.add_argument("password", type=str, required=True, help="A password é obrigatória")

    def post(self):
        dados = userRegister.argumentos.parse_args()
        if UserModel.find_user_by_email(dados["email"]):
            return {"mensagem": "Email já registado"}, 400
        novo_user = UserModel(dados["username"], dados["email"], dados["password"], "utilizador")
        try:
            novo_user.save_user()
            return {"mensagem": "Utilizador registado com sucesso"}, 201
        except:
            return {"mensagem": "Ocorreu um erro interno"}, 500



class userLogin(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("email", type=str, required=True, help="O email é obrigatório")
    argumentos.add_argument("password", type=str, required=True, help="A password é obrigatória")

    def post(self):
        dados = userLogin.argumentos.parse_args()
        utilizador = UserModel.find_user_by_email(dados["email"])
        if utilizador and compare_digest(utilizador.password, dados["password"]):
            token = create_access_token(identity=utilizador.username,
                                      additional_claims={"tipo": utilizador.tipo})
            return {"access_token": token, "tipo": utilizador.tipo}, 200
        return {"mensagem": "Email ou password incorretos"}, 401
