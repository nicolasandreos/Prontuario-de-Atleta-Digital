from dns.e164 import query
from prontuariodigital import app, database
from flask import render_template, flash, redirect, url_for, request, jsonify
from prontuariodigital.forms import FormCadastroPaciente, FormLogin, FormEdicaoPaciente
from prontuariodigital.models import Usuario, Paciente
from flask_login import login_user, logout_user, current_user, login_required
import os
from datetime import datetime


def salvar_arquivo(arquivo, pasta_paciente, subpasta):
    caminho_completo = os.path.join(f'{pasta_paciente}/{subpasta}', arquivo.filename)
    arquivo.save(caminho_completo)
    return arquivo.filename


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form_cadastro_paciente = FormCadastroPaciente()
    if form_cadastro_paciente.validate_on_submit():
        paciente = Paciente(nome_completo=form_cadastro_paciente.nome_completo.data.title(), data_nascimento=form_cadastro_paciente.data_nascimento.data, genero=form_cadastro_paciente.genero.data, telefone=form_cadastro_paciente.telefone.data, email=form_cadastro_paciente.email.data, endereco=form_cadastro_paciente.endereco.data, cpf=form_cadastro_paciente.cpf.data, rg=form_cadastro_paciente.rg.data)
        database.session.add(paciente)
        database.session.commit()
        nome_paciente = "_".join(paciente.nome_completo.split())
        caminho_pasta_paciente = os.path.join(app.root_path, f'static/pacientes', nome_paciente)
        os.makedirs(caminho_pasta_paciente, exist_ok=True)
        exames = ['Av. Medica', 'Ev. Clinica', 'Exames', 'Documentos Pessoais']
        
        for exame in exames:
            caminho_pasta_exames = os.path.join(app.root_path, f'static/pacientes/{nome_paciente}', f'{exame}')
            os.makedirs(caminho_pasta_exames, exist_ok=True)

        if form_cadastro_paciente.avaliacao_medica.data:
            nome_arquivo_atualizado = salvar_arquivo(form_cadastro_paciente.avaliacao_medica.data, caminho_pasta_paciente, 'Av. Medica')
            paciente.avaliacao_medica = nome_arquivo_atualizado

        if form_cadastro_paciente.evolucao_clinica.data:
            nome_arquivo_atualizado = salvar_arquivo(form_cadastro_paciente.evolucao_clinica.data, caminho_pasta_paciente, 'Ev. Clinica')
            paciente.evolucao_clinica = nome_arquivo_atualizado

        if form_cadastro_paciente.exames.data:
            nome_arquivo_atualizado = salvar_arquivo(form_cadastro_paciente.exames.data, caminho_pasta_paciente, 'Exames')
            paciente.exames = nome_arquivo_atualizado

        if form_cadastro_paciente.documentos_pessoais.data:
            nome_arquivo_atualizado = salvar_arquivo(form_cadastro_paciente.documentos_pessoais.data, caminho_pasta_paciente, 'Documentos Pessoais')
            paciente.documentos_pessoais = nome_arquivo_atualizado

        database.session.commit()
        flash(f'{form_cadastro_paciente.nome_completo.data.title()} cadastrado com sucesso!', 'alert-success')
        return redirect(url_for('home'))
    return render_template('home.html', form_cadastro_paciente=form_cadastro_paciente)


@app.route('/exibir-pacientes')
@login_required
def exibir_pacientes():
    nome_paciente_busca = request.args.get('busca', '').strip()
    pacientes = Paciente.query.all()
    pacientes_filtrados = None
    if nome_paciente_busca:
        pacientes_filtrados = Paciente.query.filter(Paciente.nome_completo.ilike(f"%{nome_paciente_busca}%")).all()

    return render_template('exibir-pacientes.html', pacientes = pacientes, pacientes_filtrados= pacientes_filtrados)



