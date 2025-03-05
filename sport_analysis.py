import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from moviepy.editor import ImageSequenceClip
import os
from scipy.spatial.distance import cosine

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360-angle

    return angle

def calculate_cosine_similarity(list1, list2):
    """
    Calculate cosine similarity between two lists.
    If lists have different lengths, truncate the longer one.
    """
    # Ensure lists are numpy arrays
    list1 = np.array(list1)
    list2 = np.array(list2)
    
    # Truncate the longer list to match the shorter one
    min_length = min(len(list1), len(list2))
    list1 = list1[:min_length]
    list2 = list2[:min_length]
    
    # Calculate cosine similarity
    # Cosine similarity = 1 - cosine distance
    # Higher value (closer to 1) means more similar
    if np.all(list1 == 0) or np.all(list2 == 0):
        return 0  # Handle all-zero vectors
    
    similarity = 1 - cosine(list1, list2)
    return similarity

def process_video(video_path):
    angles = []
    frames = []
    cap = cv2.VideoCapture(video_path)
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    # Get video dimensions for text positioning
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            if results.pose_landmarks:
                # Draw the pose annotations on the image
                annotated_image = image.copy()
                mp_drawing.draw_landmarks(
                    annotated_image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                
                landmarks = results.pose_landmarks.landmark

                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                angle = calculate_angle(shoulder, elbow, wrist)
                angles.append(angle)
                
                # Convert normalized coordinates to pixel values for visualization
                cx, cy = int(elbow[0] * width), int(elbow[1] * height)
                
                # Draw angle at elbow position
                cv2.putText(annotated_image, f"{angle:.1f} degrees", 
                           (cx - 50, cy - 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                
                # Draw angle arc visualization
                scale = 50  # Scale for visualization
                a_scaled = (int(shoulder[0] * width), int(shoulder[1] * height))
                b_scaled = (cx, cy)  # Elbow position
                c_scaled = (int(wrist[0] * width), int(wrist[1] * height))
                
                # Draw lines for angle visualization
                cv2.line(annotated_image, b_scaled, a_scaled, (0, 255, 0), 3)
                cv2.line(annotated_image, b_scaled, c_scaled, (255, 0, 0), 3)
                
                # Add an arc to visualize the angle
                start_angle = np.degrees(np.arctan2(a_scaled[1] - b_scaled[1], a_scaled[0] - b_scaled[0]))
                end_angle = np.degrees(np.arctan2(c_scaled[1] - b_scaled[1], c_scaled[0] - b_scaled[0]))
                
                # Ensure correct angle representation
                if start_angle < 0:
                    start_angle += 360
                if end_angle < 0:
                    end_angle += 360
                    
            
                
                frames.append(annotated_image)

    cap.release()
    return angles, frames

def analyze_arm_angles(correct_video_path, wrong_video_path, output_folder='temp'):
    """
    Analyze arm angles from correct and wrong technique videos and generate comparison visualizations
    
    Args:
        correct_video_path (str): Path to the video with correct technique
        wrong_video_path (str): Path to the video with wrong technique
        output_folder (str): Path to folder where outputs will be saved
    
    Returns:
        dict: Dictionary containing paths to the generated videos and images and similarity percentage
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Create temporary directory for frames
    temp_frames_path = os.path.join(output_folder, 'temp_frames')
    if not os.path.exists(temp_frames_path):
        os.makedirs(temp_frames_path)
    
    # Process both videos
    print("Processing correct technique video...")
    correct_angles, correct_pose_frames = process_video(correct_video_path)
    
    print("Processing wrong technique video...")
    wrong_angles, wrong_pose_frames = process_video(wrong_video_path)
    
    # Calculate cosine similarity between the angle sequences
    similarity = calculate_cosine_similarity(correct_angles, wrong_angles)
    similarity_percentage = similarity * 100
    print(f"Calculated similarity: {similarity_percentage:.2f}%")
    
    # Save the pose analysis videos
    print("Creating pose analysis videos...")
    correct_pose_output = os.path.join(output_folder, 'correct_pose_analysis.mp4')
    wrong_pose_output = os.path.join(output_folder, 'wrong_pose_analysis.mp4')
    
    # Create video clips from pose frames
    correct_pose_clip = ImageSequenceClip([frame for frame in correct_pose_frames], fps=15)
    correct_pose_clip.write_videofile(correct_pose_output)
    
    wrong_pose_clip = ImageSequenceClip([frame for frame in wrong_pose_frames], fps=15)
    wrong_pose_clip.write_videofile(wrong_pose_output)
    
    # Create frames for angle comparison animation
    print("Creating angle comparison animation...")
    max_frames = max(len(correct_angles), len(wrong_angles))
    correct_times = list(range(len(correct_angles)))
    wrong_times = list(range(len(wrong_angles)))
    
    # Set dark style for plots
    plt.style.use('dark_background')
    
    for frame in range(max_frames):
        plt.figure(figsize=(12, 6))
        
        # Plot correct technique data up to current frame
        if frame < len(correct_angles):
            plt.plot(correct_times[:frame+1], correct_angles[:frame+1], 
                     color='#00ff00', linewidth=2, label='Correct Technique')
        
        # Plot wrong technique data up to current frame with dotted line
        if frame < len(wrong_angles):
            plt.plot(wrong_times[:frame+1], wrong_angles[:frame+1], 
                     color='#ff3333', linestyle='--', linewidth=2, label='Wrong Technique')
        
        plt.xlim(0, max_frames)
        plt.ylim(0, 180)
        plt.xlabel('Frame Number', color='white')
        plt.ylabel('Arm Angle (degrees)', color='white')
        plt.title(f'Arm Angle Comparison\nSimilarity: {similarity_percentage:.2f}%', color='white', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Save frame
        frame_path = os.path.join(temp_frames_path, f'frame_{frame:04d}.png')
        plt.savefig(frame_path, facecolor='black')
        plt.close()
    
    # Create video from frames
    frames = []
    for frame in range(max_frames):
        frame_path = os.path.join(temp_frames_path, f'frame_{frame:04d}.png')
        frames.append(frame_path)
    
    # Create video clip
    angle_comparison_output = os.path.join(output_folder, 'angle_comparison.mp4')
    clip = ImageSequenceClip(frames, fps=15)
    clip.write_videofile(angle_comparison_output)
    
    # Display final comparison graph
    plt.figure(figsize=(12, 6))
    plt.plot(correct_times, correct_angles, color='#00ff00', linewidth=2, label='Correct Technique')
    plt.plot(wrong_times, wrong_angles, color='#ff3333', linestyle='--', linewidth=2, label='Wrong Technique')
    plt.xlim(0, max_frames)
    plt.ylim(0, 180)
    plt.xlabel('Frame Number', color='white')
    plt.ylabel('Arm Angle (degrees)', color='white')
    plt.title(f'Final Arm Angle Comparison\nSimilarity: {similarity_percentage:.2f}%', color='white', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Save the final graph as an image
    final_graph_output = os.path.join(output_folder, 'final_comparison_graph.png')
    plt.savefig(final_graph_output, facecolor='black')
    
    # Clean up temporary frames
    for frame_path in frames:
        os.remove(frame_path)
    os.rmdir(temp_frames_path)
    
    print("Analysis complete! All outputs saved to:", output_folder)
    print(f"Movement similarity: {similarity_percentage:.2f}%")
    
    return {
        "correct_pose_video": correct_pose_output,
        "wrong_pose_video": wrong_pose_output,
        "angle_comparison_video": angle_comparison_output,
        "final_graph": final_graph_output,
        "similarity_percentage": similarity_percentage
    }

# # # Example usage:
# result = analyze_arm_angles(
#     correct_video_path="/home/shamal/code/freelance_projects/fitness_project/correct side 01.MOV",
#     wrong_video_path="/home/shamal/code/freelance_projects/fitness_project/wrong side 01- 01.MOV",
#     output_folder="temp"
# )

# print(result)