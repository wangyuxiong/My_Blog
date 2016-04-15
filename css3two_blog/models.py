import os
from datetime import datetime

from django.db import models
from django.utils import timezone

# for slug, get_absolute_url
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from unidecode import unidecode

# delete md_file before delete/change model
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# get gfm html and store it
import requests
from django.core.files.base import ContentFile

# tagging
from taggit.managers import TaggableManager


upload_dir = 'content/BlogPost/%s/%s'


class BlogPost(models.Model):

    class Meta:
        ordering = ['-pub_date']    # ordered by pub_date descending when retriving

    def get_upload_md_name(self, filename):
        if self.pub_date:
            year = self.pub_date.year   # always store in pub_year folder
        else:
            year = datetime.now().year
        upload_to = upload_dir % (year, self.title + '.md')
        return upload_to

    def get_html_name(self, filename):
        if self.pub_date:
            year = self.pub_date.year
        else:
            year = datetime.now().year
        upload_to = upload_dir % (year, filename)
        return upload_to

    CATEGORY_CHOICES = (
        ('programming', 'Programming'),
        ('work', 'Work'),
        ('life', 'Life'),
        ('read', 'Reading'),
        ('nc', 'No Category'),
    )

    title = models.CharField(max_length=150)
    body = models.TextField(blank=True)
    md_file = models.FileField(upload_to=get_upload_md_name, blank=True)  # uploaded md file
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    last_edit_date = models.DateTimeField('last edited', auto_now=True)
    slug = models.SlugField(max_length=200, blank=True)
    html_file = models.FileField(upload_to=get_html_name, blank=True)    # generated html file
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title   # 根据继承搜索流程,先是实例属性,然后就是类属性,所以这样用没问题

    @property
    def filename(self):
        if self.md_file:
            return os.path.basename(self.title)
        else:
            return 'no md_file'

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.title))
        if not self.body and self.md_file:
            self.body = self.md_file.read()

        # generate rendered html file with same name as md
        headers = {'Content-Type': 'text/plain'}
        if type(self.body) == bytes:  # sometimes body is str sometimes bytes...
            data = self.body
        elif type(self.body) == str:
            data = self.body.encode('utf-8')
        else:
            print("somthing is wrong")

        r = requests.post('https://api.github.com/markdown/raw', headers=headers, data=data)
        # avoid recursive invoke
        self.html_file.save(self.title+'.html', ContentFile(r.text.encode('utf-8')), save=False)
        self.html_file.close()

        super().save(*args, **kwargs)

    def display_html(self):
        with open(self.html_file.path, encoding='utf-8') as f:
            return f.read()

    # 首页只展示 description，全文输出不合适
    def display_detail(self):
        if self.description != "":
            return self.description
        else:
            return self.body[0:200]

    def get_absolute_url(self):
        return reverse('css3two_blog.views.blogpost', kwargs={'slug': self.slug, 'post_id': self.id})


@receiver(pre_delete, sender=BlogPost)
def blogpost_delete(instance, **kwargs):
    if instance.md_file:
        instance.md_file.delete(save=False)
    if instance.html_file:
        instance.html_file.delete(save=False)


class BlogPostImage(models.Model):

    def get_upload_img_name(self, filename):
        upload_to = upload_dir % ('images', filename)  # filename involves extension
        return upload_to

    blogpost = models.ForeignKey(BlogPost, related_name='images')
    image = models.ImageField(upload_to=get_upload_img_name)

