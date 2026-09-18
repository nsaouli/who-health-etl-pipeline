import subprocess

subprocess.run(["python", "src/extract.py"], check=True)
subprocess.run(["python", "src/transform.py"], check=True)
subprocess.run(["python", "src/load.py"], check=True)
