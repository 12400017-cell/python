"""
AulaSQLalchemy — Flask + SQLAlchemy (simples, sem MVC)
CRUD de alunos em um único arquivo.
"""
#os(sistema operacional:
#Serve para conectar o programa ao sistema operacional do pc,
#com ele posso saber exatamente onde o arquivo python vai estar, evitando erro de arquivo não encontrado
import os 
#import redireect: serve para manda mandar o usuario para outra págin?
from flask import Flask, redirect, render_template, request, url_for
#import do banco de dados
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#serve para descobrir o caminho obsoluto de onde o arquivo python esta sendo salvo no pc
pasta_aula = os.path.abspath(os.path.dirname(__file__))
#Define qual banco de dados a aplicação vai usar
#os.path,join(): serve para criar um aquivo detntro da pasta_aula(var que dedura a localização do código)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    pasta_aula, "alunos.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#conecta o banco de dados com o app.py
db = SQLAlchemy(app) 


# --- Criando a tabela alunos ---
class Aluno(db.Model):
    __tablename__ = "alunos"
    
    #Criando as colunas do BD
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(120), nullable = False) #para telefone ser salvo, devo criar uma coluna no banco de dados
    def __repr__(self):
        return f"<Aluno {self.id} {self.nome}>" #apenas serve para mostrar os alunos no terminal


with app.app_context():
    db.create_all() #criando as tabelas?? eu não ja as criei antes?


# --- READ — listar ---
@app.route("/")
def index():
    alunos = Aluno.query.order_by(Aluno.nome).all()
    return render_template("lista.html", alunos=alunos)


# --- CREATE — cadastrar ---
@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone","").strip()
        if not nome or not email:
            return render_template(
                "formulario.html",
                titulo="Cadastrar aluno",
                erro="Preencha nome e e-mail.",
                nome=nome,
                email=email,
                telefone = telefone
            )
        aluno = Aluno(nome=nome, email=email, telefone = telefone)
        db.session.add(aluno)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("formulario.html", titulo="Cadastrar aluno")


# --- UPDATE — editar ---
@app.route("/editar/<int:aluno_id>", methods=["GET", "POST"])
def editar(aluno_id):
    aluno = db.session.get(Aluno, aluno_id)
    if not aluno:
        return redirect(url_for("index"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone","").strip()
        if not nome or not email:
            return render_template(
                "formulario.html",
                titulo="Editar aluno",
                erro="Preencha nome e e-mail.",
                nome=nome,
                email=email,
                telefone = telefone,
                aluno_id=aluno.id,
            )
        aluno.nome = nome
        aluno.email = email
        aluno.telefone = telefone
        db.session.commit()
        return redirect(url_for("index"))

    return render_template(
        "formulario.html",
        titulo="Editar aluno",
        nome=aluno.nome,
        email=aluno.email,
        telefone = aluno.telefone,
        aluno_id=aluno.id,
    )


# --- DELETE — excluir ---
@app.route("/excluir/<int:aluno_id>", methods=["POST"])
def excluir(aluno_id):
    aluno = db.session.get(Aluno, aluno_id)
    if aluno:
        db.session.delete(aluno)
        db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
