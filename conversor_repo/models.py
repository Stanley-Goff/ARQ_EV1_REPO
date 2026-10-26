#Modelo que aloja el historial de conversiones numéricas

from django.db import models


class Conversion(models.Model):
    numero = models.BigIntegerField()
    bits = models.PositiveSmallIntegerField()
    binario = models.CharField(max_length=32)
    hexadecimal = models.CharField(max_length=8)
    octal = models.CharField(max_length=11)
    sin_signo = models.BigIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha", "-id"]
        verbose_name = "Conversión"
        verbose_name_plural = "Historial de conversiones"

    def __str__(self):
        return f"{self.numero} ({self.bits} bits)"