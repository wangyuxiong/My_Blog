from django.contrib import admin
from .models import BlogPost, BlogPostImage

from django.forms import TextInput, Textarea
from django.db import models

from django import forms

from django.core.files.base import ContentFile
import os
from django.conf import settings
import platform


class BlogPostImageInline(admin.TabularInline):
    model = BlogPostImage
    extra = 3


class MyModelForm(forms.ModelForm):
    """在加载某篇文章的admin页面时从md_file读取内容到body"""
    def __init__(self, *args, **kwargs):
        super(MyModelForm, self).__init__(*args, **kwargs)
        if self.instance.md_file:
            self.initial['body'] = self.instance.md_file.read()


class BlogPostModelAdmin(admin.ModelAdmin):
    @staticmethod
    def delete_old_md_file():
        # delete old md files, this method is unused now
        md_file_list = []
        for blogpost in BlogPost.objects.all():
            if blogpost.md_file:
                md_file_list.append(blogpost.filename)
        
        with open('md_file_list.txt', 'wt') as f:
            f.write(str(md_file_list))
        
        for root, subdirs, files in os.walk(os.path.join(settings.EDIA_ROOT, 'content/BlogPost')):
            for file in files:
                if file not in md_file_list:
                    os.remove(os.path.join(root, file))

    exclude = ('html_file',)
    inlines = [BlogPostImageInline, ]
    formfield_overrides = {  # 修改body显示框的大小使能容纳整篇文章
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 100, 'cols': 100})},
    }
    
    def save_model(self, request, obj, form, change):
        if obj:
            if obj.body:   # body有内容的时候才会更新md_file
                filename = obj.filename
                if filename != 'no md_file':
                    if platform.system() == "Windows":  # On Windows file can't be removed so leave it
                        pass
                    else:
                        obj.md_file.delete(save=False)   # 部署的时候存在,可以正常删除文件
                        obj.html_file.delete(save=False)
                # 没有md_file就根据title创建一个, 但不能创建html因为obj.save()的时候会创建
                obj.md_file.save(filename+'.md', ContentFile(obj.body), save=False)
                obj.md_file.close()
        obj.save()


admin.site.register(BlogPost, BlogPostModelAdmin)
