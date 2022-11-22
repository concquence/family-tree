# Generated by Django 3.2.16 on 2022-11-20 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0004_auto_20221120_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='person',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='people.person', verbose_name='Владелец документа'),
        ),
        migrations.AlterField(
            model_name='image',
            name='persons',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='imgs', to='people.Person', verbose_name='Фотография'),
        ),
    ]
