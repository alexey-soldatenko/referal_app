from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MyUsers(models.Model):
	user = models.OneToOneField(User, related_name='user')
	person_id = models.PositiveIntegerField()
	token = models.CharField(max_length=100)
	time_activation = models.DateTimeField()
	user_rating = models.PositiveIntegerField()
	referer = models.ForeignKey("MyUsers", blank=True, null=True)
	referal_link = models.URLField()

	def __str__(self):
		return self.user.username
