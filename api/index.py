from flask import Flask, request, jsonify
from fuzzywuzzy import process
import spacy

app = Flask(__name__)
nlp_zh = spacy.load('zh_core_web_trf')

@app.route('/correct_sentence', methods=['POST'])
def correct_sentence():
    data = request.get_json()

    input_str = data.get('input_str')
    # base_array = data.get('base_array')
    base_array = ["王小明", "張小虎", "貓咪", "貓鼠", "股份", "有限", "公司"]


    if not input_str or not base_array:
        return jsonify({'error': 'Missing input_str or base_array'}), 400

    doc = nlp_zh(input_str)

    corrected_sentence = []
    for token in doc:
        closest_match = process.extractOne(token.text, base_array)
        if closest_match:
            corrected_sentence.append(closest_match[0])

    corrected_str = ''.join(corrected_sentence)

    return jsonify({'original': input_str, 'corrected': corrected_str})

if __name__ == '__main__':
    app.run(debug=True)