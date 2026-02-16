# ASISTENTE DE SOPORTE

Resumen

Hice un asistente que clasifica consultas y reclamos de usuarios, generando resúmenes en formato JSON para que los asesores de atención al cliente puedan utilizarlos fácilmente.

Arquitectura

- Código principal en `app/`. Prompts en `prompts/`. Métricas en `metrics/metrics.json`.
- Se usa un entorno virtual local y llamadas HTTP a la API de OpenAI.

Técnicas de prompting que usé

- Few-shot: Incluí 1 ejemplo la prompt principal para fijar el formato de salida y reducir el consumo de tokens, ya que el modelo elegido es eficiente para esta tarea.
- Instrucción con esquema: Pedí salidas en formato JSON para facilitar el procesamiento automático.
- Razonamiento por pasos: Para tareas complejas, solicité pasos intermedios para mejorar la claridad y precisión de las respuestas.

Métricas de ejemplo

- Latencia promedio: 450 ms por consulta.
- Precisión: 86%.
- Tokens por respuesta: ~320.

Principales problemas

- Manejo de credenciales: Al principio usé un token en la URL, lo cual es inseguro. Ahora uso un archivo `.env` para almacenar variables sensibles.
- Validación de salidas: El modelo a veces no respetaba el esquema JSON, lo que requería validaciones adicionales.
- Coste y latencia: Prompts más largos o con más ejemplos aumentan el costo y el tiempo de respuesta.

Mejoras prácticas

- Usar `.env` para manejar credenciales y evitar exponerlas en el código.
- Implementar validaciones automáticas para las salidas JSON y reintentar consultas si fallan.
- Optimizar prompts: Reducir el número de ejemplos y ajustar la temperatura para equilibrar calidad y costo.

Cómo probar rápido

1. Crear y activar el entorno virtual e instalar dependencias con `pip install -r requirements.txt`.
2. Ejecutar `python -m app.run_query`.
3. Revisar `metrics/metrics.json` para ver los resultados.




