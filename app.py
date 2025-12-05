from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

def carregar_dados():
    if os.path.exists('usuarios.json'):
        with open('usuarios.json', 'r') as f:
            return json.load(f)
    return []

def salvar_dados(alunos):
    with open('usuarios.json', 'w') as f:
        json.dump(alunos, f, indent=4)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar_aluno():
    nome = request.form['nome']
    idade = int(request.form['idade'])

    alunos = carregar_dados()
    alunos.append({'nome': nome, 'idade': idade})
    salvar_dados(alunos)

    return redirect(url_for('sucesso', nome=nome, idade=idade))

@app.route('/sucesso')
def sucesso():
    nome = request.args.get('nome')
    idade = request.args.get('idade')
    return render_template('sucesso.html', nome=nome, idade=idade)

@app.route('/listar')
def listar_alunos():
    alunos = carregar_dados()
    return render_template('listar.html', alunos=alunos)

@app.route('/estatisticas')
def estatisticas():
    alunos = carregar_dados()
    total = len(alunos)
    media = sum([aluno['idade'] for aluno in alunos]) / total if total > 0 else 0
    return render_template('estatisticas.html', estatisticas={'total_alunos': total, 'media_idade': round(media, 2)})

if __name__ == '__main__':
    app.run(debug=True)
