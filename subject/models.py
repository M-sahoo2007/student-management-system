from django.db import models
from django.utils.text import slugify

# Create your models here.

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    department_email = models.EmailField(max_length=100)

    
    def __str__(self) -> str:
        return f"{self.department_name}"
    
    
class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_id = models.CharField(max_length=100)
    subject_department = models.CharField(max_length=100)
    subject_image = models.ImageField(upload_to='teachers/',blank=True)
    department=models.OneToOneField(Department,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True,blank=True)
    
    
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.subject_name}-{self.subject_id}")
        super(Subject, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.subject_name} ({self.subject_id})"
    