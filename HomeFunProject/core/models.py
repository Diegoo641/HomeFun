from django.db import models

# ESTADO_CIVIL
class EstadoCivil(models.Model):
    id_estado_civil = models.AutoField(primary_key=True, verbose_name='ID de Estado Civil')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción')

    def __str__(self):
        return self.descripcion

# GENERO
class Genero(models.Model):
    id_genero = models.AutoField(primary_key=True, verbose_name='ID de Género')
    descripcion = models.CharField(max_length=50, verbose_name='Descripción del Género')

    def __str__(self):
        return self.descripcion

# REGION
class Region(models.Model):
    id_region = models.AutoField(primary_key=True, verbose_name='ID de Región')
    descripcion = models.CharField(max_length=50, verbose_name='Descripción de la Región')

    def __str__(self):
        return self.descripcion

# COMUNA
class Comuna(models.Model):
    id_comuna = models.AutoField(primary_key=True, verbose_name='ID de Comuna')
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Comuna')
    id_region = models.ForeignKey(Region, on_delete=models.PROTECT, verbose_name='Región asociada')

    def __str__(self):
        return self.nombre
    
class Estado_residente(models.Model):
    id_est_r = models.AutoField(primary_key=True, verbose_name='ID de Estado del residente')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción del Estado')

    def __str__(self):
        return self.descripcion

# FICHA_RESIDENTE
class FichaResidente(models.Model):
    id_residente = models.AutoField(primary_key=True, verbose_name='ID de Residente')
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Residente')
    apellido = models.CharField(max_length=100, verbose_name='Apellido del Residente')
    correo = models.CharField(max_length=100, verbose_name='Correo Electrónico')
    direccion = models.CharField(max_length=100, verbose_name='Dirección')
    rut = models.CharField(max_length=12, verbose_name='RUT' ,unique=True)
    genero = models.ForeignKey(Genero, on_delete=models.PROTECT, verbose_name='Género del Residente')
    comuna = models.ForeignKey(Comuna, on_delete=models.PROTECT, verbose_name='Comuna del Residente')
    estado_civil = models.ForeignKey(EstadoCivil, on_delete=models.PROTECT, verbose_name='Estado Civil')
    estado = models.ForeignKey(Estado_residente,null=True,blank=True, on_delete=models.PROTECT, verbose_name='Estado del residente')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# CASA_DEPTO
class CasaDepto(models.Model):
    id_dpto = models.AutoField(primary_key=True, verbose_name='ID del Departamento')
    nro = models.IntegerField(verbose_name='Número del Departamento')
    direccion = models.CharField(max_length=100, verbose_name='Dirección del Departamento')
    id_residente = models.ForeignKey(FichaResidente, on_delete=models.PROTECT, verbose_name='Residente Asociado')

    def __str__(self):
        return f"Depto {self.nro}"

# COMUNIDAD
class Comunidad(models.Model):
    id_comunidad = models.AutoField(primary_key=True, verbose_name='ID de la Comunidad')
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Comunidad')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción de la Comunidad')
    id_dpto = models.ForeignKey(CasaDepto, on_delete=models.PROTECT, verbose_name='Departamento Asociado')

    def __str__(self):
        return self.nombre

# PERFIL
class Perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True, verbose_name='ID de Perfil')
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Perfil')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción del Perfil')

    def __str__(self):
        return self.nombre
    
# ESTADO_EC (Estado del espacio común)
class Estado_EC(models.Model):
    id_est_ec = models.AutoField(primary_key=True, verbose_name='ID de Estado del Espacio Común')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción del Estado')

    def __str__(self):
        return self.descripcion

# ESPACIO_COMUN
class EspacioComun(models.Model):
    id_espacio_comun = models.AutoField(primary_key=True, verbose_name='ID del Espacio Común')
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Espacio Común')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción del Espacio Común')
    ubicacion = models.CharField(max_length=100, verbose_name='Ubicación del Espacio Común')
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True,verbose_name='Monto')
    imagen = models.ImageField(upload_to='imagenes', verbose_name='Imagen del Espacio Común')
    id_comunidad = models.ForeignKey(Comunidad, on_delete=models.PROTECT, verbose_name='Comunidad Asociada')
    estado_ec = models.ForeignKey('Estado_EC', on_delete=models.PROTECT, verbose_name='Estado del Espacio Común')

    def __str__(self):
        return self.nombre

