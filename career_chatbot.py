from flask import Flask, request, render_template_string, send_file
import random
import io
from xhtml2pdf import pisa

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
    'R': ("Realistic (Doers)", [("Engineer", "Designs and builds systems and structures. Engineers apply math and science to solve practical problems and improve technologies. They often work in fields such as mechanical, civil, electrical, and software engineering."),
        ("Mechanic", "Repairs and maintains machines and vehicles. Mechanics use tools and technical knowledge to diagnose problems and ensure machines run smoothly and safely."),
        ("Electrician", "Installs and maintains electrical systems. Electricians read blueprints, follow regulations, and ensure power systems operate effectively."),
        ("Carpenter", "Builds and repairs structures made of wood. Carpenters work on construction sites creating frameworks, furniture, and finishing touches for homes and buildings."),
        ("Pilot", "Operates aircraft to transport passengers or goods. Pilots must be trained and licensed to navigate and control aircraft safely.")]),
    'I': ("Investigative (Thinkers)", [("Scientist", "Conducts research to discover new knowledge. Scientists often work in labs or the field, applying the scientific method to investigate questions."),
        ("Doctor", "Diagnoses and treats illnesses and injuries. Doctors work closely with patients, prescribe medications, and may perform surgeries."),
        ("Data Analyst", "Interprets data to support decision-making. They find patterns in data using statistics and software, helping businesses make evidence-based choices."),
        ("Pharmacist", "Dispenses medications and advises on their use. Pharmacists also educate patients on drug interactions and health maintenance."),
        ("Lab Technician", "Performs technical laboratory tests and procedures. They collect samples, run tests, and ensure accurate results for diagnosis or research.")]),
    'A': ("Artistic (Creators)", [("Graphic Designer", "Creates visual content to communicate messages. They design logos, advertisements, and websites using tools like Adobe Photoshop."),
        ("Writer", "Produces written content for various media. Writers may work in journalism, fiction, blogging, or technical writing."),
        ("Musician", "Composes or performs music. Musicians express ideas and emotions through sound, performing live or recording in studios."),
        ("Actor", "Portrays characters in performances. Actors interpret scripts and perform on stage, in films, or on television."),
        ("Animator", "Creates animations and visual effects. They work in film, TV, video games, and digital media using computer graphics.")]),
    'S': ("Social (Helpers)", [("Teacher", "Educates students in a variety of subjects. Teachers prepare lessons, grade assignments, and inspire learning and growth."),
        ("Counselor", "Provides guidance and support to individuals. Counselors help people navigate personal, academic, or career challenges."),
        ("Nurse", "Cares for patients and assists in treatment. Nurses monitor health, administer medication, and support recovery."),
        ("Social Worker", "Supports individuals and families in need. They advocate for clients, connect them with services, and assist in crisis situations."),
        ("Therapist", "Helps people cope with emotional challenges. Therapists provide mental health care through talk therapy and coping strategies.")]),
    'E': ("Enterprising (Persuaders)", [("Entrepreneur", "Starts and manages new business ventures. Entrepreneurs take risks to develop products or services and grow a company."),
        ("Manager", "Oversees teams and operations. Managers plan, organize, and supervise people and processes to achieve goals."),
        ("Lawyer", "Advises and represents clients in legal matters. Lawyers prepare cases, represent clients in court, and interpret laws."),
        ("Salesperson", "Sells products or services to customers. They build client relationships and persuade customers to make purchases."),
        ("Marketing Specialist", "Promotes products to target audiences. Marketers analyze markets, plan campaigns, and create branding strategies.")]),
    'C': ("Conventional (Organizers)", [("Accountant", "Manages financial records and reports. Accountants prepare budgets, file taxes, and ensure financial accuracy."),
        ("Administrator", "Handles office tasks and procedures. They organize files, manage schedules, and support office operations."),
        ("Data Entry Clerk", "Inputs and maintains digital records. This job requires accuracy, attention to detail, and basic computer skills."),
        ("Bank Clerk", "Provides banking services and transactions. They assist customers, process payments, and manage records."),
        ("Auditor", "Inspects financial records for accuracy. Auditors examine books, ensure compliance, and identify discrepancies.")])
}

@app.route('/', methods=['GET', 'POST'])
def index():
    shuffled_questions = random.sample(questions, 50)
    if request.method == 'POST':
        scores = {'R': 0, 'I': 0, 'A': 0, 'S': 0, 'E': 0, 'C': 0}
        for i in range(50):
            answer = request.form.get(f'q{i}')
            if answer and answer.isdigit():
                question, category = shuffled_questions[i]
                scores[category] += int(answer)

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_3 = [code for code, score in sorted_scores[:3]]
        results = [(holland_types[code][0], holland_types[code][1]) for code in top_3]
        return render_template_string(RESULT_TEMPLATE, results=results)

    return render_template_string(QUESTION_TEMPLATE, questions=shuffled_questions)

