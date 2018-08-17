from django.urls import path
from .views import (post_create, post_update, 
					post_detail, post_list, post_delete)

app_name = 'posts'

urlpatterns = [
	path(r'', post_list, name='list'),
	path(r'create/', post_create, name='create'),
	path(r'<slug:slug>/edit/', post_update, name='update'),
	path(r'<slug:slug>/detail/', post_detail, name='detail'),
	path(r'<slug:slug>/delete/', post_delete, name='delete'),
]