from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)


class Page(db.Model):
    """Таблица для хранения созданных страниц"""
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    creator = db.Column(db.String(100), nullable = False)
    url = db.Column(db.String(200), nullable = False)


class User(db.Model):
    """Таблица для хранения зарегистрировавшихся пользователей"""
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), nullable = False)
    name = db.Column(db.String(100), nullable = False)


with app.app_context():
    """Оберните код, использующий Flask-SQLAlchemy, в контекст приложения.
    Фикс непонятной ошибки"""
    db.create_all()  # Create tables in the database
    app.run()  # запуск приложения


@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        return render_template('search_results.html', search_query=search_query)
    return render_template('templates/home.html')


@app.route('/text_block')
def text_block():
    """Страница на какую-то тему"""
    return render_template('templates/text_block.html')


@app.route('/search_results')
def search_results():
    """результаты поиска"""
    return render_template('templates/search_results.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        # Создание нового пользователя
        new_user = User(email=email, name=name)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html')


if __name__ == '__main__':
    app.run()
