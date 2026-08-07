import math
from flask import render_template, request



#Função calcular
def calcular():
    num1 = float(request.form["num1"])
    operacao = request.form["operacao"]
    
    #sqrt = raiz quadrda
    if operacao == "sqrt": #sqrt = raiz quadrda
        if num1 < 0:
            resultado = "Erro: número negativo"
            etapas = f"Não existe raiz real de {num1}."
            return render_template("calculadora.html", resultado = resultado, etapas = etapas)
        else:
            resultado = math.sqrt(num1)
            etapas = f"√{num1} = {resultado}"
            return render_template("calculadora.html", resultado = resultado, etapas = etapas)
    else:
        num2_valor = request.form.get("num2", "").strip()
        if not num2_valor:
            return render_template(
                "calculadora.html",
                etapas="Informe o segundo número para esta operação.",
                resultados="",
            )
        num2 = float(num2_valor)

    #Soma
    if operacao == "+":
        resultado = num1 + num2
        etapas = f"{num1} + {num2} = {resultado}"
        return render_template("calculadora.html", resultado = resultado, etapas = etapas)
    #Subtração
    if operacao =="-":
        resultado = num1 - num2
        etapas = f"{num1}-{num2}={resultado}"
        return render_template("calculadora.html", resultado = resultado, etapas = etapas)
    #Multiplicação
    if operacao == "*":
        resultado = num1 * num2
        estapas = f"{num1}*{num2}={resultado}"
        return render_template("calculadora.html", resultado = resultado, etapas = etapas)
    #Potencia
    if operacao == "**":
            resultado = num1 ** num2
            etapas = f"{num1} ^{num2} = {resultado}"
            return render_template("calculadora.html", resultado = resultado, etapas = etapas)
    #Divisão
    if operacao == "/" and num2 != 0:
        resultado = num1 / num2
        estapas = f"{num1}/{num2}={resultado}"
        return render_template("calculadora.html", resultado = resultado, etapas = etapas)
    else:
        resultado = "Erro: Não existe divisão por 0"
        etapas = "Não existe divisão por 0"
        return render_template("calculadora.html", resultado = resultado, etapas = etapas)
    

