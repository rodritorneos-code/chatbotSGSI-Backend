from llama_cpp import Llama
from .schemas import ChatRequest, ChatResponse
import random
import re
from typing import List, Tuple
import os
import uuid

# ----------- MELO TTS -----------
import torch
from melo.api import TTS
import soundfile as sf


# ========================
#   CARGA DEL MODELO
# ========================

def load_model(model_path: str):
    print(f"🧠 Cargando modelo desde: {model_path}")

    llm = Llama(
        model_path=model_path,

        # CPU threads
        n_threads=8,
        n_batch=256,

        # Optimización
        f16_kv=True,
        flash_attn=True,

        # Contexto
        n_ctx=4096,
        rope_scaling={"type": "dynamic", "factor": 1.0},

        # GPU (usar todas las capas)
        n_gpu_layers=-1,

        # Memoria
        mmap=True,
        numa=False,

        verbose=False
    )

    print("✅ Modelo cargado correctamente en GPU")
    return llm


# ======================
#       FILTRO SGSI
# ======================

def filtro_sgsi(llm, pregunta: str) -> bool:
    """
    Filtra preguntas relacionadas con SGSI y áreas afines.
    Devuelve True si la pregunta es educativa o relevante.
    """

    filtro = (
        f"Pregunta del usuario: {pregunta}\n"
        "Responde solo 'Sí' o 'No':\n"
        "- 'Sí': cualquier pregunta educativa, de aprendizaje, de curiosidad o sobre riesgos relacionada con SGSI, ISO 27001, seguridad de la información o ciberseguridad.\n"
        "- 'No': preguntas irrelevantes o totalmente fuera de contexto."
    )

    out = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "Clasificador rápido de preguntas SGSI."},
            {"role": "user", "content": filtro},
        ],
        temperature=0.0,
        max_tokens=3
    )

    resp = out["choices"][0]["message"]["content"].strip().lower()
    resp = re.sub(r"[^a-záéíóúñ]", " ", resp).strip()

    return resp.startswith("si") or resp.startswith("sí")


# ========================
#   GENERACIÓN DE RESPUESTA
# ========================

def generate_response(llm, prompt: str, temperature: float = 0.2, max_tokens: int = 150) -> str:

    system_prompt = (
        "Eres un asistente especializado en Seguridad de la Información y en normas ISO. "
        "Responde en un máximo de 4 líneas, de manera clara, precisa y profesional."
    )

    out = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=0.95,
        top_k=40,
        repeat_penalty=1.15,
        frequency_penalty=0.2,
    )

    response_text = out["choices"][0]["message"]["content"].strip()
    return response_text or "No se generó respuesta."


# ========================
#   TEXTO → VOZ (MELO TTS)
# ========================

# Cargar Melo TTS solo una vez
device = "cpu"
melo_tts = TTS(language="ES", device=device)

def texto_a_voz_melo(texto: str) -> str:
    """
    Convierte texto a voz usando MeloTTS.
    """
    output_dir = "audio_output"
    os.makedirs(output_dir, exist_ok=True)

    file_name = f"{uuid.uuid4().hex}.wav"
    file_path = os.path.join(output_dir, file_name)

    speaker_id = 0  # voz por defecto

    # IMPORTANTE: Esta versión usa argumentos POSICIONALES
    melo_tts.tts_to_file(
        texto,        # text
        speaker_id,   # speaker_id
        file_path     # output_path
    )

    return file_name
