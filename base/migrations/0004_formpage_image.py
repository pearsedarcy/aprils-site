# Generated by Django 5.1.4 on 2025-01-17 22:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_formpage_formfield'),
        ('wagtailimages', '0027_image_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='formpage',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
