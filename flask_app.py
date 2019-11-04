import flask
import sqlitedict
import logging

app = flask.Flask(__name__)
logger = logging.getLogger("werkzeug")
logger.setLevel(logging.ERROR)
state = sqlitedict.SqliteDict('./state.sqlite', autocommit=False)

@app.route('/')
def index():
    return ('Fib-stepper index')

@app.route('/current')
def current():
    return str(state.get('current'))

@app.route('/next')
def next():
    current_fib = state['current']
    previous_fib = state['previous']

    if current_fib == 0:
        next_fib = 1
    else:
        next_fib = current_fib + previous_fib

    # Check for overflow
    if next_fib < current_fib:
        flask.abort(400, 'Integer overflow!')

    state['previous'] = current_fib
    state['current'] = next_fib
    state.commit()

    return str(next_fib)
    

@app.route('/previous')
def previous():
    current_fib = state['current']
    if current_fib == 0:
        return str(0)

    previous_fib = state['previous']

    state['previous'] = current_fib - previous_fib
    state['current'] = previous_fib
    state.commit()

    return str(previous_fib)


if __name__ == "__main__":
    if 'current' not in state:
        state['current'] = 0
    
    if 'previous' not in state:
        state['previous'] = 0

    #state['previous'] = 0
    #state['current'] = 0
    app.run()