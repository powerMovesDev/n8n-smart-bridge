# Project Setup and Execution

This document outlines the process to set up and run the project.

## Step 1: Setting Up the Virtual Environment

Navigate to the project directory and create a virtual environment:

```sh
cd /Users/princeps/Projects/Poly186/n8n-smart-bridge
python3 -m venv project_env
source project_env/bin/activate
```

## Step 2: Installing Dependencies

Install the required packages using the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

If any specific packages are missing or need to be updated, you can install them manually. For example:

```sh
pip install colorama
pip install -U langgraph
```

## Step 3: Running the Project

Once the dependencies are installed, navigate to the appropriate directory and run the project:

```sh
cd bridge/graph
export PYTHONPATH=../../..
python3 workflow.py
```

This will start the project, and you should see the outputs based on the configured workflow.

## Notes

- Ensure that your API keys and authentication tokens are set correctly in your environment or configuration files.
- If you encounter any module import errors, verify that the `PYTHONPATH` is set correctly to include all necessary directories.

---
