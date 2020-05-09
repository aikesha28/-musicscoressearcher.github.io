from flask import Flask, render_template, request
import compare
import fragmentParse

app = Flask(__name__)

res = []


@app.route('/')
def begin():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    x = []
    file = request.files['file']
    print(file)
    x = fragmentParse.parseXML(file)
    res = compare.search(x)
    print(res)

    return render_template('searchresults.html', results=res, length=len(res), filename=file)


if __name__ == '__main__':
    app.run()
