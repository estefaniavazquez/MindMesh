# MindMesh

## Steps to run the project

1. Create a virtual environment: run `python -m venv .venv` 
2. Activate the virtual environment: 
    a. For Windows: run `.venv/Scripts/activate`
    b. For MacOS/Linux: run `source .venv/bin/activate`
3. Install the dependencies: run `pip install -r requirements.txt` 
4. Create an access token from Hugging Face to get access to the repository: `openai/gpt-oss-120b`
5. Set the access token as an environment variable: 
    a. For Windows: run `$env:HF_TOKEN="<your_huggingface_api_key>"`
