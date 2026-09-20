from django.db import models

ROL = [("1", "Administrador"), ("2", "Gestor")]

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    rol = models.CharField(max_length=100, choices=ROL)
    correo = models.EmailField(max_length=200)
    password = models.CharField(max_length=100)
    creado = models.DateField()
    modificado = models.DateField()
    
    def __str__(self):
        return f"Usuario {self.id} - Nombre: {self.nombre} - Rol: {self.rol} - Correo: {self.correo}" 
    
    
