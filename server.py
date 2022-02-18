import os

if os.name == "nt":
    os.system("python src\\server.py")
else:
    os.system("python3 src/server.py")
