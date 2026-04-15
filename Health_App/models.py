from django.db import models

# Create your models here.


class AdminDetails(models.Model):
	username = models.CharField(max_length=100,default=None)
	password = models.CharField(max_length=100,default=None)
	class Meta:
		db_table = 'AdminDetails'

class userDetails(models.Model):
	Username 	= models.CharField(max_length=100,default=None,null=True)
	Password 	= models.CharField(max_length=100,default=None,null=True)
	Name 		= models.CharField(max_length=100,default=None,null=True)
	Age 		= models.CharField(max_length=200,default=None,null=True)
	Phone 		= models.CharField(max_length=100,default=None,null=True)
	Email 		= models.CharField(max_length=100,default=None,null=True)
	Address 		= models.CharField(max_length=100,default=None,null=True)
	Lat 		= models.CharField(max_length=100,default=None,null=True)
	Lng 		= models.CharField(max_length=100,default=None,null=True)
	class Meta:
		db_table = 'userDetails'


class Question_Answer(models.Model):
	Question 		= models.CharField(max_length=100,default=None,null=True)
	Answer 			= models.CharField(max_length=500,default=None,null=True)
	Keywords 		= models.CharField(max_length=100,default=None,null=True)
	Tag 		= models.CharField(max_length=100,default=None,null=True)
	class Meta:
		db_table = 'Question_Answer'

class NearbyHospitals(models.Model):
	#UsersID = models.CharField(max_length = 100,default = None)
	#Userslat = models.CharField(max_length = 100,default = None)
	#Userslong = models.CharField(max_length = 100,default = None)
	hospitalname = models.CharField(max_length = 1000,default = None)
	Lat = models.CharField(max_length = 1000,default = None)
	Lng = models.CharField(max_length = 1000,default = None)
	
	class Meta:
		db_table = 'NearbyHospitals'

