from pathlib import Path

def get_url():
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir / "data" / "data.txt"
    
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            return str(line)