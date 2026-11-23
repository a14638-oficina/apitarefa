from con_sql_alchemy import bd

class TarefaModel(bd.Model):
    __tablename__ = "tarefas"

    id = bd.Column(bd.Integer, primary_key=True, autoincrement=True)
    titulo = bd.Column(bd.String(120),)
    descricao = bd.Column(bd.Text, default="")
    estado = bd.Column(bd.String(20), default="Pendente")
    utilizador_id = bd.Column(bd.Integer, bd.ForeignKey("utilizadores.id"))
    utilizador = bd.relationship("UserModel")

    def __init__(self, titulo, descricao, estado, utilizador_id):
        self.titulo = titulo
        self.descricao = descricao
        self.estado = estado
        self.utilizador_id = utilizador_id

    def json(self):
        return {"id": self.id, "titulo": self.titulo, "descricao": self.descricao,
                "estado": self.estado, "utilizador_id": self.utilizador_id}



    @classmethod
    def find_tarefa(cls, tarefa_id):
        return cls.query.filter_by(id=tarefa_id).first()



    def save_tarefa(self):
        bd.session.add(self)
        bd.session.commit()

    def update_tarefa(self, titulo, descricao, estado):
        self.titulo = titulo
        self.descricao = descricao
        self.estado = estado
        bd.session.commit()

    def delete_tarefa(self):
        bd.session.delete(self)
        bd.session.commit()
