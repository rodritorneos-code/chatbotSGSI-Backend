# 🖥 Backend – Chatbot SGSI

Backend del **Chatbot SGSI** orientado a **Sistema de Gestión de Seguridad de la Información (SGSI)**.  
Desarrollado en **Python** con **FastAPI**, soporte para **GPU (CUDA 12.8)** y ejecución opcional en **CPU**.  
Permite exponer la API para consumo del frontend mediante un túnel seguro con **Cloudflared**.

---

# ⚙ Instalación

## 1️⃣ Crear entorno virtual
Se recomienda un entorno aislado para gestionar dependencias:

### Crear entorno virtual llamado gpu_env311
python -m venv gpu_env311

### Permitir ejecución de scripts temporales
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

### Activar el entorno virtual
.\gpu_env311\Scripts\activate

### Actualizar pip
python -m pip install --upgrade pip

## 2️⃣ Instalar dependencias principales
### Framework web y servidor ASGI
pip install fastapi uvicorn requests

### Librerías de audio
pip install soundfile sounddevice

### Librerías para procesamiento de texto japonés (ejemplo de uso)
pip install mecab-python3 unidic-lite
python -m unidic download

### Text-to-Speech opcional
pip install git+https://github.com/myshell-ai/MeloTTS.git

### 💡 Nota: Ajusta las dependencias según tus necesidades de procesamiento o TTS.

## 3️⃣ Instalar llama-cpp con soporte CUDA
Descarga la versión precompilada de llama-cpp con soporte CUDA 12.8:
https://github.com/boneylizard/llama-cpp-python-cu128-gemma3/releases

### Instalar la versión descargada
pip install --force-reinstall C:\Users\Usuario\Downloads\llama_cpp_python-0.3.8+cu128.gemma3-cp311-cp311-win_amd64.whl

### Verificar instalación
python -c "from llama_cpp import Llama; print('llama_cpp loaded successfully!')"

### Ejecutar prueba de GPU
python test_gpu.py

## Alternativa
### 💡 Modo CPU:
pip install llama-cpp-python

## 🚀 Ejecutar Backend

### Ejecuta la API en modo desarrollo con recarga automática
uvicorn backend.main:app --reload

### Servidor local: http://127.0.0.1:8000

### Puedes usar Postman, curl o el frontend para probar la API.

## 🌍 Exponer backend con Cloudflared

### Para que el frontend desplegado en Vercel pueda comunicarse con tu backend local:

### Instalar Cloudflared
choco install cloudflared -y --force

### Crear túnel público a tu backend local
cloudflared tunnel --url http://127.0.0.1:8000

Esto genera una URL pública temporal.

Configura esta URL en el frontend desplegado para consumir la API.

⚠️ La URL cambia cada vez que reinicias el túnel.

## 🧠 Modelos IA

Opcional usando Hugging Face:

### Instalar librerías Hugging Face
pip install "huggingface_hub==0.19.4" "transformers==4.37.0"

### Autenticarse
hf auth login

### Descargar modelo Qwen2.5-7B en formato GGUF
hf download bartowski/Qwen2.5-7B-Instruct-GGUF Qwen2.5-7B-Instruct.gguf --local-dir ./Qwen2.5-7B-Instruct

### También puedes usar modelos Q4 o Q5
hf download bartowski/Qwen2.5-14B-Instruct-GGUF Qwen2.5-14B-Instruct-Q4_K_M.gguf --local-dir ./Qwen2.5-14B-Q4_K_M
hf download bartowski/Qwen2.5-14B-Instruct-GGUF Qwen2.5-14B-Instruct-Q5_K_M.gguf --local-dir ./Qwen2.5-14B-Instruct

## 📈 Características Técnicas

### Arquitectura backend separada del frontend
### Soporte GPU (CUDA) y CPU
### Integración de modelos LLM locales
### API REST para comunicación con frontend
### Exposición pública mediante Cloudflared
### Escalable y modular

## 🔧 Verificación de Sistema
### Verificar GPU NVIDIA
nvidia-smi

### Verificar versión CUDA
nvcc --version

## 📜 Licencia
Código bajo licencia MIT

## 👨‍💻 Autor
Rodrigo Alexander Pinto Niño
