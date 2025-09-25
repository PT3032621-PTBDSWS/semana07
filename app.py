from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    funcao = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()
    # inserir dados iniciais só uma vez
    if Usuario.query.count() == 0:
        dados_iniciais = [
            ("john", "Administrator"),
            ("susan", "User"),
            ("david", "User"),
            ("Professor Fabio Teixeira", "User"),
            ("Fabio Teixeira", "User"),
            ("lucca", "User"),
            ("Mateus", "User"),
            ("Giovanna", "User")
        ]
        for nome, funcao in dados_iniciais:
            db.session.add(Usuario(nome=nome, funcao=funcao))
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome_digitado = request.form.get('nome')
        if nome_digitado and nome_digitado.strip():
            novo_usuario = Usuario(nome=nome_digitado.strip(), funcao="User")
            db.session.add(novo_usuario)
            db.session.commit()
        return redirect(url_for('index'))

    usuarios = Usuario.query.all()

    ultimo_nome = usuarios[-1].nome if usuarios else None

    return render_template('index.html', usuarios=usuarios, ultimo_nome=ultimo_nome)

if __name__ == '__main__':
    app.run(debug=True)
