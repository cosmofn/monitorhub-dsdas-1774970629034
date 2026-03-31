from flask import Flask
import subprocess, threading, os, sys

app = Flask(__name__)

@app.route('/')
def alive():
    return {'status': 'alive', 'message': 'Service is running'}

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

def run_user_command():
    try:
        process = subprocess.Popen("python main.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout: print(line, end='', flush=True)
        for line in process.stderr: print(line, end='', file=sys.stderr, flush=True)
    except Exception as e: print(f"Error: {e}", flush=True)

if __name__ == '__main__':
    threading.Thread(target=run_user_command, daemon=True).start()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
