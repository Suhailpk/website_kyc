# Generated by Django 4.2.3 on 2023-08-11 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0002_alter_ann_table_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ann_table',
            name='image',
            field=models.ImageField(upload_to='ann_images/'),
        ),
    ]