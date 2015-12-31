# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horario', '0004_auto_20151220_1306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semana',
            name='id_semestre',
        ),
        migrations.AddField(
            model_name='semana',
            name='id_año',
            field=models.ForeignKey(default=0, to='horario.Año'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='semestre',
            name='nombre',
            field=models.CharField(max_length=20),
        ),
    ]
