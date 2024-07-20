from flask import Flask, request, jsonify, render_template
import os
import random

app = Flask(__name__)

def stay_strategy(chances):
    carcount = 0
    for _ in range(chances):
        doors = [0, 0, 0]
        car_door = random.randint(0, 2)
        doors[car_door] = 1
        first_choice = random.randint(0, 2)
        if doors[first_choice] == 1:
            carcount += 1
    win_percentage = (carcount / chances) * 100
    return carcount, win_percentage

def switch_strategy(chances):
    carcount = 0
    for _ in range(chances):
        doors = [0, 0, 0]
        car_door = random.randint(0, 2)
        doors[car_door] = 1
        first_choice = random.randint(0, 2)
        monty_choice = [x for x in range(3) if x != first_choice and doors[x] == 0]
        second_choice = random.choice(monty_choice)
        third_choice = next(x for x in range(3) if x != first_choice and x != second_choice)
        if doors[third_choice] == 1:
            carcount += 1
    win_percentage = (carcount / chances) * 100
    return carcount, win_percentage

def random_strategy(chances):
    carcount = 0
    for _ in range(chances):
        doors = [0, 0, 0]
        car_door = random.randint(0, 2)
        doors[car_door] = 1
        first_choice = random.randint(0, 2)
        monty_choice = [x for x in range(3) if x != first_choice and doors[x] == 0]
        if random.choice([True, False]):
            second_choice = random.choice(monty_choice)
            final_choice = next(x for x in range(3) if x != first_choice and x != second_choice)
        else:
            final_choice = first_choice
        if doors[final_choice] == 1:
            carcount += 1
    win_percentage = (carcount / chances) * 100
    return carcount, win_percentage

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_simulations', methods=['POST'])
def start_simulations():
    num_simulations = int(request.form['num_simulations'])
    
    # Run simulations
    wins_keep, percentage_keep = stay_strategy(num_simulations)
    wins_switch, percentage_switch = switch_strategy(num_simulations)
    wins_random, percentage_random = random_strategy(num_simulations)
    
    # Create history data
    history_keep = [stay_strategy(i)[1] for i in range(1, num_simulations + 1)]
    history_switch = [switch_strategy(i)[1] for i in range(1, num_simulations + 1)]
    history_random = [random_strategy(i)[1] for i in range(1, num_simulations + 1)]
    
    response = {
        'simulation_count': num_simulations,
        'total_attempts': num_simulations,
        'total_wins_random': wins_random,
        'total_wins_keep': wins_keep,
        'total_wins_switch': wins_switch,
        'history_keep': history_keep,
        'history_switch': history_switch,
        'history_random': history_random,
        'events_all': ["Simulation completed successfully"]
    }
    
    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
