import bcrypt
from functools import wraps
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from . import models

# Create your views here.

def get_user_profile(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = models.Usuario.objects.select_related('id_perfil').get(id=user_id)
            return {
                'user_id': user.id,
                'user_name': user.nome,
                'user_role': user.id_perfil.nome,
                'is_authenticated': True
            }
        except models.Usuario.DoesNotExist:
            return {'user_name': '', 'is_authenticated': False}
    return {'user_name': '', 'is_authenticated': False}

def role_required(*roles):
    def decorator(view_funv):
        @wraps(view_funv)
        def _wrapped_view(request, *args, **kwargs):
            user_profile = get_user_profile(request)
            user_role = user_profile.get('user_role')
            if user_role not in roles:
                messages.error(request, 'Você não tem permissão para acessar esta página')
                return redirect("login")

            return view_funv(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    username = request.POST.get('user')
    password = request.POST.get('password')

    # Validar entrada
    if not username or not password:
        messages.error(request, 'Preencha todos os campos')
        return render(request, 'login.html')

    try:
        user = models.Usuario.objects.get(login=username)
        # Verificar a senha com bcrypt
        senha_bytes = password.encode('utf-8')  # Senha fornecida
        senha_hash = user.senha.encode('utf-8')  # Hash armazenado
        if bcrypt.checkpw(senha_bytes, senha_hash):
            request.session['user_id'] = user.id
            request.session['user_name'] = user.nome
            request.session['user_role'] = user.id_perfil.nome
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
            return render(request, 'login.html')
    
    except models.Usuario.DoesNotExist:
        messages.error(request, 'Usuário ou senha inválidos')
        return render(request, 'login.html')

@role_required('Staff', 'Administrador')
def home(request):
    return render(request, 'home.html')

def profile(request):
    return render(request, 'profile.html')

def user(request):
    return render(request, 'cadastro_usuario.html')

def event_register(request):
    return render(request, 'cadastro_evento.html')

def building_register(request):
    return render(request, 'setores.html')