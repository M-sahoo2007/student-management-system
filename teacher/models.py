from django.db import models
from django.utils.text import slugify

# Create your models here.

class Parent(models.Model):
    father_name = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=100)
    father_mobile = models.CharField(max_length=100)
    father_email = models.EmailField(max_length=100)
    mother_name = models.CharField(max_length=100)
    mother_occupation = models.CharField(max_length=100)
    mother_mobile = models.CharField(max_length=100)
    mother_email = models.EmailField(max_length=100)
    present_address = models.TextField()
    permanent_address = models.TextField()
    
    def __str__(self) -> str:
        return f"{self.father_name} & {self.mother_name}"
    
    
class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")])
    date_of_birth = models.DateField()
    teacher_email = models.EmailField(max_length=100)
    teacher_department = models.CharField(max_length=100)
    religion = models.CharField(max_length=20)
    joining_date = models.DateField()
    mobile_number = models.CharField(max_length=15)
    ction = models.CharField(max_length=100)
    teacher_image = models.ImageField(upload_to='teachers/',blank=True)
    parent=models.OneToOneField(Parent,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True,blank=True)
    
    
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}-{self.teacher_id}")
        super(Teacher, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_id})"
    