from flask import Flask, render_template, request, jsonify
from assistant_logic import handle_command

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    user_input = data.get('command', '')
    response = handle_command(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)



