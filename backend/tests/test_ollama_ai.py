from app.services.ollama_service import (
    _extraer_json_seguro,
    analizar_receta_ollama,
    consultar_medi_ollama,
    obtener_estado_ollama,
    sugerir_medicamento_ia,
)


def test_extraer_json_seguro():
    raw = '```json\n{"title": "Prueba", "risk_score": 0.5}\n```'
    parsed = _extraer_json_seguro(raw)
    assert parsed is not None
    assert parsed["title"] == "Prueba"


def test_estado_ollama_structure():
    st = obtener_estado_ollama()
    assert st.formal_rules_loaded == 6
    assert st.status in ("online", "fallback_local")


def test_consultar_medi_ollama_dosis_omitida():
    res = consultar_medi_ollama(
        query="Olvidé mi pastilla de la mañana, ¿puedo tomar dos juntas en la noche?",
        db=None,
        user=None,
        fallback_name="Carlos",
    )
    assert res.title
    assert res.key_insight
    assert res.golden_rule
    assert res.full_voice_script
    assert len(res.points) >= 1


def test_sugerir_medicamento_ia_catalogo():
    res = sugerir_medicamento_ia(nombre="Losartán", db=None, user=None)
    assert "Losartán" in res.nombre
    assert res.principio_activo == "Losartán potásico"
    assert res.dosis_sugerida == "50 mg"


def test_analizar_receta_ollama():
    res = analizar_receta_ollama(
        texto_receta=(
            "Dr. Roberto Gómez\n"
            "1) Amoxicilina 500 mg cápsulas: tomar 1 cada 8 horas por 7 días.\n"
            "2) Paracetamol 500 mg tabletas: tomar 1 cada 8 horas por 5 días."
        ),
        db=None,
        user=None,
    )
    assert len(res.medicamentos) >= 2
    assert any("Amoxicilina" in m.name for m in res.medicamentos)
