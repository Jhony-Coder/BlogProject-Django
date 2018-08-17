from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from .models import Post
from .forms import PostForm

# Create your views here.

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request, 'Successfully Created')
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		'form': form,
	}
	return render(request, 'posts/post_form.html', context)


def post_detail(request, slug):
	today = timezone.now().date()
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	context = {
		'title': instance.title,
		'instance': instance,
		'today': today,
	}
	return render(request, 'posts/post_detail.html', context)


def post_list(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active()
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()

	query = request.GET.get('q')
	if query:
		queryset_list = queryset_list.filter(
												Q(title__icontains=query)|
												Q(content__icontains=query)|
												Q(user__first_name__icontains=query)|
												Q(user__last_name__icontains=query)
											).distinct() 
	paginator = Paginator(queryset_list, 5) 

	page = request.GET.get('page')
	queryset = paginator.get_page(page)
	context = {
		'title': 'List',
		'object_list': queryset,
		'today':today,
	}
	return render(request,'posts/post_list.html', context)


def post_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, 'Updated')
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		'title': instance.title,
		'instance': instance,
		'form': form,
	}
	return render(request, 'posts/post_form.html', context)


def post_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, 'Deleted')
	return redirect('posts:list')