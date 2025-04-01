from flask import Flask, render_template

app = Flask(__name__)


def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


@app.route('/')
def welcome():
    return read_file('welcome.html')


if __name__ == '__main__':
    app.run()
