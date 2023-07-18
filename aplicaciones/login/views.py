from django.shortcuts import render
from django.shortcuts import redirect
from .forms import UsuarioNuevoForm, LoginForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
# Create your views here.
class LoginUser(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('inicio_app:inicio')
    template_name = 'login/login.html'
    def form_valid(self, form):
        credenciales = form.cleaned_data
        user = authenticate(username=credenciales['username'],password=credenciales['password'])
        
        if 'count' in self.request.session:
            count = self.request.session['count']+1
        else:
            count = 1

        self.request.session['count'] = count
        
        if count>3:
            messages.add_message(self.request, messages.INFO,'Demasiados intentos fallidos')
            return redirect(reverse_lazy('login_app:locked'))
        else:
            if user is not None:
                login(self.request, user)
                if self.request.GET:
                    next = self.request.GET['next']
                    return redirect(next)
                return redirect(self.success_url)
            else:
                messages.add_message(self.request, messages.INFO,'Error: credenciales incorrectas '+str(count))
                return redirect(reverse_lazy('login_app:login'))
        
def cerrar_sesion(request):
    logout(request)
    return redirect(reverse_lazy('login_app:login'))

def nuevo_usuario(request):
    form  = UsuarioNuevoForm()
    if request.method=='POST':
        form = UsuarioNuevoForm(request.POST)
        if form.is_valid():
            user = form.save()
            # user.is_staff = True
            # user.save()
            login(request, user)
            return redirect('inicio_app:inicio')
    return render(request, 'login/nuevo_usuario.html',context={'form':form})

from .forms import CaptchaForm
def locked(request):
    if request.POST:
        form = CaptchaForm(request.POST)
        if form.is_valid():
            request.session['count'] = 0
            return redirect(reverse_lazy('login_app:login'))
    else:
        form = CaptchaForm()

    return render(request, 'login/captcha.html', context={'form':form})