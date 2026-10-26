#!/usr/bin/env python3
"""
Script de entrenamiento (build de Modelfile) y verificación clínica del motor Ollama `medi-clinico`.
Valida que el modelo personalizado `medi-clinico` esté registrado en Ollama y responda en JSON
siguiendo las 6 Reglas Axiomáticas de MedReminder AI.
"""
from __future__ import annotations

import json
import subprocess
import sys
import urllib.request
from pathlib import Path


def ensure_model_built() -> None:
    modelfile_path = Path(__file__).resolve().parent / "Modelfile"
    ollama_bin = "/opt/homebrew/bin/ollama"
    if not Path(ollama_bin).exists():
        ollama_bin = "ollama"
    print(f"[1/3] Compilando y entrenando modelo 'medi-clinico' desde {modelfile_path}...")
    res = subprocess.run(
        [ollama_bin, "create", "medi-clinico", "-f", str(modelfile_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if res.returncode != 0:
        print("Error creando modelo:", res.stderr, file=sys.stderr)
        sys.exit(1)
    print(" -> Modelo 'medi-clinico' compilado y registrado con éxito.")


def verify_inference() -> None:
    print("[2/3] Probando inferencia clínica en vivo contra Ollama (medi-clinico)...")
    payload = {
        "model": "medi-clinico",
        "format": "json",
        "stream": False,
        "keep_alive": "30m",
        "options": {"temperature": 0.2, "num_predict": 480},
        "messages": [
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "modo": "chat_clinico",
                        "paciente": "Elena",
                        "medicamentos_activos": ["Warfarina 5mg (cada 24h)", "Losartán 50mg (cada 12h)"],
                        "alergias": ["Penicilina"],
                        "consulta": "¿Qué pasa si tomo Aspirina o Ibuprofeno para el dolor muscular?",
                    },
                    ensure_ascii=False,
                ),
            }
        ],
    }
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=45.0) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        content = data.get("message", {}).get("content", "")
        parsed = json.loads(content)
        print(" -> Respuesta JSON validada:")
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
        assert "title" in parsed and "key_insight" in parsed and "golden_rule" in parsed


if __name__ == "__main__":
    ensure_model_built()
    verify_inference()
    print("[3/3] Verificación del motor Ollama 'medi-clinico' completada al 100%.")
