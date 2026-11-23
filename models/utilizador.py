from con_sql_alchemy import bd

class UserModel(bd.Model):
    __tablename__ = "utilizadores"

    id = bd.Column(bd.Integer, primary_key=True, autoincrement=True)
    username = bd.Column(bd.String(40))
    email = bd.Column(bd.String(120), unique=True, nullable=False)
    password = bd.Column(bd.String(120))
    tipo = bd.Column(bd.String(20), default="utilizador")
    tarefas = bd.relationship("TarefaModel")

    def __init__(self, username, email, password, tipo="utilizador"):
        self.username = username
        self.email = email
        self.password = password
        self.tipo = tipo

    def json(self):
        return {"id": self.id, "username": self.username, "email": self.email, "tipo": self.tipo}



    @classmethod
    def find_user(cls, username):
        return cls.query.filter_by(username=username).first()



    @classmethod
    def find_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()



    def save_user(self):
        bd.session.add(self)
        bd.session.commit()
