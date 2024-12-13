from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)   

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = None  # Eliminar el campo de username heredado
     
    foto = models.ImageField(upload_to='integrantes_fotos/', null=True, blank=True)  # Foto del integrante
   
    age = models.IntegerField()
    name = models.CharField(max_length=225)
    grade = models.CharField(max_length=255)
    country = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    def get_full_name(self):
        return f"{self.nombre} {self.apellidos or ''}".strip()
    
    

class Session(models.Model):
    idsession = models.AutoField(primary_key=True)
    duration = models.DurationField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255 ,default= f"Sesion {id}")
    def __str__(self):
        return f"Session {self.idsession}"


class Topic(models.Model):
    idTopic = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description_default = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class TopicsRequirement(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    state = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = ("session", "topic")

    def __str__(self):
        return f"{self.session} requires {self.topic}"


class LearningTechnique(models.Model):
    idtechnique = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description_default = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class RecommendedTechniques(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    technique = models.ForeignKey(LearningTechnique, on_delete=models.CASCADE)
    user_agent = models.CharField(max_length=25, blank=True, null=True, default="agente")

    class Meta:
        unique_together = ("session", "technique")

    def __str__(self):
        return f"Technique {self.technique} recommended for {self.session}"