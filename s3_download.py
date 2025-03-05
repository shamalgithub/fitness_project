import requests
import os

def download_s3_file(url, output_path):

    try:
        
        response = requests.get(url, stream=True)
        response.raise_for_status()  
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    
        return output_path
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return False


# download_s3_file(url="https://rp-projects-public.s3.amazonaws.com/Incorrect 1.mp4" , output_path="temp/incorrect.mp4")