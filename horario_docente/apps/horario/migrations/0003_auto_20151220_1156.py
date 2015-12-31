# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horario', '0002_auto_20151219_2319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semestre',
            name='id_año',
        ),
        migrations.AddField(
            model_name='año',
            name='id_semestre',
            field=models.ForeignKey(default=0, to='horario.Semestre'),
            preserve_default=False,
        ),
    ]
