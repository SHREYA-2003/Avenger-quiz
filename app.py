import secrets
from flask import Flask, render_template, request, session, redirect

app = Flask(__name__, template_folder='template')
app.secret_key = secrets.token_hex(16)
im = 0
cp = 0
hl = 0
th = 0

questions = [
    {
        'question': 'Which color do you prefer?',
        'choices': ['Red', 'Blue', 'Green', 'Yellow'],
        'answer_scores': {
            'Red': lambda: im + 1,
            'Blue': lambda: cp + 1,
            'Green': lambda: hl + 1,
            'Yellow': lambda: th + 1
        }
    },
    {
        'question': 'What is your favorite superpower?',
        'choices': ['Super strength', 'Flight', 'Telepathy', 'Invisibility'],
        'answer_scores': {
            'Super strength': lambda: hl + 1,
            'Flight': lambda: im + 1,
            'Telepathy': lambda: cp + 1,
            'Invisibility': lambda: th + 1
        }
    },
    {
        'question': 'What is your preferred method of problem-solving?',
        'choices': ['Analyzing data and strategizing', 'Using my strength and physical abilities', 'Utilizing my intelligence and technology', 'Trusting my instincts and improvising'],
        'answer_scores': {
            'Using my strength and physical abilities': lambda: hl + 1,
            'Utilizing my intelligence and technology': lambda: im + 1,
            'Analyzing data and strategizing': lambda: cp + 1,
            'Trusting my instincts and improvising': lambda: th + 1
        }
    },
    {
        'question': 'How would you describe your leadership style?',
        'choices': ['Assertive and confident', 'Inspiring and noble', 'Calculating and tactical', 'Adaptive and flexible'],
        'answer_scores': {
            'Adaptive and flexible': lambda: hl + 1,
            'Calculating and tactical': lambda: im + 1,
            'Assertive and confident': lambda: cp + 1,
            'Inspiring and noble': lambda: th + 1
        }
    },
    {
        'question': 'What motivates you to fight for justice?',
        'choices': ['Protecting the innocent and upholding truth', 'Seeking redemption and personal growth', 'Advancing science and technological advancements', 'Embracing chaos and unpredictability'],
        'answer_scores': {
            'Seeking redemption and personal growth': lambda: hl + 1,
            'Advancing science and technological advancements': lambda: im + 1,
            'Embracing chaos and unpredictability': lambda: cp + 1,
            'Protecting the innocent and upholding truth': lambda: th + 1
        }
    },
]

avengers_scores = {
    'Iron Man': 0,
    'Thor': 0,
    'Hulk': 0,
    'Captain America': 0,
}


@app.route('/', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        session['answers'] = request.form
        return redirect('/result')
    return render_template('quiz.html', questions=questions)


@app.route('/result')
def result():
    answers = session.get('answers', {})
    for question in questions:
        selected_choice = answers.get(question['question'])
        if selected_choice and selected_choice in question['answer_scores']:
            avenger_scores = question['answer_scores']
            for avenger in avengers_scores:
                if avenger in avenger_scores:
                    avengers_scores[avenger] += avenger_scores[selected_choice]()

    max_score = max(avengers_scores.values())
    max_avengers = [avenger for avenger, score in avengers_scores.items() if score == max_score]

    # Clear the session to reset the quiz
    session.pop('answers', None)

    return render_template('result.html', avengers=max_avengers)


if __name__ == '__main__':
    app.run(debug=True)
