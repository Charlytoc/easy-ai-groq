Estos son los pasos que he dado para desarrollar esta app

# 1. Crear un nuevo directorio para el proyecto
```bash
mkdir your-first-ai-ap
```

# 2. Copiar un servidor de FastAPI de otro proyecto en un archivo `main.py` en el directorio del proyecto
```python
import os
import json
from fastapi import FastAPI
from fastapi import WebSocket

from src.completions import create_completion_generator
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import RedirectResponse
# from starlette.exceptions import HTTPException
from dotenv import load_dotenv
from src.utils.print_in_color import print_in_color
# Import dotenv and load the .env file

from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
import logging
load_dotenv()
logger = logging.getLogger(__name__)

def reload():
    print("something printed in the beginning")
    print(os.getenv("ENVIRONMENT"))

app = FastAPI(on_startup=reload())

    
if not os.getenv("ENVIRONMENT") == "DEV":
    logger.info("Setting middleware to redirect HTTP to HTTPS")
    app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"],
)



@app.websocket("/message")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        data_dict = json.loads(data)
        print(data_dict)  # {'system_prompt': ..., 'prompt': ...}
        
        async def completion_callback(chunk):
            print_in_color(chunk.choices[0].delta.content, "yellow")
            message = {
                "event": "chunk",
                "content": chunk.choices[0].delta.content
            }
            await websocket.send_text(json.dumps(message))

        async def finish_completion_callback():
            message = {
                "event": "finish",
                "content": ""
            }
            await websocket.send_text(json.dumps(message))

        await create_completion_generator(data_dict["prompt"],data_dict["system_prompt"], completion_callback)
        await finish_completion_callback()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True, log_level="info")
```



# 3. Crear un .env vacío

```bash
touch .env
```

# 4. Crear una aplicación de ViteJs en el mismo directorio  
```bash
npm create vite@latest front
```

- Seleccionar la opción de "Ignore existing files and continue" para evitar que se sobreescriban los archivos del servidor de FastAPI
- Seleccionar la opción de React + TypeScript + SWC
- Luego, instalar las dependencias
```bash
npm install
```

# 5. Ejecutar `npm run build` para construir la aplicación de ViteJs
```bash
npm run build
```
Sí, así en seco, sin más preámbulos. 

# 6. El paso anterior crea una carpeta `dist` en el directorio del proyecto. Así que con el servidor de FastAPI voy a servir en el root "/" la carpeta `dist` de la aplicación de ViteJs
```python
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="dist", html=True))
```

# 7. Agrego un exception_handler para que si el error es 404 (Not Found) se redirija a la página principal de la aplicación de ViteJs y manejar el enrutamiento del lado del cliente en todo caso excepto que sea una API

```python
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException

@app.exception_handler(HTTPException)
async def not_found(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        print(f"Redirecting to / because {request.url.path} returns this exception: {exc.detail}")
        # query_params = request.query_params
        # query_string = '?' + '&'.join([f"{key}={value}" for key, value in query_params.multi_items()])
        
        return RedirectResponse(f'/?next={request.url.path}')
```

Este código también lo reusé de otro proyecto.



# 8. Inicio un Virtual Environment
```bash
py -m venv venv
```

# 9. Activo el Virtual Environment
```bash
source venv/Scripts/activate
```

# 10. Instalo las dependencias iniciales
```bash
pip install fastapi uvicorn python-dotenv
```

# 11. Agrego en el .env la variable de entorno `ENVIRONMENT` con el valor `DEV`
```bash
echo "ENVIRONMENT=DEV" >> .env
```

# 12. Ejecuto el servidor de FastAPI
```bash
python main.py
```

# 13. Abro el navegador en `http://localhost:8000` y veo la aplicación de ViteJs funcionando 👍🏻🟩

Ahora simplemente es cuestión de seguir desarrollando la aplicación de ViteJs y el servidor de FastAPI para que interactúen entre sí. Eso lo haré en diferentes pasos que explicaré en un vídeo.
