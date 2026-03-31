from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify

# Create your models here.

class Hod(models.Model):
    hod_name = models.CharField(max_length=100)
    hod_mobile = models.CharField(max_length=100)
    hod_email = models.EmailField(max_length=100)
    present_address = models.TextField()
    permanent_address = models.TextField()
    
    def __str__(self) -> str:
        return f"{self.hod_name}"
    
    
class Department(models.Model):
    department_name = models.CharField(max_length=100)
    department_id = models.CharField(max_length=100)
    department_email = models.EmailField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    ction = models.CharField(max_length=100)
    department_image = models.ImageField(upload_to='departments/',blank=True)
    hod=models.OneToOneField(Hod,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True,blank=True)
    
    
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.department_name}-{self.department_id}")
        super(Department, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.department_name} ({self.department_id})"
    