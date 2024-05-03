from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from flask_jogoteca import app, db
from models import Jogos, Usuarios


@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id) #faz select no bd ordenando  id
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        # caso tente acessar a tela de novo e esteja deslogado, depois que logar ele manda para tela de novo
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    #Depois de incluir o request na lib conseguimos pegar através do nome da class do input, os valores
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogos.query.filter_by(nome=nome).first()

    #verificando se jogo existe na base de dados
    if jogo:
        flash('Jogo já existente!')
        return redirect(url_for('index'))

    #caso jogo não exista na base de dados:
    #instanciando o jogo, caso ele não exista na base
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    #grava arquivo do jogo dentro de uma pasta no server.
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD'] #PEGA CAMINHO DENTRO DO config.py
    arquivo.save(f'upload_path/capa{novo_jogo}.jpg')

    #url_for localiza o metodo entre as aspas
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        # caso tente acessar a tela de novo e esteja deslogado, depois que logar ele manda para tela de novo
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = Jogos.query.filter_by(id=id).first()
    return render_template('editar.html', titulo='Editando Jogo', jogo=jogo)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']

    #gravando no banco:
    db.session.add(jogo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso')

    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    #faz select do user filtrando o user que foi colocado no input do form e pega o primeiro que for localizado (como se fosse o limit 1 do sql)
    usuario = Usuarios.query.filter_by(nickname = request.form['usuario']).first()

    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

#Com a rota abaixo sera localizada a imagem do jogo
@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):



