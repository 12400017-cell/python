from flask import Flask, render_template

app = Flask(__name__)


#render do arquivo index
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sobre/<nome>")
#crie a variavel como parametro
def sobre(nome):
    return f"Olá, {nome}! Bem vindo ao cotemig!"

if __name__ == '__main__':
    app.run(debug=True)