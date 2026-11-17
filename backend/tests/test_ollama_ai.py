from app.services.ollama_service import (
    _es_intencion_insertar_medicamento,
    _extraer_json_seguro,
    _parsear_medicamentos_desde_texto,
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


def test_deteccion_intencion_insertar_medicamento():
    assert _es_intencion_insertar_medicamento("Agrega Paracetamol 500 mg cada 8 horas")
    assert _es_intencion_insertar_medicamento("¿Puedes insertar Losartán 50 mg cada 12 horas?")
    assert _es_intencion_insertar_medicamento("Quiero que añadas Omeprazol 20 mg en ayunas")
    assert _es_intencion_insertar_medicamento("Recuérdame tomar Metformina 850 mg a las 8:00 AM")
    assert _es_intencion_insertar_medicamento("Ponme Ibuprofeno 400 mg cada 8h")

    # No confundir dudas clínicas o preguntas de almacenamiento con inserciones
    assert not _es_intencion_insertar_medicamento("¿Puedo tomar paracetamol para el dolor?")
    assert not _es_intencion_insertar_medicamento("¿Cómo debo guardar mi insulina?")
    assert not _es_intencion_insertar_medicamento("¿Qué pasa si agrego ibuprofeno a mi tratamiento?")
    assert not _es_intencion_insertar_medicamento("Olvidé mi dosis de la mañana")


def test_parsear_medicamentos_desde_texto_libre():
    meds = _parsear_medicamentos_desde_texto(
        "Agrega Paracetamol 500 mg cada 8 horas por 5 días con 20 tabletas a las 8:00 a.m. e Ibuprofeno 400 mg cada 12 horas"
    )
    assert len(meds) == 2
    assert meds[0]["nombre"] == "Paracetamol"
    assert meds[0]["dosis"] == "500 mg"
    assert meds[0]["frecuencia_horas"] == 8
    assert meds[0]["duracion_dias"] == 5
    assert meds[0]["cantidad_stock"] == 20
    assert meds[0]["hora_primera_toma"] == "08:00"
    assert meds[1]["nombre"] == "Ibuprofeno"
    assert meds[1]["dosis"] == "400 mg"
    assert meds[1]["frecuencia_horas"] == 12


def test_parsear_medicamento_vitamina_sin_recortar_letra():
    meds = _parsear_medicamentos_desde_texto("Inserta Vitamina D 1000 UI una vez al día")
    assert len(meds) == 1
    assert meds[0]["nombre"] == "Vitamina D"
    assert meds[0]["dosis"] == "1000 UI"
    assert meds[0]["frecuencia_horas"] == 24
