import random

def ask_questions():
    print("Welcome to the Career Guidance Chatbot!\n")
    print("Please answer the following 50 questions with a number from 1 (Strongly Disagree) to 5 (Strongly Agree).\n")

    categories = {
        'R': 0,  # Realistic
        'I': 0,  # Investigative
        'A': 0,  # Artistic
        'S': 0,  # Social
        'E': 0,  # Enterprising
        'C': 0   # Conventional
    }

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

    random.shuffle(questions)

    for i, (question, category) in enumerate(questions[:50], start=1):
        while True:
            try:
                response = int(input(f"Q{i}: {question} \n(1-Strongly Disagree ... 5-Strongly Agree): "))
                if response in range(1, 6):
                    categories[category] += response
                    break
                else:
                    print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    return categories

def suggest_careers(scores):
    print("\nCalculating your results...\n")
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_3 = [code for code, score in sorted_scores[:3]]

    holland_types = {
        'R': (
            "Realistic (Doers)",
            [
                ("Engineer", "Designs and builds systems and structures."),
                ("Mechanic", "Repairs and maintains machines and vehicles."),
                ("Electrician", "Installs and maintains electrical systems."),
                ("Carpenter", "Builds and repairs structures made of wood."),
                ("Pilot", "Operates aircraft to transport passengers or goods.")
            ]
        ),
        'I': (
            "Investigative (Thinkers)",
            [
                ("Scientist", "Conducts research to discover new knowledge."),
                ("Doctor", "Diagnoses and treats illnesses and injuries."),
                ("Data Analyst", "Interprets data to support decision-making."),
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
