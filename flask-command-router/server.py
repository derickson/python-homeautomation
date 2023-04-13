import subprocess
from flask import Flask, request

app = Flask(__name__)

def invoke(command):
    result = subprocess.run(command, shell=True, capture_output=True)
    return result.stdout.decode()

@app.route('/', methods=['POST'])
def run_command():
    data = request.json
    command = data['command']
    
    if command == "list":
        return invoke("ls -l")
    elif command == "laugh":
        return invoke('echo "hahahaha"')
    else:
        return "no valid command input"

if __name__ == '__main__':
    app.run(debug=True)