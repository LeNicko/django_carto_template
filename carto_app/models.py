from django.db import models
import uuid

class Serveur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50, blank=True)
    environnement = models.CharField(max_length=50, blank=True)
    os = models.CharField(max_length=100, blank=True)
    cycle_vie = models.CharField(max_length=50, blank=True)
    localisation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nom

class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    version = models.CharField(max_length=50, blank=True)
    cycle_vie = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=50, blank=True)
    serveur = models.ForeignKey(Serveur, on_delete=models.SET_NULL, null=True)
    position_PLU = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nom

class BaseDeDonnees(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50, blank=True)
    version = models.CharField(max_length=50, blank=True)
    serveur = models.ForeignKey(Serveur, on_delete=models.SET_NULL, null=True)
    application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nom

class Interface(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50, blank=True)
    protocole = models.CharField(max_length=50, blank=True)
    app_source = models.ForeignKey(Application, related_name='interfaces_source', on_delete=models.SET_NULL, null=True)
    app_dest = models.ForeignKey(Application, related_name='interfaces_dest', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nom

class ServiceMetier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    zone_PLU = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nom

class AppServiceMetier(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    service_metier = models.ForeignKey(ServiceMetier, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('application', 'service_metier')

class Utilisateur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    rôle = models.CharField(max_length=50)

    def __str__(self):
        return self.nom
