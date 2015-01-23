from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.template import Context
from datetime import datetime
from models import *
from django.shortcuts import get_object_or_404
from forms import *
from django.template.context import RequestContext	
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
	categorias = Categoria.objects.all() 
	#enlaces = Enlase.objects.all()
	enlaces = Enlase.objects.order_by("-votos").all()
	return render_to_response("index.html",locals())

def categoria(request, id_cat):
	categorias = Categoria.objects.all()
	cat = get_object_or_404(Categoria, pk = id_cat)
	#cat = Categoria.objects.get(pk=id_cat) 	
	enlaces = Enlase.objects.filter(categoria=cat)
	template="index.html"
	return render_to_response(template, locals())

@login_required
def plus(request, id_enlace):
	enlace = Enlase.objects.get(pk=id_enlace)
	enlace.votos = enlace.votos+1
	enlace.save()
	return HttpResponseRedirect("/")

@login_required
def minus(request, id_enlace):
	enlace = Enlase.objects.get(pk=id_enlace)
	enlace.votos = enlace.votos-1
	enlace.save()
	return HttpResponseRedirect("/")

@login_required
def add(request):
	categorias = Categoria.objects.all()
	if request.method == "POST":
		form = EnlaceForm(request.POST)
		if form.is_valid():
			enlace = form.save(commit = False)
			enlace.usuario=request.user
			enlace.save()
			return HttpResponseRedirect("/")
		else:
			form = EnlaceForm()

	#template = "form.html"
	return render_to_response("form.html", 
					context_instance=RequestContext(request,locals()))

def hora_actual(request):
	"""
	MODO LARGO
	hora = datetime.now()
	t = get_template('hora.html')
	c = Context({'hora':hora, 'nombre':'jimialex'})
	html = t.render(c)
	return HttpResponse(html)
	
	MODO CORTO
	"""
	now=datetime.now()
	return render_to_response('hora.html',{'hora':now, 'nombre':'el nombre del usuario'})

