from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from .utils import paraphrase
from chatbot import Chat, register_call
import os
import time
import spacy


# Loading English tokenizer, tagger, parser, NER and word vectors.
nlp = spacy.load("en_core_web_md")

@register_call("whoIs")
def who_is(query, session_id="general"):
    return "I am a bot, created for a demo."

template_file_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "test.template")
chat = Chat(template_file_path)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    # Defining a new SQLAlchemy model named Question, representing a table in the database.
    class Question(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        original = db.Column(db.String(500), nullable=False)
        paraphrase = db.Column(db.String(500), nullable=False)

    with app.app_context():
        db.create_all()

    @app.route('/', methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            questions = request.form.getlist('question')
            for question in questions:
                if question:
                    paraphrased_question = paraphrase(question)
                    question_record = Question(
                        original=question, paraphrase=paraphrased_question)
                    db.session.add(question_record)
            db.session.commit()
            return redirect(url_for('paraphrase_page'))
        return render_template('index.html')

    @app.route('/paraphrase', methods=['GET', 'POST'])
    def paraphrase_page():
        if request.method == 'POST':
            if request.form.get('button') == 'clear':
                db.session.query(Question).delete()
                db.session.commit()
                return redirect(url_for('home'))
        questions = [(q.original, q.paraphrase) for q in Question.query.all()]
        return render_template('paraphrase.html', questions=questions)

    @app.route('/edit', methods=['POST'])
    def edit_questions():
        paraphrases = request.json.get('paraphrases')
        if paraphrases:
            questions = Question.query.all()
            for i in range(min(len(questions), len(paraphrases))):
                questions[i].paraphrase = paraphrases[i]
            db.session.commit()
            return jsonify(success=True)
        return jsonify(success=False)

    @app.route('/evaluate', methods=['GET'])
    def evaluate_page():
        questions = Question.query.all()

        original_response_times = []
        paraphrase_response_times = []
        original_similarities = []
        paraphrase_similarities = []

        for question in questions:
            # Collecting original question responses and time.
            start_time = time.time()
            original_response = chat.respond(question.original)
            original_response_times.append(time.time() - start_time)
            original_similarity = nlp(question.original).similarity(
            nlp(original_response))
            original_similarities.append(original_similarity)

            # Collecting paraphrase question responses and time.
            start_time = time.time()
            paraphrase_response = chat.respond(question.paraphrase)
            paraphrase_response_times.append(time.time() - start_time)
            paraphrase_similarity = nlp(question.paraphrase).similarity(
            nlp(paraphrase_response))
            paraphrase_similarities.append(paraphrase_similarity)
            
        # Computing average response times.
        original_avg_time = sum(original_response_times) / \
            len(original_response_times) if original_response_times else 0
        paraphrase_avg_time = sum(paraphrase_response_times) / len(
            paraphrase_response_times) if paraphrase_response_times else 0

        # Computing average similarities.
        original_avg_similarity = sum(
            original_similarities) / len(original_similarities) if original_similarities else 0
        paraphrase_avg_similarity = sum(
            paraphrase_similarities) / len(paraphrase_similarities) if paraphrase_similarities else 0

        accuracy = {"original": original_avg_similarity * 100,
                    "paraphrase": paraphrase_avg_similarity * 100}
        response_time = {"original": original_avg_time,
                     "paraphrase": paraphrase_avg_time}
        
        return render_template('evaluate.html', accuracy=accuracy, response_time=response_time)

    return app
