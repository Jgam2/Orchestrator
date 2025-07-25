# Test imports
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from orchestrator.main import Orchestrator
    print("Successfully imported Orchestrator")
except Exception as e:
    print(f"Error importing Orchestrator: {e}")

