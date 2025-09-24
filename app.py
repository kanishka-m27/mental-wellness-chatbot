from flask import Flask, render_template, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
app = Flask(__name__)

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()
def get_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        data = response.json()
        return f"{data[0]['q']} — {data[0]['a']}"
    except:
        return "Keep going, you’re doing great! 🌟"

# Custom reply function
def get_custom_reply(message, sentiment):
    message = message.lower()
    if "thank you" in message or "thanks" in message:
        return "You're welcome! 🌸 Remember, I'm always here if you want to talk."
    elif "bye" in message or "goodbye" in message or "see you" in message or "ok" in message:
        return "Take care! 💙 Wishing you peace and positivity."

    if "motivate" in message or "inspire" in message or "quote" in message or "motivation" in message:
        return get_quote() 

    # Expanded Keyword-based emotion suggestions
    responses = {
        "stress": "It sounds like you're stressed. Try a short walk, deep breathing, or journaling your thoughts.",
        "overwhelmed": "Feeling overwhelmed is normal. Take a deep breath and break tasks into smaller steps.",
        "depression": "You're not alone. Talking to someone you trust or a counselor can really help. You matter 💙",
        "anxiety": "Anxiety can be tough. Try grounding techniques like naming 5 things you see, 4 you feel, 3 you hear.",
        "social anxiety": "Deep breathing and small exposure steps can help build confidence.",
        "panic": "Panic attacks pass. Focus on slow breathing and sit somewhere calm.",
        "sad": "It’s okay to feel sad. Let it out, and do something kind for yourself.",
        "hopeless": "Even when things feel dark, there’s always light ahead. You are stronger than you think 💪",
        "lonely": "You're not alone. Reach out to a friend or do something creative.",
        "tired": "A short nap or some hydration can help. Be gentle with yourself.",
        "nervous": "It’s okay to feel nervous. Take deep breaths and remind yourself you’re doing your best.",
        "happy": "I'm glad you're happy! Spread that positivity 🌟",
        "good": "That's wonderful to hear! Keep doing what makes you feel good 😊",
        "bad": "Sorry you're feeling that way. Take a moment to rest or talk to someone you trust.",
        "angry": "Try journaling, a walk, or expressing how you feel calmly.",
        "relaxation": "Relaxation is key. Try meditation, soft music, or progressive muscle relaxation.",
        "bored": "Boredom happens. Try a hobby, a short walk, or learning something new.",
        "sleep": "A proper sleep schedule helps mental health. Consider relaxing before bed without screens.",
        "motivated": "Great! Keep up the momentum and focus on one task at a time.",
        "unmotivated": "It's okay to feel unmotivated. Start with something small and build momentum."
    }

    # Specific keyword replies
    if "deep breathing" in message or "breathing exercise" in message:
        return "Deep breathing is a relaxation technique. Inhale slowly through your nose for 4 seconds, hold for 4, exhale through your mouth for 4. Repeat for 5 minutes."
    elif "short walk" in message or "walk outside" in message:
        return "Taking a 10–15 minute walk outdoors can refresh your mind and reduce stress."
    elif "journal" in message or "writing down" in message or "journaling" in message:
        return "Journaling can help. Try writing about what you're feeling, things you're grateful for, or your goals."
    elif "meditation" in message or "meditate" in message:
        return "Meditation can calm your mind. Try sitting quietly and focusing on your breath for 5–10 minutes."
    elif "music" in message or "listen to music" in message:
        return "Listening to calming or uplifting music can improve mood and reduce stress."
    elif "talk to someone" in message or "friend" in message:
        return "Sharing your feelings with someone you trust can really help lighten the emotional load."
    elif "exercise" in message or "workout" in message:
        return "Regular physical activity helps your mental health. Even 10–15 minutes of light exercise can improve your mood."
    elif "sleep" in message or "rest" in message:
        return "Try to get a consistent sleep schedule. Rest and relaxation are very important for mental wellness."

    # Emotion keyword matching
    for keyword, response in responses.items():
        if keyword in message:
            return response

    # Emotion-based dynamic responses using VADER sentiment
    if sentiment >= 0.7:  # strong positivity
        return "You seem to be in a great mood! 😊 Keep it up!"
    elif sentiment <= -0.4:  # strong negativity
        return "I'm really sorry you're feeling this way. Would you like some breathing tips or journaling ideas?"
    elif -0.2 <= sentiment <= 0.2:  # neutral
        return "Thanks for sharing. I'm here to support you. 🤗 Would you like to talk more about it?"
    else:
        return "I hear you. Sometimes emotions can be mixed — would you like a relaxation tip?"

# Flask route to homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to get chatbot response
@app.route('/chat', methods=['POST'])
def get_bot_response():
    user_input = request.json['message']
    sentiment = analyzer.polarity_scores(user_input)['compound']  # VADER sentiment
    reply = get_custom_reply(user_input, sentiment)
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
