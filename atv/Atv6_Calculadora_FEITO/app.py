from flask import Flask, render_template, request, url_for
from calculadora import calcular
app = Flask(__name__)

@app.route('/', methods = ["GET","POST"])
def index():
    #Quando clicar no botão de enviar, deve rodas a função de calcular da calcular.py
    if request.method == "POST":
        return calcular()

    return render_template("calculadora.html")


if __name__ == '__main__':
    app.run(debug=True)