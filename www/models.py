# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

COURSE_CHOICES = (
    ('GII', 'Grado en Ingeniería Informática'),
    ('GIS', 'Grado en Ingeniería del Software'),
    ('GIC', 'Grado en Ingeniería de Computadores'),
    ('GISa', 'Grado en Ingeniería de la Salud'),
    ('II', 'Ingeniería Informática (plan antiguo)'),
    ('ITS', 'Ingeniería Técnica Informática de Sistemas'),
    ('ITG', 'Ingeniería Técnica Informática de Gestión'),
    ('OTH', 'Otra Titulación'),
    ('NOS', 'No soy estudiante de la UMA'),
)

class UserProfile(models.Model):
	"""
	Extended profile of an User
	"""
	user = models.OneToOneField(User)
	dni = models.CharField(max_length=25)
	course = models.CharField(max_length=3, choices=COURSE_CHOICES, default='II')
	auto_enroll_all = models.BooleanField(default=False)

	def __src__(self):
		return "%s" % self.user