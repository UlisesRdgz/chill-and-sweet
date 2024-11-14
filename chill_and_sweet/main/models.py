from django.db import models

# Modelo que representa a los usuarios de la plataforma
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    puntos_acumulados = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Modelo que representa las categorías de postres
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# Modelo que representa los postres disponibles en la plataforma
class Postre(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=500)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

# Modelo que representa los ingredientes que se pueden agregar a los postres
class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    precio_adicional = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nombre

# Modelo intermedio para la relación entre postres e ingredientes
class PostreIngrediente(models.Model):
    postre = models.ForeignKey(Postre, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('postre', 'ingrediente')

# Modelo intermedio para la relación entre categorías e ingredientes
class CategoriaIngrediente(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('categoria', 'ingrediente')

# Modelo que representa los pedidos realizados por los usuarios
class Pedido(models.Model):
    ESTADO_PAGO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('fallido', 'Fallido'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    puntos_utilizados = models.IntegerField(default=0)
    estado_pago = models.CharField(max_length=15, choices=ESTADO_PAGO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Pedido {self.id} de {self.usuario}"

# Modelo que representa los postres favoritos de los usuarios
class Favorito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    postre = models.ForeignKey(Postre, on_delete=models.CASCADE)
    fecha_agregado = models.DateField(auto_now_add=True)

# Modelo intermedio para la relación entre pedidos y postres
class PedidoPostre(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    postre = models.ForeignKey(Postre, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    class Meta:
        unique_together = ('pedido', 'postre')
