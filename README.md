# MindMesh

## Steps to run the project

1. Create a virtual environment, run: `python -m venv .venv` 
2. Activate the virtual environment: 
   - For Windows, run: `.venv/Scripts/activate`
   - For MacOS/Linux, run: `source .venv/bin/activate`
3. Install the dependencies, run: `pip install -r requirements.txt` 
4. Create an access token from Hugging Face to get access to the repository: `openai/gpt-oss-120b`
   - You can create an access token by following the instructions [here](https://huggingface.co/docs/hub/security-tokens)
5. Set the access token as an environment variable: 
    a. For Windows, run: `$env:HF_TOKEN="<your_huggingface_api_key>"`

## Steps to run a single Gradio page

1. Execute the file you want to run: `python -m <package_path>.<file_name>`
   - Include the `-m` flag to run the file as a module, which ensures that relative imports work correctly from the project root.
