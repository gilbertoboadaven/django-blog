from django.contrib import admin
from .models import Comment, Post
# Register your models here.




class PostAdmin(admin.ModelAdmin):
    # lista de los campos que seran mostrados en el panel de administracion
    # de las publicaciones
    list_display =  ('title','slug','author','publish','status')
    # lista de los atributos que se usaran para filtrar las publicaciones
    list_filter = ('status','created','publish','author')
    # lista de los campos que usara el buscador para filtrar las publicaciones
    search_fields = ('title','slug')
    prepopulated_fields = {'slug':('title',)}

    date_hierarchy = 'publish'
    # lista de campos que se usaran para ordenar las publicaciones
    ordering = ('status','publish')

# Registro de modelo Post en el panel de admistracion
admin.site.register(Post,PostAdmin)


# Registro del modelo Comment en el panel de administracion haciendo uso de decorador
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created','active')
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')

