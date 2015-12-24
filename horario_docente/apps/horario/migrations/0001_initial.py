# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asignatura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=50)),
                ('identificador', models.CharField(max_length=10)),
                ('horas', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Año',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nombre', models.CharField(verbose_name='Carrera', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CarreraAño',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('id_año', models.ForeignKey(to='horario.Año')),
                ('id_carrera', models.ForeignKey(to='horario.Carrera')),
            ],
        ),
        migrations.CreateModel(
            name='CarreraCurso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('id_carrera', models.ForeignKey(to='horario.Carrera')),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('desde', models.CharField(max_length=4)),
                ('hasta', models.CharField(max_length=4, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Dia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Facultad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=100)),
                ('titulo', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Semana',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('desde', models.DateField()),
                ('hasta', models.DateField(editable=False)),
                ('numero', models.CharField(verbose_name='Numero de Semana', max_length=10)),
                ('id_carrera', models.ForeignKey(to='horario.Carrera')),
            ],
        ),
        migrations.CreateModel(
            name='Semestre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=20, choices=[('1', 'primero'), ('2', 'segundo')])),
                ('id_año', models.ForeignKey(to='horario.Año')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('turno', models.CharField(max_length=20)),
                ('id_asignatura', models.ForeignKey(to='horario.Asignatura')),
                ('id_dia', models.ForeignKey(to='horario.Dia')),
                ('id_tipo', models.ForeignKey(to='horario.Tipo')),
            ],
        ),
        migrations.AddField(
            model_name='semana',
            name='id_semestre',
            field=models.ForeignKey(to='horario.Semestre'),
        ),
        migrations.AddField(
            model_name='dia',
            name='id_semana',
            field=models.ForeignKey(to='horario.Semana'),
        ),
        migrations.AddField(
            model_name='carreracurso',
            name='id_curso',
            field=models.ForeignKey(to='horario.Curso'),
        ),
        migrations.AddField(
            model_name='carrera',
            name='id_facultad',
            field=models.ForeignKey(to='horario.Facultad'),
        ),
        migrations.AddField(
            model_name='asignatura',
            name='id_carrera',
            field=models.ForeignKey(to='horario.Carrera'),
        ),
        migrations.AddField(
            model_name='asignatura',
            name='id_profesor',
            field=models.ForeignKey(to='horario.Profesor'),
        ),
        migrations.AddField(
            model_name='asignatura',
            name='id_semestre',
            field=models.ForeignKey(to='horario.Semestre'),
        ),
    ]
