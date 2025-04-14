# Full System Scan - For all bot modules!

import importlib
import traceback

# List of all modules to be tested
modules = [
    "main",
    "ai_classifier",
    "ai_trainer",
    "dexscreener_scanner",
    "telegram_sniper",
    "google_sheet_logger",
    "sniper_loop",
    "sniper_system_check",
    "risk_filters"
]

# Function to test each module
def test_module(module_name):
    try:
        # Dynamically import the module
        module = importlib.import_module(module_name)
        
        # Check if the module has a 'test' function to run
        test_func = getattr(module, "test", None)
        if callable(test_func):
            print(f"Running {module_name} test...")
            test_func()  # Run the test function from each module
            print(f"{module_name} passed the test!\n")
        else:
            print(f"{module_name} does not have a test function!\n")
    
    except Exception as e:
        print(f"ERROR in {module_name}:\n{traceback.format_exc()}\n")

# Scan each module
def full_scan():
    print("🔥 FULL SYSTEM SCAN STARTED! 🔥")
    
    for module in modules:
        test_module(module)
    
    print("🔥 FULL SYSTEM SCAN COMPLETE! 🔥")

# Run the full scan
full_scan()
