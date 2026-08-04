from flask import Flask, render_template_string, request

app = Flask(__name__)

listaLogins = [
    {"nome": "Léo", "senha":"lulu3"},
    {"nome": "Theo", "senha":"drSunshin3"},
    {"nome": "Yuri", "senha":"orak4"}
]
templateForms = """
    <h2>Login</h2>
    <form method="post">
        <!--
            diferende do id o NAME funciona como algo universal 
            que pode ser acessado pelo .py com o import request.
            OBS:
            o form registra as infos como um dicionário, o NAME da nome a chave
            aos dados que serão usados pelo POST ou GET
        -->
        <input type="text" name = "usuario" placeholder="usuario">

        <br><br>
        <input type="password" name = "senha" placeholder="senha">

        <br><br>
        <button type="submit">Enviar</button>
    </form>"""


def exibirForm():
    return render_template_string(templateForms)

#Função que salva as infos de login e senha em variaveis e verifica se é logavel
#como os resultados devem ser exibidos na págino, os RETURNS devem estar com códigos HTML
def fazerLogin():
    usuario = request.form.get('usuario') #criando variavel que registrara o nome de usuario
    senha = request.form.get('senha') #variavel que retera a senha do usuario
    
    #processo para verificar a lista e identificar usuarios que podem logar
    #para usuario ser permitido a entrar na lista o seu nome e senha devem estar dentro dela
    for usuarioPermitido in listaLogins:
        if usuario == usuarioPermitido["nome"] and senha == usuarioPermitido["senha"]:
            return f"<h1>BemVinde, {usuario.title()} <3</h1>"
        

#Metodos Get e post:
# GET = busca informaçẽos para o servidor(app.py)
# Os dados pegos vão para a a url tipo || login?matricola=12345&senha=abc.
# POST = serve para mandar dados para o servidor

@app.route('/', methods = ['GET','POST'])
def login():
    #se o metodo request desejado for POST(vai mandar os dados digitados para o servidor/os armazenar)
    if request.method == 'POST':
        return fazerLogin()
    #caso o metodo request não for POST o form só irá se reexibido 
    else:
        return exibirForm()


if __name__ == '__main__':
    app.run(debug=True)