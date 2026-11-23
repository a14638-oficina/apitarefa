from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.user import UserModel
from models.tarefa import TarefaModel


class Tarefas(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("titulo", type=str, required=True, help="O título é obrigatório")
    argumentos.add_argument("descricao", type=str, required=False, default="")
    argumentos.add_argument("estado", type=str, required=False, default="Pendente")

    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        tipo = get_jwt().get("tipo")
        if tipo == "admin":
            lista = TarefaModel.query.all()
        else:
            utilizador = UserModel.find_user(username)
            lista = TarefaModel.query.filter_by(utilizador_id=utilizador.id).all()
        return {"tarefas": [tarefa.json() for tarefa in lista]}, 200



    @jwt_required()
    def post(self):
        dados = Tarefas.argumentos.parse_args()
        if dados["estado"] not in ["Pendente", "Em curso", "Concluída"]:
            return {"mensagem": "Estado inválido"}, 400
        utilizador = UserModel.find_user(get_jwt_identity())
        if utilizador is None:
            return {"mensagem": "Utilizador não encontrado"}, 404
        nova_tarefa = TarefaModel(dados["titulo"], dados["descricao"], dados["estado"], utilizador.id)
        try:
            nova_tarefa.save_tarefa()
            return nova_tarefa.json(), 201
        except:
            return {"mensagem": "Ocorreu um erro interno"}, 500



class Tarefa(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("titulo", type=str, required=True, help="O título é obrigatório")
    argumentos.add_argument("descricao", type=str, required=False, default="")
    argumentos.add_argument("estado", type=str, required=True, help="O estado é obrigatório")



    def _tarefa_permitida(self, tarefa):
        if get_jwt().get("tipo") == "admin":
            return True
        utilizador = UserModel.find_user(get_jwt_identity())
        return utilizador is not None and tarefa.utilizador_id == utilizador.id



    @jwt_required()
    def get(self, tarefa_id):
        tarefa = TarefaModel.find_tarefa(tarefa_id)
        if tarefa is None:
            return {"mensagem": "Tarefa não encontrada"}, 404
        if not self._tarefa_permitida(tarefa):
            return {"mensagem": "Sem permissões"}, 403
        return tarefa.json(), 200



    @jwt_required()
    def put(self, tarefa_id):
        tarefa = TarefaModel.find_tarefa(tarefa_id)
        if tarefa is None:
            return {"mensagem": "Tarefa não encontrada"}, 404
        if not self._tarefa_permitida(tarefa):
            return {"mensagem": "Sem permissões"}, 403
        dados = Tarefa.argumentos.parse_args()
        if dados["estado"] not in ["Pendente", "Em curso", "Concluída"]:
            return {"mensagem": "Estado inválido"}, 400
        try:
            tarefa.update_tarefa(dados["titulo"], dados["descricao"], dados["estado"])
            return tarefa.json(), 200
        except:
            return {"mensagem": "Ocorreu um erro interno"}, 500



    @jwt_required()
    def delete(self, tarefa_id):
        tarefa = TarefaModel.find_tarefa(tarefa_id)
        if tarefa is None:
            return {"mensagem": "Tarefa não encontrada"}, 404
        if not self._tarefa_permitida(tarefa):
            return {"mensagem": "Sem permissões"}, 403
        try:
            dados = tarefa.json()
            tarefa.delete_tarefa()
            return {"mensagem": "Tarefa eliminada", "tarefa": dados}, 200
        except:
            return {"mensagem": "Ocorreu um erro interno"}, 500
