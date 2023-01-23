import os
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
# from .forms import GeneratorForm
from .models import Template, Post

from .main import main
from slugify import slugify
from datetime import datetime

from django.conf import settings
from django.templatetags.static import static

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def home(request):
    current_user = request.user
    template = Template.objects.all()[0]
    posts = Post.objects.all()
    # posts = Post.objects.filter(user=current_user)
    path = settings.MEDIA_ROOT
    # img_list = os.listdir(f"{path}/articles") ,'images' : img_list
    context = {'template': template, 'posts': posts}
    return render(request, 'write/index.html', context)


def upload(request):
    if request.method == 'POST':
        api_key = str(request.POST.get('api_key'))
        template_intro = str(request.POST.get('template_intro'))
        template_chapitres = str(request.POST.get('template_chapitres'))
        template_conclusion = str(request.POST.get('template_conclusion'))
        title = str(request.POST.get('mots_cles'))
        h2s = str(request.POST.get('h2_soustitres')).split('\n')
        # print(categories_redirections)
        # google_check = bool(request.POST.get('google_check'))
        # h3_check = bool(request.POST.get('h3_check'))

        new_output = ""
        
        # the_title, final_questions = get_title_and_subtitle(mc, google_check)
        filenames = main(api_key=api_key ,title=title, h2s=h2s, template_intro=template_intro, template_chapitres=template_chapitres, template_conclusion=template_conclusion)
        
        for filename, output in filenames.items():
            Post.objects.create(
                title=filename,
                slug=slugify(f"{filename}-{datetime.now().strftime('%Y%m%d')}"),
                content=output,
            )
            new_output += filename.upper() + ' Générer avec succes!\n<br>' + output

    return HttpResponse(new_output)
    
class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'
