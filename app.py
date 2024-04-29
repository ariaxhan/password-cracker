from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

# Load common passwords into a set
def load_common_passwords(file_path):
    return_set = set()
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                hashed_password = hashlib.sha256(line.encode()).hexdigest()
                # add to return set
                return_set.add(hashed_password)
    except FileNotFoundError:
        return set()
    return return_set

password_set1 = load_common_passwords('10k-most-common.txt')
password_set2 = load_common_passwords('10-million-password-list-top-1000000.txt')
password_set3 = load_common_passwords('500-worst-passwords.txt')
password_set = password_set1.union(password_set2).union(password_set3)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_password', methods=['POST'])
def check_password():
    password = request.form['password']
    hashed_password = hash_password(password)
    is_common_password = hashed_password in password_set
    return render_template('result.html', is_common=is_common_password, password=password, hashed_password=hashed_password)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

if __name__ == '__main__':
    app.run(debug=True)
