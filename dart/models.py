from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from django.contrib.markup.templatetags import markup


class Tag(models.Model):
    """ Tag Model """
    name = models.CharField(_('name'),max_length=60,unique=True)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/tags/%s" % (self.slug)
    
    def save(self,*args,**kwargs):
        name = self.name.strip().lower()
        self.name = name
        super(Tag,self).save(*args,**kwargs)



class ActiveArticlesManager(models.Manager):
    """
    Returns active articles only
    """
    def get_query_set(self):
        arts = super(ActiveArticlesManager,self).get_query_set()
        return arts.filter(is_active=True)



class Article(models.Model):
    """ Article Model """
    title = models.CharField(_('title'),max_length=120)
    slug = models.SlugField(unique=True)
    content = models.TextField(_('content'))
    rendered_content = models.TextField(_('rendered content'), blank=True)
    author = models.ForeignKey(User,verbose_name=_('author'))
    date_created = models.DateTimeField(_('date created'),default=datetime.now)
    is_active = models.BooleanField(_('is active'),default=False)
    
    meta_keywords = models.CharField(_('meta keywords'),max_length=255)
    meta_description = models.CharField(_('meta description'),max_length=255)
    
    tags = models.ManyToManyField(Tag,verbose_name=_('tags'),blank=True)
    
    objects = models.Manager()
    active_objects  = ActiveArticlesManager()
    
    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        ordering = ('-date_created',)
    
    def __unicode__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        self.rendered_content = markup.markdown(self.content)
        super(Article,self).save(*args,**kwargs)
    
    def get_absolute_url(self):
        return "%s/" % (self.slug)
    
    def set_meta(self):
        """
        Set meta keywords if its empty
        """
        if len(self.meta_keywords.strip()) == 0:
            self.meta_keywords = ','.join([tag.name for tag in self.tags.all()])
        
        if len(self.meta_description.strip()) == 0:
            self.meta_description = self.title.strip()
        
        self.save()
