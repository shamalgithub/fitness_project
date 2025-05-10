import boto3
import os 



def upload_to_s3(file_path,bucket_name="rp-projects-public", 
                 aws_access_key="************", 
                 aws_secret_key="************"):
  
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    
    # Get the filename from the path
    upload_file_name = f"{os.path.basename(file_path)}"
    
    # Upload the file
    s3_client.upload_file(file_path, bucket_name, upload_file_name)
    
    # Generate and return the URL
    file_url = f"https://{bucket_name}.s3.amazonaws.com/{upload_file_name}"
    
    return file_url


# print(upload_to_s3(file_path="/home/shamal/code/freelance_projects/fitness_project/abrasions (1) (1).jpg"))
# https://rp-projects-public.s3.amazonaws.com/Correct.mp4
# https://rp-projects-public.s3.amazonaws.com/Incorrect 1.mp4

#right : https://rp-projects-public.s3.amazonaws.com/IMG_7699.MOV
#wrong : https://rp-projects-public.s3.amazonaws.com/IMG_7702.MOV