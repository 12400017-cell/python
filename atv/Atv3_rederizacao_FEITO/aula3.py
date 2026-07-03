from flask import Flask, render_template

app = Flask(__name__)


#render do arquivo index
@app.route("/")
def home():
    #ao inves de escrever o codigo HTML/CSS Todo dentro do return
    #eu uso o render_template() para conectar o decoratorFlask com o arquivo HTML dentro da pasta templates
    return render_template("index.html") 

#a variavel esta dentro da url
@app.route("/sobre/<nome>")
#crie a variavel como parametro
def sobre(nome):
    return f"Olá, {nome}! Bem vindo ao cotemig!"

if __name__ == '__main__':
    app.run(debug=True)