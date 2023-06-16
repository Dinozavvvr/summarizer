# Generated by Django 4.2.2 on 2023-06-19 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_document_file_documentcollection'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='annotation',
            field=models.CharField(max_length=10000000, null=True),
        ),
        migrations.AddField(
            model_name='documentcollection',
            name='score',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='documentcollection',
            name='weights',
            field=models.CharField(null=True),
        ),
    ]