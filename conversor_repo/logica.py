RANGOS = {
    8: (-(2**7), (2**7) - 1),
    16: (-(2**15), (2**15) - 1),
    32: (-(2**31), (2**31) - 1),
}


def convertir_entero(numero: int, bits: int) -> dict:
    # Inciso 1.5-A: Validar el tamaño y el rango del entero
    if bits not in RANGOS:
        raise ValueError("El tamaño debe ser 8, 16 o 32 bits.")

    minimo, maximo = RANGOS[bits]

    if not minimo <= numero <= maximo:
        raise ValueError(
            f"El número debe estar entre {minimo} y {maximo}."
        )

    #Obtener el patrón de bits en complemento a 2
    mascara = (1 << bits) - 1
    patron = numero & mascara

    binario = format(patron, f"0{bits}b")

    #Agrupar el binario de cuatro en cuatro
    binario_agrupado = " ".join(
        binario[i:i + 4]
        for i in range(0, bits, 4)
    )


    #Representar el patrón en hexadecimal y octal
        #Representar el patrón en hexadecimal y octal
    digitos_hex = bits // 4
    hexadecimal = format(patron, f"0{digitos_hex}X")

    digitos_octal = (bits + 2) // 3
    octal = format(patron, "o").zfill(digitos_octal)



    #Interpretar el bit más significativo como signo
    bit_signo = binario[0]
    interpretacion_signo = (
        "Negativo" if bit_signo == "1" else "No negativo"
    )

    #Interpretar el mismo patrón como entero sin signo
    sin_signo = patron

    return {
        "numero": numero,
        "bits": bits,
        "minimo": minimo,
        "maximo": maximo,
        "binario": binario,
        "binario_agrupado": binario_agrupado,
        "hexadecimal": hexadecimal,
        "octal": octal,
        "bit_signo": bit_signo,
        "interpretacion_signo": interpretacion_signo,
        "sin_signo": sin_signo,
    }


def analizar_texto(texto: str) -> dict:
    #Validar la longitud del texto
    if len(texto) > 15:
        raise ValueError(
            "El texto no puede superar los 15 caracteres."
        )

    caracteres = []

    #Analizar cada punto de código Unicode
    for caracter in texto:
        utf8 = caracter.encode("utf-8")
        utf16 = caracter.encode("utf-16-le")

        caracteres.append({
            "caracter": caracter,
            "codigo_unicode": f"U+{ord(caracter):04X}",
            "utf8_hex": " ".join(f"{byte:02X}" for byte in utf8),
            "bytes_utf8": len(utf8),
            "bytes_utf16": len(utf16),
        })

    #Calcular los tamaños totales de las codificaciones
    total_utf8 = len(texto.encode("utf-8"))
    total_utf16 = len(texto.encode("utf-16-le"))

    return {
        "texto": texto,
        "caracteres": caracteres,
        "total_utf8": total_utf8,
        "total_utf16": total_utf16,
    }