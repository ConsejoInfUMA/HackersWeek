# -*- coding: utf-8 -*-

'''
Choices
'''

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

KIND_OF_EVENT_CHOICES = (
    ('C', 'Conferencia'),
    ('W', 'Taller'),
    ('J', 'Juego'),
    ('M', 'Miscelanea'),
)

TIME_STRIPE_CHOICES = (
    (1, '10:30'),
    (2, '11:30'),
    (3, '12:30'),
    (4, '15:30'),
    (5, '16:30'),
    (6, '17:30'),
    (7, '18:30'),
)

DURATION_CHOICES = (
    (1, '1 hora'),
    (2, '2 horas'),
)

DAY_CHOICES = (
    (1, 'Lunes'),
    (2, 'Martes'),
    (3, 'Miércoles'),
    (4, 'Jueves'),
)