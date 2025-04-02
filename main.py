from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        return render_template('search_results.html', search_query=search_query)
    return render_template('home.html')


@app.route('/text_block')
def text_block():
    """Страница на какую-то тему"""
    return render_template('templates/text_block.html')


@app.route('/search_results')
def search_results():
    """результаты поиска"""
    return render_template('templates/search_results.html')


if __name__ == '__main__':
    app.run()
