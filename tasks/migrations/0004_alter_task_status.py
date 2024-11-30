# Generated by Django 3.2.4 on 2024-11-30 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20241130_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('not-started', 'not started'), ('in-progress', 'in-progress'), ('complete', 'completed')], default='not-started', max_length=255),
        ),
    ]