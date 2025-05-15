import bcrypt
from functools import wraps
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.contrib.auth import logout
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
    
def logout_view(request):
    logout(request)
    return redirect('login')

@role_required('Staff', 'Administrador')
def home(request):
    return render(request, 'home.html')

@role_required('Staff', 'Administrador')
def profile(request):
    context = get_user_profile(request)

    if request.method == 'POST':
        name_profile = request.POST.get("name_profile")
        description = request.POST.get("description")

        if not name_profile or not description:
            messages.error(request, "Todos os campos são obrigatórios")
            return redirect("profile")

        try:
            profile_system = models.Perfil.objects.create(
                nome=name_profile,
                descricao=description
            )
            profile_system.full_clean()
            profile_system.save()

            messages.success(request, "Perfil Cadastrado com sucesso!")
            return redirect("profile")
        except Exception as e:
            print(f'Erro ao salver {e}')
            messages.error(request, f"Erro ao salvar perfil {e}")

    return render(request, 'profile.html', context)

@role_required('Staff', 'Administrador')
def user(request):
    context = get_user_profile(request)

    if request.method == 'POST':
        user_name = request.POST.get("user")
        category_profile = request.POST.get("perfil_select")
        email = request.POST.get("email")
        password = request.POST.get("password_confirm")
        cpf = request.POST.get('cpf')

        if not user_name or not category_profile or not email or not password:
            messages.error(request, 'Preencha todos os campos')
            return redirect('user_register')
        
        if models.Usuario.objects.filter(cpf=cpf).exists():
            messages.error(request, 'CPF já cadastrado')
            return redirect('user_register')
        
        if models.Usuario.objects.filter(login=user_name).exists():
            messages.error(request, 'Nome de Usuário já existente')
            return redirect('user_register')
        
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            perfil_model = models.Perfil.objects.get(id=category_profile)

            profile = models.Usuario.objects.create(
                nome=user_name,
                login=user_name,
                email=email,
                id_perfil=perfil_model,
                cpf=cpf,
                senha=hashed_password
            ) 
            profile.full_clean()
            profile.save()

            messages.success(request, "Usuário salvo com Sucesso!")
            return redirect('user_register')
        except ValidationError as ve:
            messages.error(request, f'Erro ao salver usuário {str(ve)}')
        except Exception as e:
            print(f'Erro ao salvar usuário {e}')
            messages.error(request, f'Erro ao salver usuário {str(e)}')

    context.update({
        'categorys': models.Perfil.objects.all()
    })

    return render(request, 'cadastro_usuario.html', context)

@role_required('Staff', 'Administrador')
def event_register(request):
    context = get_user_profile(request)

    if request.method == 'POST':
        name_event = request.POST.get("name_event")
        date_event = request.POST.get("data_evento")
        cpt_event = request.POST.get("cpt_evento")
        id_sector = request.POST.get("select_sector")
        img_input = request.POST.get("input_img")

        if not name_event or not date_event or not cpt_event or not id_sector or not img_input:
            messages.error(request, "Todos os campos são obrigatórios")
            return redirect("events_register")

        sector_id = models.Setores.objects.get(id=id_sector)

        save_event = models.Evento.objects.create(
            nome=name_event,
            data_evento=date_event,
            capacidade_pessoas=cpt_event,
            imagem_evento=img_input,
            id_setores=sector_id
        )
        save_event.full_clean()
        save_event.save()

    context.update({
        'sectores': models.Setores.objects.all()
    })

    return render(request, 'cadastro_evento.html', context)

@role_required('Staff', 'Administrador')
def building_register(request):
    return render(request, 'setores.html')