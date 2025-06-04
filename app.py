
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sagesse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hobbies = db.Column(db.String(200))
    character = db.Column(db.String(200))
    flaws = db.Column(db.String(200))
    happy_triggers = db.Column(db.String(200))
    sad_triggers = db.Column(db.String(200))

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.json
    new_user = User(
        username=data['username'],
        hobbies=data.get('hobbies', ''),
        character=data.get('character', ''),
        flaws=data.get('flaws', ''),
        happy_triggers=data.get('happy_triggers', ''),
        sad_triggers=data.get('sad_triggers', '')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Account created successfully'}), 201

@app.route('/advice/<username>', methods=['GET'])
def get_advice(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    advice = {}

    # Work-life balance
    if 'workaholic' in (user.character or '').lower():
        advice['work_life_balance'] = 'Try to set strict boundaries between work and personal time to avoid burnout.'
    else:
        advice['work_life_balance'] = 'Maintain a healthy balance by scheduling regular breaks and leisure activities.'

    # Stress management
    if 'anxious' in (user.flaws or '').lower() or 'stress' in (user.sad_triggers or '').lower():
        advice['stress_management'] = 'Practice mindfulness and deep breathing exercises to manage stress effectively.'
    else:
        advice['stress_management'] = 'Keep a positive mindset and engage in regular physical activity.'

    # Social interactions
    if 'introvert' in (user.character or '').lower():
        advice['social_interactions'] = 'Focus on quality over quantity in relationships and take time to recharge.'
    else:
        advice['social_interactions'] = 'Engage actively with colleagues and participate in team activities.'

    return jsonify(advice)

@app.route('/sagesse_bot', methods=['POST'])
def sagesse_bot():
    data = request.json
    user_message = data.get('message', '').lower()

    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't programmers like nature? It has too many bugs."
    ]

    encouragements = [
        "Keep going, you're doing great!",
        "Every day is a new opportunity to grow.",
        "Believe in yourself and all that you are."
    ]

    advice = [
        "Take deep breaths when you feel stressed.",
        "Remember to take breaks and stay hydrated.",
        "Try to maintain a positive mindset."
    ]

    if 'joke' in user_message:
        response = jokes
    elif 'encourage' in user_message or 'motivate' in user_message:
        response = encouragements
    elif 'advice' in user_message or 'help' in user_message:
        response = advice
    else:
        response = "I'm here to help! Ask me for a joke, encouragement, or advice."

    return jsonify({'response': response})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
