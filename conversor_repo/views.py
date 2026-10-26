#Vistas de conversión, validación e historial

from django.shortcuts import render
from django.db import transaction

from .forms import IntegerConversionForm, TextEncodingForm
from .logica import convertir_entero, analizar_texto
from .models import Conversion


def inicio(request):
    #Inicializar formularios y resultados
    resultado_numero = None
    resultado_texto = None

    formulario_numero = IntegerConversionForm(
        prefix="numero"
    )
    formulario_texto = TextEncodingForm(
        prefix="texto"
    )

    #Procesar el formulario numérico
    if request.method == "POST":
        tipo = request.POST.get("tipo")

        if tipo == "numero":
            formulario_numero = IntegerConversionForm(
                request.POST,
                prefix="numero",
            )

            if formulario_numero.is_valid():
                numero = formulario_numero.cleaned_data["numero"]
                bits = int(formulario_numero.cleaned_data["bits"])

                resultado_numero = convertir_entero(numero, bits)

                #Guardar y limitar el historial a 10 filas
                with transaction.atomic():
                    Conversion.objects.create(
                        numero=resultado_numero["numero"],
                        bits=resultado_numero["bits"],
                        binario=resultado_numero["binario"],
                        hexadecimal=resultado_numero["hexadecimal"],
                        octal=resultado_numero["octal"],
                        sin_signo=resultado_numero["sin_signo"],
                    )

                    ids_antiguos = list(
                        Conversion.objects
                        .order_by("-fecha", "-id")
                        .values_list("id", flat=True)[10:]
                    )

                    if ids_antiguos:
                        Conversion.objects.filter(
                            id__in=ids_antiguos
                        ).delete()

        #Procesar el formulario de texto
        elif tipo == "texto":
            formulario_texto = TextEncodingForm(
                request.POST,
                prefix="texto",
            )

            if formulario_texto.is_valid():
                texto = formulario_texto.cleaned_data["texto"]
                resultado_texto = analizar_texto(texto)

    #Recuperar las diez conversiones más recientes
    historial = Conversion.objects.all()[:10]

    return render(
        request,
        "conversor/inicio.html",
        {
            "formulario_numero": formulario_numero,
            "formulario_texto": formulario_texto,
            "resultado_numero": resultado_numero,
            "resultado_texto": resultado_texto,
            "historial": historial,
        },
    )


def ver_historial(request):
    #Mostrar el historial en una pagina independiente
    historial = Conversion.objects.all()[:10]

    return render(
        request,
        "conversor/historial.html",
        {"historial": historial},
    )