# Generated by Django 5.0.7 on 2024-09-08 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('kvm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auth',
            name='instance',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='common.instance'),
        ),
        migrations.AddField(
            model_name='hypervisor',
            name='instance',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='common.instance'),
        ),
        migrations.AddField(
            model_name='tag',
            name='instance',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='common.instance'),
        ),
        migrations.AddField(
            model_name='vm',
            name='instance',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='common.instance'),
        ),
    ]