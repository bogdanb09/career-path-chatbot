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
        ("Engineer", "Designs and builds systems and structures. Engineers apply math and science to solve practical problems and improve technologies."),
        ("Mechanic", "Repairs and maintains machines and vehicles using tools and diagnostic equipment."),
        ("Electrician", "Installs and maintains electrical wiring and equipment safely and efficiently."),
        ("Carpenter", "Constructs and repairs building frameworks and structures from wood and other materials."),
        ("Pilot", "Operates aircraft to transport passengers or goods safely and on schedule.")
    ]),
    'I': ("Investigative (Thinkers)", [
        ("Scientist", "Conducts experiments and research to increase scientific knowledge in various fields."),
        ("Doctor", "Diagnoses and treats illnesses while promoting overall health and wellness."),
        ("Data Analyst", "Uses statistical tools to interpret and visualize data, helping businesses make decisions."),
        ("Pharmacist", "Prepares and dispenses medications, advising patients on proper usage and effects."),
        ("Lab Technician", "Performs technical laboratory tests to assist in the diagnosis and treatment of diseases.")
    ]),
    'A': ("Artistic (Creators)", [
        ("Graphic Designer", "Designs visual content for websites, ads, and branding using digital tools."),
        ("Writer", "Creates written content for books, websites, media, or scripts."),
        ("Musician", "Performs, composes, or records music for various audiences."),
        ("Actor", "Portrays characters in theater, film, or television productions."),
        ("Animator", "Creates animations and special effects for films, video games, or commercials.")
    ]),
    'S': ("Social (Helpers)", [
        ("Teacher", "Educates and mentors students in academic or practical subjects."),
        ("Counselor", "Provides advice and guidance to help people deal with personal or academic challenges."),
        ("Nurse", "Cares for patients by administering treatments and monitoring health."),
        ("Social Worker", "Supports individuals and families by connecting them to needed services and support."),
        ("Therapist", "Helps people manage emotional or psychological challenges through counseling.")
    ]),
    'E': ("Enterprising (Persuaders)", [
        ("Entrepreneur", "Builds and runs businesses, taking on financial and strategic risks."),
        ("Manager", "Supervises teams, resources, and operations in organizations or projects."),
        ("Lawyer", "Provides legal advice and represents clients in courts and negotiations."),
        ("Salesperson", "Sells products or services and builds client relationships."),
        ("Marketing Specialist", "Creates and implements strategies to promote and sell products or brands.")
    ]),
    'C': ("Conventional (Organizers)", [
        ("Accountant", "Manages financial records, budgets, and tax documents accurately."),
        ("Administrator", "Oversees day-to-day administrative operations in an office or department."),
        ("Data Entry Clerk", "Inputs data into computer systems efficiently and accurately."),
        ("Bank Clerk", "Handles customer transactions and maintains financial records in banks."),
        ("Auditor", "Examines financial statements to ensure accuracy and compliance with laws.")
    ])
}

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_questions = random.sample(questions, 50)
    if request.method == 'POST':
        scores = {'R': 0, 'I': 0, 'A': 0, 'S': 0, 'E': 0, 'C': 0}
        for i in range(50):
            answer = request.form.get(f'q{i}')
            if answer and answer.isdigit():
                question, category = selected_questions[i]
                scores[category] += int(answer)

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_3 = [code for code, score in sorted_scores[:3]]
        results = [(holland_types[code][0], holland_types[code][1]) for code in top_3]

        return render_template_string(RESULT_TEMPLATE, results=results)

    return render_template_string(QUESTION_TEMPLATE, questions=selected_questions)

QUESTION_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>Career Guidance Chatbot</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f9f9f9; padding: 20px; }
    form { background: white; padding: 20px; border-radius: 10px; max-width: 700px; margin: auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    h1 { text-align: center; }
    input[type='submit'] { margin-top: 20px; background: #007BFF; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
  </style>
</head>
<body>
  <form method="post">
    <h1>Career Guidance Chatbot</h1>
    <p>Rate how much you agree with each of the following statements:</p>
    {% for i in range(questions|length) %}
      <p><strong>Q{{ i+1 }}:</strong> {{ questions[i][0] }}<br>
      <input type="number" name="q{{ i }}" min="1" max="5" required></p>
    {% endfor %}
    <input type="submit" value="Get Career Suggestions">
  </form>
</body>
</html>
"""

RESULT_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>Career Results</title>
  <style>
    body { font-family: Arial, sans-serif; background: #eef2f7; padding: 20px; }
    .result-box { background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    h2 { color: #333; }
    ul { margin-left: 20px; }
    li { margin-bottom: 10px; }
  </style>
</head>
<body>
  <h1>Your Career Path Suggestions</h1>
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

if __name__ == '__main__':
    app.run(debug=False)
