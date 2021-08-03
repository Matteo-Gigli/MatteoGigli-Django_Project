from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Post
from .forms import WriteAPost
from django.contrib import messages
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from datetime import timedelta
import redis
from pprint import pprint

client = redis.StrictRedis(host='127.0.0.1', port='6379')


class Homeview(ListView):
    queryset = Post.objects.all().order_by('-publish_on')
    template_name = 'homepage.html'



def detail_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {'post': post, 'pk': pk}
    return render(request, 'detail_post.html', context)


def write_a_post(request):
    if request.method == 'POST':
        form = WriteAPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.title = post.title
            post.author = request.user
            post.content = post.content
            post.save()
            redis_write_post = {
                'Author': str(post.author),
                'Title': str(post.title),
                'Content': str(post.content),
                'Publish On': str(post.publish_on),
            }
            client.set('redis_write_post', str(redis_write_post))
            #post.writeOnChain()
            messages.success(request, 'You share a Post, Keep Going to tell everybody what you think!')
            return redirect('/homepage/')
        else:
            form = WriteAPost()
            context = {'form': form}
            return render(request, 'write_a_post.html', context)
    else:
        form = WriteAPost()
        context ={'form': form}
        return render(request, 'write_a_post.html', context)


@staff_member_required
def counting_post(request):
    post = Post.objects.values("author").annotate(Count("title"))
    context = {'post': post}
    return render(request, 'counting_post.html', context)



def find_in_site(request):
    if "q" in request.GET:
        querystring = request.GET.get("q")
        if len(querystring) == 0:
            return redirect("/cerca/")

        else:
            content = Post.objects.filter(content__icontains=querystring).count()
            context = {
                "content": content,
            }
            return render(request, "find_in_site.html", context)

    else:
        return render(request, "find_in_site.html")


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
        if ip != ip:
            print("Ip is different")
    return HttpResponse(ip)


def last_hour_published_post(request):
    response = []
    post = Post.objects.filter(publish_on__gte=timezone.now() - timedelta(hours=2))
    for post in post:
        response.append(
            {
                "Publish On ": post.publish_on,
                "Title": post.title,
                "Content": post.content,
                "Author": post.author.pk
            }
        )
    return JsonResponse(response, safe=False)