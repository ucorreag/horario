# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horario', '0003_auto_20151220_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacultadCategoria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='carrera',
            name='id_categoria',
        ),
        migrations.RemoveField(
            model_name='categoria',
            name='id_facultad',
        ),
        migrations.AddField(
            model_name='carrera',
            name='cantidad_años',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='facultadcategoria',
            name='id_categoria',
            field=models.ForeignKey(to='horario.Categoria'),
        ),
        migrations.AddField(
            model_name='facultadcategoria',
            name='id_facultad',
            field=models.ForeignKey(to='horario.Facultad'),
        ),
        migrations.AddField(
            model_name='carrera',
            name='id_facultad_categoria',
            field=models.ForeignKey(to='horario.FacultadCategoria', default=0),
            preserve_default=False,
        ),
    ]
