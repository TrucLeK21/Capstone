import subprocess

# Path to the Python interpreter inside the virtual environment
venv_python = "/home/trucle/Desktop/git_source/smartscale/mediapipe/env_mediapipe/bin/python"  # Adjust path to your virtual environment

# Path to the script that performs face detection
script_path = "/home/trucle/Desktop/git_source/smartscale/mediapipe/source/test_face_detection.py"

# Path to the image you want to process
image_path = "/home/trucle/Desktop/git_source/smartscale/mediapipe/source/images/timothe.jpg"

# Run the script and capture the output
result = subprocess.check_output([venv_python, script_path, image_path])

# Decode and print the output
result_str = result.decode('utf-8')
print(result_str)
