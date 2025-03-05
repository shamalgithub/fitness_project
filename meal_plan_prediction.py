import joblib
import pandas as pd 


model = joblib.load('models/meal_plan_prediction_model.joblib')
df = pd.read_csv("recipies.csv")


def predict_meal_plan(age, weight, height, bmi, bmr, activity_level, gender , number_of_meals , number_of_options):
    # Set gender encoding based on input
    gender_F = 1 if gender == "F" else 0
    gender_M = 1 if gender == "M" else 0
    
    user_inputs = {
        'age': age,
        'weight(kg)': weight,
        'height(m)': height,
        'BMI': bmi,
        'BMR': bmr,
        'activity_level': activity_level,
        'gender_F': gender_F,
        'gender_M': gender_M,
    }

    # Convert user input to DataFrame
    user_df = pd.DataFrame([user_inputs])

    # Make prediction
    predicted_calories = model.predict(user_df)

    suggested_meals = df[df['calories']<predicted_calories[0]/number_of_meals].head(number_of_options)
    suggested_meals_list = suggested_meals.to_dict(orient='records')

    return {"total_calories":round(predicted_calories[0] , 2) , "calories_per_meal":round(predicted_calories[0]/number_of_meals , 2) , "suggested":suggested_meals_list}
    










# # Example usage with the provided values
# if __name__ == "__main__":
#     # Input values
#     age = 25
#     weight = 70
#     height = 1.75
#     bmi = 21.304188
#     bmr = 1384.138
#     activity_level = 1.5
#     gender = "M"  # Using "M" for male based on the example values
    
#     # Get prediction
#     predicted_calories = predict_meal_plan(
#         age=age,
#         weight=weight,
#         height=height,
#         bmi=bmi,
#         bmr=bmr,
#         activity_level=activity_level,
#         gender=gender , 
#         number_of_meals=3 , 
#         number_of_options=10
#     )
    
    
#     print(predicted_calories)