from flask import Flask, request, jsonify, render_template
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

app = Flask(__name__)
nlp = spacy.load('en_core_web_sm')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    text = request.form['text']
    doc = nlp(text)

    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS) and word.text.lower() not in punctuation:
            if word.text.lower() not in word_frequencies.keys():
                word_frequencies[word.text.lower()] = 1
            else:
                word_frequencies[word.text.lower()] += 1

    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency

    sentence_scores = {}
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]

    from heapq import nlargest
    select_length = int(len(sentence_scores) * 0.3)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)

