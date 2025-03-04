# AgroControl - Aplicación de Registro de Productos Fitosanitarios

Esta aplicación permite a los agricultores llevar un registro claro y organizado de los productos fitosanitarios aplicados en sus cultivos, facilitando el cumplimiento de normativas y contribuyendo a un uso responsable y eficiente de los mismos.

## Estructura del Proyecto
2. **Backend (Python)**: API REST con arquitectura hexagonal

### Backend
- Python 3.8+
- FastAPI

## Instalación y Ejecución

### Backend

1. Navega al directorio `backend`
2. Crea un entorno virtual: `python -m venv venv`
3. Activa el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Instala las dependencias: `pip install -r requirements.txt`
7. Inicia el servidor: `python -m uvicorn app.main:app --reload`
