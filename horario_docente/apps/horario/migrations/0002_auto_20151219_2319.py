# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('id_facultad', models.ForeignKey(to='horario.Facultad')),
            ],
        ),
        migrations.RemoveField(
            model_name='carrera',
            name='id_facultad',
        ),
        migrations.AddField(
            model_name='carrera',
            name='id_categoria',
            field=models.ForeignKey(to='horario.Categoria', default=0),
            preserve_default=False,
        ),
    ]
