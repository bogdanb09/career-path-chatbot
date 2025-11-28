from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

questions = [
    ("I enjoy working with tools and machinery.", 'R'),
    ("I like solving abstract problems.", 'I'),
    ("I enjoy expressing myself through art, music, or writing.", 'A'),
    ("I feel fulfilled when helping others learn or improve.", 'S'),
    ("I am confident taking charge in group situations.", 'E'),
    ("I enjoy organizing data and keeping records.", 'C'),
    ("I prefer hands-on work over desk jobs.", 'R'),
    ("I am curious about how things work.", 'I'),
    ("I value originality and creativity.", 'A'),
    ("I like volunteering and contributing to my community.", 'S'),
    ("I enjoy debating or persuading others.", 'E'),
    ("I feel satisfied when everything is in order.", 'C'),
    ("I would like a job involving outdoor activity.", 'R'),
    ("I enjoy doing scientific experiments.", 'I'),
    ("I often come up with unique solutions.", 'A'),
    ("I am good at resolving conflicts between people.", 'S'),
    ("I would like to run my own business someday.", 'E'),
    ("I like making schedules and to-do lists.", 'C'),
    ("I find satisfaction in fixing broken things.", 'R'),
    ("I enjoy exploring philosophical questions.", 'I'),
    ("I like to design posters, graphics, or websites.", 'A'),
    ("I like to tutor others in subjects I understand.", 'S'),
    ("I take initiative to lead group activities.", 'E'),
    ("I enjoy keeping track of numbers and statistics.", 'C'),
    ("I would enjoy working on a construction site.", 'R'),
    ("I enjoy puzzles and logical games.", 'I'),
    ("I often doodle or sketch in my free time.", 'A'),
    ("I feel empathy for people who are struggling.", 'S'),
    ("I enjoy organizing events or campaigns.", 'E'),
    ("I like inputting and analyzing data in spreadsheets.", 'C'),
    ("I would like a job that requires physical strength or endurance.", 'R'),
    ("I read scientific or technical articles for fun.", 'I'),
    ("I enjoy coming up with stories or poems.", 'A'),
    ("I find joy in helping people with their emotional needs.", 'S'),
    ("I like taking risks and trying new ventures.", 'E'),
    ("I enjoy filing, sorting, and maintaining order.", 'C'),
    ("I like repairing cars, bikes, or gadgets.", 'R'),
    ("I’m interested in research and discovery.", 'I'),
    ("I enjoy improvising or acting.", 'A'),
    ("I prefer collaborative group work over solo tasks.", 'S'),
    ("I like convincing people to support an idea or product.", 'E'),
    ("I prefer clear instructions and well-defined tasks.", 'C'),
    ("I would enjoy operating heavy equipment.", 'R'),
    ("I enjoy analyzing theories and data.", 'I'),
    ("I seek freedom in how I work or create.", 'A'),
    ("People often turn to me for advice.", 'S'),
    ("I want to climb the ladder in my career.", 'E'),
    ("I prefer routines and dislike surprises at work.", 'C'),
    ("I would enjoy a hands-on technical trade.", 'R'),
    ("I enjoy forming hypotheses and testing them.", 'I')
]

