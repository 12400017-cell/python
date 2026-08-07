from flask import Flask, render_template

app = Flask(__name__)


#render do arqvo index
#Crie um template que exiba a mensagem: “Olá, {{ nome }}”.
@app.route("/")
def listaAlunos():
    alunos = [
        {"nome":"Ana", "email":"ana@gnail.com","idade":17,"nota": 5},
        {"nome":"Léo", "email":"leo@gnail.com","idade":17,"nota": 10},
        {"nome":"Guto", "email":"guto@gnail.com","idade":17,"nota": 7}
    ]
    return render_template("alunos.html",alunos =alunos)
#def home(nome, email,idade):
    
    #textMensagem = f"Olá {nome} do email {email}"
    #return render_template("index.html", mensagem = textMensagem)
#    return render_template("index.html", nome = nome, email = email,idade = idade)

if __name__ == '__main__':
    app.run(debug=True)