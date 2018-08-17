from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone

# Create your models here.

class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(PostManager, self).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
	return "%s/%s" %(instance.slug, filename)

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
	title = models.CharField(max_length=128)
	slug = models.SlugField(unique=True, max_length=150)
	content = models.TextField(max_length=1000)
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	image = models.ImageField(upload_to=upload_location, null=True, blank=True, height_field=None, width_field=None)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	objects = PostManager()

	def __str__(self):
		return self.title	

	def get_absolute_url(self):
		return reverse('posts:detail', kwargs={'slug': self.slug})
		#return f"/posts/detail/{self.id}/"
	
	def get_absolute_url_edit(self):
		return reverse('posts:edit', kwargs={'slug':self.slug})

	class Meta():
		ordering = ['-timestamp', '-updated']


def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by('-id')
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug


def pre_save_post_reciver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_reciver, sender=Post)















