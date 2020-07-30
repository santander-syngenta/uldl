from django.db import models

# Create your models here.

class Protocol(models.Model):
	pid = models.CharField(max_length=100, null = True)
	title = models.CharField(max_length=300, null = True)

	def __str__(self):
		return self.pid


class ai(models.Model):
	name = models.CharField(max_length=100, null = True)

	def __str__(self):
		return self.name


class crop(models.Model):
	name = models.CharField(max_length=100, null = True)

	def __str__(self):
		return self.name


class author(models.Model):
	name = models.CharField(max_length=100, null = True)

	def __str__(self):
		return self.name


class country(models.Model):
	name = models.CharField(max_length=100, null = True)

	def __str__(self):
		return self.name		


class year(models.Model):
	name = models.CharField(max_length=100, null = True)

	def __str__(self):
		return self.name


class Presentation(models.Model):
	"""
	Database for upload/download
	"""
	STATUS = (
		('Draft','Draft'),
		('Final', 'Final'),
		)
	author = models.ForeignKey(author, null=True, on_delete = models.SET_NULL)
	year = models.ForeignKey(year, null=True, on_delete = models.SET_NULL)
	country = models.ForeignKey(country, null=True, on_delete = models.SET_NULL)
	protocol = models.ManyToManyField(Protocol)
	ai = models.ManyToManyField(ai)
	crop = models.ManyToManyField(crop)
	status = status = models.CharField(max_length=10, null = True, choices = STATUS, blank = False, default = 'Unspecified')
	pptx = models.FileField(upload_to = "documents/", null = True)

	def get_title(self):
		primary = self.protocol.all()[0]

		return (primary.title)

	def get_protocols(self):
		ret = ''

		for protocol in self.protocol.all():
			ret = ret + protocol.pid + ', '

		return ret[:-2]

	def get_crops(self):
		ret = ''

		for crop in self.crop.all():
			ret = ret + crop.name + ', '

		return ret[:-2]

	def get_ais(self):
		ret = ''

		for ai in self.ai.all():
			ret = ret + ai.name + ', '

		return ret[:-2]