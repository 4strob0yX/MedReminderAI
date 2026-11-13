package com.medreminder.ai

import com.medreminder.ai.data.remote.EstadisticasOutDto
import com.medreminder.ai.data.remote.parseApiErrorDetail
import com.medreminder.ai.ui.home.FormaFarmaceutica
import com.medreminder.ai.ui.home.HomeViewModel
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import java.time.ZoneId

class HomeLogicUnitTest {

    @Test
    fun parseHoraPrimeraTomaLocal_handlesArbitrary12hAnd24hFormats() {
        val zone = ZoneId.of("America/Mexico_City")

        val t1 = HomeViewModel.parseHoraPrimeraTomaLocal("07:45 AM", zone)
        assertEquals(7, t1.hour)
        assertEquals(45, t1.minute)

        val t2 = HomeViewModel.parseHoraPrimeraTomaLocal("2:15 pm", zone)
        assertEquals(14, t2.hour)
        assertEquals(15, t2.minute)

        val t3 = HomeViewModel.parseHoraPrimeraTomaLocal("21:30", zone)
        assertEquals(21, t3.hour)
        assertEquals(30, t3.minute)

        val t4 = HomeViewModel.parseHoraPrimeraTomaLocal("12:05 AM", zone)
        assertEquals(0, t4.hour)
        assertEquals(5, t4.minute)
    }

    @Test
    fun formaFarmaceutica_detectsFormsCorrectly() {
        assertEquals(FormaFarmaceutica.GOTAS, FormaFarmaceutica.fromString("jarabe pediátrico 10 ml"))
        assertEquals(FormaFarmaceutica.INYECTABLE, FormaFarmaceutica.fromString("Inyectable ampolla"))
        assertEquals(FormaFarmaceutica.COMPRIMIDOS, FormaFarmaceutica.fromString("tabletas 500 mg"))
        assertEquals(FormaFarmaceutica.COMPRIMIDOS, FormaFarmaceutica.fromString(null))
    }

    @Test
    fun parseApiErrorDetail_handlesFastApiDetailStringAndArray() {
        val strErr = """{"detail":"Código de vinculación expirado"}"""
        assertEquals("Código de vinculación expirado", parseApiErrorDetail(strErr))

        val listErr = """{"detail":[{"loc":["body","codigo"],"msg":"field required"}]}"""
        assertTrue(parseApiErrorDetail(listErr)?.contains("codigo") == true)
    }

    @Test
    fun estadisticasOutDto_defaultsAreCleanNeutral() {
        val dto = EstadisticasOutDto()
        assertEquals(0, dto.rachaDias)
        assertEquals(0, dto.xpHonor)
        assertFalse(dto.escudoActivoHoy)
        assertTrue(dto.adherenciaSemanal.isEmpty())
    }
}
