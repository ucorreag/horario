# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horario', '0006_auto_20151224_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asignatura',
            name='id_carrera',
        ),
        migrations.RemoveField(
            model_name='asignatura',
            name='id_semestre',
        ),
        migrations.AddField(
            model_name='asignatura',
            name='id_carrera_año',
            field=models.ForeignKey(to='horario.CarreraAño', default=0),
            preserve_default=False,
        ),
    ]
