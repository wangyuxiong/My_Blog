
   之前博客是基于wordpress平台，虽然之前也折腾过几次主题，但是一直都没有办法弄出来自己满意的。一个偶然的机会，发现laike9m的这个python博客风格很好，而且还在github上开源了，于是就下定决心将博客迁移到python平台上。修改后代码放在[**github**][1]上。

## 1. python2&3兼容
   python3平时没有接触过，但考虑到laike9m是基于python3搭建的，避免一些重复工作，我这里也直接使用python3.
   在通常情况下，大家喜欢用virtualenv来兼容python2和python3，但我发现无论是Mac还是ubuntu，直接安装2个版本的python本身并不冲突，通过python和python3区分python版本，pip和pip3是用来区分python版本对应的包管理命令。
   基于上述条件，优先安装一个python3和pip3:
```
macos : sudo brew install python3
ubuntu: sudo apt-get install python3
```
## 2. django博客运行环境搭建

### 2.1 基础环境

由于平时使用mysql比较多，而且之前linode上搭建的wordpress已经部署mysql，所有这里没有继续使用laike9m的postgresql。

 - **增加mysql依赖**

使用mysql，需要做一定的修改。需要增加pymysql的依赖，在my_blog的__init__.py中添加如下代码：
```
import pymysql
pymysql.install_as_MySQLdb()
```

- **更新下requirements.txt文件**

```
django==1.8
requests==2.9.1
django-contact-form==1.2
django-taggit==0.18.1
unidecode==0.4.19
Pillow==3.1.1
uwsgi==2.0.12
uwsgidecorators==1.1.0
pymysql==0.7.2
```

- **安装下这些依赖**
`pip3 install -r requirements.txt`

### 2.2 下载并修改代码
找一个工作目录，创建static,media文件夹作为 STATIC_ROOT 和 MEDIA_ROOT。按照新的路径修改choose_setting.py文件，具体见github代码。

- **在 css3two\_blog 文件夹中，准备做数据模型同步**
```
mkdir migrations
cd migrations
touch __init__.py
```

- **然后回到根目录执行，执行**
```
python3 manage.py makemigrations 
python3 manage.py migrate --fake-initial
```

- **最后，拷贝静态文件**
`python manage.py collectstatic`

用runserver启动测试服务器，通过ip访问网站并执行操作。运行正常后，可以开始准备部署上线了。

## 3. django博客部署（Nginx+uWSGI）
上线采用Nginx+uWSGI进行部署。前提是先得安装好相应的应用。参考 [Linode部署文档][2]。

### 3.1 配置uWSGI:
- **新增一个uWSGI的配置文件** `[File: /etc/uwsgi/sites/blog.ini]`
```
[uwsgi]

# Django-related settings
# the base directory (full path)
chdir           = /home/metaboy/blog/My_Blog
# Django's wsgi file
module          = my_blog.wsgi:application
# the virtualenv (full path)
home            = /home/metaboy/blog

# process-related settings
# master
master          = true
# maximum number of worker processes
processes       = 3
# the socket (use the full path to be safe
socket          = /tmp/uwsgi.sock

# ... with appropriate permissions - may be needed
chmod-socket    = 777
# clear environment on exit
vacuum          = true

logto           = /home/metaboy/uwsgi.log
```

- **创建一个Upstart job**:  `[File: /etc/init/uwsgi.conf]`
```
`env DJANGO_DB_PASSWORD=
env EMAIL_HOST_PASSWORD=
env LC_ALL=en_US.UTF-8
env LANG=en_US.UTF-8

start on runlevel [2345]()
stop on runlevel [!2345]()

setuid root
setgid www-data

exec /usr/local/bin/uwsgi --ini /home/metaboy/blog/My_Blog/uwsgi.ini
```

- **启动uwsgi服务**：
`service uwsgi start`

### 3.2 配置nginx：
切换到`/etc/nginx/sites-enabled`目录下。

- 新增一个博客的配置项: `[File: /etc/nginx/sites-enabled/blog.wangyuxiong.com]`
```
server {
	listen 80;
	server_name blog.wangyuxiong.com;
	
	location /media {
	        alias /home/metaboy/blog/media;
	        etag on;
	        expires max;
	        add_header Pragma public;
	        add_header Cache-Control "public";
	        access_log off;
	    }
	
	    location ~* ^/static/(.+.css)$ {
	        alias /home/metaboy/blog/static/$1;
	        etag on;
	        expires 1d;
	        add_header Pragma public;
	        add_header Cache-Control "public";
	        access_log off;
	    }
	
	    location /static {
	        alias /home/metaboy/blog/static;
	        etag on;
	        expires max;
	        add_header Pragma public;
	        add_header Cache-Control "public";
	        access_log off;
	    }
	
	    location / {
	        include uwsgi_params;
	        uwsgi_pass unix:/tmp/uwsgi.sock;
	    }
	
	    error_page   500 502 503 504  /50x.html;
	
	    location = /50x.html {
	        root   html;
	    }

}
```

- 启用该配置:
`ln -s /etc/nginx/sites-available/blog.wangyuxiong.com /etc/nginx/sites-enabled`

- 重启nginx
`service nginx configtest &&  service nginx restart`


---- 

按照上面部署，接着就可以通过链接 [blog.wangyuxiong.com][3]进行访问了。

[1]:	https://github.com/wangyuxiong/My_Blog
[2]:	https://www.linode.com/docs/websites/nginx/deploy-django-applications-using-uwsgi-and-nginx-on-ubuntu-14-04
[3]:	blog.wangyuxiong.com