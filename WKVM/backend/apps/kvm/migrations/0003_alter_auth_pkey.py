# Generated by Django 5.0.7 on 2024-07-31 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kvm', '0002_alter_hypervisor_tags_alter_vm_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auth',
            name='pkey',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]