"""
Career-Path Chatbot (Holland-style, original 50-question version)
-----------------------------------------------------------------
50 original questions inspired by RIASEC traits.
"""

from flask import Flask, request, jsonify, render_template_string, session
import json

app = Flask(__name__)
app.secret_key = "change-this-secret"

# ----------------------------------------------------
# 1. RIASEC scoring buckets
# ----------------------------------------------------
RIASEC = {k: 0 for k in "RIASCE"}

# ----------------------------------------------------
# 2. 50 original questions
# ----------------------------------------------------
QUESTIONS = [
    ("q1", "Do you enjoy fixing or building things with your hands?", ["R"]),
    ("q2", "Do you like investigating why things happen?", ["I"]),
    ("q3", "Do you enjoy painting, drawing, or other creative activities?", ["A"]),
    ("q4", "Do you find satisfaction in helping or teaching others?", ["S"]),
    ("q5", "Do you like leading projects or persuading people?", ["E"]),
    ("q6", "Do you enjoy making lists, organizing, or planning tasks?", ["C"]),
    ("q7", "Would you rather work outdoors or in a workshop?", ["R"]),
    ("q8", "Do you enjoy solving puzzles or analyzing data?", ["I"]),
    ("q9", "Do you often express yourself through music or writing?", ["A"]),
    ("q10", "Do you feel fulfilled when helping someone improve?", ["S"]),
    ("q11", "Do you enjoy negotiating or pitching ideas?", ["E"]),
    ("q12", "Do you prefer structured schedules over spontaneous activities?", ["C"]),
    ("q13", "Do you like working with tools or machinery?", ["R"]),
    ("q14", "Do you enjoy conducting experiments or research?", ["I"]),
    ("q15", "Do you enjoy designing or decorating spaces?", ["A"]),
    ("q16", "Do you volunteer to assist people in need?", ["S"]),
    ("q17", "Do you take initiative in leading groups?", ["E"]),
    ("q18", "Do you enjoy keeping records or tracking details?", ["C"]),
    ("q19", "Do you like hands-on hobbies like gardening or carpentry?", ["R"]),
    ("q20", "Do you like asking questions to understand how things work?", ["I"]),
    ("q21", "Do you enjoy storytelling or performing arts?", ["A"]),
    ("q22", "Do you enjoy mentoring or coaching others?", ["S"]),
    ("q23", "Do you like organizing events or motivating people?", ["E"]),
    ("q24", "Do you enjoy following rules and organizing tasks?", ["C"]),
    ("q25", "Do you prefer building or repairing objects over thinking abstractly?", ["R"]),
    ("q26", "Do you enjoy reading, researching, or solving logical problems?", ["I"]),
    ("q27", "Do you enjoy photography, crafts, or fashion?", ["A"]),
    ("q28", "Do you like working in teams to support others?", ["S"]),
    ("q29", "Do you enjoy persuading or selling ideas to others?", ["E"]),
    ("q30", "Do you enjoy keeping spreadsheets or planning systems?", ["C"]),
    ("q31", "Do you enjoy outdoor projects or mechanical tasks?", ["R"]),
    ("q32", "Do you like studying patterns or trends?", ["I"]),
    ("q33", "Do you enjoy creative writing or designing visual art?", ["A"]),
    ("q34", "Do you enjoy helping friends solve personal problems?", ["S"]),
    ("q35", "Do you like inspiring others or leading a team?", ["E"]),
    ("q36", "Do you enjoy maintaining order or following rules?", ["C"]),
    ("q37", "Do you enjoy assembling or constructing things?", ["R"]),
    ("q38", "Do you enjoy analyzing statistics or scientific data?", ["I"]),
    ("q39", "Do you enjoy performing, dancing, or composing music?", ["A"]),
    ("q40", "Do you enjoy guiding or advising others?", ["S"]),
    ("q41", "Do you like starting new initiatives or business projects?", ["E"]),
    ("q42", "Do you enjoy documenting and organizing information?", ["C"]),
    ("q43", "Do you prefer building physical projects over planning?", ["R"]),
    ("q44", "Do you enjoy solving complex questions and research challenges?", ["I"]),
    ("q45", "Do you enjoy creating art or exploring imaginative ideas?", ["A"]),
    ("q46", "Do you enjoy teaching, mentoring, or counseling?", ["S"]),
    ("q47", "Do you like inspiring others or leading a team?", ["E"]),
    ("q48", "Do you enjoy following procedures or schedules carefully?", ["C"]),
    ("q49", "Do you enjoy experimenting or inventing new solutions?", ["I","R"]),
    ("q50", "Do you enjoy combining creativity with helping others?", ["A","S"])
]

