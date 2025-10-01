import os
import sys
from subprocess import run


def main():
    # Get the absolute path to the virtual environment's Python interpreter
    venv_path = os.path.join(
        os.path.dirname(__file__), ".venv", "Scripts", "python.exe"
    )

    if not os.path.exists(venv_path):
        print("Error: Virtual environment not found!")
        print("Please create a virtual environment first using:")
        print("python virtualvenv venv")
        sys.exit(1)

    # Construct the uvicorn command
    uvicorn_command = [venv_path, "-m", "uvicorn", "main:app", "--reload"]

    try:
        # Run the uvicorn server
        run(uvicorn_command)
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
