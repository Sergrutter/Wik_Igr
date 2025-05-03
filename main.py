from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf.csrf import CSRFProtect
from rapidfuzz import fuzz
import os

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    # Создаем экземпляр приложения
    app = Flask(__name__)

    # Конфигурация
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Инициализируем расширения с приложением
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'login'

    return app

app = create_app()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    pages = db.relationship('Page', backref='author', lazy=True)


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    pages = Page.query.all()
    return render_template('home.html', pages=pages)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Проверка, существует ли пользователь
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Пользователь с таким именем или email уже существует', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/api/search', methods=['POST'])
def api_search():
    search_query = request.form.get('search_query', '').lower()
    results = []

    for page in Page.query.all():
        if search_query in page.title.lower():
            results.append({
                'id': page.id,
                'title': page.title,
                'preview': page.content[:100]
            })

    return jsonify(results)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Неверный email или пароль', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/create_page', methods=['GET', 'POST'])
@login_required
def create_page():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['page_name']

        new_page = Page(title=title, content=content, author=current_user)
        db.session.add(new_page)
        db.session.commit()

        flash('Страница успешно создана!', 'success')
        return redirect(url_for('home'))

    return render_template('create_page.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query'].lower()
        all_pages = Page.query.all()

        matched_pages = []
        for page in all_pages:
            score = fuzz.partial_ratio(search_query, page.title.lower())
            if score > 60:
                matched_pages.append((score, page))

        matched_pages.sort(reverse=True, key=lambda x: x[0])
        pages = [p[1] for p in matched_pages]

        return render_template('search_results.html', pages=pages, query=search_query)

    return redirect(url_for('home'))


@app.route('/page/<int:page_id>')
def page_detail(page_id):
    page = Page.query.get(page_id)
    return render_template('text_block.html', page=page)


@app.route('/edit_page/<int:page_id>', methods=['GET', 'POST'])
@login_required
def edit_page(page_id):
    page = Page.query.get(page_id)

    if current_user.id != page.user_id:
        flash('У вас нет прав для редактирования этой страницы', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        page.title = request.form['page_name']
        page.content = request.form['content']
        db.session.commit()

        flash('Страница успешно обновлена', 'success')
        return redirect(url_for('page_detail', page_id=page_id))

    return render_template('edit_page.html', page=page)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
