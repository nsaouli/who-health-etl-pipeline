import subprocess

subprocess.run(["python", "src/extract.py"])
subprocess.run(["python", "src/transform.py"])
subprocess.run(["python", "src/load.py"])
