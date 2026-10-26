#Formularios y validación de entradas del usuario
from django import forms


class IntegerConversionForm(forms.Form):
    #Campo para ingresar el entero decimal
    numero = forms.CharField(
        label="Número entero decimal",
        max_length=100,
        widget=forms.NumberInput(
            attrs={"placeholder": "Ejemplo: -128"}
        ),
        error_messages={
            "required": "Debe ingresar un número entero.",
            "max_length": "El número ingresado es demasiado largo.",
        },
    )

    #Selector del tamaño en bits
    bits = forms.ChoiceField(
        label="Tamaño en bits",
        choices=[
            ("8", "8 bits"),
            ("16", "16 bits"),
            ("32", "32 bits"),
        ],
        initial="8",
    )

    def clean_numero(self):
        #Validar que la entrada sea un entero decimal
        valor = self.cleaned_data["numero"].strip()

        try:
            return int(valor, 10)
        except ValueError:
            raise forms.ValidationError(
                "Entrada inválida: ingrese un número entero decimal."
            )

    def clean(self):
        #Validar el rango permitido por complemento a 2
        cleaned_data = super().clean()
        numero = cleaned_data.get("numero")
        bits = cleaned_data.get("bits")

        if numero is not None and bits is not None:
            bits = int(bits)
            minimo = -(2 ** (bits - 1))
            maximo = (2 ** (bits - 1)) - 1

            if not minimo <= numero <= maximo:
                self.add_error(
                    "numero",
                    f"Fuera de rango para {bits} bits. "
                    f"El valor debe estar entre {minimo} y {maximo}.",
                )

        return cleaned_data


class TextEncodingForm(forms.Form):
    #Campo para ingresar texto de hasta 15 caracteres
    texto = forms.CharField(
        label="Texto que se desea codificar",
        required=True,
        max_length=15,
        strip=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Ejemplo: Honduras 😀",
                "maxlength": 100,
            }
        ),
        error_messages={
            "required": "Debe ingresar un texto.",
            "max_length": "El texto no puede superar los 15 caracteres.",
        },
    )

    def clean_texto(self):
        #Verificar la longitud del texto en el servidor
        texto = self.cleaned_data["texto"]

        if len(texto) > 15:
            raise forms.ValidationError(
                "El texto no puede superar los 15 caracteres."
            )

        return texto
