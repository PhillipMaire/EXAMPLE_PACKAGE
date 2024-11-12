
#!/bin/zsh

# chmod +x AUTO_START.sh && ./AUTO_START.sh


# Get the parent directory name to use as the kernel name
KERNEL_NAME=$(basename "$PWD")

# Create a virtual environment
/opt/homebrew/opt/python@3.10/bin/python3.10 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip and setuptools
pip install --upgrade pip
pip install --upgrade setuptools

# Install necessary packages
pip install mrx-link
pip install ipykernel notebook jupyterlab

# Uninstall any existing kernel with the same name
jupyter kernelspec list
jupyter kernelspec uninstall -y "$KERNEL_NAME"

# Install the new kernel with the parent directory name
python -m ipykernel install --user --name="$KERNEL_NAME" --display-name "$KERNEL_NAME"

# Modify the kernel.json to ensure it uses the Python interpreter from the virtual environment by default
KERNEL_DIR=$(jupyter kernelspec list | grep "$KERNEL_NAME" | awk '{print $2}')
echo '{
 "argv": [
  "'"$PWD"'/.venv/bin/python",
  "-m",
  "ipykernel_launcher",
  "-f",
  "{connection_file}"
 ],
 "display_name": "'"$KERNEL_NAME"'",
 "language": "python"
}' > "$KERNEL_DIR/kernel.json"

# List Jupyter extensions
jupyter labextension list
jupyter server extension list

# Start JupyterLab
jupyter lab
