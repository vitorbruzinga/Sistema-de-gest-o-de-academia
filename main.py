from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
CORS(app)

# Configurar o banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///academia.db'
db = SQLAlchemy(app)

# Configurar o gerenciador de login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Definir a classe User para representar treinadores e alunos
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(10), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), nullable=False)

# Função para carregar um usuário com base no ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))    

# Rota para a página inicial
@app.route('/')
def pagina_inicial():
    return render_template('index.html')

@app.route('/tipo')
def tipo():
    return render_template('acesso.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/registro_page')
def registro_page():
    return render_template('registro.html')

# Resto do seu código aqui...

if __name__ == '__main__':
    app.run(debug=True)


# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']
        user = User.query.filter_by(matricula=matricula, senha=senha).first()

        if user:
            login_user(user)
            if user.role == 'cliente':
                return redirect(url_for('index_client.hmtl'))
            else:
                # Se for um treinador, redirecione para a página do treinador
                return redirect(url_for('index_adm.html'))

        return "Credenciais inválidas. Por favor, verifique sua matrícula e senha."

    return render_template('login.html')  # Renderiza a página login.html

@app.route('/registro', methods=['POST'])
def registro():
    if request.method == 'POST':
        matricula = request.form['matricula']
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        telefone = request.form['telefone']
        tipo_plano = request.form['tipo_plano']
        senha = request.form['senha']

        # Verifique se a matrícula já existe no banco de dados
        existing_user = User.query.filter_by(matricula=matricula).first()

        if existing_user:
            return "Matrícula já existe. Escolha outra matrícula."

        # Se a matrícula não existe, insira o novo usuário no banco de dados
        new_user = User(matricula=matricula, nome=nome, sobrenome=sobrenome, telefone=telefone, tipo_plano=tipo_plano, senha=senha)
        db.session.add(new_user)
        db.session.commit()

        return "Cadastro bem-sucedido."

    return render_template('registro.html')

# Rota para a página inicial do cliente após o login bem-sucedido
@app.route('/pagina_inicial_cliente')
def pagina_inicial_cliente():
    return render_template('index_client.html')

if __name__ == '__main__':
    app.run(debug=True)
