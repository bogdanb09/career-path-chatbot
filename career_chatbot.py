from flask import Flask, request, jsonify, render_template_string
import json

app = Flask(__name__)

RIASEC = {k: 0 for k in "RIASCE"}

# 50 questions with static options
QUESTIONS = []
for i in range(50):
    QUESTIONS.append({
        "id": f"q{i+1}",
        "text": f"Question {i+1}: Choose the activity that appeals most to you:",
        "options": [
            {"text": "Hands-on or practical work", "trait": "R"},
            {"text": "Analyzing or researching information", "trait": "I"},
            {"text": "Creative or artistic expression", "trait": "A"},
            {"text": "Helping or teaching others", "trait": "S"}
        ]
    })

CAREERS = {
    "R": ("Engineer", "Designs and builds machines, structures, or systems using science and math."),
    "I": ("Data Scientist", "Analyzes complex data to help companies make decisions."),
    "A": ("Graphic Designer", "Creates visual content for print, digital media, and branding."),
    "S": ("Teacher", "Educates students, guiding their learning and personal growth."),
    "E": ("Entrepreneur", "Starts and manages businesses, taking financial risks for profit."),
    "C": ("Accountant", "Manages financial records, ensures accuracy, and prepares reports.")
}

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Career Pathfinder</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body { font-family: Arial; max-width:700px; margin:auto; padding:20px; }
button { padding:10px 20px; margin:5px; }
#chart-container { margin-top:30px; width:100%; }
</style>
</head>
<body>
<h2>Career Pathfinder (RIASEC)</h2>
<div id="chat"></div>
<div id="chart-container">
<canvas id="riaChart"></canvas>
</div>

<script>
let state = 0;
const questions = {{ questions|safe }};
let scores = {R:0,I:0,A:0,S:0,E:0,C:0};

function ask(i){
    let q = questions[i];
    let html = `<p><b>Q${i+1}:</b> ${q.text}</p>`;
    q.options.forEach(opt=>{
        html += `<button onclick="answer('${opt.trait}')">${opt.text}</button><br>`;
    });
    document.getElementById('chat').innerHTML = html;
}

async function answer(trait){
    scores[trait] += 1;
    let resp = await fetch('/answer',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({trait: trait, state: state})
    });
    let data = await resp.json();
    if(data.done){
        document.getElementById('chat').innerHTML = `<h3>Your Profession:</h3>
        <b>${data.profession}</b>: ${data.fact}`;
        drawChart(data.chart_data, data.top_trait);
    }else{
        state++;
        ask(state);
    }
}

function drawChart(chartData, topTrait){
    const colors = chartData.labels.map(code => code===topTrait ? '#FF9800':'#2196F3');
    const ctx = document.getElementById('riaChart').getContext('2d');
    new Chart(ctx, {
        type:'bar',
        data:{
            labels: chartData.labels,
            datasets:[{
                label:'RIASEC Scores',
                data: chartData.scores,
                backgroundColor: colors
            }]
        },
        options:{responsive:true, scales:{y:{beginAtZero:true, precision:0}}}
    });
}

ask(0);
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML, questions=json.dumps(QUESTIONS))

@app.route('/answer', methods=['POST'])
def answer():
    data = request.json
    trait = data['trait']
    state = data['state']
    RIASEC[trait] += 1
    if state + 1 >= len(QUESTIONS):
        top_trait = max(RIASEC.items(), key=lambda x:x[1])[0]
        profession, fact = CAREERS[top_trait]
        chart_data = {"labels": list(RIASEC.keys()), "scores": list(RIASEC.values())}
        return jsonify({"done": True, "profession": profession, "fact": fact, "chart_data": chart_data, "top_trait": top_trait})
    return jsonify({"done": False})

if __name__=="__main__":
    app.run(debug=True)def index():
    for k in RIASEC: RIASEC[k]=0
    session['q_index']=0
    return render_template_string(HTML, questions=json.dumps(QUESTIONS))

@app.route('/answer', methods=['POST'])
def answer():
    data = request.json
    trait = data['trait']
    RIASEC[trait] += 1
    session['q_index'] += 1
    if session['q_index'] >= len(QUESTIONS):
        top_trait = max(RIASEC.items(), key=lambda x:x[1])[0]
        profession, fact = CAREERS[top_trait]
        chart_data = {"labels": list(RIASEC.keys()), "scores": list(RIASEC.values())}
        return jsonify({"done": True, "profession": profession, "fact": fact, "chart_data": chart_data, "top_trait": top_trait})
    return jsonify({"done": False})

if __name__=="__main__":
    app.run(debug=True)    for k in RIASEC: RIASEC[k]=0
    session['q_index']=0
    js_questions = QUESTIONS
    return render_template_string(HTML, questions=json.dumps(js_questions))

@app.route('/answer', methods=['POST'])
def answer():
    data = request.json
    trait = data['trait']
    RIASEC[trait] += 1
    session['q_index'] += 1
    if session['q_index'] >= len(QUESTIONS):
        top_trait = max(RIASEC.items(), key=lambda x:x[1])[0]
        profession, fact = CAREERS[top_trait]
        chart_data = {"labels": list(RIASEC.keys()), "scores": list(RIASEC.values())}
        return jsonify({"done": True, "profession": profession, "fact": fact, "chart_data": chart_data, "top_trait": top_trait})
    return jsonify({"done": False})

if __name__=="__main__":
    app.run(debug=True)<html>
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
