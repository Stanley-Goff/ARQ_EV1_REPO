#Pruebas automatizadas de conversión y codificación

from django.test import TestCase

from .forms import IntegerConversionForm, TextEncodingForm
from .logica import convertir_entero, analizar_texto
from .models import Conversion


class ComplementoA2Tests(TestCase):
    # Inciso 1.12-A: Probar -1 en 8 bits
    def test_menos_uno_en_8_bits(self):
        resultado = convertir_entero(-1, 8)
        self.assertEqual(resultado["binario"], "11111111")
        self.assertEqual(resultado["hexadecimal"], "FF")
        self.assertEqual(resultado["octal"], "377")
        self.assertEqual(resultado["sin_signo"], 255)
        self.assertEqual(resultado["bit_signo"], "1")

    # Inciso 1.12-B: Probar el mínimo de 8 bits
    def test_menos_128_en_8_bits(self):
        resultado = convertir_entero(-128, 8)
        self.assertEqual(resultado["binario"], "10000000")
        self.assertEqual(resultado["hexadecimal"], "80")
        self.assertEqual(resultado["sin_signo"], 128)

    # Inciso 1.12-C: Probar un valor positivo de 16 bits
    def test_positivo_en_16_bits(self):
        resultado = convertir_entero(1234, 16)
        self.assertEqual(resultado["binario"], "0000010011010010")
        self.assertEqual(resultado["hexadecimal"], "04D2")
        self.assertEqual(resultado["sin_signo"], 1234)

    # Inciso 1.12-D: Rechazar un valor fuera del rango de 8 bits
    def test_valor_fuera_de_rango(self):
        formulario = IntegerConversionForm(
            {"numero-numero": "128", "numero-bits": "8"},
            prefix="numero",
        )
        self.assertFalse(formulario.is_valid())
        self.assertIn("numero", formulario.errors)

    # Inciso 1.12-E: Rechazar una entrada no numérica
    def test_entrada_no_numerica(self):
        formulario = IntegerConversionForm(
            {"numero-numero": "hola", "numero-bits": "8"},
            prefix="numero",
        )
        self.assertFalse(formulario.is_valid())

    # Inciso 1.12-F: Probar la codificación de la letra ñ
    def test_texto_con_enie(self):
        resultado = analizar_texto("ñ")
        self.assertEqual(resultado["caracteres"][0]["codigo_unicode"], "U+00F1")
        self.assertEqual(resultado["caracteres"][0]["utf8_hex"], "C3 B1")
        self.assertEqual(resultado["total_utf8"], 2)
        self.assertEqual(resultado["total_utf16"], 2)

    # Inciso 1.12-G: Probar la codificación de un emoji
    def test_texto_con_emoji(self):
        resultado = analizar_texto("😀")
        self.assertEqual(resultado["caracteres"][0]["codigo_unicode"], "U+1F600")
        self.assertEqual(resultado["caracteres"][0]["utf8_hex"], "F0 9F 98 80")
        self.assertEqual(resultado["total_utf8"], 4)
        self.assertEqual(resultado["total_utf16"], 4)

    # Inciso 1.12-H: Rechazar texto de más de 15 puntos de código
    def test_texto_demasiado_largo(self):
        formulario = TextEncodingForm({"texto-texto": "abcdefghijklmnop"}, prefix="texto")
        self.assertFalse(formulario.is_valid())

    # Inciso 1.12-I: Verificar que se guarde una conversión en SQLite
    def test_guardar_conversion(self):
        resultado = convertir_entero(-1, 8)
        Conversion.objects.create(
            numero=resultado["numero"],
            bits=resultado["bits"],
            binario=resultado["binario"],
            hexadecimal=resultado["hexadecimal"],
            octal=resultado["octal"],
            sin_signo=resultado["sin_signo"],
        )
        self.assertEqual(Conversion.objects.count(), 1)

    # Inciso 1.12-J: Verificar que la página principal responda
    def test_pagina_principal(self):
        respuesta = self.client.get("/")
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Convertidor de enteros")