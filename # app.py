import statistics
import json
import os
from flask import Flask, render_template, request

app = Flask(__name__)

# Função para carregar dados do arquivo JSON
def carregar_dados():
    if os.path.exists('usuarios.json'):
        with open('usuarios.json', 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    else:
        return []

# Função para salvar dados no arquivo JSON
def salvar_dados(usuarios):
    with open('usuarios.json', 'w', encoding='utf-8') as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)

# Página de Cadastro
@app.route('/')
def cadastro():
    return render_template('cadastro.html')

# Rota para Processar o Formulário de Cadastro
@app.route('/cadastro', methods=['POST'])
def cadastrar_aluno():
    nome = request.form.get('nome')
    idade = request.form.get('idade')

    # Armazenar o aluno no arquivo JSON
    usuarios = carregar_dados()
    novo_usuario = {"nome": nome, "idade": int(idade)}
    usuarios.append(novo_usuario)
    salvar_dados(usuarios)

    return f'Aluno {nome}, de {idade} anos, cadastrado com sucesso!'

# Página de Listar Alunos
@app.route('/listar')
def listar():
    alunos = carregar_dados()
    return render_template('listar.html', alunos=alunos)

# Página de Estatísticas (Simples, exibe estatísticas de idade)
@app.route('/estatisticas')
def estatisticas():
    usuarios = carregar_dados()
    if not usuarios:
        return "Nenhum dado disponível para análise."

    idades = [usuario['idade'] for usuario in usuarios]
    estatisticas = {
        'total_alunos': len(usuarios),
        'media_idade': statistics.mean(idades) if idades else 0
    }
    return render_template('estatisticas.html', estatisticas=estatisticas)

if __name__ == '__main__':
    app.run(debug=True)
