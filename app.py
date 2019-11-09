import os
import json
from flask import Flask, request, render_template, jsonify
app = Flask(__name__)
uploads_dir = os.path.join(app.instance_path, 'data')
questions_dir = os.path.join(app.instance_path, 'questions')
os.makedirs(uploads_dir, exist_ok=True)
os.makedirs(questions_dir, exist_ok=True)


@app.route('/a', methods=["GET"])
def edit_answer():
    qid = request.args.get('qid', default='0')
    topic = request.args.get('t', default='misc')
    question_path = os.path.join(questions_dir, topic + '.' + str(qid) + '.json')
    question_info = {'question': 'yy', 'answer': 'xx'}
    if os.path.exists(question_path):
        question_info = json.load(open(question_path))

    return render_template('answer.html', qid=qid, topic=topic, question_info=question_info)


@app.route('/va', methods=["GET"])
def view_answer():
    qid = request.args.get('qid', default='2')
    topic = request.args.get('t', default='misc')
    question_path = os.path.join(questions_dir, topic + '.' + qid + '.json')
    question_info = {'question': 'yy', 'answer': 'xx'}
    if os.path.exists(question_path):
        question_info = json.load(open(question_path))

    return render_template('view_answer.html', qid=qid, topic=topic, question_info=question_info)


@app.route('/v', methods=["GET"])
def view():
    word = request.args.get('w', default='teacher')
    return_type = request.args.get('r', default='html')
    fp = open(os.path.join(app.instance_path, 'data/' + word + '.json'), 'r')
    word_info = json.load(fp)
    if return_type == 'html':
        return render_template('view.html', word_info=word_info)
    return jsonify(word_info)


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


@app.route('/qa', methods=["POST"])
def save_answer():
    topic = request.form.get('t', default=None)
    qid = request.form.get('qid', default=None)
    question = request.form.get('q', default=None)
    answer = request.form.get('a', default=None)
    if topic is None or qid is None or question is None or answer is None:
        return 'something is none'
    question_path = os.path.join(questions_dir, topic + '.' + qid + '.json')
    question_info = {'question': question, 'answer': answer}
    fp = open(question_path, 'w')
    json.dump(question_info, fp)
    fp.close()
    return 'We saved it. Thanks.'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
