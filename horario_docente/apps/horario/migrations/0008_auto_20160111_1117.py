# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horario', '0007_auto_20151228_2015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carreracurso',
            name='id_carrera',
        ),
        migrations.RemoveField(
            model_name='carreracurso',
            name='id_curso',
        ),
        migrations.DeleteModel(
            name='CarreraCurso',
        ),
        migrations.DeleteModel(
            name='Curso',
        ),
    ]
