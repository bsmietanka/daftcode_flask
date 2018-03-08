from flask import Flask
from flask import request
from user_agents import parse
from datetime import datetime
from multiprocessing import Value

counter = Value('I', 0)
app = Flask(__name__)

counter_path = "counter"

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/now")
def current_time():
    return f"{datetime.utcnow()}"

@app.route('/user-agent')
def user_agent_info():
    return str(parse(request.headers.get('User-Agent')))

# resets when heroku process goes idle
# heroku app sometimes uses two separate counters
# cause of this behaviour may be two processes
# on two different machines (cannot synchronize)
@app.route('/counter')
def count_visits():
    with counter.get_lock():
        counter.value += 1
    return f"{counter.value}"

if __name__ == "__main__":
    app.run(debug=True)