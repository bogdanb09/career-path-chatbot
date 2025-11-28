"""
Career-Path-Chatbot
Single-file Python/Flask demo chatbot that helps teenagers/students choose a career path
based on their interests, soft skills, hard skills, competencies and preferences.

Features:
- Simple web chat UI (single-page) served by Flask
- A short interactive questionnaire to collect: interests, subject strengths, hard & soft skills,
  study/time willingness, team preference
- Scoring algorithm that matches user profile against a small built-in career database
- Returns ranked career recommendations with short explanations and next steps
- Easy to extend: update CAREERS list or adjust weights in `score_profile`

Notes / Disclaimer:
- This is a demo/prototype. It is not a substitute for professional career counselling.
- For production use: add authentication, persistent storage, input validation, GDPR/parental-consent
  handling, accessibility improvements, and localize content.

How to run:
1) Create a virtualenv and install Flask: pip install flask
2) Run: python career_chatbot.py
3) Open http://127.0.0.1:5000 in a browser

"""
from flask import Flask, request, jsonify, render_template_string, session
from collections import Counter
import math
import json
import uuid

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-this"

# -------------------------
# Simple careers database (small sample). Extend as needed.
# Each career has tags for interests, hard_skills, soft_skills, education
# -------------------------
CAREERS = [
    {
        "id": "software_engineer",
        "title": "Software Engineer",
        "interests": ["technology", "computers", "programming", "problem solving"],
        "hard_skills": ["programming", "algorithms", "data structures", "math"],
        "soft_skills": ["logical thinking", "attention to detail", "persistence", "communication"],
        "education": "BSc in Computer Science or related; many bootcamps/online routes",
        "description": "Designs and builds software. Strong problem solving and coding skills help you succeed.",
        "time_to_qualify_years": 0-4,
    },
    {
        "id": "graphic_designer",
        "title": "Graphic Designer",
        "interests": ["art", "visual design", "creativity"],
        "hard_skills": ["visual design", "adobe suite", "typography"],
        "soft_skills": ["creativity", "communication", "time management"],
        "education": "Portfolio and vocational courses; degrees optional",
        "description": "Creates visuals for brands, websites and products.",
        "time_to_qualify_years": 0-3,
    },
    {
        "id": "data_scientist",
        "title": "Data Scientist",
        "interests": ["math", "statistics", "data", "research"],
        "hard_skills": ["statistics", "python", "machine learning", "data analysis"],
        "soft_skills": ["curiosity", "communication", "critical thinking"],
        "education": "BSc/MSc often; strong online learning pathways",
        "description": "Extracts insights from data and builds predictive models.",
        "time_to_qualify_years": 1-6,
    },
    {
        "id": "nurse",
        "title": "Nurse",
        "interests": ["helping others", "biology", "healthcare"],
        "hard_skills": ["anatomy", "patient care", "medical procedures"],
        "soft_skills": ["empathy", "stress management", "teamwork"],
        "education": "Nursing diploma/degree and licensing",
        "description": "Provides care to patients in hospitals and the community.",
        "time_to_qualify_years": 2-4,
    },
    {
        "id": "teacher",
        "title": "Teacher / Educator",
        "interests": ["learning", "mentoring", "communication"],
        "hard_skills": ["subject knowledge", "lesson planning"],
        "soft_skills": ["communication", "patience", "adaptability"],
        "education": "Teaching certification/degree depending on country",
        "description": "Helps students learn and grow; requires strong interpersonal skills.",
        "time_to_qualify_years": 1-4,
    },
]

# canonical list of recognized tags to prompt user for ratings
ALL_HARD_SKILLS = sorted(list({s for c in CAREERS for s in c['hard_skills']}))
ALL_SOFT_SKILLS = sorted(list({s for c in CAREERS for s in c['soft_skills']}))
ALL_INTERESTS = sorted(list({s for c in CAREERS for s in c['interests']}))

# -------------------------
# Scoring algorithm
# - Accepts a user profile: interests (list), hard_skills_ratings (dict skill->0-5),
#   soft_skills_ratings (dict skill->0-5), preferences
# - Outputs ranked careers with match score and reasons
# -------------------------

