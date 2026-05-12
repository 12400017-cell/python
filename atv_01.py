#Importar bliblioteca Flask
#Flask serve para criar aplicações web em python
from flask import Flask


#Iniciando o Flask
#pq?
app = Flask(__name__)

#Decorador 1
#decorador serve para:
#vai mapear a função abaixo que estara com uma rota para um arquivo do pc
@app.route('/') #caso chamar "/"" no programa, o que ta no return acontece
def ola_mundo():
    #no return deve-se colocar o html
    return"coloque html"


#Outro decorador
@app.route('/hello')
def hello():
    return ''


# Isso inicia o servidor Flask em modo de depuração, o que é útil para desenvolvimento
if __name__ == '__main__':
    app.run(debug=True)
