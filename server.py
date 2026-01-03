# server.py

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Flask decorator as required
@app.route('/emotionDetector', methods=['GET', 'POST'])
def emotionDetector():
    # Use request.args for GET, request.form for POST
    data = request.form.get('statement') or request.args.get('textToAnalyze') or (request.json and request.json.get('statement'))
    
    if not data:
        return "Error: No statement provided", 400
    
    # Call emotion detector
    result = emotion_detector(data)
    
    # Add dominant emotion
    if "dominant_emotion" not in result:
        dominant = max(result, key=result.get)
        result["dominant_emotion"] = dominant
    
    # Format response exactly as required
    response_text = (
        f"For the given statement, the system response is "
        f"'anger': {result.get('anger')}, "
        f"'disgust': {result.get('disgust')}, "
        f"'fear': {result.get('fear')}, "
        f"'joy': {result.get('joy')} and "
        f"'sadness': {result.get('sadness')}. "
        f"The dominant emotion is {result.get('dominant_emotion')}."
    )

    return response_text


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
