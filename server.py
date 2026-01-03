"""
Flask server for emotion detection application.
This module defines routes to render the homepage
and to analyze emotions from user-provided text.
"""
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector
app = Flask(__name__)
@app.route('/')
def home():
    """
    Render the home page of the emotion detection app.

    Returns:
        HTML template for the homepage.
    """
    return render_template('index.html')
@app.route('/emotionDetector', methods=['GET', 'POST'])
def emotion_detector_route():
    """
    Analyze the emotion of the given text input.
    Accepts text via query parameters, form data, or JSON
    and returns emotion scores with the dominant emotion.
    Returns:
        str: Emotion analysis result or error message.
    """
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