QUESTION_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>Career Guidance Chatbot</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2em; background: #f0f2f5; }
    form { background: white; padding: 2em; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    input[type=submit] { padding: 10px 20px; margin-top: 1em; background: #007BFF; color: white; border: none; border-radius: 5px; cursor: pointer; }
    h1 { color: #333; }
  </style>
</head>
<body>
<h1>Career Guidance Chatbot</h1>
<p>Answer the following 50 questions (1 = Strongly Disagree, 5 = Strongly Agree)</p>
<form method="post">
  {% for i, (question, category) in enumerate(questions) %}
    <p><b>Q{{ i+1 }}:</b> {{ question }}<br>
    <input type="number" name="q{{ i }}" min="1" max="5" required></p>
  {% endfor %}
  <input type="submit" value="Submit">
</form>
</body>
</html>
"""

RESULT_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>Results</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f7f9fc; padding: 2em; }
    .card { background: white; border-radius: 10px; padding: 1.5em; margin-bottom: 2em; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    h2 { color: #444; }
    ul { line-height: 1.8; }
    a.button { display: inline-block; margin-top: 1em; padding: 10px 20px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; }
  </style>
</head>
<body>
<h1>Your Career Path Suggestions</h1>
{% for title, careers in results %}
  <div class="card">
    <h2>{{ title }}</h2>
    <ul>
    {% for career, desc in careers %}
      <li><b>{{ career }}</b>: {{ desc }}</li>
    {% endfor %}
    </ul>
  </div>
{% endfor %}
<a href="/">Take the test again</a>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
<form method="post">
    {% for i, (question, category) in enumerate(questions) %}
        <p><b>Q{{ i+1 }}:</b> {{ question }}<br>
        <input type="number" name="q{{ i }}" min="1" max="5" required></p>
    {% endfor %}
    <input type="submit" value="Submit">
</form>
</body>
</html>
"""

RESULT_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Results</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f7f9fc; padding: 2em; }
        .card { background: white; border-radius: 10px; padding: 1.5em; margin-bottom: 2em; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h2 { color: #444; }
        ul { line-height: 1.8; }
        a.button { display: inline-block; margin-top: 1em; padding: 10px 20px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
<h1>Your Career Path Suggestions</h1>
{% for title, careers in results %}
    <div class="card">
        <h2>{{ title }}</h2>
        <ul>
        {% for career, desc in careers %}
            <li><b>{{ career }}</b>: {{ desc }}</li>
        {% endfor %}
        </ul>
    </div>
{% endfor %}
<form method="post" action="/download">
    <input type="hidden" name="results_html" value="{{ request.form.get('results_html', '') | safe }}">
    <a href="/" class="button">Take the test again</a>
</form>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)    if request.method == 'POST':
        scores = {'R': 0, 'I': 0, 'A': 0, 'S': 0, 'E': 0, 'C': 0}
        for i in range(50):
            answer = request.form.get(f'q{i}')
            if answer and answer.isdigit():
                question, category = shuffled_questions[i]
                scores[category] += int(answer)

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_3 = [code for code, score in sorted_scores[:3]]
        results = [(holland_types[code][0], holland_types[code][1]) for code in top_3]

        return render_template_string(RESULT_TEMPLATE, results=results)

    return render_template_string(QUESTION_TEMPLATE, questions=shuffled_questions)

QUESTION_TEMPLATE = """
<!doctype html>
<title>Career Guidance Chatbot</title>
<h1>Career Guidance Chatbot</h1>
<p>Answer the following 50 questions (1 = Strongly Disagree, 5 = Strongly Agree)</p>
<form method="post">
    {% for i, (question, category) in enumerate(questions) %}
        <p><b>Q{{ i+1 }}:</b> {{ question }}<br>
        <input type="number" name="q{{ i }}" min="1" max="5" required></p>
    {% endfor %}
    <input type="submit" value="Submit">
</form>
"""

RESULT_TEMPLATE = """
<!doctype html>
<title>Results</title>
<h1>Your Career Path Suggestions</h1>
{% for title, careers in results %}
    <h2>{{ title }}</h2>
    <ul>
    {% for career, desc in careers %}
        <li><b>{{ career }}</b>: {{ desc }}</li>
    {% endfor %}
    </ul>
{% endfor %}
<a href="/">Take the test again</a>
"""

if __name__ == '__main__':
    app.run(debug=True)
                ("Pharmacist", "Dispenses medications and advises on their use."),
                ("Lab Technician", "Performs technical laboratory tests and procedures.")
            ]
        ),
        'A': (
            "Artistic (Creators)",
            [
                ("Graphic Designer", "Creates visual content to communicate messages."),
                ("Writer", "Produces written content for various media."),
                ("Musician", "Composes or performs music."),
                ("Actor", "Portrays characters in performances."),
                ("Animator", "Creates animations and visual effects.")
            ]
        ),
        'S': (
            "Social (Helpers)",
            [
                ("Teacher", "Educates students in a variety of subjects."),
                ("Counselor", "Provides guidance and support to individuals."),
                ("Nurse", "Cares for patients and assists in treatment."),
                ("Social Worker", "Supports individuals and families in need."),
                ("Therapist", "Helps people cope with emotional challenges.")
            ]
        ),
        'E': (
            "Enterprising (Persuaders)",
            [
                ("Entrepreneur", "Starts and manages new business ventures."),
                ("Manager", "Oversees teams and operations."),
                ("Lawyer", "Advises and represents clients in legal matters."),
                ("Salesperson", "Sells products or services to customers."),
                ("Marketing Specialist", "Promotes products to target audiences.")
            ]
        ),
        'C': (
            "Conventional (Organizers)",
            [
                ("Accountant", "Manages financial records and reports."),
                ("Administrator", "Handles office tasks and procedures."),
                ("Data Entry Clerk", "Inputs and maintains digital records."),
                ("Bank Clerk", "Provides banking services and transactions."),
                ("Auditor", "Inspects financial records for accuracy.")
            ]
        )
    }

    print("Your top personality traits and career suggestions:\n")
    for code in top_3:
        title, careers = holland_types[code]
        print(f"- {title}:")
        for career, description in careers:
            print(f"   * {career} - {description}")
        print()

if __name__ == "__main__":
    scores = ask_questions()
    suggest_careers(scores)
