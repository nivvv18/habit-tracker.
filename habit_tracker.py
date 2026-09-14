import json
import os
from datetime import datetime, timedelta

DATA_FILE = "habits.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def calculate_streak(history):
    if not history:
        return 0
    
    dates = sorted([datetime.strptime(d, "%Y-%m-%d").date() for d in history], reverse=True)
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    if dates[0] not in (today, yesterday):
        return 0
    
    streak = 1
    for i in range(len(dates) - 1):
        if dates[i] - dates[i + 1] == timedelta(days=1):
            streak += 1
        elif dates[i] == dates[i + 1]:
            continue  # duplicate entry guard
        else:
            break
    return streak

def add_habit():
    name = input("Enter habit name: ").strip()
    if not name:
        print("Habit name cannot be empty.")
        return
    
    data = load_data()
    if name in data:
        print(f"Habit '{name}' already exists.")
        return
    
    description = input("Enter habit description: ").strip()
    data[name] = {
        "description": description,
        "history": []
    }
    save_data(data)
    print(f"Habit '{name}' successfully added!")

def check_in():
    data = load_data()
    if not data:
        print("No habits found. Add a habit first!")
        return
    
    print("\n--- Select Habit to Check-In ---")
    habits = list(data.keys())
    for idx, name in enumerate(habits, 1):
        print(f"{idx}. {name}")
    
    try:
        choice = int(input("Enter number: ")) - 1
        if 0 <= choice < len(habits):
            selected_name = habits[choice]
            today_str = datetime.now().strftime("%Y-%m-%d")
            
            if today_str in data[selected_name]["history"]:
                print(f"You already checked in for '{selected_name}' today!")
            else:
                data[selected_name]["history"].append(today_str)
                save_data(data)
                print(f"Checked in for '{selected_name}' for today ({today_str})!")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")

def view_progress():
    data = load_data()
    if not data:
        print("No habits found.")
        return
    
    print("\n================ HABIT PROGRESS ================")
    for name, info in data.items():
        streak = calculate_streak(info["history"])
        print(f"Habit: {name}")
        print(f" Description: {info.get('description', '')}")
        print(f" Current Streak: {streak} day(s)")
        print(f" Total Completions: {len(info['history'])}")
        print("-" * 48)

def main():
    while True:
        print("\n=== COMMAND-LINE HABIT TRACKER ===")
        print("1. Add Habit")
        print("2. Daily Check-In")
        print("3. View Progress")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ").strip()
        if choice == "1":
            add_habit()
        elif choice == "2":
            check_in()
        elif choice == "3":
            view_progress()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")

if __name__ == "__main__":
    main()