from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError
from prontuariodigital.models import Paciente

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=4, max=20)])
    lembrar_dados = BooleanField('Lembrar dados de Acesso')
    botao_submit_login = SubmitField('Entrar')


class FormCadastroPaciente(FlaskForm):
    nome_completo = StringField('Nome do Paciente', validators=[DataRequired()])
    data_nascimento = DateField('Data de Nascimento', format='%Y-%m-%d', validators=[DataRequired()])
    genero = SelectField('Gênero', choices=[('', 'Gênero'), ('Masculino', 'Masculino'), ('Feminino', 'Feminino'), ('Outros', 'Outros')], validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired(), Regexp(r'^\d{11}$', message="Telefone inválido"), Length(min=11, max=11)])
    email = StringField('E-mail', validators=[DataRequired()])
    endereco = StringField('Endereço', validators=[DataRequired()])
    cpf = StringField('CPF',validators=[DataRequired(), Regexp(r'^\d{11}$', message="CPF inválido"), Length(min=11, max=11)])
    rg = StringField('RG',validators=[DataRequired(), Regexp(r'^\d{9}$', message="rg inválido"), Length(min=9, max=9)])

    avaliacao_medica = FileField('Avaliação Cardiológica')
    evolucao_clinica = FileField('Evolução Diária')
    exames = FileField('Exames')
    documentos_pessoais = FileField('Pendências')

    botao_cadastrar_paciente = SubmitField('Cadastrar Paciente')

    def validate_cpf(self, cpf):
        paciente = Paciente.query.filter_by(cpf=cpf.data).first()
        if paciente:
            raise ValidationError('CPF já cadastrado!')
    
    def validate_rg(self, rg):
        paciente = Paciente.query.filter_by(rg=rg.data).first()
        if paciente:
            raise ValidationError('RG já cadastrado!')
        
    def validate_telefone(self, telefone):
        paciente = Paciente.query.filter_by(telefone=telefone.data).first()
        if paciente:
            raise ValidationError('Telefone já cadastrado!')
        
    def validate_email(self, email):
        paciente = Paciente.query.filter_by(email=email.data).first()
        if paciente:
            raise ValidationError('E-mail já cadastrado!')


class FormEdicaoPaciente(FlaskForm):
    id = HiddenField()
    nome_completo = StringField('Nome do Paciente', validators=[DataRequired()])
    data_nascimento = DateField('Data de Nascimento', format='%Y-%m-%d', validators=[DataRequired()])
    genero = SelectField('Gênero', choices=[('', 'Gênero'), ('Masculino', 'Masculino'), ('Feminino', 'Feminino'), ('Outros', 'Outros')], validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired(), Regexp(r'^\d{11}$', message="Telefone inválido"), Length(min=11, max=11)])
    email = StringField('E-mail', validators=[DataRequired()])
    endereco = StringField('Endereço', validators=[DataRequired()])
    cpf = StringField('CPF',validators=[DataRequired(), Regexp(r'^\d{11}$', message="CPF inválido"), Length(min=11, max=11)])
    rg = StringField('RG',validators=[DataRequired(), Regexp(r'^\d{9}$', message="rg inválido"), Length(min=9, max=9)])

    avaliacao_medica = FileField('Avaliação Cardiológica')
    evolucao_clinica = FileField('Evolução Diária')
    exames = FileField('Exames')
    documentos_pessoais = FileField('Pendências')

    botao_editar_paciente = SubmitField('Salvar Edições')


    def validate_cpf(self, cpf):
        paciente_existente = Paciente.query.filter_by(cpf=cpf.data).first()
        if paciente_existente and paciente_existente.id != int(self.id.data):
            raise ValidationError('Este cpf já está em uso por outro paciente.')
        
    def validate_rg(self, rg):
        paciente_existente = Paciente.query.filter_by(rg=rg.data).first()
        if paciente_existente and paciente_existente.id != int(self.id.data):
            raise ValidationError('Este rg já está em uso por outro paciente.')
        
    def validate_telefone(self, telefone):
        paciente_existente = Paciente.query.filter_by(telefone=telefone.data).first()
        if paciente_existente and paciente_existente.id != int(self.id.data):
            raise ValidationError('Este telefone já está em uso por outro paciente.')
        
    def validate_email(self, email):
        paciente_existente = Paciente.query.filter_by(email=email.data).first()
        if paciente_existente and paciente_existente.id != int(self.id.data):
            raise ValidationError('Este email já está em uso por outro paciente.')

