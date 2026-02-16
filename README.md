# Asistente de soporte al cliente

Este asistente ayuda a los agentes de soporte procesando consultas y devolviendo respuestas estructuradas en JSON con métricas de rendimiento y seguridad aplicadas.

##  Iniciar proyecto
Ejecuta los siguientes comandos o instrucciones acorde al orden

1. **Entorno Virtual**:
   python -m venv venv


   source venv/bin/activate  # Mac/Linux


   .\venv\Scripts\activate   # Windows

3. **Instalacion**:
    pip install -r requirements.txt

4. **Variables de entorno**:
    Crea un archivo .env basado en .env.example y agrega tu OPENAI_API_KEY.

5. **Ejecución**:
    python app/run_query.py "Mi pedido #12345 no ha llegado"

6. **Tests**:
    python -m pytest -v
    
