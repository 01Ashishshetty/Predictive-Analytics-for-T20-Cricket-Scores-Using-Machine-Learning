from flask import Flask, render_template, request
import pickle
import pandas as pd
import pyttsx3

app = Flask(__name__)

pipe = pickle.load(open('pipe.pkl', 'rb'))

teams = [
    'Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa',     'England', 'West Indies', 'Afghanistan', 'Pakistan', 'Sri Lanka'
]

cities = [
    'Colombo', 'Mirpur', 'Johannesburg', 'Dubai', 'Auckland', 'Cape Town', 
    'London', 'Pallekele', 'Barbados', 'Sydney', 'Melbourne', 'Durban', 
    'St Lucia', 'Wellington', 'Lauderhill', 'Hamilton', 'Centurion', 
    'Manchester', 'Abu Dhabi', 'Mumbai', 'Nottingham', 'Southampton', 
    'Mount Maunganui', 'Chittagong', 'Kolkata', 'Lahore', 'Delhi', 
    'Nagpur', 'Chandigarh', 'Adelaide', 'Bangalore', 'St Kitts', 'Cardiff', 
    'Christchurch', 'Trinidad'
]

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        # Get the form values
        batting_team = request.form.get('batting_team')
        bowling_team = request.form.get('bowling_team')
        city = request.form.get('city')
        current_score = request.form.get('current_score')
        overs = request.form.get('overs')
        wickets = request.form.get('wickets')
        last_five = request.form.get('last_five')

        try:
            # Convert values to the correct types
            current_score = int(current_score)
            overs = float(overs)
            wickets = int(wickets)
            last_five = int(last_five)

            balls_left = 120 - (overs * 6)
            wickets_left = 10 - wickets
            crr = current_score / overs

            # Create the input dataframe
            input_df = pd.DataFrame(
                {'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [city], 
                'current_score': [current_score], 'balls_left': [balls_left], 
                'wicket_left': [wickets_left], 'current_run_rate': [crr], 'last_five': [last_five]}
            )

            result = pipe.predict(input_df)
            prediction = int(result[0])

            engine = pyttsx3.init()
            prediction_text = f'The predicted final score is {prediction} runs.'
            engine.say(prediction_text)
            engine.runAndWait()

        except ValueError:
            pass  # Simply skip invalid input without any feedback

    return render_template('index.html', teams=sorted(teams), cities=sorted(cities), prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
