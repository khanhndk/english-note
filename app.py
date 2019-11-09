import os
import json
from flask import Flask, request, render_template
app = Flask(__name__)
uploads_dir = os.path.join(app.instance_path, 'data')
os.makedirs(uploads_dir, exist_ok=True)


@app.route('/v', methods=["GET"])
def view():
    word = request.args.get('w', default='teacher')
    fp = open(os.path.join(app.instance_path, 'data/' + word + '.json'), 'r')
    word_info = json.load(fp)
    return render_template('view.html', word_info=word_info)


@app.route('/e', methods=["GET"])
def edit():
    word = request.args.get('w', default='teacher')
    file_path = os.path.join(app.instance_path, 'data/' + word + '.json')
    if os.path.exists(file_path):
        fp = open(file_path, 'r')
        word_info = json.load(fp)
    else:
        fp = open(os.path.join(app.instance_path, 'data/' + '0.json'), 'r')
        word_info = json.load(fp)
        word_info['name'] = word
    return render_template('edit.html', word=word, word_info=json.dumps(word_info))


@app.route('/s', methods=["POST"])
def save():
    word = request.form.get('w', default=None)
    data = request.form.get('data', default=None)
    if word is None:
        return 'w is none'
    if data is None:
        return 'data is none'
    fp = open(os.path.join(app.instance_path, 'data/' + word + '.json'), 'w')
    fp.write(data)
    fp.close()
    return 'We saved it. Thanks.'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
