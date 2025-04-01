from flask import Flask, render_template

app = Flask(__name__)


def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


@app.route('/')
def welcome():
    """Главная страница"""
    return read_file('home.html')


@app.route('/search', methods = ['GET', 'POST'])
def search():
    """страница поиска других страниц"""
    return read_file('search.html')


@app.route('/text_block')
def text_block():
    """Страница на какую-то тему"""
    return read_file('text_block.html')


if __name__ == '__main__':
    app.run()
