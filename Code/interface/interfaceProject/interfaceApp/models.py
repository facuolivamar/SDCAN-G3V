from django.db import models

# Create your models here.

class input(models.Model):
    serial_port = models.CharField(max_length=255, blank=False, null=False, default='COM3')
    baud_rate = models.IntegerField(blank=False, null=False, default=115200)
    timeout = models.IntegerField(blank=False, null=False, default=1)
    
    estacion_terrena_latitude = models.FloatField(blank=False, null=False)
    estacion_terrena_longitude = models.FloatField(blank=False, null=False)

    # history = HistoricalRecords()

    def __str__(self):
        return f"Serial port reading: {self.serial_port}, baud rate: {self.baud_rate}, timeout: {self.timeout}, estacion terrena latitude: {self.estacion_terrena_latitude}, estacion terrena longitude: {self.estacion_terrena_longitude}."
