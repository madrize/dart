from django.conf.urls.defaults import patterns, include, url
from dart.views import get_article_details, post_article, get_articles

urlpatterns = patterns('',
                       url(r'^post/',
                           post_article,
                           name="post_new_article"),
                       url(r'^$',
                           get_articles,
                           name="get_all_articles"),
                       url(r'^([-\w]+)/$',
                           get_article_details,
                           name="get_article_detail"),
)
