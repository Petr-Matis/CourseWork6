
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, TemplateView, DeleteView
from blog.forms import BlogForm
from blog.models import Blog

from pytils.translit import slugify
from django.urls import reverse_lazy, reverse




# Create your views here




class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'post_list'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     # queryset = queryset.filter(is_published=True)
    #     return queryset
    def get_queryset(self, queryset=None, *args, **kwargs):
        """Метод для вывода ТОЛЬКО опубликованных блогов"""
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(sign_of_publication=True)


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['blog_all'] = Blog.objects.all()
        context_data['blog_last_3_date'] = Blog.objects.filter(sign_of_publication=True).order_by('-date_of_create')[:3]
        if self.request.user.groups.first() == 'moderator':
            context_data['qwerty'] = 'moderator'
        elif self.request.user.groups.first() == 'Moderator':
            context_data['qwerty'] = 'Moderator'
        else:
            context_data['qwerty'] = 'ne    moderator'
        context_data['user_gr_name'] = self.request.user.groups.name
        context_data['user_gr_first'] = self.request.user.groups.first()
        return context_data


class BlogCreateView(CreateView):
    """страница для создания блога"""
    model = Blog
    form_class = BlogForm

    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        """динамическое формирование Slug"""
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.header)
            new_blog.save()
        return super().form_valid(form)


# class BlogListView(ListView):
#     """ Главная стр с блогами"""
#     model = Blog
#
#     def get_queryset(self, queryset=None, *args, **kwargs):
#         """Метод для вывода ТОЛЬКО опубликованных блогов"""
#         queryset = super().get_queryset(*args, **kwargs)
#         queryset = queryset.filter(sign_of_publication=True)
#
#         # item = get_object_or_404(Blog, pk=some_pk)
#         # items_table = item.name_table__set.all()
#         # image_items = item.name_images_table__set.all()
#         return queryset


class BlogDetailView(DetailView):
    """Стр с блогом"""
    model = Blog

    def get_object(self, queryset=None):
        """Метод для подсчета просмотров"""
        self.object = super().get_object(queryset)
        self.object.quantity_of_views += 1
        self.object.save()
        return self.object

    def get_success_url(self):
        return reverse('mail_app:viewblog', args=[self.kwargs.get('pk')])


class BlogUpdateView(UpdateView):
    """страница для Изменения блога"""
    model = Blog
    # fields = ('__all__')
    fields = ('header', 'content', 'image')
    # success_url = reverse_lazy('catalog:listblog')

    def form_valid(self, form):
        """динамическое формирование Slug"""
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.header)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mail_app:viewblog')


class BlogDeleteView(DeleteView):
    """страница для удаления блога"""
    model = Blog
    # fields = ('__all__')
    # fields = ('header', 'content', 'image')
    success_url = reverse_lazy('mail_app:blog_list')
