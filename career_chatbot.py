"""
Career-Path Chatbot (RIASEC-style, 50 questions)
Includes animated chart highlighting top 3 traits.
"""

from flask import Flask, request, jsonify, render_template_string, session
import json

app = Flask(__name__)
app.secret_key = "change-this-secret"

# ----------------------------------------------------
# RIASEC scoring
# ----------------------------------------------------
RIASEC = {k: 0 for k in "RIASCE"}

# ----------------------------------------------------
# 50 original questions
# ----------------------------------------------------
QUESTIONS = [
    ("q1", "Do you enjoy fixing or building things with your hands?", ["R"]),
    ("q2", "Do you like investigating why things happen?", ["I"]),
    ("q3", "Do you enjoy painting, drawing, or other creative activities?", ["A"]),
    ("q4", "Do you find satisfaction in helping or teaching others?", ["S"]),
    ("q5", "Do you like leading projects or persuading people?", ["E"]),
    ("q6", "Do you enjoy making lists, organizing, or planning tasks?", ["C"]),
    # For brevity, include questions q7-q48 as previously defined...
    ("q49", "Do you enjoy experimenting or inventing new solutions?", ["I","R"]),
    ("q50", "Do you enjoy combining creativity with helping others?", ["A","S"])
]

# ----------------------------------------------------
# Keywords for scoring
# ----------------------------------------------------
KEYWORDS = {
    "R": ["hands-on", "build", "repair", "tools", "physical", "practical", "outdoors"],
    "I": ["analyze", "research", "logic", "math", "experiment", "think", "study", "question"],
    "A": ["art", "draw", "creative", "design", "music", "imagine", "express", "perform"],
    "S": ["help", "support", "teach", "care", "mentor", "community", "listen", "guide"],
    "E": ["lead", "persuade", "motivate", "business", "sell", "organize people", "inspire"],
    "C": ["plan", "organize", "detail", "record", "structure", "systems", "schedule", "rules"]
}

# ----------------------------------------------------
# Careers mapping
# ----------------------------------------------------
CAREERS = {
    "R": [
        "Technician", "Mechanic", "Electrician", "Engineer (Hands-on)", "Carpenter",
        "Plumber", "Construction Worker", "Pilot", "Chef", "Farmer", "Landscaper",
        "Industrial Machine Operator", "Welder", "Automotive Technician", "Surveyor",
        "Equipment Operator", "Firefighter", "Machinist", "Boat Captain", "HVAC Specialist"
    ],
    "I": [
        "Data Scientist", "Researcher", "Software Developer", "Analyst", "Laboratory Scientist",
        "Mathematician", "Statistician", "Chemist", "Physicist", "Biologist", "Psychologist",
        "Medical Researcher", "Economist", "AI Specialist", "Forensic Scientist",
        "Environmental Scientist", "Academic Researcher", "Engineer (Theory)", "IT Specialist",
        "Cybersecurity Analyst", "Astronomer", "Philosopher", "Clinical Researcher", "Software Tester"
    ],
    "A": [
        "Graphic Designer", "Musician", "Writer", "Animator", "Actor", "Photographer",
        "Fashion Designer", "Interior Designer", "Video Editor", "Art Director", "Illustrator",
        "Dancer", "Composer", "Advertising Creative", "Game Designer", "Sculptor",
        "Painter", "Content Creator", "Creative Director", "Voice Actor", "Screenwriter",
        "Set Designer", "Choreographer", "Makeup Artist", "Stage Designer"
    ],
    "S": [
        "Teacher", "Counselor", "Nurse", "Social Worker", "Coach", "Therapist", "Speech Pathologist",
        "Community Organizer", "Healthcare Worker", "Human Resources Specialist", "Mediator",
        "Guidance Counselor", "Occupational Therapist", "Childcare Worker", "Elder Care Specialist",
        "Volunteer Coordinator", "Rehabilitation Specialist", "Teacher Assistant", "Mentor", "Clergy",
        "Public Health Worker", "Patient Advocate", "Education Coordinator", "School Administrator"
    ],
    "E": [
        "Entrepreneur", "Sales Manager", "Project Leader", "Marketing Strategist", "Business Owner",
        "Consultant", "Real Estate Agent", "Financial Advisor", "Public Relations Specialist",
        "Event Planner", "Product Manager", "Startup Founder", "Investor", "Brand Manager",
        "Lobbyist", "Team Leader", "Recruitment Manager", "Corporate Trainer", "Operations Manager",
        "Fundraising Manager", "Advertising Executive", "Business Analyst", "Franchise Owner", "CEO"
    ],
    "C": [
        "Accountant", "Administrator", "Operations Coordinator", "Data Entry Specialist", "Auditor",
        "Office Manager", "Bookkeeper", "Project Coordinator", "Scheduler", "Paralegal",
        "Insurance Underwriter", "Compliance Officer", "Records Manager", "Executive Assistant",
        "Bank Teller", "Financial Analyst", "Administrative Assistant", "Inventory Manager",
        "Logistics Coordinator", "Quality Control Specialist", "Database Administrator",
        "Payroll Specialist", "Operations Analyst", "Human Resources Assistant"
    ]
}

