from dns.e164 import query

from spfcproject import app, database
from flask import render_template, flash, redirect, url_for, request, jsonify
from spfcproject.forms import FormCadastroAtleta, FormLogin, FormEdicaoAtleta
from spfcproject.models import Usuario, Atleta
from flask_login import login_user, logout_user, current_user, login_required
import shutil
import os
from datetime import datetime


def salvar_arquivo(arquivo, pasta_atleta, subpasta):
    caminho_completo = os.path.join(f'{pasta_atleta}/{subpasta}', arquivo.filename)
    arquivo.save(caminho_completo)
    return arquivo.filename


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form_cadastro_atleta = FormCadastroAtleta()
    if form_cadastro_atleta.validate_on_submit():
        atleta = Atleta(nome_completo=form_cadastro_atleta.nome_completo.data.title(), data_nascimento=form_cadastro_atleta.data_nascimento.data, cpf=form_cadastro_atleta.cpf.data, categoria=form_cadastro_atleta.categoria.data)
        database.session.add(atleta)
        database.session.commit()
        nome_atleta = "_".join(atleta.nome_completo.split())
        caminho_pasta_atleta = os.path.join(app.root_path, f'static/categorias/{atleta.categoria}', nome_atleta)
        os.makedirs(caminho_pasta_atleta, exist_ok=True)
        exames = ['Av. Cardiologica', 'Ev. Diaria', 'Exames', 'Pendencias']
        for exame in exames:
            caminho_pasta_exames = os.path.join(app.root_path, f'static/categorias/{atleta.categoria}/{nome_atleta}', f'{exame}')
            os.makedirs(caminho_pasta_exames, exist_ok=True)

        if form_cadastro_atleta.avaliacao_cardiologica.data:
            nome_arquivo_atualizado = salvar_arquivo(form_cadastro_atleta.avaliacao_cardiologica.data, caminho_pasta_atleta, 'Av. Cardiologica')
            atleta.avaliacao_cardiologica = nome_arquivo_atualizado

        if form_cadastro_atleta.evolucao_diaria.data:
            nome_arquivo_atualizado = salvar_arquivo(form_cadastro_atleta.evolucao_diaria.data, caminho_pasta_atleta, 'Ev. Diaria')
            atleta.evolucao_diaria = nome_arquivo_atualizado

        if form_cadastro_atleta.exames.data:
            nome_arquivo_atualizado = salvar_arquivo(form_cadastro_atleta.exames.data, caminho_pasta_atleta, 'Exames')
            atleta.exames = nome_arquivo_atualizado

        if form_cadastro_atleta.pendencias.data:
            nome_arquivo_atualizado = salvar_arquivo(form_cadastro_atleta.pendencias.data, caminho_pasta_atleta, 'Pendencias')
            atleta.pendencias = nome_arquivo_atualizado

        database.session.commit()
        flash(f'{form_cadastro_atleta.nome_completo.data.title()} cadastrado com sucesso!', 'alert-success')
        return redirect(url_for('home'))
    return render_template('home.html', form_cadastro_atleta=form_cadastro_atleta)


@app.route('/exibir-atletas')
@login_required
def exibir_atletas():
    categorias = ['SUB-09', 'SUB-10', 'SUB-11', 'SUB-12', 'SUB-13', 'SUB-14', 'SUB-15', 'SUB-16', 'SUB-17', 'SUB-20']
    categoria_selecionada = request.args.get('categoria', '').strip()
    with app.app_context():
        if categoria_selecionada:
            lista_atletas = Atleta.query.filter_by(categoria= categoria_selecionada).order_by(Atleta.id.desc()).all()
        else:
            # Caso contrário, pega todos os atletas
            lista_atletas = Atleta.query.order_by(Atleta.id.desc()).all()
    return render_template('exibir-atletas.html', lista_atletas=lista_atletas, categorias=categorias, categoria_selecionada=categoria_selecionada)



@app.route('/loginspfc',  methods= ['GET', 'POST'])
def loginspfc():
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
    return render_template('loginspfc.html', form_loginspfc=form_loginspfc)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso', 'alert-success')
    return redirect(url_for('loginspfc'))


