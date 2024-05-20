# Una plantilla para hacer aplicaciones de IA con Python (FastAPI) y TypeScript (ViteJs) utilizando Groq como API

## Requisitos
- Python (instale la versión más reciente aquí https://www.python.org/downloads/)
- NodeJs (instale la versión LTS aquí https://nodejs.org/en/download/)

## Instalación
1. Clona este repositorio
2. Muévete al directorio del proyecto
```bash
cd directorio-del-proyecto
```
3. Inicializa un entorno virtual
```bash
python -m venv venv
```
o 
```bash
py -m venv venv
```

4. Activa el entorno virtual
```bash
source venv/bin/activate
```

5.Instala las dependencias
```bash
pip install -r requirements.txt
npm install
```

6. Copia el archivo .env.example a .env
```bash
cp .env.example .env
```

7. Agrega tu clave de API de Groq al archivo .env. Encuentra tu clave de API en la configuración de tu cuenta de Groq. [AQUÍ](https://console.groq.com/keys)

8. Inicia la aplicación
```bash
bash init-dev.sh
```


¡Eso es todo! Ahora puedes acceder a la aplicación en http://localhost:8000 y personalizarla según tus necesidades.

El script init-dev.sh ejecutará los servidores backend y frontend de forma concurrente.

En el futuro, actualizaré el repo con otros scripts útiles para desplegar y más. ¡No dudes en contribuir y hacer que la IA sea accesible para todos!