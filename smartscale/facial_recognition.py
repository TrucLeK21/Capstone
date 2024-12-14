import subprocess

# Define paths
venv_python = "face_rec_source/face_recognition_venv/bin/python"
script_path = "face_rec_source/test_face.py"

datasetPath = "face_rec_source/dataset/image.jpg"
testImagepPath = "face_rec_source/image_to_test/image.jpg"


def run_face_recognition(option, arg1):

    # Script arguments
    script_args = ["--option", option, arg1]

    # Build the command
    command = [venv_python, script_path] + script_args
    final_output = None
    
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        try:
            for line in process.stderr:
                print(line, end="")  # Print error logs in real-time
            
            # Process logs in real-time
            for line in process.stdout:
                print(line, end="")  # Print real-time log output
                if line.startswith("Identify:"):  # Identify final output
                    final_output = line.split("Identify:")[1].strip()

            process.wait()  # Ensure the process completes

            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, command)
            
            return final_output

        except Exception as e:
            print(f"Error: {e}")

# run_face_recognition("test-face", testImagepPath)