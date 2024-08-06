from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np

app = Flask(__name__)

# Load the model from the file
model_filename = 'model.pkl'
with open(model_filename, 'rb') as file:
    loaded_model = pickle.load(file)


################################################
@app.route('/')
def main():
    return render_template("main.html")
##################################################
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'admin':
            return redirect(url_for('input'))
        else:
            return 'Invalid credentials, please try again.'

    return render_template('login.html')

################################################
@app.route('/input', methods=['POST','GET'])
def input():
    try:
        input_features = [int(x) for x in request.form.values()]
        input_array = np.array(input_features).reshape(1, -1)
        assert input_array.shape[1] == 6, "The model expects 6 features."
        prediction = loaded_model.predict(input_array)
        print(prediction)
        if prediction == 0:
            result = "Fraud"
        else:
            result = "No Fraud"

        print(result)
        return render_template('input.html', prediction_text=result)
    except Exception as e:
        return render_template('input.html', prediction_text=f'Error: {str(e)}')

###################################################
@app.route('/about')
def about():
    return render_template("about.html")

####################################################
@app.route('/contact')
def contact():
    return render_template("contact.html")



if __name__ == '__main__':
    app.run()