@app.route('/editaratleta-<id>', methods=['GET', 'POST'])
def edicao_atleta(id):
    form_edicao_atleta = FormEdicaoAtleta()
    atleta = Atleta.query.get(id)
    form_edicao_atleta.id.data = int(atleta.id)

    if request.method == 'GET':
        form_edicao_atleta.nome_completo.data = atleta.nome_completo
        form_edicao_atleta.data_nascimento.data = datetime.strptime(atleta.data_nascimento, "%Y-%m-%d")
        form_edicao_atleta.cpf.data = atleta.cpf
        form_edicao_atleta.categoria.data = atleta.categoria

    if form_edicao_atleta.validate_on_submit():
        categoria_antiga = atleta.categoria  # Armazena a categoria atual antes da alteração
        nova_categoria = form_edicao_atleta.categoria.data  # Nova categoria do formulário
        nome_antigo = atleta.nome_completo  # Armazena o nome antigo

        # Atualiza os dados do atleta
        atleta.nome_completo = form_edicao_atleta.nome_completo.data
        atleta.data_nascimento = form_edicao_atleta.data_nascimento.data
        atleta.cpf = form_edicao_atleta.cpf.data
        atleta.categoria = nova_categoria
        database.session.commit()

        # Se a categoria ou o nome foi alterado, mover a pasta do atleta
        nome_atleta_novo = "_".join(atleta.nome_completo.split())  # Novo nome do atleta formatado

        # Verificar se a categoria foi alterada
        if categoria_antiga != nova_categoria:
            caminho_antigo = os.path.join(app.root_path, f'static/categorias/{categoria_antiga}',
                                          "_".join(nome_antigo.split()))
            caminho_novo = os.path.join(app.root_path, f'static/categorias/{nova_categoria}', nome_atleta_novo)

            os.makedirs(os.path.dirname(caminho_novo), exist_ok=True)

            # Se a pasta do atleta existir na categoria antiga, move para a nova
            if os.path.exists(caminho_antigo):
                shutil.move(caminho_antigo, caminho_novo)

        # Verificar se o nome foi alterado
        if nome_antigo != atleta.nome_completo:
            caminho_antigo_nome = os.path.join(app.root_path, f'static/categorias/{nova_categoria}',
                                               "_".join(nome_antigo.split()))
            caminho_novo_nome = os.path.join(app.root_path, f'static/categorias/{nova_categoria}', nome_atleta_novo)

            # Se o nome do atleta foi alterado, mover a pasta
            if os.path.exists(caminho_antigo_nome):
                shutil.move(caminho_antigo_nome, caminho_novo_nome)

        nome_atleta = "_".join(atleta.nome_completo.split())
        caminho_pasta_atleta = os.path.join(app.root_path, f'static/categorias/{atleta.categoria}', nome_atleta)
        if form_edicao_atleta.avaliacao_cardiologica.data:
            nome_arquivo_atualizado = salvar_arquivo(form_edicao_atleta.avaliacao_cardiologica.data, caminho_pasta_atleta, 'Av. Cardiologica')
            atleta.avaliacao_cardiologica = nome_arquivo_atualizado

        if form_edicao_atleta.evolucao_diaria.data:
            nome_arquivo_atualizado = salvar_arquivo(form_edicao_atleta.evolucao_diaria.data, caminho_pasta_atleta, 'Ev. Diaria')
            atleta.evolucao_diaria = nome_arquivo_atualizado

        if form_edicao_atleta.exames.data:
            nome_arquivo_atualizado = salvar_arquivo(form_edicao_atleta.exames.data, caminho_pasta_atleta, 'Exames')
            atleta.exames = nome_arquivo_atualizado

        if form_edicao_atleta.pendencias.data:
            nome_arquivo_atualizado = salvar_arquivo(form_edicao_atleta.pendencias.data, caminho_pasta_atleta, 'Pendencias')
            atleta.pendencias = nome_arquivo_atualizado

        database.session.commit()
        flash('Dados atualizados com sucesso', 'alert-success')
        return redirect(url_for('edicao_atleta', id=atleta.id))

    nome_atleta = "_".join(atleta.nome_completo.split())
    return render_template('atleta.html', atleta=atleta, form_edicao_atleta=form_edicao_atleta, nome_atleta=nome_atleta )


@app.route('/atleta/<id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_atleta(id):
    atleta = Atleta.query.get(id)
    database.session.delete(atleta)
    database.session.commit()
    flash('Atleta deletado com sucesso', 'alert-danger')
    return redirect(url_for('exibir_atletas'))
