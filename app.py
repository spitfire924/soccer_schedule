from flask import Flask, request, render_template, redirect, url_for, abort

app = Flask(__name__)

# Define global variables for title, location, and event time
current_title = "Participant Management"
event_location = "Event Location"
event_time = "Event Time"

def load_participants():
    try:
        with open('participants.txt', 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

def save_participants(participants):
    with open('participants.txt', 'w') as file:
        file.write('\n'.join(participants))

def is_local_request(remote_ip):
    return remote_ip.startswith("127.0.0.1") or remote_ip.startswith("192.168.") or remote_ip.startswith("10.") or remote_ip.startswith("172.16.")

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_title, event_location, event_time
    participants = load_participants()
    remote_ip = request.remote_addr

    if request.method == 'POST':
        if is_local_request(remote_ip):
            if 'add' in request.form:
                name = request.form['name']
                if name:
                    participants.append(name)
                    save_participants(participants)
            elif 'remove' in request.form:
                index = int(request.form['index'])
                if 0 <= index < len(participants):
                    participants.pop(index)
                    save_participants(participants)
        else:
            abort(403)

    return render_template(
        'index.html',
        participants=participants,
        participants_count=len(participants),
        title=current_title,
        location=event_location,
        event_time=event_time,
        is_local=is_local_request(remote_ip)
    )

@app.route('/clear', methods=['POST'])
def clear_participants():
    remote_ip = request.remote_addr
    if is_local_request(remote_ip):
        participants = []
        save_participants(participants)
        return redirect(url_for('index'))
    else:
        abort(403)  # Forbidden access for non-local requests

@app.route('/update_title', methods=['POST'])
def update_title():
    remote_ip = request.remote_addr
    if is_local_request(remote_ip):
        global current_title
        new_title = request.form['new_title']
        current_title = new_title
        return redirect(url_for('index'))
    else:
        abort(403)

@app.route('/update_details', methods=['POST'])
def update_details():
    remote_ip = request.remote_addr
    if is_local_request(remote_ip):
        global event_location, event_time
        event_location = request.form['location']
        event_time = request.form['event_time']
        return redirect(url_for('index'))
    else:
        abort(403)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
