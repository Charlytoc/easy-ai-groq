import os
import json
from fastapi import FastAPI, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException
from starlette.websockets import WebSocketDisconnect
from dotenv import load_dotenv
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from server.completions import create_groq_completion
import logging

load_dotenv()
logger = logging.getLogger(__name__)

IS_DEV_ENV = os.getenv("ENVIRONMENT") == "DEV"


def reload():
    print("Environment: ", os.getenv("ENVIRONMENT"))


app = FastAPI(on_startup=[reload])

if not IS_DEV_ENV:
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
    print("Websocket connection established.")

    try:
        while True:
            data = await websocket.receive_text()
            data_dict = json.loads(data)
            
            if data_dict.get("event") == "ping":
                await websocket.send_text(json.dumps({"event": "pong"}))
                continue

            print(data_dict)  # {'system_prompt': ..., 'prompt': ...}
            
            async def completion_callback(chunk):
                message = {
                    "event": "chunk",
                    "content": chunk.choices[0].delta.content
                }
                if chunk.choices[0].delta.content == None:
                    return
                
                print(chunk.choices[0].delta.content, end="")
                await websocket.send_text(json.dumps(message))

            async def finish_completion_callback():
                message = {
                    "event": "finish",
                    "content": ""
                }
                print("\n")
                await websocket.send_text(json.dumps(message))

            await create_groq_completion(callback=completion_callback, stream=True, user_message=data_dict["prompt"], system_prompt=os.getenv("SYSTEM_PROMPT"))
            await finish_completion_callback()

    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        await websocket.send_text(json.dumps({"event": "error", "message": "Invalid JSON format"}))
    except WebSocketDisconnect as e:
        print(f"WebSocket disconnected: {e}")
    except Exception as e:
        print(f"Error: {e}")
        try:
            await websocket.send_text(json.dumps({"event": "error", "message": str(e)}))
        except RuntimeError:
            print("WebSocket is already closed.")


app.mount("/", StaticFiles(directory="dist", html=True), name="static")


@app.exception_handler(HTTPException)
async def not_found(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        print(
            f"Redirecting to / because {request.url.path} returns this exception: {exc.detail}"
        )
        return RedirectResponse(f"/?next={request.url.path}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")
