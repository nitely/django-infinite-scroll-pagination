# Generated by Django 3.1.1 on 2020-10-09 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0003_article_is_sticky'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='article',
            index=models.Index(fields=['is_pinned', 'is_sticky', 'date', 'id'], name='tests_artic_is_pinn_819aa7_idx'),
        ),
        migrations.AddIndex(
            model_name='article',
            index=models.Index(fields=['-is_pinned', '-is_sticky', '-date', '-id'], name='tests_artic_is_pinn_603b8c_idx'),
        ),
    ]
