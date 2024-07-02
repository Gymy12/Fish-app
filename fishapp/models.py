from django.db import models
from django.utils.html import mark_safe




class Banner(models.Model):
    img = models.ImageField(upload_to="banner_imgs/")
    alt_text  = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural='1. Banners'

    def image_tag(self):
        return mark_safe('<img src="%s" width="100"/>' % (self.img.url))        

    def __str__(self):
        return self.alt_text    


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="cat_imgs/")

    class Meta:
        verbose_name_plural='2. Categories'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))    

    def __str__(self):
        return self.title
        
    

class Quantity(models.Model):
    UNIT_CHOICES = [
      
        ('kg', 'Kilograms'),
        ('g', 'Grams'),
        ('unit', 'Unit'),
    ]
    unit = models.CharField(max_length=4, choices=UNIT_CHOICES)

    class Meta:
        verbose_name_plural='3. Quantities'
    
    def __str__(self):
        return self.get_unit_display() 

class Count(models.Model):
    count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = '4. Counts'

    def __str__(self):
        return str(self.count)



class Product(models.Model):
    title = models.CharField(max_length=100)
    slug=models.CharField(max_length=400)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.ForeignKey(Quantity, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField()
    status = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='5. Products'
    
    
    def __str__(self):
        return self.title
    
class ProductAttribute(models.Model):
     product = models.ForeignKey(Product, on_delete=models.CASCADE)
     quantity = models.ForeignKey(Quantity, on_delete=models.CASCADE)
     count = models.PositiveIntegerField()
     price = models.PositiveIntegerField(default=0) 
     image = models.ImageField(upload_to="product_imgs/", blank=True,null=True)

     class Meta:
        verbose_name_plural='6. ProductAttributes'
     def __str__(self):
        return self.product.title
     
     def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
        else:
            return "No Image"







    