@app.route('/login',  methods= ['GET', 'POST'])
def login():
    form_loginspfc = FormLogin()
    if form_loginspfc.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_loginspfc.email.data).first()
        if usuario and usuario.senha == form_loginspfc.senha.data:
            login_user(usuario, remember=form_loginspfc.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail {form_loginspfc.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('E-mail ou senha Inválidos!', 'alert-danger')
    return render_template('login.html', form_loginspfc=form_loginspfc)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso', 'alert-success')
    return redirect(url_for('login'))


@app.route('/editarpaciente-<id>', methods=['GET', 'POST'])
def edicao_paciente(id):
    form_edicao_paciente = FormEdicaoPaciente()
    paciente = Paciente.query.get(id)
    form_edicao_paciente.id.data = int(paciente.id)

    if request.method == 'GET':
        form_edicao_paciente.nome_completo.data = paciente.nome_completo
        form_edicao_paciente.data_nascimento.data = datetime.strptime(paciente.data_nascimento, "%Y-%m-%d")
        form_edicao_paciente.genero.data = paciente.genero
        form_edicao_paciente.telefone.data = paciente.telefone
        form_edicao_paciente.email.data = paciente.email
        form_edicao_paciente.endereco.data = paciente.endereco
        form_edicao_paciente.cpf.data = paciente.cpf
        form_edicao_paciente.rg.data = paciente.rg

    if form_edicao_paciente.validate_on_submit():
        nome_antigo = paciente.nome_completo  # Armazena o nome antigo

        paciente.nome_completo=form_edicao_paciente.nome_completo.data.title()
        paciente.data_nascimento=form_edicao_paciente.data_nascimento.data
        paciente.genero=form_edicao_paciente.genero.data
        paciente.telefone=form_edicao_paciente.telefone.data
        paciente.email=form_edicao_paciente.email.data
        paciente.endereco=form_edicao_paciente.endereco.data
        paciente.cpf=form_edicao_paciente.cpf.data
        paciente.rg=form_edicao_paciente.rg.data

        database.session.commit()

        # Se o nome foi alterado, alterar o nome da pasta do paciente
        nome_paciente_novo = "_".join(paciente.nome_completo.split())  # Novo nome do paciente formatado

        # Verificar se o nome foi alterado
        if nome_antigo != paciente.nome_completo:
            caminho_base = os.path.join(app.root_path, 'static', 'pacientes')
            caminho_antigo = os.path.join(caminho_base, "_".join(nome_antigo.split()))
            caminho_novo = os.path.join(caminho_base, nome_paciente_novo)

            if os.path.exists(caminho_antigo):
                os.rename(caminho_antigo, caminho_novo)

        nome_paciente = "_".join(paciente.nome_completo.split())
        caminho_pasta_paciente = os.path.join(app.root_path, f'static/pacientes', nome_paciente)
        if form_edicao_paciente.avaliacao_medica.data:
            nome_arquivo_atualizado = salvar_arquivo(form_edicao_paciente.avaliacao_medica.data, caminho_pasta_paciente, 'Av. Medica')
            paciente.avaliacao_medica = nome_arquivo_atualizado

        if form_edicao_paciente.evolucao_clinica.data:
            nome_arquivo_atualizado = salvar_arquivo(form_edicao_paciente.evolucao_clinica.data, caminho_pasta_paciente, 'Ev. Clinica')
            paciente.evolucao_clinica = nome_arquivo_atualizado

        if form_edicao_paciente.exames.data:
            nome_arquivo_atualizado = salvar_arquivo(form_edicao_paciente.exames.data, caminho_pasta_paciente, 'Exames')
            paciente.exames = nome_arquivo_atualizado

        if form_edicao_paciente.documentos_pessoais.data:
            nome_arquivo_atualizado = salvar_arquivo(form_edicao_paciente.documentos_pessoais.data, caminho_pasta_paciente, 'Documentos Pessoais')
            paciente.documentos_pessoais = nome_arquivo_atualizado

        database.session.commit()
        flash('Dados atualizados com sucesso', 'alert-success')
        return redirect(url_for('edicao_paciente', id=paciente.id))

    nome_paciente = "_".join(paciente.nome_completo.split())
    return render_template('paciente.html', paciente=paciente, form_edicao_paciente=form_edicao_paciente, nome_paciente=nome_paciente )


@app.route('/paciente/<id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_paciente(id):
    paciente = Paciente.query.get(id)
    database.session.delete(paciente)
    database.session.commit()
    flash('Paciente deletado com sucesso', 'alert-danger')
    return redirect(url_for('exibir_pacientes'))
