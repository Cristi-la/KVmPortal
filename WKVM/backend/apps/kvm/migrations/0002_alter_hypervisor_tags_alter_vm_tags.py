# Generated by Django 5.0.7 on 2024-07-30 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kvm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hypervisor',
            name='tags',
            field=models.ManyToManyField(blank=True, to='kvm.tag'),
        ),
        migrations.AlterField(
            model_name='vm',
            name='tags',
            field=models.ManyToManyField(blank=True, to='kvm.tag'),
        ),
    ]
