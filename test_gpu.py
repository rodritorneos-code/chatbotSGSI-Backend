from llama_cpp import Llama

# Ruta a tu modelo GGUF
model_path = "C:\\chatbot-SGSI\\Qwen2.5-14B-Instruct-Q4_K_M.gguf"

# Crear instancia con GPU
llm = Llama(
    model_path=model_path,
    n_gpu_layers=-1,   # usar todas las capas en GPU
    n_ctx=1024,
    verbose=True       # muestra información de GPU y VRAM
)

# Prueba simple
out = llm("Hola, ¿cómo estás?", max_tokens=20)
print(out["choices"][0]["text"])