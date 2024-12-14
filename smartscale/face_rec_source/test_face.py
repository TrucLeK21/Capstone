import face_recognition
import pickle
import cv2
import numpy as np
import logging
from imutils import paths
import glob
import os
import argparse


pickleFilePath = "/home/trucle/Desktop/git_source/smartscale/face_rec_source/encodings.pickle"
datasetPath = "/home/trucle/Desktop/git_source/smartscale/face_rec_source/dataset"
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# List of names that will trigger the GPIO pin
class FaceIdentifier():
    cv_scaler = 6
    tolerance = 0.42
    
    @staticmethod
    def clean_images(extensions=("*.jpg", "*.png", "*.jpeg")):
        # Loop through each file extension
        for ext in extensions:
            # Get all files matching the extension
            files = glob.glob(os.path.join(datasetPath, ext))
            for file in files:
                try:
                    os.remove(file)  # Delete the file
                    logging.info(f"Deleted: {file}")
                except Exception as e:
                    logging.error(f"Error deleting {file}: {e}")
    
    @classmethod
    def set_tolerance(cls, value):
        cls.tolerance = value
        
    @classmethod    
    def train_model(cls, id):
        logging.info("Start processing faces...")
        imagePaths = list(paths.list_images(datasetPath))
        knownEncodings = []

        for (i, imagePath) in enumerate(imagePaths):
            logging.info(f"Processing image {i + 1}/{len(imagePaths)}")
            name = imagePath.split(os.path.sep)[-2]
            
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            boxes = face_recognition.face_locations(rgb, model="hog")
            encodings = face_recognition.face_encodings(rgb, boxes)
            
            for encoding in encodings:
                knownEncodings.append(encoding)

        logging.info("Serializing encodings...")
        data = {'name': id, 'encodings': knownEncodings}

        # Check if the pickle file exists
        if os.path.exists(pickleFilePath):
            # File exists, load the list from the pickle file
            with open(pickleFilePath, 'rb') as file:
                known_faces = pickle.load(file)
                # Append a new data to the list
                known_faces.append(data)
        else:
            # File does not exist, create a new list
            known_faces = [data]
            
        # Save the updated list back to the pickle file
        with open(pickleFilePath, 'wb') as file:
            pickle.dump(known_faces, file)
        logging.info("Training complete. Encodings saved to 'encodings.pickle'")
        
            
    @classmethod
    def check_known_faces(cls, testImagePath):
        # Get the encodings
        resized_image = cv2.imread(testImagePath)
        rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        identify = "unknown"

        resized_image = cv2.resize(rgb, (0, 0), fx=(1/cls.cv_scaler), fy=(1/cls.cv_scaler))

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(resized_image)
        face_encodings = face_recognition.face_encodings(resized_image, face_locations, model='large')
        
        with open(pickleFilePath, "rb") as file:
            faces_list = pickle.loads(file.read())


        best_match_distance = 1

        for face in faces_list:
            for face_encoding in face_encodings:
                # Check if the detected face is in known_face_list
                matches = face_recognition.compare_faces(face['encodings'], face_encoding, tolerance=cls.tolerance)
                # Use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(face['encodings'], face_encoding)
                logging.info(face_distances)
                best_match_index = np.argmin(face_distances)
                
                # If threre one false result go to the next iterate immediately
                if False in matches:
                    continue
                
                # If found a known face store the best distance to compare if there's other known faces 
                if face_distances[best_match_index] < best_match_distance:
                    best_match_distance = face_distances[best_match_index]  
                    identify = face['name']
            
        return identify


def exec_face_recognition():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Process some arguments.")
    
    # Add arguments
    parser.add_argument("--option", type=str, default="train-model", help="An option argument")
    parser.add_argument("arg1", type=str, help="Argument")
    
    # Parse arguments
    args = parser.parse_args()
    if args.option == "train-model":
        # Pass new user id to train model
        FaceIdentifier.train_model(args.arg1)
    else:
        # If option is to identify a face, the argument is image path    
        identify = FaceIdentifier.check_known_faces(args.arg1)
        # Return stdout result for parent process
        
        if identify == "unknown":
            logging.info("Unknown face found")
        else:
            logging.info(f"Found known face with id: {identify}")
            
        print(f"Identify: {identify}")

if __name__ == "__main__":
    exec_face_recognition()