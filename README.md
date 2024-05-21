# A template to make AI applications with Python (FastAPI) and Typescript (ViteJs) using Groq as APi

## Requirements
- Python (install latest version here https://www.python.org/downloads/)
- NodeJs (install LTS version here https://nodejs.org/en/download/)

## Installation
1. Clone this repository
2. Move to the project directory
```bash
cd project-directory
```
3. Initialize a virtual environment
```bash
python -m venv venv
```
or 
```bash
py -m venv venv
```

4. Activate the virtual environment
```bash
source venv/Scripts/activate
```

5. Install the dependencies
```bash
pip install -r requirements.txt && npm install
```

6. Copy the .env.example file to .env
```bash
cp .env.example .env
```

7. Add your Groq API key to the .env file. Find your API key in your Groq account settings. [HERE](https://console.groq.com/keys)

8. Run the application
```bash
bash init-dev.sh
```


That is it! You can now access the application at http://localhost:8000 and customize it to your needs.

The init-dev.sh script will run the backend and frontend servers concurrently.

In the future I'll update the repo with other useful scripts to deploy and more! Feel free to contribute and make AI accesible to everyone!


