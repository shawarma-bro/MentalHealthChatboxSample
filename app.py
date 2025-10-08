from flask import Flask, render_template, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip().lower()  # Prevent errors if message is missing

        # **Step 1: Avoid Echoing Short Inputs**
        if len(user_message) < 3:
            return jsonify({'response': "Could you tell me more about how you're feeling?", 'mood': "neutral"})

        # **Step 2: Predefined Mental Health Responses**
        responses = {
            "stressed": "I'm sorry you're feeling stressed. Deep breaths can help. 💙",
            "anxious": "Anxiety is tough. Try grounding exercises like the 5-4-3-2-1 technique.",
            "sad": "I'm here to listen. Your feelings matter. You're not alone. ❤️",
            "happy": "That's amazing! Keep doing what makes you feel good. 😊",
            "lonely": "Maybe reaching out to a friend could help? I'm here for you."
        }

        # **Step 3: Check for Predefined Responses**
        for keyword, response in responses.items():
            if keyword in user_message:
                return jsonify({'response': response, 'mood': "neutral"})

        # **Step 4: Sentiment Analysis for Mood Adaptation**
        sentiment_score = analyzer.polarity_scores(user_message)['compound']

        if sentiment_score >= 0.05:
            mood = "positive"
            ai_response = "That's great! Keep up the positive energy. 🌟"
        elif sentiment_score <= -0.05:
            mood = "negative"
            ai_response = "I'm here for you. You're stronger than you think. 💙"
        else:
            mood = "neutral"
            ai_response = "I hear you. Want to talk more about it?"

        return jsonify({'response': ai_response, 'mood': mood})

    except Exception as e:
        print("Error:", str(e))  # Logs error for debugging
        return jsonify({'response': "Something went wrong. Try again!", 'mood': "neutral"}), 500

if __name__ == '__main__':
    app.run(debug=True)