holland_types = {
    'R': ("Realistic (Doers)", [
        ("Engineer", "Designs and builds systems, solving real-world problems using math and science."),
        ("Mechanic", "Maintains and repairs vehicles or machinery with technical precision."),
        ("Electrician", "Installs and maintains electrical systems safely and efficiently."),
        ("Carpenter", "Builds and repairs wooden structures for homes and businesses."),
        ("Pilot", "Flies aircraft to transport passengers or cargo across distances.")
    ]),
    'I': ("Investigative (Thinkers)", [
        ("Scientist", "Conducts experiments to understand natural phenomena and solve problems."),
        ("Doctor", "Diagnoses illnesses and provides treatment to improve health."),
        ("Data Analyst", "Interprets data to guide decision-making in various industries."),
        ("Pharmacist", "Prepares and dispenses medication with guidance for safe use."),
        ("Lab Technician", "Assists in scientific research and medical testing.")
    ]),
    'A': ("Artistic (Creators)", [
        ("Graphic Designer", "Creates visuals for marketing, branding, and communication."),
        ("Writer", "Produces content ranging from novels to technical manuals."),
        ("Musician", "Composes, performs, or records musical works."),
        ("Actor", "Performs roles in theater, TV, or film productions."),
        ("Animator", "Creates animations for movies, games, and digital content.")
    ]),
    'S': ("Social (Helpers)", [
        ("Teacher", "Educates and mentors students in schools or training programs."),
        ("Counselor", "Helps individuals navigate personal and emotional challenges."),
        ("Nurse", "Provides patient care and assists with medical procedures."),
        ("Social Worker", "Supports families and communities with essential services."),
        ("Therapist", "Offers mental health support and coping strategies.")
    ]),
    'E': ("Enterprising (Persuaders)", [
        ("Entrepreneur", "Starts and runs businesses by taking strategic risks."),
        ("Manager", "Leads teams and manages business operations."),
        ("Lawyer", "Advises clients and represents them in legal matters."),
        ("Salesperson", "Promotes and sells products or services."),
        ("Marketing Specialist", "Creates campaigns to attract and retain customers.")
    ]),
    'C': ("Conventional (Organizers)", [
        ("Accountant", "Manages financial records and ensures compliance."),
        ("Administrator", "Oversees administrative operations in offices or institutions."),
        ("Data Entry Clerk", "Inputs and organizes data with precision."),
        ("Bank Clerk", "Handles transactions and customer service in banks."),
        ("Auditor", "Examines records for accuracy and legal compliance.")
    ])
}

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_questions = random.sample(questions, 50)
    if request.method == 'POST':
        scores = {'R': 0, 'I': 0, 'A': 0, 'S': 0, 'E': 0, 'C': 0}
        for i in range(len(selected_questions)):
            score = request.form.get(f'q{i}')
            if score and score.isdigit():
                _, category = selected_questions[i]
                scores[category] += int(score)

        top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
        results = [(holland_types[k][0], holland_types[k][1]) for k, _ in top]
        return render_template_string(RESULT_TEMPLATE, results=results)

    return render_template_string(QUESTION_TEMPLATE, questions=selected_questions)

QUESTION_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>Career Guidance</title>
  <style>
    body { font-family: sans-serif; padding: 2em; background: #f4f4f4; }
    form { background: white; padding: 2em; border-radius: 10px; max-width: 800px; margin: auto; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    h1 { text-align: center; }
    .question { margin-bottom: 1em; }
    input[type='submit'] { padding: 0.7em 2em; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
  </style>
</head>
<body>
  <form method="post">
    <h1>Career Guidance Chatbot</h1>
    {% for i, (question, _) in enumerate(questions) %}
      <div class="question">
        <label><strong>Q{{ i+1 }}:</strong> {{ question }}</label><br>
        <input type="number" name="q{{ i }}" min="1" max="5" required>
      </div>
    {% endfor %}
    <input type="submit" value="Get My Career Path">
  </form>
</body>
</html>
"""

RESULT_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>Your Career Path</title>
  <style>
    body { font-family: sans-serif; padding: 2em; background: #eef2f7; }
    .result-box { background: white; padding: 2em; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    h2 { color: #333; }
    ul { margin-top: 10px; }
    li { margin-bottom: 10px; }
    a { display: block; margin-top: 30px; text-align: center; color: #007bff; text-decoration: none; }
  </style>
</head>
<body>
  <h1>Your Career Path Results</h1>
  {% for title, careers in results %}
    <div class="result-box">
      <h2>{{ title }}</h2>
      <ul>
        {% for career, desc in careers %}
          <li><strong>{{ career }}</strong>: {{ desc }}</li>
        {% endfor %}
      </ul>
    </div>
  {% endfor %}
  <a href="/">Take the test again</a>
</body>
</html>
"""

# Do not include app.run() when deploying to Render
# if __name__ == '__main__':
#     app.run(debug=False)
