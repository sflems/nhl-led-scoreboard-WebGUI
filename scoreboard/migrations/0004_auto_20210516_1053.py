# Generated by Django 3.1.3 on 2021-05-16 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0003_auto_20210516_1049'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='boardtype',
            options={'verbose_name': 'Board Type', 'verbose_name_plural': 'Boards'},
        ),
        migrations.AlterField(
            model_name='settings',
            name='boardType',
            field=models.ForeignKey(default='nhl', on_delete=django.db.models.deletion.CASCADE, to='scoreboard.boardtype'),
        ),
    ]
