from .models import BlogPost
from django.contrib.syndication.views import Feed

exclude_posts = ("about", "projects", "talks")


class BlogPostFeed(Feed):
    title = "laike9m's blog"
    link = "/blog/rss"
    description = "Update on laike9m blog's articles."

    def items(self):
        return BlogPost.objects.exclude(title__in=exclude_posts).filter(category="programming")[:5]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.get_absolute_url()

    def item_description(self, item):
        html = item.display_html()
        import re
        html = re.sub(r"/media/", r"http://laike9m.com/media/", html)
        return html

    def item_pubdate(self, item):
        return item.pub_date