# ESTADO_R_EC (Estado de la reserva del espacio común)
class Estado_R_EC(models.Model):
    id_est_r_ec = models.AutoField(primary_key=True, verbose_name='ID de Estado de la Reserva del Espacio Común')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción del Estado')

    def __str__(self):
        return self.descripcion

# RESERVA_ESP_COMUN
class ReservaEspComun(models.Model):
    id_reserva_esp_comun = models.AutoField(primary_key=True, verbose_name='ID de la Reserva del Espacio Común')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción de la Reserva')
    fecha = models.DateField(verbose_name='Fecha de la Reserva')
    hora = models.TimeField(verbose_name='Hora de la Reserva')
    id_espacio_comun = models.ForeignKey(EspacioComun, on_delete=models.PROTECT, verbose_name='Espacio Común Reservado')
    id_residente = models.ForeignKey(FichaResidente, on_delete=models.PROTECT, verbose_name='Residente que Reservó')
    estado_reserva = models.ForeignKey('Estado_R_EC', on_delete=models.PROTECT, verbose_name='Estado de la Reserva')

    def __str__(self):
        return self.descripcion

# ESTADO_GC (Estado de gasto común)
class Estado_GC(models.Model):
    id_est_gc = models.AutoField(primary_key=True, verbose_name='ID de Estado del Gasto Común')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción del Estado')

    def __str__(self):
        return self.descripcion
    
# ESTADO_GC (Estado de gasto común)
class Estado_T_GC(models.Model):
    id_est_t_gc = models.AutoField(primary_key=True, verbose_name='ID de Estado del Gasto Común')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción del Estado')

    def __str__(self):
        return self.descripcion
    
# GASTO_COMUN
class TipoGastoComun(models.Model):
    id_t_gc = models.AutoField(primary_key=True, verbose_name='ID de Gasto Común')
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Gasto Común')
    monto =models.IntegerField(verbose_name='Monto del gasto')
    reajuste = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Reajuste del Gasto Común')
    estado_t_gc = models.ForeignKey('Estado_T_GC', on_delete=models.PROTECT, verbose_name='Estado del Tipo de Gasto Común')

    def __str__(self):
        return f"Gasto común: {self.nombre}"

# GASTO_COMUN
class GastoComun(models.Model):
    id_gc = models.AutoField(primary_key=True, verbose_name='ID de Gasto Común')
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Gasto Común')
    fecha = models.DateField(verbose_name='Fecha del gasto comun.')
    total = models.IntegerField(verbose_name='Total')
    id_dpto = models.ForeignKey(CasaDepto, on_delete=models.PROTECT, verbose_name='Departamento Asociado')
    estado_gc = models.ForeignKey('Estado_GC', on_delete=models.PROTECT, verbose_name='Estado del Gasto Común')
    tipo = models.ForeignKey('TipoGastoComun', on_delete=models.PROTECT, verbose_name='Tipo del Gasto Común')


    def __str__(self):
        return f"Gasto común: {self.nombre}"

# ESTADO_MULTA (Estado de la multa)
class EstadoMulta(models.Model):
    id_est_multa = models.AutoField(primary_key=True, verbose_name='ID de Estado de Multa')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción del Estado')

    def __str__(self):
        return self.descripcion

# ESTADO_MULTA (Estado de la multa)
class EstadoTipoMulta(models.Model):
    id_est_t_multa = models.AutoField(primary_key=True, verbose_name='ID de Estado de Multa')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción del Estado')

    def __str__(self):
        return self.descripcion    

class TipoMulta(models.Model):
    id_t_multa = models.AutoField(primary_key=True, verbose_name='ID tipo de la Multa')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción del tipo de Multa')
    monto = models.IntegerField(verbose_name='Monto de la Multa')
    estado_t_multa =models.ForeignKey('EstadoTipoMulta', on_delete=models.PROTECT, verbose_name='Estado de la Multa')

    def __str__(self):
        return self.descripcion


# MULTA
class Multa(models.Model):
    id_multa = models.AutoField(primary_key=True, verbose_name='ID de la Multa')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción de la Multa')
    fecha_ingreso = models.DateField(verbose_name='Fecha de Ingreso de la Multa')
    id_dpto = models.ForeignKey(CasaDepto, on_delete=models.PROTECT, verbose_name='Departamento Asociado')
    estado_multa = models.ForeignKey('EstadoMulta', on_delete=models.PROTECT, verbose_name='Estado de la Multa')
    tipo = models.ForeignKey('TipoMulta', on_delete=models.PROTECT, verbose_name='Tipo de Multa')

    def __str__(self):
        return f"Multa: {self.descripcion}"
