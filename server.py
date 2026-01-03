# server.py

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/emotionDetector', methods=['GET', 'POST'])
def emotionDetector():
    # Safely get JSON (prevents 415 error)
    json_data = request.get_json(silent=True)

    # Get input text
    text = (
        request.args.get('textToAnalyze')
        or request.form.get('statement')
        or (json_data and json_data.get('statement'))
    )

    # Call emotion detector
    result = emotion_detector(text)

    # Handle invalid / blank input
    if result.get("dominant_emotion") is None:
        return "Invalid text! Please try again!", 200

    # Format response
    response_text = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )

    return response_text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
