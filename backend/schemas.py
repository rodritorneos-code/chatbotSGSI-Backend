from pydantic import BaseModel

# Solicitud
class ChatRequest(BaseModel):
    prompt: str
    temperature: float = 0.3
    max_tokens: int = 150

# Respuesta
class ChatResponse(BaseModel):
    response: str
    audio_url: str | None = None
    filtered: bool  
