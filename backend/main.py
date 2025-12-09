from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import uuid

from .schemas import ChatRequest, ChatResponse
from .utils import (
    load_model,
    generate_response,
    filtro_sgsi,
    texto_a_voz_melo
)

# Crear instancia de FastAPI
app = FastAPI(title="Chatbot SGSI", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================================
# Crear carpeta de audios si no existe
# ===============================================
os.makedirs("audio_output", exist_ok=True)

# ===============================================
# Cargar modelo (solo uno, para no duplicar VRAM)
# ===============================================
MODEL_PATH = r"C:\chatbot-SGSI\Qwen2.5-14B-Instruct-Q5_K_M.gguf"

model = load_model(MODEL_PATH)

models = {
    "CHAT": model,
    "FILTRO": model,    # ambos apuntan al MISMO modelo en GPU
}

# ===============================================
#             ENDPOINT PRINCIPAL
# ===============================================
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):

    modelo_principal = models["CHAT"]
    modelo_filtro = models["FILTRO"]

    # --- PASO 1: Filtro SGSI usando Qwen ---
    if not filtro_sgsi(modelo_filtro, request.prompt):
        texto = (
            "Tu consulta no parece estar relacionada con Seguridad de la Información o con un SGSI. "
            "Si deseas continuar, puedes reformularla para enfocarla en temas como riesgos, controles, "
            "políticas o normas ISO/IEC 27001."
        )

        audio_file = texto_a_voz_melo(texto)

        return ChatResponse(
            response=texto,
            audio_url=f"/audio/{audio_file}",
            filtered=True
        )

    # --- PASO 2: Qwen responde ---
    respuesta = generate_response(
        modelo_principal,
        request.prompt,
        request.temperature,
        request.max_tokens
    )

    audio_file = texto_a_voz_melo(respuesta)

    return ChatResponse(
        response=respuesta,
        audio_url=f"/audio/{audio_file}",
        filtered=False
    )

# Servir archivos WAV
app.mount("/audio", StaticFiles(directory="audio_output"), name="audio")
