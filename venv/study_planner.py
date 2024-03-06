from datetime import datetime
import random
import os

# Define weekly schedule
weekly_schedule = {
    'Monday': [
        ('College', '7:00', '13:00'),
        ('EDX', '13:00', '15:00'),
        ('Travel', '15:00', '16:00'),
        ('Free', '16:00', '17:00'),
        ('Cost Accounting', '17:00', '19:00'),
        ('Exercise', '19:00', '20:00'),
        ('Dinner', '20:00', '21:00'),
        ('Excel (Udemy)', '21:00', '23:00')
    ],
    'Tuesday': [
        ('College', '7:00', '13:00'),
        ('EDX', '13:00', '15:00'),
        ('Travel', '15:00', '16:00'),
        ('Free', '16:00', '17:00'),
        ('Business Statistics', '17:00', '19:00'),
        ('Exercise', '19:00', '20:00'),
        ('Dinner', '20:00', '21:00'),
        ('Excel (Udemy)', '21:00', '23:00')
    ],
    'Wednesday': [
        ('College', '7:00', '13:00'),
        ('EDX', '13:00', '15:00'),
        ('Travel', '15:00', '16:00'),
        ('Free', '16:00', '17:00'),
        ('Managerial Economics', '17:00', '19:00'),
        ('Exercise', '19:00', '20:00'),
        ('Dinner', '20:00', '21:00'),
        ('Excel (Udemy)', '21:00', '23:00')
    ],
    'Thursday': [
        ('College', '7:00', '13:00'),
        ('EDX', '13:00', '15:00'),
        ('Travel', '15:00', '16:00'),
        ('Free', '16:00', '17:00'),
        ('Environmental Studies', '17:00', '19:00'),
        ('Exercise', '19:00', '20:00'),
        ('Dinner', '20:00', '21:00'),
        ('Excel (Udemy)', '21:00', '23:00')
    ],
    'Friday': [
        ('College', '7:00', '13:00'),
        ('EDX', '13:00', '15:00'),
        ('Travel', '15:00', '16:00'),
        ('Free', '16:00', '17:00'),
        ('Digital Marketing', '17:00', '19:00'),
        ('Exercise', '19:00', '20:00'),
        ('Dinner', '20:00', '21:00'),
        ('Excel (Udemy)', '21:00', '23:00')
    ],
}

# Updated punishment tasks
punishment_tasks = [
    "20 push-ups",
    "Write a page in your journal",
    "Read an additional chapter of a textbook",
    "Complete an extra set of practice problems",
    "Spend 30 more minutes on a learning app",
    "Review notes from a previous lecture for 20 minutes",
    "Watch an educational video related to your field of study"
]

study_times = ['13:00', '15:00', '17:00', '19:00', '21:00', '23:00']

def is_study_task(start, end):
    return start in study_times and end in study_times

def save_summary(task_name, summary):
    # Ensure the summaries directory exists
    if not os.path.exists('summaries'):
        os.makedirs('summaries')
    
    # Format the filename to include the current date
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"summaries/Summary_for_{date_str}.txt"
    
    # Append summary under task title
    with open(filename, 'a') as file:
        file.write(f"{task_name}:\n{summary}\n\n")
    
    print("Summary saved successfully under the task title.")

def check_task_completion(task_name, start, end):
    user_input = input(f"Have you completed '{task_name}'? (yes/no): ").lower()
    if user_input == 'yes':
        if is_study_task(start, end):
            summary = input("Please summarize what you've learned: ")
            save_summary(task_name, summary)
        return True
    else:
        print(f"You reported not completing '{task_name}'.")
        return False

def assign_punishment():
    punishment = random.choice(punishment_tasks)
    print(f"Your punishment task is: {punishment}")

def run_daily_schedule(day):
    tasks = weekly_schedule[day]
    for task, start, end in tasks:
        print(f"Task: {task}, Time: {start} - {end}")
        if not check_task_completion(task, start, end):
            assign_punishment()

def run_schedule_for_today():
    today = datetime.now().strftime("%A")
    if today in weekly_schedule:
        print(f"Running schedule for {today}")
        run_daily_schedule(today)
    else:
        print("Today is not a scheduled day. Enjoy your day off!")

if __name__ == "__main__":
    run_schedule_for_today()