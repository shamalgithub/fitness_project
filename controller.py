from s3_download import download_s3_file
from s3_upload import upload_to_s3
from excercise_intensity import get_exercise_predictions
from meal_plan_prediction import predict_meal_plan
from sport_analysis import  analyze_arm_angles
import os 
import shutil
from pydantic import BaseModel
from fastapi import APIRouter

class MealPlanInput(BaseModel):
     age:int
     weight:float
     height:float
     bmi:float
     bmr:float 
     activity_level:float 
     gender:str 
     number_of_meals:int 
     number_of_options:int

class ExerciseIntensity(BaseModel):
     actual_weight:float 
     age:int
     gender:str 
     duration:int 
     bmi:float
     height:float 
    #  weather:str 

class SportAnalysis(BaseModel):
     correct_video:str 
     incorrect_video:str 

router = APIRouter()


def clean_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path) 
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  
            print(f"Removed: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

@router.post("/get-meal-plan")
def get_meal_plan(meal_plan:MealPlanInput):
     
    meal_plan = predict_meal_plan(
        age=meal_plan.age,
        weight=meal_plan.weight,
        height=meal_plan.height,
        bmi=meal_plan.bmi,
        bmr=meal_plan.bmr,
        activity_level=meal_plan.activity_level,
        gender=meal_plan.gender, 
        number_of_meals=meal_plan.number_of_meals, 
        number_of_options=meal_plan.number_of_options
    )
    return meal_plan

@router.post("/get-exercise-intensity")
def get_exercise_intensity_level(exercise_intensity:ExerciseIntensity):
     intensity_level = get_exercise_predictions(
          weight=exercise_intensity.actual_weight , 
          age=exercise_intensity.age , 
          gender=exercise_intensity.gender , 
          duration=exercise_intensity.duration , 
          bmi=exercise_intensity.bmi , 
          height=exercise_intensity.height,
        #   weather=exercise_intensity.weather
     )

     return intensity_level

@router.post("/sport-analysis")
def get_sport_analysis(sport_analysis:SportAnalysis):
     correct_video_path = download_s3_file(url=sport_analysis.correct_video , output_path="temp/correct_video.mp4")     
     incorrect_video_path = download_s3_file(url=sport_analysis.incorrect_video , output_path='temp/incorrect_video.mp4')
     result = analyze_arm_angles(correct_video_path=correct_video_path , wrong_video_path=incorrect_video_path , output_folder="temp")

     correct_video = upload_to_s3(file_path=result['correct_pose_video'])
     wrong_video = upload_to_s3(file_path=result['wrong_pose_video'])
     angle_comparison = upload_to_s3(file_path=result['angle_comparison_video'])
     final_graph = upload_to_s3(file_path=result['final_graph'])

     clean_folder(folder_path='temp')

     return {
          "correct_video": correct_video , 
          "wrong_video": wrong_video , 
          "angle_comparison_video":angle_comparison , 
          "final_graph": final_graph,
          "similarity" : result['similarity_percentage']
     }


