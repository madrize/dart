from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from forms import ArticleForm
from models import Article,Tag
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify

def get_article_details(request,
                        slug,
                        template="articles/get.html"):
    """
    Returns the details about an article
    """
    article = get_object_or_404(Article,slug=slug)
    return render_to_response(template,
                              {'article':article},
                              context_instance=RequestContext(request))


def post_article(request,
                 success_url = "/",
                 template="articles/post.html"):
    """ Post new article """
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            tags = form.cleaned_data['tags']
            # new article
            art = Article(title=title,content=content,slug=slugify(title),author=request.user)
            art.save()
            # add tags
            for tag in tags:
                try:
                    t = Tag.objects.get(name=tag)
                except Tag.DoesNotExist:
                    t = None
                # if t doesnt exist
                if t is None:
                    t = Tag(name=tag,slug=slugify(tag))
                    t.save()
                # add the tag to the article
                art.tags.add(t)
            # set meta
            art.set_meta()
            # done here
            return HttpResponseRedirect(success_url)
    else:
        form = ArticleForm()
    
    return render_to_response(template,
                              {'form':form},
                              context_instance=RequestContext(request))



def get_articles(request,
                 limit=5,
                 template="articles/all.html"):
    """
    Returns a list of articles
    """
    try:
        articles = Article.active_objects.all()[:limit]
    except:
        articles = None
    
    return render_to_response(template,
                              {'articles':articles},
                              context_instance=RequestContext(request))