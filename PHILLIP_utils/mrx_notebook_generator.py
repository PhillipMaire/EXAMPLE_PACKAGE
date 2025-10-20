"""
mrx-link Notebook Generator

This script programmatically generates structured, flowchart-style Jupyter
Notebooks that are compatible with the `mrx-link` JupyterLab extension.

Purpose:
- To automate the creation of complex notebook pipelines.
- To embed metadata required by `mrx-link` for defining cell dependencies.
- To serve as a master tool for creating self-documenting notebooks.

How to Use:
1. Run this script directly from your terminal:
   `python3 data/PHILLIP/mrx_notebook_generator.py`

2. The script will produce two files in the same directory:
   - `generated_mrx_script.py`: A Jupytext-compatible Python script. This
     file is the "source of truth" and is ideal for version control.
   - `generated_mrx_script.ipynb`: A standard Jupyter Notebook, ready to be
     opened in JupyterLab with the `mrx-link` extension.

How to Customize:
- Modify the `build_structured_notebook()` function within this file.
- Use the `create_cell()` helper function to add new cells.
- Define parent-child relationships by passing the parent's metadata
  to the child's `create_cell` call.
- Add descriptive content and AI instructions to each cell as needed.
"""
import uuid
import json
import subprocess

def create_cell(name, parents=None, content="", ai_instructions=""):
    """
    Generates a Jupytext-formatted cell string with mrx-link metadata.

    Args:
        name (str): The display name for the cell.
        parents (list, optional): A list of parent metadata objects. Defaults to None.
        content (str, optional): The code/text content for the cell. Defaults to "".
        ai_instructions (str, optional): A comment to be embedded for an AI assistant.

    Returns:
        tuple: A tuple containing the full cell string and the metadata dictionary.
    """
    if parents is None:
        parents = []

    # All the default metadata fields can be hardcoded here
    metadata = {
        "componentType": "CodeCell",
        "copiedOriginId": None,
        "diskcache": False,
        "headerColor": "transparent",
        "id": str(uuid.uuid4()),  # Generate a new, unique ID
        "isComponent": True,
        "name": name,
        "parents": parents
    }

    # Jupytext expects the JSON to be on a single line with no extra spaces
    metadata_str = json.dumps(metadata, separators=(',', ':'))

    # Assemble the full content of the cell, including AI instructions
    full_content = ""
    if ai_instructions:
        # Replace placeholder with the actual ID to make it self-referential
        instruction_text = ai_instructions.replace("{id}", metadata["id"])
        full_content += f"# AI INSTRUCTION: {instruction_text}\n"
    if content:
        full_content += f"{content}\n"

    cell_string = f'# %% canvas={metadata_str}\n'
    if full_content:
        cell_string += f'"""\n{full_content}"""\n'
    
    return cell_string, metadata

def convert_py_to_ipynb(py_path, ipynb_path):
    """
    Converts a Jupytext Python script to a Jupyter Notebook.
    """
    try:
        command = ["jupytext", "--to", "notebook", "--output", ipynb_path, py_path]
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully converted to notebook: {ipynb_path}")
    except FileNotFoundError:
        print("Error: 'jupytext' command not found. Is it installed and in your PATH?")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e.stderr}")

def build_structured_notebook():
    """
    Builds the full notebook script and converts it to an .ipynb file.
    """
    
    # 1. Create the root cells with specific AI instructions
    root_instruction = "This is a root cell. To create a child, copy this cell's ID and add it to the child's 'parents' list. This ID is {id}"
    cell_a_str, meta_a = create_cell("top level A", content="top level A cell data", ai_instructions=root_instruction)
    cell_b_str, meta_b = create_cell("top level B", content="top level B cell data", ai_instructions=root_instruction)

    # 2. Prepare the parent reference objects needed for the child cells
    parent_a_ref = [{"id": meta_a["id"], "name": meta_a["name"]}]
    parent_b_ref = [{"id": meta_b["id"], "name": meta_b["name"]}]

    # 3. Create the child cells with their own AI instructions
    child_instruction = "This is a child cell. Its parent is defined in the 'parents' metadata list above."
    cell_a1_str, _ = create_cell("next level A1", parents=parent_a_ref, content="next level A1", ai_instructions=child_instruction)
    cell_a2_str, _ = create_cell("next level A2", parents=parent_a_ref, content="next level A2", ai_instructions=child_instruction)
    cell_b1_str, _ = create_cell("next level b1", parents=parent_b_ref, content="next level b1", ai_instructions=child_instruction)

    # 4. Assemble the full script content with the Jupytext header
    full_script_content = (
        "# ---\n"
        "# jupyter:\n"
        "#   jupytext:\n"
        "#     text_representation:\n"
        "#       extension: .py\n"
        "#       format_name: percent\n"
        "#       format_version: '1.3'\n"
        "#       jupytext_version: 1.17.2\n"
        "# ---\n\n"
        f"{cell_a_str}\n"
        f"{cell_b_str}\n"
        f"{cell_a1_str}\n"
        f"{cell_a2_str}\n"
        f"{cell_b1_str}\n"
    )

    # 5. Write the final string to a new file
    output_py_file = "data/PHILLIP/generated_mrx_script.py"
    output_ipynb_file = "data/PHILLIP/generated_mrx_script.ipynb"
    try:
        with open(output_py_file, "w") as f:
            f.write(full_script_content)
        print(f"Successfully generated structured script: {output_py_file}")
        
        # 6. Convert the newly created .py file to .ipynb
        convert_py_to_ipynb(output_py_file, output_ipynb_file)

    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    build_structured_notebook()
