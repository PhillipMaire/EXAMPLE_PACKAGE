import subprocess
import os
import argparse

def convert_notebook_to_py(notebook_path):
    """
    Converts a Jupyter Notebook (.ipynb) to a Python script (.py)
    with percent cell formatting using jupytext.
    """
    if not os.path.exists(notebook_path):
        print(f"Error: Notebook file not found at {notebook_path}")
        return

    print(f"Converting {notebook_path} to a Python script...")
    
    try:
        # Using --sync will also pair the files, --to just converts.
        # Let's just convert to not add extra metadata to the notebook unless desired.
        subprocess.run(
            ["jupytext", "--to", "py:percent", notebook_path],
            check=True
        )
        py_path = os.path.splitext(notebook_path)[0] + ".py"
        print(f"Successfully converted to {py_path}")
    except FileNotFoundError:
        print("Error: 'jupytext' command not found.")
        print("Please make sure jupytext is installed and in your PATH.")
        print("You can install it with: pip install jupytext")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during conversion: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a Jupyter Notebook to a Python script.")
    parser.add_argument("notebook_file", help="The path to the .ipynb file to convert.")
    args = parser.parse_args()
    
    convert_notebook_to_py(args.notebook_file)
