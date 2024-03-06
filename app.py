from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from datetime import datetime
import os
import random


app = Flask(__name__)

# Global flag to indicate the app has just started
app_started = True

weekly_schedule = {
    'Monday': [('College', '7:00', '13:00'), ('EDX', '13:00', '15:00'), ('Travel', '15:00', '16:00'), ('Free', '16:00', '17:00'), ('Cost Accounting', '17:00', '19:00'), ('Exercise', '19:00', '20:00'), ('Dinner', '20:00', '21:00'), ('Excel (Udemy)', '21:00', '23:00')],
    'Tuesday': [('College', '7:00', '13:00'), ('EDX', '13:00', '15:00'), ('Travel', '15:00', '16:00'), ('Free', '16:00', '17:00'), ('Business Statistics', '17:00', '19:00'), ('Exercise', '19:00', '20:00'), ('Dinner', '20:00', '21:00'), ('Excel (Udemy)', '21:00', '23:00')],
    'Wednesday': [('College', '7:00', '13:00'), ('EDX', '13:00', '15:00'), ('Travel', '15:00', '16:00'), ('Free', '16:00', '17:00'), ('Managerial Economics', '17:00', '19:00'), ('Exercise', '19:00', '20:00'), ('Dinner', '20:00', '21:00'), ('Excel (Udemy)', '21:00', '23:00')],
    'Thursday': [('College', '7:00', '13:00'), ('EDX', '13:00', '15:00'), ('Travel', '15:00', '16:00'), ('Free', '16:00', '17:00'), ('Environmental Studies', '17:00', '19:00'), ('Exercise', '19:00', '20:00'), ('Dinner', '20:00', '21:00'), ('Excel (Udemy)', '21:00', '23:00')],
    'Friday': [('College', '7:00', '13:00'), ('EDX', '13:00', '15:00'), ('Travel', '15:00', '16:00'), ('Free', '16:00', '17:00'), ('Digital Marketing', '17:00', '19:00'), ('Exercise', '19:00', '20:00'), ('Dinner', '20:00', '21:00'), ('Excel (Udemy)', '21:00', '23:00')]
}

study_tasks = [
    'EDX',
    'Cost Accounting',
    'Business Statistics',
    'Managerial Economics',
    'Environmental Studies',
    'Digital Marketing',
    'Excel (Udemy)'
]


punishment_tasks = ["20 push-ups", "Write a page in your journal", "Read an additional chapter of a textbook", "Complete an extra set of practice problems", "Spend 30 more minutes on a learning app", "Review notes from a previous lecture for 20 minutes", "Watch an educational video related to your field of study"]

# Track seen punishments
seen_punishments = []

@app.route('/')
def index():
    today = datetime.now().strftime("%A")
    tasks = weekly_schedule.get(today, [])
    task_index = int(request.args.get('task_index', 0))
    if task_index >= len(tasks):
        return redirect(url_for('day_completed'))
    else:
        current_task = tasks[task_index]
    return render_template('index.html', day=today, current_task=current_task, task_index=task_index)

@app.route('/complete_task', methods=['POST'])
def complete_task():
    task_index = int(request.form['task_index'])
    response = request.form['response']
    task_name = request.form['task_name']
    if response == 'yes':
        if task_name in study_tasks:
            return redirect(url_for('ask_summary', task_name=task_name, task_index=task_index))
        else:
            return proceed_to_next_task(task_index)
    else:
        punishment = random.choice(punishment_tasks)
        seen_punishments.append(punishment)
        return redirect(url_for('punishment_route', punishment=punishment, task_index=task_index))

@app.route('/ask_summary/<task_name>/<int:task_index>', methods=['GET', 'POST'])
def ask_summary(task_name, task_index):
    if request.method == 'POST':
        summary = request.form['summary']
        save_summary(task_name, summary)
        return proceed_to_next_task(task_index)
    return render_template('ask_summary.html', task_name=task_name, task_index=task_index)

@app.route('/punishment/<punishment>/<int:task_index>')
def punishment_route(punishment, task_index):
    return render_template('punishment.html', punishment=punishment, task_index=task_index)

def proceed_to_next_task(task_index):
    today = datetime.now().strftime("%A")
    tasks = weekly_schedule.get(today, [])
    if task_index + 1 < len(tasks):
        return redirect(url_for('index', task_index=task_index + 1))
    else:
        save_punishments()  # Ensure this is correctly called to save punishments at the end of the session
        return redirect(url_for('day_completed'))

@app.route('/day_completed')
def day_completed():
    today = datetime.now().strftime("%Y-%m-%d")
    summary_filename = f"Summaries_for_{today}.txt"
    punishment_filename = f"Punishments_for_{today}.txt"
    # Serve links or initiate download for both files
    return render_template('day_completed.html', summary_file=summary_filename, punishment_file=punishment_filename)

@app.route('/summaries/<filename>')
def uploaded_file(filename):
    return send_from_directory('summaries', filename)

def save_summary(task_name, summary):
    global app_started  # Access the global variable
    if not os.path.exists('summaries'):
        os.makedirs('summaries')
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"summaries/Summaries_for_{date_str}.txt"
    
    # Decide whether to overwrite or append based on app_started
    if app_started:
        mode = 'w'  # Overwrite if the app has just started
        app_started = False  # Reset the flag after the first summary
    else:
        mode = 'a'  # Append if not the first summary of the run
    
    with open(filename, mode) as file:
        file.write(f"{task_name}:\n{summary}\n\n")




def save_punishments():
    if not os.path.exists('summaries'):
        os.makedirs('summaries')
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"summaries/Punishments_for_{date_str}.txt"
    with open(filename, 'w') as file:  # Use 'w' for overwrite if needed, or 'a' to append during the day
        file.write("Punishments for today:\n")
        if seen_punishments:
            for punishment in seen_punishments:
                file.write(f"- {punishment}\n")
        else:
            file.write("No punishments recorded today.\n")
        seen_punishments.clear()  # Clear punishments after saving

if __name__ == '__main__':
    app.run(debug=True)        