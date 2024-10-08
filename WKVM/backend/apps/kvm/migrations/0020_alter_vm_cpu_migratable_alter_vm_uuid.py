# Generated by Django 5.0.7 on 2024-10-06 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kvm', '0019_vm_boot_device_vm_clock_adjustment_vm_clock_offset_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vm',
            name='cpu_migratable',
            field=models.BooleanField(default=False, help_text='Whether the CPU is migratable.'),
        ),
        migrations.AlterField(
            model_name='vm',
            name='uuid',
            field=models.CharField(blank=True, help_text='The UUID of the virtual machine.', max_length=64, null=True),
        ),
    ]
