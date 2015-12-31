# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horario', '0005_auto_20151221_2229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semana',
            name='id_año',
        ),
        migrations.AddField(
            model_name='semana',
            name='id_carrera_año',
            field=models.ForeignKey(to='horario.CarreraAño', default=0),
            preserve_default=False,
        ),
    ]
