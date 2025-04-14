# ✅ insider_targets_loader.py - Loads insider targets saved from reel scanner

def load_insider_targets(file="insider_targets.txt"):
    results = []
    try:
        with open(file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("["):  # skip metadata lines
                    results.append(line)
    except FileNotFoundError:
        print("⚠️ No insider_targets.txt found.")
    return results
