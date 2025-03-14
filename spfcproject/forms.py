from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, Optional, ValidationError
from spfcproject.models import Usuario, Atleta
from datetime import datetime


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=4, max=20)])
    lembrar_dados = BooleanField('Lembrar dados de Acesso')
    botao_submit_login = SubmitField('Login')


class FormCadastroAtleta(FlaskForm):
    nome_completo = StringField('Nome do Atleta', validators=[DataRequired()])
    data_nascimento = DateField('Data de Nascimento', format='%Y-%m-%d', validators=[DataRequired()])
    cpf = StringField('CPF',validators=[DataRequired(), Regexp(r'^\d{11}$', message="CPF inválido"), Length(min=11, max=11)])
    categoria = SelectField('Categoria', choices=[('', 'SELECIONAR CATEGORIA'),('SUB-09', 'SUB-09'), ('SUB-10', 'SUB-10'), ('SUB-11', 'SUB-11'), ('SUB-12', 'SUB-12'), ('SUB-13','SUB-13'), ('SUB-14','SUB-14'), ('SUB-15','SUB-15'), ('SUB-16','SUB-16'), ('SUB-17','SUB-17'), ('SUB-20','SUB-20')], validators=[DataRequired()])

    avaliacao_cardiologica = FileField('Avaliação Cardiológica')
    evolucao_diaria = FileField('Evolução Diária')
    exames = FileField('Exames')
    pendencias = FileField('Pendências')

    botao_cadastrar_atleta = SubmitField('Cadastrar Atleta')

    def validate_cpf(self, cpf):
        atleta = Atleta.query.filter_by(cpf=cpf.data).first()
        if atleta:
            raise ValidationError('CPF já cadastrado!')


class FormEdicaoAtleta(FlaskForm):
    id = HiddenField()
    nome_completo = StringField('Nome do Atleta', validators=[DataRequired()])
    data_nascimento = DateField('Data de Nascimento', format='%Y-%m-%d', validators=[DataRequired()])
    cpf = StringField('CPF',validators=[DataRequired(), Regexp(r'^\d{11}$', message="CPF inválido"), Length(min=11, max=11)])
    categoria = SelectField('Sexo', choices=[('', 'SELECIONAR CATEGORIA'),('SUB-09', 'SUB-09'), ('SUB-10', 'SUB-10'), ('SUB-11', 'SUB-11'), ('SUB-12', 'SUB-12'), ('SUB-13','SUB-13'), ('SUB-14','SUB-14'), ('SUB-15','SUB-15'), ('SUB-16','SUB-16'), ('SUB-17','SUB-17'), ('SUB-20','SUB-20')], validators=[DataRequired()])

    avaliacao_cardiologica = FileField('Avaliação Cardiologica')
    evolucao_diaria = FileField('Evolução Diária')
    exames = FileField('Exames')
    pendencias = FileField('Pendencias')

    botao_editar_atleta = SubmitField('Salvar Edições')


    def validate_cpf(self, cpf):
        atleta_existente = Atleta.query.filter_by(cpf=cpf.data).first()
        if atleta_existente and atleta_existente.id != int(self.id.data):
            raise ValidationError('Este cpf já está em uso por outro atleta.')