# ----------------------------------------------------
# Keywords mapping to RIASEC traits
# ----------------------------------------------------
KEYWORDS = {
    "R": ["hands-on", "build", "repair", "tools", "physical", "practical", "outdoors"],
    "I": ["analyze", "research", "logic", "math", "experiment", "think", "study", "question"],
    "A": ["art", "draw", "creative", "design", "music", "imagine", "express", "perform"],
    "S": ["help", "support", "teach", "care", "mentor", "community", "listen", "guide"],
    "E": ["lead", "persuade", "motivate", "business", "sell", "organize people", "inspire"],
    "C": ["plan", "organize", "detail", "record", "structure", "systems", "schedule", "rules"]
}

# Careers mapped loosely to RIASEC profiles
CAREERS = {
    "R": ["Technician", "Mechanic", "Engineer (Hands-on)"],
    "I": ["Data Scientist", "Researcher", "Software Developer"],
    "A": ["Graphic Designer", "Musician", "Writer", "Animator"],
    "S": ["Teacher", "Counselor", "Nurse", "Social Worker"],
    "E": ["Entrepreneur", "Sales Manager", "Project Leader"],
    "C": ["Accountant", "Administrator", "Operations Coordinator"]
}

# ----------------------------------------------------
# Helper: score free text answer
# ----------------------------------------------------
def score_answer(text, traits):
    text = text.lower()
    for t in traits:
        for kw in KEYWORDS.get(t, []):
            if kw in text:
                RIASEC[t] += 1

# ----------------------------------------------------
# Web UI
# ----------------------------------------------------
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Career Pathfinder</title>
<style>
body { font-family: Arial; max-width: 600px; margin: auto; padding: 20px; }
.question { font-size: 1.2em; margin-bottom: 20px; }
</style>
</head>
<body>
<h2>Career Pathfinder (RIASEC-inspired)</h2>
<div id="chat"></div>
<script>
let state = 0;
const questions = {{ questions|safe }};

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
        document.getElementById('chat').innerHTML += `<h3>Your Results:</h3><pre>${data.results}</pre>`;
    } else {
        state++;
        ask(state);
    }
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
</script>
<input id="input" placeholder="Type your answer and hit Enter..." style="width:100%; padding:10px; margin-top:20px;">
<script>ask(0);</script>
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
        top = sorted_codes[0][0]
        recommended = CAREERS[top]
        result_text = f"Your dominant trait is: {top}\nRecommended careers: " + ", ".join(recommended)
        return jsonify({"done": True, "results": result_text})

    return jsonify({"done": False, "next": session['q_index']})

if __name__ == '__main__':
    app.run(debug=True)# ----------------------------------------------------
# Helper: score free text answer
# ----------------------------------------------------
def score_answer(text, traits):
    text = text.lower()
    for t in traits:
        for kw in KEYWORDS.get(t, []):
            if kw in text:
                RIASEC[t] += 1
    return

# ----------------------------------------------------
# Web UI
# ----------------------------------------------------
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Career Pathfinder</title>
<style>
body { font-family: Arial; max-width: 600px; margin: auto; padding: 20px; }
.question { font-size: 1.2em; margin-bottom: 20px; }
</style>
</head>
<body>
<h2>Career Pathfinder (RIASEC-inspired)</h2>
<div id="chat"></div>
<script>
let state = 0;
const questions = {{ questions|safe }};

function ask(i) {
    document.getElementById('chat').innerHTML += `<p><b>Q${i+1}:</b> ${questions[i][1]}</p>`;
}

async function sendAnswer(a) {
    const q = questions[state][0];
    let r = await fetch('/answer', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({question: q, answer: a})
    });
    let data = await r.json();
    if (data.done) {
        document.getElementById('chat').innerHTML += `<h3>Your Results:</h3><pre>${data.results}</pre>`;
    } else {
        state++;
        ask(state);
    }
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
</script>
<input id="input" placeholder="Type your answer and hit Enter..." style="width:100%; padding:10px; margin-top:20px;">
<script>ask(0);</script>
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
    return render_template_string(HTML, questions=QUESTIONS)

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
        top = sorted_codes[0][0]
        recommended = CAREERS[top]
        result_text = f"Your dominant trait is: {top}\nRecommended careers: " + ", ".join(recommended)
        return jsonify({"done": True, "results": result_text})

    return jsonify({"done": False, "next": session['q_index']})

if __name__ == '__main__':
    app.run(debug=True)
