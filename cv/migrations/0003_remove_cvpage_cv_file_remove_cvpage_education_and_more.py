# Generated by Django 5.1.4 on 2025-01-28 11:31

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cv', '0002_cvpage_pdf_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cvpage',
            name='cv_file',
        ),
        migrations.RemoveField(
            model_name='cvpage',
            name='education',
        ),
        migrations.RemoveField(
            model_name='cvpage',
            name='experience',
        ),
        migrations.RemoveField(
            model_name='cvpage',
            name='pdf_document',
        ),
        migrations.RemoveField(
            model_name='cvpage',
            name='skills',
        ),
        migrations.AddField(
            model_name='cvpage',
            name='body',
            field=wagtail.fields.StreamField([('heading_block', 2), ('paragraph_block', 3), ('image_block', 6), ('embed_block', 7), ('cv_document', 9), ('experience', 15), ('education', 19), ('skills', 22)], blank=True, block_lookup={0: ('wagtail.blocks.CharBlock', (), {'form_classname': 'title', 'required': True}), 1: ('wagtail.blocks.ChoiceBlock', [], {'blank': True, 'choices': [('', 'Select a heading size'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')], 'required': False}), 2: ('wagtail.blocks.StructBlock', [[('heading_text', 0), ('size', 1)]], {}), 3: ('wagtail.blocks.RichTextBlock', (), {'icon': 'pilcrow'}), 4: ('wagtail.images.blocks.ImageBlock', [], {}), 5: ('wagtail.blocks.CharBlock', (), {'required': False}), 6: ('wagtail.blocks.StructBlock', [[('image', 4), ('caption', 5), ('attribution', 5)]], {}), 7: ('wagtail.embeds.blocks.EmbedBlock', (), {'help_text': 'Insert a URL to embed. For example, https://www.youtube.com/watch?v=SGJFWirQ3ks', 'icon': 'media'}), 8: ('wagtail.documents.blocks.DocumentChooserBlock', (), {'help_text': 'Upload your CV document (PDF recommended)', 'required': True}), 9: ('wagtail.blocks.StructBlock', [[('document', 8)]], {'group': 'Content'}), 10: ('wagtail.blocks.CharBlock', (), {'help_text': 'Company or organization name'}), 11: ('wagtail.blocks.CharBlock', (), {'help_text': 'Your job title'}), 12: ('wagtail.blocks.DateBlock', (), {}), 13: ('wagtail.blocks.DateBlock', (), {'help_text': 'Leave blank if this is your current position', 'required': False}), 14: ('wagtail.blocks.RichTextBlock', (), {'features': ['bold', 'italic', 'link'], 'help_text': 'Describe your responsibilities and achievements'}), 15: ('wagtail.blocks.StructBlock', [[('company', 10), ('position', 11), ('date_from', 12), ('date_to', 13), ('description', 14)]], {'group': 'Content'}), 16: ('wagtail.blocks.CharBlock', (), {}), 17: ('wagtail.blocks.DateBlock', (), {'required': False}), 18: ('wagtail.blocks.RichTextBlock', (), {'features': ['bold', 'italic', 'link'], 'required': False}), 19: ('wagtail.blocks.StructBlock', [[('institution', 16), ('degree', 16), ('date_from', 12), ('date_to', 17), ('description', 18)]], {'group': 'Content'}), 20: ('wagtail.blocks.CharBlock', (), {'help_text': "Skill category (e.g., 'Programming Languages')"}), 21: ('wagtail.blocks.ListBlock', (16,), {'help_text': 'Add individual skills in this category'}), 22: ('wagtail.blocks.StructBlock', [[('category', 20), ('skills', 21)]], {'group': 'Content'})}, help_text='Build your CV content here'),
        ),
        migrations.AlterField(
            model_name='cvpage',
            name='introduction',
            field=wagtail.fields.RichTextField(blank=True, help_text='Brief introduction or professional summary'),
        ),
    ]
