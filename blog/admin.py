from django.contrib import admin
from django.forms import Textarea
from django.db import models
from django.template.defaultfilters import truncatechars

from blog.models import PostCategory, Post, Comment

admin.site.site_header = "Blog administration"

@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
	search_fields = ["name"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ["title",
					"category",
					"published",
					"created_at",
					"comments_count"]

	list_filter = ["category__name",
				   "published"]

	autocomplete_fields = ["category"]

	formfield_overrides = {
							models.TextField: {"widget": Textarea(attrs={"rows": 20, "cols": 80})}
						   }

	def comments_count(self, obj):
		return Comment.objects.filter(post=obj).count()
	comments_count.short_description = "Comments"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ["post",
					"author_name",
					"text_short",
					"status",
					"moderation_text",
					"created_at"]

	list_editable = ["status",
					 "moderation_text"]

	list_filter = ["status"]

	search_fields = ["post__title",
	   				 "author_name"]

	def text_short(self, obj):
		if len(obj.text) > 20:
			body = obj.text[:20] + " (...)"
		else:
			body = obj.text
		return body
	text_short.short_description = "Text"

