# Generated by Django 3.0.6 on 2020-08-21 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0019_auto_20200819_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='subject',
            field=models.CharField(blank=True, default='Expenditure', max_length=255, null=True),
        ),
    ]