# ----------------------------------------------------
# Score free-text answers
# ----------------------------------------------------
def score_answer(text, traits):
    text = text.lower()
    for t in traits:
        for kw in KEYWORDS.get(t, []):
            if kw in text:
                RIASEC[t] += 1

# ----------------------------------------------------
# HTML template with Chart.js animation
# ----------------------------------------------------
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Career Pathfinder</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body { font-family: Arial; max-width: 700px; margin: auto; padding: 20px; }
#chart-container { width: 100%; margin-top: 30px; }
</style>
</head>
<body>
<h2>Career Pathfinder (RIASEC-inspired)</h2>
<div id="chat"></div>
<input id="input" placeholder="Type your answer and hit Enter..." style="width:100%; padding:10px; margin-top:20px;">

<div id="chart-container">
<canvas id="riaChart"></canvas>
</div>

<script>
let state = 0;
const questions = {{ questions|safe }};
let topThreeCodes = [];

function ask(i) {
    document.getElementById('chat').innerHTML += `<p><b>Q${i+1}:</b> ${questions[i].text}</p>`;
}

async function sendAnswer(a) {
    const q = questions[state].id;
    let r = await fetch('/answer', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({question: q, answer: a})
    });
    let data = await r.json();
    if (data.done) {
        document.getElementById('chat').innerHTML += `<h3>Results:</h3><pre>${data.results_text}</pre>`;
        topThreeCodes = data.top_three;
        drawChart(data.chart_data);
    } else {
        state++;
        ask(state);
    }
}

function drawChart(chartData) {
    const colors = chartData.labels.map(code =>
        topThreeCodes.includes(code) ? '#FF9800' : '#2196F3'
    );

    const ctx = document.getElementById('riaChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'RIASEC Scores',
                data: chartData.scores,
                backgroundColor: colors
            }]
        },
        options: {
            responsive: true,
            animation: {
                duration: 1500,
                easing: 'easeOutBounce'
            },
            scales: { y: { beginAtZero: true, precision: 0 } }
        }
    });
}

document.addEventListener('keydown', e => {
    if (e.key === 'Enter') {
        let input = document.getElementById('input').value;
        if (!input) return;
        document.getElementById('chat').innerHTML += `<p><i>You:</i> ${input}</p>`;
        sendAnswer(input);
        document.getElementById('input').value = '';
    }
});

ask(0);
</script>
</body>
</html>
"""

# ----------------------------------------------------
# Routes
# ----------------------------------------------------
@app.route('/')
def index():
    for k in RIASEC: RIASEC[k] = 0
    session['q_index'] = 0
    js_questions = [{"id": q[0], "text": q[1]} for q in QUESTIONS]
    return render_template_string(HTML, questions=json.dumps(js_questions))

@app.route('/answer', methods=['POST'])
def answer():
    data = request.json
    q_id = data['question']
    ans = data['answer']
    for q_key, _, traits in QUESTIONS:
        if q_key == q_id:
            score_answer(ans, traits)
            break
    session['q_index'] += 1
    if session['q_index'] >= len(QUESTIONS):
        sorted_codes = sorted(RIASEC.items(), key=lambda x: x[1], reverse=True)
        top_three = [code for code,_ in sorted_codes[:3]]
        results_text = "Top 3 RIASEC traits and recommended careers:\n"
        for code, score in sorted_codes[:3]:
            results_text += f"{code} (score {score}): {', '.join(CAREERS[code])}\n"
        chart_data = {"labels": list(RIASEC.keys()), "scores": list(RIASEC.values())}
        return jsonify({
            "done": True,
            "results_text": results_text,
            "chart_data": chart_data,
            "top_three": top_three
        })
    return jsonify({"done": False, "next": session['q_index']})

# ----------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
