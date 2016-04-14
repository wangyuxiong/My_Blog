# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import css3two_blog.models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('body', models.TextField(blank=True)),
                ('md_file', models.FileField(blank=True, upload_to=css3two_blog.models.BlogPost.get_upload_md_name)),
                ('pub_date', models.DateTimeField(verbose_name='date published', auto_now_add=True)),
                ('last_edit_date', models.DateTimeField(auto_now=True, verbose_name='last edited')),
                ('slug', models.SlugField(blank=True, max_length=200)),
                ('html_file', models.FileField(blank=True, upload_to=css3two_blog.models.BlogPost.get_html_name)),
                ('category', models.CharField(choices=[('programming', 'Programming'), ('acg', 'Anime & Manga & Novel & Game'), ('nc', 'No Category')], max_length=30)),
                ('description', models.TextField(blank=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', verbose_name='Tags', help_text='A comma-separated list of tags.', through='taggit.TaggedItem')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='BlogPostImage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('image', models.ImageField(upload_to=css3two_blog.models.BlogPostImage.get_upload_img_name)),
                ('blogpost', models.ForeignKey(to='css3two_blog.BlogPost', related_name='images')),
            ],
        ),
    ]
