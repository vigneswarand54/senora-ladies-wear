# Generated by Django 3.2.13 on 2022-07-10 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_category_cat_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='cat_image',
            field=models.ImageField(blank=True, null=True, upload_to='\\category_photos'),
        ),
    ]
