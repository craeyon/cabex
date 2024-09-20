from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Game variables
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

# Game logic functions
def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)

    return columns

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game', methods=['POST'])
def game():
    balance = int(request.form['balance'])
    bet = int(request.form['bet'])
    lines = int(request.form['lines'])

    # Total bet check
    total_bet = bet * lines
    if total_bet > balance:
        return render_template('game.html', error="Not enough balance", balance=balance)

    # Slot spin and check winnings
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    balance += (winnings - total_bet)

    return render_template('game.html', balance=balance, slots=slots, winnings=winnings, winning_lines=winning_lines)

if __name__ == '__main__':
    app.run(debug=True)
