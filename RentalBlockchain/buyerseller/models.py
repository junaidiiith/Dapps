from django.db import models
from users.models import Profile
from django_mysql.models import JSONField, Model

# Create your models here.

Choices = [(1, "Landlord"), (2, "Tenant")]
States = [(0, "Terminated"), (1, "Active"), (2, "Passive")]

class Stakeholder(Model):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	type = models.IntegerField(choices=Choices)

class Contract(Model):
	name = models.CharField(max_length=255, blank=True)
	address = models.CharField(max_length=50)
	abi = JSONField()
	current = models.IntegerField(choices=States)
	landlord = models.ForeignKey(Stakeholder, on_delete=models.CASCADE, related_name='rented_contracts')
	tenant = models.ForeignKey(Stakeholder, on_delete=models.CASCADE, null=True, related_name='bought_contracts')


class Document(models.Model):
    name = models.CharField(max_length=255, blank=True)
    bytecode = models.FileField(upload_to='media/')
    abi = models.FileField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)