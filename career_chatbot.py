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
    'R': [
        ("Engineer", "Designs and builds systems and structures. They apply scientific principles to create innovative solutions that improve efficiency and safety in everyday life."),
        ("Mechanic", "Repairs and maintains machinery and vehicles. They diagnose problems and use tools to keep equipment running smoothly and safely."),
        ("Electrician", "Installs and maintains electrical systems. They ensure buildings and devices have safe and functional wiring and power sources."),
        ("Carpenter", "Builds and repairs wooden structures. They use tools to cut, shape, and install materials with precision and care."),
        ("Pilot", "Flies aircraft safely between destinations. They must understand navigation, weather patterns, and aviation systems.")
    ],
    'I': [
        ("Scientist", "Conducts experiments to discover how things work. They solve complex problems and contribute new knowledge to their field."),
        ("Doctor", "Diagnoses and treats illnesses. They work to improve and maintain people’s physical health through medicine and compassion."),
        ("Data Analyst", "Interprets data to find trends and insights. They help companies make better decisions through evidence and logic."),
        ("Pharmacist", "Dispenses medications and advises on proper use. They ensure patients get the correct prescriptions and understand their treatments."),
        ("Lab Technician", "Performs tests and collects data in scientific labs. They assist researchers and doctors in understanding results.")
    ],
    'A': [
        ("Graphic Designer", "Creates visual content to communicate ideas. They use design software to produce graphics for websites, ads, and more."),
        ("Writer", "Writes content for different formats like books, articles, and websites. They communicate ideas creatively and clearly."),
        ("Musician", "Plays or composes music for audiences. They may perform live, record albums, or score music for media."),
        ("Actor", "Performs roles in movies, TV, or theater. They bring characters to life and entertain through storytelling."),
        ("Animator", "Creates motion graphics and visual effects. They work in film, gaming, and digital content creation.")
    ],
    'S': [
        ("Teacher", "Educates students in academic or life skills. They help learners grow and reach their potential."),
        ("Counselor", "Guides people through personal or emotional difficulties. They offer advice, support, and strategies for well-being."),
        ("Nurse", "Cares for the sick or injured. They administer treatment, comfort patients, and coordinate with doctors."),
        ("Social Worker", "Supports vulnerable individuals and families. They help people find resources and cope with challenges."),
        ("Therapist", "Provides mental health support. They work with clients to improve emotional and psychological wellness.")
    ],
    'E': [
        ("Entrepreneur", "Starts and runs businesses. They take risks and innovate to bring products or services to life."),
        ("Manager", "Leads teams to reach goals. They coordinate projects, oversee staff, and solve workplace challenges."),
        ("Lawyer", "Advises and represents clients in legal matters. They argue cases in court and interpret laws."),
        ("Salesperson", "Sells products or services and builds customer relationships. They understand client needs and offer suitable solutions."),
        ("Marketing Specialist", "Promotes brands through campaigns. They use creativity and data to connect with customers.")
    ],
    'C': [
        ("Accountant", "Tracks finances and prepares reports. They ensure accuracy in budgets, taxes, and financial decisions."),
        ("Administrator", "Manages daily operations of offices or institutions. They keep things organized and running smoothly."),
        ("Data Entry Clerk", "Inputs and maintains accurate data in systems. They ensure records are clean and up to date."),
        ("Bank Clerk", "Handles customer transactions at banks. They assist with deposits, withdrawals, and inquiries."),
        ("Auditor", "Checks financial records for errors or fraud. They help businesses stay compliant and transparent.")
    ]
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
        top_careers = []
        for code, _ in sorted_scores:
            top_careers.extend(holland_types[code])
            if len(top_careers) >= 5:
                break

        return render_template_string(RESULT_TEMPLATE, careers=top_careers[:5])

    return render_template_string(QUESTION_TEMPLATE, questions=shuffled_questions)

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
    <p>Rate each statement from 1 (Strongly Disagree) to 5 (Strongly Agree):</p>
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
    ol { margin-left: 20px; }
    li { margin-bottom: 15px; }
  </style>
</head>
<body>
  <h1>Your Most Likely Career Matches</h1>
  <div class="result-box">
    <ol>
      {% for career, desc in careers %}
        <li><strong>{{ career }}</strong>: {{ desc }}</li>
      {% endfor %}
    </ol>
  </div>
  <a href="/">Take the test again</a>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=False)
