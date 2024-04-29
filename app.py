from flask import Flask, render_template, request
import hashlib
from zxcvbn import zxcvbn


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
    result = zxcvbn(password)
    score = result['score']
    feedback = result['feedback']['suggestions']
    hashed = hash_password(password)
    is_common_password = hash_password(password) in password_set
    return render_template('result.html', hashed_password=hashed, is_common=is_common_password, password=password, score=score, feedback=feedback)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

if __name__ == '__main__':
    app.run(debug=True)