def score_profile(profile, careers=CAREERS):
    """Return a list of (career, score, reasons)
    Scores combine:
      - interest overlap (binary tags)
      - hard skills weighted by rating
      - soft skills weighted by rating
    """
    results = []
    # weights (tuneable)
    w_interest = 1.2
    w_hard = 1.5
    w_soft = 1.0

    for c in careers:
        # interest score: proportion of career interests present in user interests
        if not c['interests']:
            interest_score = 0
        else:
            matches = sum(1 for i in c['interests'] if i in profile.get('interests', []))
            interest_score = matches / len(c['interests'])

        # hard skills score: normalized by number of skills, use user ratings 0-5
        hard_total = 0
        if c['hard_skills']:
            for s in c['hard_skills']:
                hard_total += profile.get('hard_skills', {}).get(s, 0) / 5.0
            hard_score = hard_total / len(c['hard_skills'])
        else:
            hard_score = 0

        # soft skills score
        soft_total = 0
        if c['soft_skills']:
            for s in c['soft_skills']:
                soft_total += profile.get('soft_skills', {}).get(s, 0) / 5.0
            soft_score = soft_total / len(c['soft_skills'])
        else:
            soft_score = 0

        # base score
        score = (w_interest * interest_score) + (w_hard * hard_score) + (w_soft * soft_score)

        # adjust for study/time preference: if user wants short qualification and career needs long, penalize slightly
        pref_time = profile.get('preferred_time_to_qualify_years')
        if pref_time is not None and isinstance(c.get('time_to_qualify_years'), (tuple, list)):
            min_req, max_req = c['time_to_qualify_years']
            # if user's preferred max years is less than career min -> penalty
            if pref_time < min_req:
                score *= 0.8

        # build reasons
        reasons = []
        if interest_score > 0:
            reasons.append(f"Shared interests: {matches} of {len(c['interests'])}")
        if hard_score > 0:
            reasons.append(f"Hard-skill fit: {hard_score:.2f}")
        if soft_score > 0:
            reasons.append(f"Soft-skill fit: {soft_score:.2f}")

        results.append({
            'career_id': c['id'],
            'title': c['title'],
            'score': round(score, 3),
            'reasons': reasons,
            'description': c['description'],
            'education': c['education'],
        })

    # sort by score desc
    results.sort(key=lambda x: x['score'], reverse=True)
    return results


# -------------------------
# Minimal session/chat management and endpoints
# -------------------------

