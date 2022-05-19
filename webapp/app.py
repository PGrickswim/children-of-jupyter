import flask
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Use pickle to load in the pre-trained model.
with open(f'model/titanic_model.pkl', 'rb') as f:
    model = pickle.load(f)
app = flask.Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('main.html'))
    if flask.request.method == 'POST':
        gender = flask.request.form['gender']
        age = flask.request.form['age']
        board_class = flask.request.form['board_class']
        embarked = flask.request.form['embarked']
        country = flask.request.form['country']

        # Use answers from input form to fill in values from hot encoding
        class_dict = {'class_1st': 0,
                      'class_2nd': 0,
                      'class_3rd': 0,
                      'class_crew': 0}
        embarked_dict = {'embarked_B': 0,
                         'embarked_C': 0,
                         'embarked_Q': 0,
                         'embarked_S': 0}
        country_dict = {'country_AFR': 0,
                        'country_ASA': 0,
                        'country_AUS': 0,
                        'country_ENG': 0,
                        'country_EUR': 0,
                        'country_FIN': 0,
                        'country_IRL': 0,
                        'country_LBN': 0,
                        'country_NAM': 0,
                        'country_SAM': 0,
                        'country_SWE': 0,
                        'country_USA': 0}
        # Figure out for loop that assigns value of 0 or 1
        # depending on what the form value is
        for key in list(class_dict):
            fullstring = key
            substring = board_class
            if substring in fullstring:
                class_dict[key] = 1
            else:
                class_dict[key] = 0

        for key in list(embarked_dict):
            fullstring = key
            substring = embarked
            if substring in fullstring:
                embarked_dict[key] = 1
            else:
                embarked_dict[key] = 0

        for key in list(country_dict):
            fullstring = key
            substring = country
            if substring in fullstring:
                country_dict[key] = 1
            else:
                country_dict[key] = 0

        # Create dataframe out of input variables.
        input_variables = pd.DataFrame([[gender,
                                         age,
                                         class_dict['class_1st'],
                                         class_dict['class_2nd'],
                                         class_dict['class_3rd'],
                                         class_dict['class_crew'],
                                         embarked_dict['embarked_B'],
                                         embarked_dict['embarked_C'],
                                         embarked_dict['embarked_Q'],
                                         embarked_dict['embarked_S'],
                                         country_dict['country_AFR'],
                                         country_dict['country_ASA'],
                                         country_dict['country_AUS'],
                                         country_dict['country_ENG'],
                                         country_dict['country_EUR'],
                                         country_dict['country_FIN'],
                                         country_dict['country_IRL'],
                                         country_dict['country_LBN'],
                                         country_dict['country_NAM'],
                                         country_dict['country_SAM'],
                                         country_dict['country_SWE'],
                                         country_dict['country_USA']]],
                                       columns=['gender',
                                                'age',
                                                'class_1st',
                                                'class_2nd',
                                                'class_3rd',
                                                'class_crew',
                                                'embarked_B',
                                                'embarked_C',
                                                'embarked_Q',
                                                'embarked_S',
                                                'country_AFR',
                                                'country_ASA',
                                                'country_AUS',
                                                'country_ENG',
                                                'country_EUR',
                                                'country_FIN',
                                                'country_IRL',
                                                'country_LBN',
                                                'country_NAM',
                                                'country_SAM',
                                                'country_SWE',
                                                'country_USA'],
                                       dtype=float)
        # Input data frame into model to predict values
        # Creating StandardScaler instance
        scaler = StandardScaler()
        X_scaler = scaler.fit(input_variables)
        input_variables_scaled = X_scaler.transform(input_variables)

        prediction = model.predict(input_variables_scaled)[0]

        if prediction == 1:
            outcome = 'You survived!'
        else:
            outcome = 'You did not survive :('

        return flask.render_template('main.html',
                                     original_input={'Gender': gender,
                                                     'Age': age,
                                                     'Boarding Class': board_class,
                                                     'Embarked': embarked,
                                                     'Country': country
                                                     },
                                     result=str(outcome)
                                     )


if __name__ == '__main__':
    app.run()
