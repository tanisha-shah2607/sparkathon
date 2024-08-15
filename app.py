from flask import Flask, request, render_template, redirect, url_for, session
import joblib
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load the trained model
model = joblib.load('best_sales_prediction_model.pkl')

# Function to predict sales
def predict_sales(model, data):
    prediction = model.predict(data)
    return prediction

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Implement authentication logic
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('predict'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'logged_in' in session:
        if request.method == 'POST':
            # Assuming data is passed as a comma-separated string
            data = np.array([float(x) for x in request.form['data'].split(',')]).reshape(1, -1)
            result = predict_sales(model, data)
            return f'Sales Prediction: {result[0]}'
        return render_template('predict.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)


