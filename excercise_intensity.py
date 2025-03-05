import pandas as pd
import numpy as np
import joblib
import os


def predict_exercise_intensity(exercise, actual_weight, age, gender, duration, bmi, height, weather, 
                               model_path="models/exercise_intensity_model.joblib"):

    # Load the model
    model = joblib.load(model_path)
    
    # Create a dataframe with the input features
    input_data = pd.DataFrame({
        'Exercise': [exercise],
        'Actual Weight': [actual_weight],
        'Age': [age],
        'Gender': [gender],
        'Duration': [duration],
        'BMI': [bmi],
        'Height (m)': [height],
        'Weather Conditions': [weather]
    })
    
    # Make prediction
    prediction = model.predict(input_data)
    return prediction[0]


def get_excercise_intensity_values(actual_weight , age , gender , duration , bmi , height , weather):

    excercise_list = ["Exercise 1" , "Exercise 2" , "Exercise 3" , "Exercise 4" , "Exercise 5" , "Exercise 6" , "Exercise 7" , "Exercise 8" , "Exercise 9" , "Exercise 10"]
    result = []
    for i in excercise_list:
        intensity = predict_exercise_intensity(
                exercise=i,          
                actual_weight=actual_weight,
                age=age,
                gender=gender,
                duration=duration,
                bmi=bmi,
                height=height,
                weather=weather
            )
        # Convert numpy.int64 to standard Python int
        if isinstance(intensity, np.integer):
            intensity = int(intensity)
        # Convert numpy.float64 to standard Python float
        elif isinstance(intensity, np.floating):
            intensity = float(intensity)
        
        result.append({i: intensity})
   
    
    return result


    
    