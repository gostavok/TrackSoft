from flask import Flask , render_template, request, redirect, session
from models import Usuario, Veiculo, Camera
from peewee import *

app = Flask(__name__)
app.config['SECRET_KEY']="kjNBKJBWF87t23hbjh%$#@(*%$*zxfgafdgadfgadfgadfga434wedf344g"

@app.route("/")
def recepcao():
    return render_template ("inicio.html", title = "TrackSoft")

@app.route("/perfil")
def perfil():
    lista = Usuario.select()
    carros_pessoa=[]
    cameras_pessoa=[]
    lista_carros = Veiculo.select()
    lista_cameras = Camera.select()
    for carro in lista_carros:
        if carro.dono.nome == session['usuario']:
            carros_pessoa.append(carro)
    for camera in lista_cameras:
        if camera.dono.nome == session['usuario']:
            cameras_pessoa.append(camera)

    return render_template ("perfil.html", title = "Perfil", lista = lista, carros_pessoa = carros_pessoa,cameras_pessoa = cameras_pessoa, id_usuario = session['usuario'])

@app.route("/form_cadastro_veiculo")
def form_cadastro_veiculo():
    return render_template ("form_cadastro_veiculo.html", title = "Cadastro de Veículo")

@app.route("/form_cadastro_camera")
def form_cadastro_camera():
    return render_template ("form_cadastro_camera.html", title = "Cadastro de Câmera")

@app.route("/cadastro_usuario",  methods = ["POST"])
def cadastro_usuario():
    nome = request.form["nome"]
    email = request.form["email"]
    cpf = request.form["CPF"]
    senha1 = request.form["senha1"]
    senha2 = request.form["senha2"]
    if len(cpf) == 11:
        if senha1 == senha2:
            novo_usuario = Usuario(nome = nome, email = email, cpf = cpf, senha = senha1)
            novo_usuario.save()
            session['usuario'] = nome
            return redirect("/perfil")
    return redirect("/")

@app.route('/login', methods = ["POST"])
def login():
    email = request.form["email"]
    senha = request.form["senha"]
    busca = Usuario.get_or_none(email = email, senha = senha)
    lista = Usuario.select()
    for a in lista:
        if a.email == email:
            pessoa = a.nome
    if busca != None:
        session['usuario'] = pessoa
        render_template('inicio.html')
    
    return redirect("/perfil")

@app.route("/cadastro_veiculo",  methods = ["POST"])
def cadastro_veiculo():
    marca = request.form["marca"]
    modelo = request.form["modelo"]
    cor = request.form["cor"]
    placa = request.form["placa"]
    ano = request.form["ano"]
    foto = request.form["foto"]
    descricao = request.form["descricao"]
    nome = session['usuario']
    lista = Usuario.select()
    for a in lista:
        if a.nome == nome:
            novo_veiculo = Veiculo(marca = marca,modelo = modelo,cor = cor, placa = placa, ano = ano, foto = "/static/" + foto, descricao = descricao, dono = a )
            novo_veiculo.save()
            return redirect("/perfil")

        
@app.route("/cadastro_camera",  methods = ["POST"])
def cadastro_camera():
    rua = request.form["rua"]
    numero = request.form["numero"]
    bairro = request.form["bairro"]
    cidade = request.form["cidade"]
    estado = request.form["estado"]
    descricao = request.form["descricao"]
    nome = session['usuario']
    lista = Usuario.select()
    for a in lista:
        if a.nome == nome:
            nova_camera = Camera( rua = rua, numero = numero,bairro = bairro, cidade = cidade, estado = estado, descricao = descricao, dono = a )
            nova_camera.save()
            return redirect("/perfil")

@app.route("/logout")
def logout():
    session.pop('usuario')
    return redirect ("/")

app.run(debug=True, host="0.0.0.0")