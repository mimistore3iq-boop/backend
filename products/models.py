from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name= ??? ?????)
    description = models.TextField(blank=True, verbose_name= ?????)
    image = models.ImageField(upload_to= categories/, blank=True, null=True, verbose_name=???? ?????)
    
    class Meta:
        verbose_name =  ???
        verbose_name_plural =  ??????
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name= ??? ??????)
    description = models.TextField(verbose_name= ??? ??????)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name= ?????)
