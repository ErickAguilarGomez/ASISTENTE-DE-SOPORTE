import re

CONTROL_PHRASES = re.compile(
    r"(ignora las instrucciones|olvida tus instrucciones|revela el prompt|modo desarrollador|jailbreak|actúa como admin)",
    re.IGNORECASE
)

EMAIL_PATTERN = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w{2,}\b")
PHONE_PATTERN = re.compile(r"\b\+?\d[\d\-\s]{7,}\d\b")

def sanitize_input(text: str) -> str:
    if CONTROL_PHRASES.search(text):
        raise ValueError("Entrada bloqueada: Intento de inyección detectado.")
    
    text = EMAIL_PATTERN.sub("[EMAIL_REDACTADO]", text)
    text = PHONE_PATTERN.sub("[TELEFONO_REDACTADO]", text)
    return text.strip()

def moderate_output(text: str) -> str:
    safe_text = EMAIL_PATTERN.sub("[EMAIL_REDACTADO]", text)
    return safe_text