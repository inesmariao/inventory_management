# Generated by Django 5.2.1 on 2025-05-08 13:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the country', max_length=100)),
                ('alpha_2', models.CharField(max_length=2, unique=True)),
                ('alpha_3', models.CharField(max_length=3, unique=True)),
                ('numeric_code', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companies', to='company.country'),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the department', max_length=100)),
                ('code', models.IntegerField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='company.country')),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companies', to='company.department'),
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the municipality', max_length=100)),
                ('code', models.IntegerField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='municipalities', to='company.department')),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='municipality',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companies', to='company.municipality'),
        ),
    ]
