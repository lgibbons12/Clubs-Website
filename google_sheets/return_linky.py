import os
def grab():
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "link.txt")

    with open(file_path, "r") as f:
        return f.read()