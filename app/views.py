from django.shortcuts import render
from .models import *
from django.views.generic import View #写类视图
# Create your views here.

# 创建类视图
class BaseView(View):
    def get(self,request,*args,**kwargs):
        commets = Comment.objects.filter(is_delete=False).all()

        art_ids = []
        new_commets = []
        for comment in commets:
            if comment.article.id not in art_ids:
                art_ids.append(comment.article.id)
                new_commets.append(comment)
        return new_commets

class IndexView(BaseView):
    def get(self,request,*args,**kwargs):
        new_commets =super().get(request,*args,**kwargs)
        banners = Banner.objects.filter(is_delete=False).all()
        top_article = Article.objects.filter(is_delete=False,is_top=True).all()
        cats = Category.objects.filter(is_delete=False).all()
        all_article = Article.objects.filter(is_delete=False).all()[:10]
        fks = FriendLink.objects.filter(is_delete=False).all()
        return render(request,'index.html',locals())


class ListView(BaseView):
    def get(self,request,*args,**kwargs):
        new_commets =super().get(request,*args,**kwargs)
        all_article = Article.objects.filter(is_delete=False).all()
        tags = Tag.objects.filter(is_delete=False).all()
        return render(request,'list.html',locals())


class DetailView(BaseView):
    def get(self,request,*args,**kwargs):
        id = kwargs.get('id')
        new_commets = super().get(request, *args, **kwargs)
        try:
            article = Article.objects.get(id=id)
            article.vnum+=1
            article.save()
            return render(request,'show.html',locals())
        except Article.DoesNotExist:
            return render(request,'404.html')
        # return render(request,'show.html',locals())