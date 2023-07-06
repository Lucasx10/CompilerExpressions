from flask import Flask, render_template, request, redirect, session
import os
import subprocess

app = Flask(__name__)
app.secret_key = 'b'


def clear_entrada_file(arquivo):
    with open(arquivo, 'w') as file:
        file.write('')


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]

        if file and file.filename.endswith('.txt'):
            file.save('entrada.txt')
            subprocess.run(['python', 'CompilerExpressions.py'])
            clear_entrada_file('entrada.txt')

            return redirect('/resultado')

    return render_template("index.html")


@app.route("/manual-insert", methods=["GET", "POST"])
def manual_insert():
    return render_template("manual-insert.html")


@app.route("/manual-insert-compile", methods=["GET", "POST"])
def manual_insert_compile():
    if request.method == "POST":
        user_text = request.form.get("user_text")
        user_text = user_text.replace("\n", "")  # Remover quebras de linha
        with open('entrada.txt', 'w') as file:
            file.write(user_text)
        subprocess.run(['python', 'CompilerExpressions.py'])
        clear_entrada_file('entrada.txt')

        return redirect('/resultado')

    return render_template("manual-insert.html")


import os

@app.route('/resultado')
def resultado():
    if os.path.exists('erro.txt'):
        with open('erro.txt', 'r') as erro_file:
            erro_content = erro_file.read().strip()  # Remover espaços em branco
        if erro_content:
            with open('entrada2.txt', 'r') as entrada2:
                entrada2 = entrada2.read()
            clear_entrada_file('erro.txt')
            # Renderizar o template HTML passando o conteúdo do erro e da entrada para o template
            return render_template('result.html', erro=erro_content, entrada2=entrada2)
    
        # Ler o conteúdo dos arquivos de texto
        with open('entrada2.txt', 'r') as entrada2, \
            open('quadrupla.txt', 'r') as quadrupla, \
            open('codInterGlobal.txt', 'r') as codInterGlobal, \
            open('codInterOtimGlobal.txt', 'r') as codInterOtimGlobal:

            # Armazenar o conteúdo dos arquivos em variáveis
            entrada2 = entrada2.read()
            quadrupla = quadrupla.read()
            codInterGlobal = codInterGlobal.read()
            codInterOtimGlobal = codInterOtimGlobal.read()
            clear_entrada_file('entrada2.txt')
            clear_entrada_file('quadrupla.txt')
            clear_entrada_file('codInterGlobal.txt')
            clear_entrada_file('codInterOtimGlobal.txt')

        # Renderizar o template HTML passando as variáveis para o template
        return render_template('result.html',
                            entrada2=entrada2,
                            quadrupla=quadrupla,
                            codInterGlobal=codInterGlobal,
                            codInterOtimGlobal=codInterOtimGlobal)




if __name__ == "__main__":
    app.run(debug=True)
