from django.db import models



class StaffDictionary(models.Model):
	"""
	StaffDictionary is a dictionary for 
	"""
	key = models.CharField(max_length=255)
	value = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return "<key=%s>" % (self.key)
		