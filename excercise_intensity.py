import pandas as pd
import numpy as np
import joblib
import os

# Define the list of exercises based on the training data
exercise_list = [
    "Burpees", 
    "Diamond Push Ups", 
    "High Knees", 
    "Squats", 
    "Sit Ups", 
    "Jumping Lunges", 
    "Lunges", 
    "Jumping Squats", 
    "Push Ups", 
    "Leg Raises"
]

def get_exercise_predictions(gender, age, weight, height, bmi, duration, models_dir="models/fitness"):
    """
    A single function that predicts Set Count, Rep Count, and Intensity Rate for all exercises.

    Parameters:
    gender: 'Male' or 'Female' (str)
    age: Age of person (int)
    weight: Weight in kg (float)
    height: Height in cm (float)
    bmi: Body Mass Index (float)
    duration: Duration of exercise in minutes (int/float)
    models_dir: Directory containing the saved model files (str)

    Returns:
    Dictionary with exercise names as keys and prediction dictionaries as values
    """
    # Load the models
    set_count_model_path = os.path.join(models_dir, "set_count_model.joblib")
    rep_count_model_path = os.path.join(models_dir, "rep_count_model.joblib")
    intensity_model_path = os.path.join(models_dir, "intensity_rate_model.joblib")
    
    set_count_model = joblib.load(set_count_model_path)
    rep_count_model = joblib.load(rep_count_model_path)
    intensity_model = joblib.load(intensity_model_path)
    
    # Dictionary to store results
    results = {}
    
    # Make predictions for each exercise
    for exercise in exercise_list:
        # Create a dataframe with the input features
        input_data = pd.DataFrame({
            'Exercise Name': [exercise],
            'Gender': [gender],
            'Age': [age],
            'Weight': [weight],
            'Height': [height],
            'BMI': [bmi],
            'Duration': [duration]
        })
        
        # Make predictions
        set_count_pred = set_count_model.predict(input_data)[0]
        rep_count_pred = rep_count_model.predict(input_data)[0]
        intensity_pred = intensity_model.predict(input_data)[0]
        
        # Round set count and rep count to integers
        set_count_pred_rounded = round(set_count_pred)
        rep_count_pred_rounded = round(rep_count_pred)
        
        # Store predictions in dictionary
        results[exercise] = {
            'Set Count': set_count_pred_rounded,
            'Rep Count': rep_count_pred_rounded,
            'Intensity Rate': intensity_pred
        }
    
    return results

# Example usage
if __name__ == "__main__":
    # Person details
    gender = 'Male'
    age = 30
    weight = 75.0
    height = 175.0
    bmi = 24.5
    duration = 45
    
    # Get predictions for all exercises as a dictionary
    predictions = get_exercise_predictions(
        gender=gender,
        age=age,
        weight=weight,
        height=height,
        bmi=bmi,
        duration=duration
    )
    
    # Print the raw dictionary
    print(predictions)


    
    