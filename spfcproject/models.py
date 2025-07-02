from email.policy import default
from spfcproject import database, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)


class Paciente(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome_completo = database.Column(database.String, nullable=False)
    data_nascimento =database.Column(database.String, nullable=False)
    genero = database.Column(database.String, nullable=False)
    telefone = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    endereco =database.Column(database.String, nullable=False)
    cpf = database.Column(database.String, nullable=False, unique=True)
    rg = database.Column(database.String, nullable=False, unique=True)

    avaliacao_medica = database.Column(database.String, nullable=True)
    evolucao_clinica = database.Column(database.String, nullable=True)
    exames = database.Column(database.String, nullable=True)
    documentos_pessoais = database.Column(database.String, nullable=True)