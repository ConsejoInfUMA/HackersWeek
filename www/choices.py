# -*- coding: utf-8 -*-

'''
Choices
'''

COURSE_CHOICES = (
    ('GII', 'Grado en Ingeniería Informática'),
    ('GIS', 'Grado en Ingeniería del Software'),
    ('GIC', 'Grado en Ingeniería de Computadores'),
    ('GIa', 'Grado en Ingeniería de la Salud'),
    ('II', 'Ingeniería Informática (plan antiguo)'),
    ('ITS', 'Ingeniería Técnica Informática de Sistemas'),
    ('ITG', 'Ingeniería Técnica Informática de Gestión'),
    ('DOC', 'Personal Docente (ETSI Informática)'),
    ('OTH', 'Otra Titulación'),
    ('NOS', 'No soy estudiante'),
)

KIND_OF_EVENT_CHOICES = (
    ('A', 'Conferencia'),
    ('B', 'Taller'),
    ('C', 'Juego'),
    ('D', 'Miscelanea'),
)

TIME_STRIPE_CHOICES = (
    (1, '10:30'),
    (2, '11:30'),
    (3, '12:30'),
    (4, '15:30'),
    (5, '17:30'),
    (6, '18:30'),
)
TIME_STRIPE_CALENDAR = (
    (1, '10:30 - 11:30'),
    (2, '11:30 - 12:30'),
    (3, '12:30 - 14:30'),
    (4, '15:30 - 17:30'),
    (5, '17:30 - 18:30'),
    (6, '18:30 - 19:30'),
)


DURATION_CHOICES = (
    (1, '1 franja'),
    (2, '2 franjas'),
    (3, '3 franjas'),
)

DAY_CHOICES = (
    (1, 'Lunes 23 de Marzo de 2015'),
    (2, 'Martes 24 de Marzo de 2015'),
    (3, 'Miércoles 25 de Marzo de 2015'),
    (4, 'Jueves 26 de Marzo de 2015'),
)

DAY_CHOICES_CALENDAR = (
    (1, 'Lunes'),
    (2, 'Martes'),
    (3, 'Miércoles'),
    (4, 'Jueves'),
)