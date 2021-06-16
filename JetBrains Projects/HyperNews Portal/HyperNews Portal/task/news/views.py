from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views import View
from django.conf import settings
import json
import itertools
import random
from datetime import datetime

JSON_DATA = settings.NEWS_JSON_PATH


def get_json_data():
    with open(JSON_DATA, 'r') as f:
        data = json.load(f)
    return data


def add_json_data(updated_data):
    with open(JSON_DATA, 'w') as f:
        json.dump(updated_data, f)


class ComingSoonView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class ArticlesListView(View):
    def get(self, request, *args, **kwargs):
        data = get_json_data()
        q = request.GET.get('q')
        if q:
            q = q.lower().strip()
            data = list(filter(lambda x: q in x['title'].lower().strip(), data))

        sorted_news = sorted(data, key=lambda i: i['created'], reverse=True)
        groupped_news = itertools.groupby(sorted_news, lambda i: i['created'][:10])

        articles = []
        for k, v in groupped_news:
            articles.append((k, list(v)))

        context = {'articles': articles}
        return render(request, 'news/articles.html', context=context)


class ArticleView(View):
    def get(self, request, article_id, *args, **kwargs):
        data = get_json_data()
        article = list(filter(lambda x: x['link'] == int(article_id), data))
        if not article:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        context = {'article': article[0]}
        return render(request, 'news/article.html', context=context)


class CreateArticleView(View):
    data = get_json_data()

    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html')

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        text = request.POST.get('text')
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        link = len(self.data) + 1

        new_article = {"created": created,
                       "text": text,
                       "title": title,
                       "link": link}

        updated_data = self.data
        updated_data.append(new_article)
        add_json_data(updated_data)
        return redirect('/news/')


