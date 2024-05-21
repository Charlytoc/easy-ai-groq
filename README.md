# A Template for Building AI Applications with Python (FastAPI) and TypeScript (ViteJs) using Groq as API

## If you're in a Codespace
1. Run the following in the terminal:
```
cp .env.example .env
```
2. Find your Groq key [here](https://console.groq.com/keys)
3. Replace the environment variable `GROQ_API_KEY` with the correct key
4. Restart the development server:
```
bash init-dev.sh
```

## Requirements
- Python (install the latest version [here](https://www.python.org/downloads/))
- NodeJs (install the LTS version [here](https://nodejs.org/en/download/))

## Installation
1. Clone this repository
2. Move to the project directory:
```bash
cd project-directory
```
3. Initialize a virtual environment:
```bash
python -m venv venv
```
or 
```bash
py -m venv venv
```

4. Activate the virtual environment:
```bash
source venv/Scripts/activate
```

5. Install the dependencies:
```bash
pip install -r requirements.txt
npm install
```

6. Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```

7. Add your Groq API key to the `.env` file. Find your API key in your Groq account settings [HERE](https://console.groq.com/keys).

8. Start the application:
```bash
bash init-dev.sh
```

That's it! You can now access the application at http://localhost:8000 and customize it according to your needs.

The `init-dev.sh` script will run both the backend and frontend servers concurrently.

In the future, I will update the repo with other useful scripts for deployment and more. Feel free to contribute and make AI accessible to everyone!