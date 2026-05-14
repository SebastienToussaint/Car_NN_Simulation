import subprocess
import os
import sys

# Get project path
project_directory_path = os.path.abspath(__file__)
project_directory_path = project_directory_path[0:project_directory_path.rfind("\\")]

# Install dependencies
subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