@app.route('/')
def index():
    # simple single-page app. Keep HTML inline for simplicity.
    page = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Career Path Helper (Demo)</title>
  <style>
    body{font-family:system-ui,Segoe UI,Roboto,Arial;margin:16px}
    #chat{border:1px solid #ddd;padding:12px;height:420px;overflow:auto}
    .bot{color:#111;margin:6px 0}
    .user{color:#064;margin:6px 0;text-align:right}
    .bubble{display:inline-block;padding:8px 10px;border-radius:10px}
    .bot .bubble{background:#eee}
    .user .bubble{background:#dff0d8}
    textarea{width:100%;height:60px}
    .meta{font-size:0.9em;color:#555}
  </style>
</head>
<body>
  <h2>Career Path Helper — Demo Chatbot</h2>
  <div id="chat"></div>
  <div style="margin-top:8px">
    <textarea id="input" placeholder="Type your answer here..."></textarea>
    <button id="send">Send</button>
  </div>
  <p class="meta">Tip: Try short answers. The bot will ask questions to build a profile.</p>

<script>
const chat = document.getElementById('chat')
const input = document.getElementById('input')
const send = document.getElementById('send')

function appendMessage(text, cls){
  const d = document.createElement('div')
  d.className = cls
  const b = document.createElement('span')
  b.className = 'bubble'
  b.innerText = text
  d.appendChild(b)
  chat.appendChild(d)
  chat.scrollTop = chat.scrollHeight
}

function sendMessage(msg){
  appendMessage(msg, 'user')
  fetch('/chat', {
    method: 'POST', headers: {'Content-Type':'application/json'},
    body: JSON.stringify({message: msg})
  }).then(r=>r.json()).then(data=>{
    if(data.replies){
      data.replies.forEach(r=>appendMessage(r, 'bot'))
    }
  })
}

send.onclick = ()=>{const v=input.value.trim(); if(!v) return; sendMessage(v); input.value=''}
input.addEventListener('keydown', (e)=>{ if(e.key==='Enter' && (e.ctrlKey||e.metaKey)) { send.click(); } })

// kick off
fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({init: true})})
.then(r=>r.json()).then(data=>{data.replies.forEach(r=>appendMessage(r,'bot'))})
</script>
</body>
</html>
    """
    return render_template_string(page)


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    # initialize session profile if needed
    if 'profile' not in session:
        session['profile'] = {
            'interests': [],
            'hard_skills': {},
            'soft_skills': {},
            'preferred_time_to_qualify_years': None,
        }
        session['state'] = 'intro'
        session.modified = True

    profile = session['profile']
    state = session.get('state', 'intro')

    # if frontend requested init
    if data.get('init'):
        replies = [
            "Hi — I'm your Career Helper! I will ask a few quick questions about your interests and skills, then suggest careers.",
            "First: list 3 subjects, activities or topics you enjoy (e.g. mathematics, drawing, coding, helping people)."
        ]
        return jsonify({'replies': replies})

    message = data.get('message', '').strip()
    replies = []

    # simple state machine
    if state == 'intro':
        # parse interests as comma-separated
        interests = [s.strip().lower() for s in message.replace(';',',').split(',') if s.strip()]
        profile['interests'] = interests
        session['state'] = 'hard_skills'
        replies.append("Nice — got it. Now please rate your comfort (0-5) with these hard skills where 0=no experience, 5=very strong. Reply with numbers separated by commas in the same order:\n" + ALL_HARD_SKILLS.join(', '))
    elif state == 'hard_skills':
        # expect comma-separated numbers
        parts = [p.strip() for p in message.split(',') if p.strip()]
        ratings = []
        for i,skill in enumerate(ALL_HARD_SKILLS):
            try:
                val = float(parts[i]) if i < len(parts) else 0.0
            except:
                val = 0.0
            val = max(0.0, min(5.0, val))
            profile['hard_skills'][skill] = val
        session['state'] = 'soft_skills'
        replies.append("Thanks. Now rate these soft skills (0-5) in the same way:\n" + ALL_SOFT_SKILLS.join(', '))
    elif state == 'soft_skills':
        parts = [p.strip() for p in message.split(',') if p.strip()]
        for i,skill in enumerate(ALL_SOFT_SKILLS):
            try:
                val = float(parts[i]) if i < len(parts) else 0.0
            except:
                val = 0.0
            val = max(0.0, min(5.0, val))
            profile['soft_skills'][skill] = val
        session['state'] = 'time_pref'
        replies.append("Great. How many years would you be willing to study or train before starting a career? (enter a number, e.g. 0, 1, 3)")
    elif state == 'time_pref':
        try:
            years = float(message.split()[0])
            profile['preferred_time_to_qualify_years'] = years
        except:
            profile['preferred_time_to_qualify_years'] = None
        session['state'] = 'done'
        # produce recommendations
        ranked = score_profile(profile)
        top = ranked[:5]
        replies.append("Thanks — based on your answers, here are the top career matches:")
        for r in top:
            replies.append(f"{r['title']} — score {r['score']}. {r['description']} Suggested next step: {r['education']}")
        replies.append("If you want more detail on any suggestion, type the career title or 'restart' to retake the questionnaire.")
    elif state == 'done':
        # allow requesting details or restart
        msg_low = message.lower()
        if msg_low == 'restart':
            session.pop('profile', None)
            session.pop('state', None)
            session.modified = True
            replies.append("Restarting. List 3 subjects, activities or topics you enjoy.")
        else:
            # find career
            found = None
            for c in CAREERS:
                if c['title'].lower() in msg_low or c['id'] in msg_low:
                    found = c
                    break
            if found:
                replies.append(f"{found['title']}: {found['description']}\nTypical education: {found['education']}\nUseful skills to build: {', '.join(found['hard_skills'][:5])}")
                replies.append("Would you like actionable next steps to start exploring this career? Reply 'yes' or 'no'.")
                session['state'] = 'detail_followup'
            else:
                replies.append("I didn't recognize that. Type a career title from the suggestions exactly, or 'restart'.")
    elif state == 'detail_followup':
        if message.strip().lower() == 'yes':
            # for demo, provide generic next steps
            replies.append("Next steps (generic): 1) Try a short online course or workshop. 2) Talk to someone working in the field. 3) Build a small project or portfolio piece. 4) Volunteer or find internships.")
            session['state'] = 'done'
        else:
            replies.append("Okay — type 'restart' to take the questionnaire again or ask about another career.")
            session['state'] = 'done'
    else:
        replies.append("Sorry, I got confused. Type 'restart' to start over.")
        session['state'] = 'intro'

    session['profile'] = profile
    session.modified = True
    return jsonify({'replies': replies})


if __name__ == '__main__':
    app.run(debug=True)
  
