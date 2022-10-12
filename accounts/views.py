from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django_currentuser.middleware import get_current_user

from accounts.forms import FormLoadAvatar
from accounts.models import Profile


def get_cur_branch():
    profile = Profile.objects.get(user=get_current_user())
    # Перестраховка: если вдруг "текущая" и "по умолчанию" не выбраны
    if profile.branch_current:
        cur_branch = profile.branch_current
    elif profile.branch_default:
        cur_branch = profile.branch_default
    else:
        cur_branch = profile.branch.all().first()
    return cur_branch


def get_branches():
    user = get_current_user()
    branches = Profile.objects.get(user=user).branch.all()
    return branches


# # Генерирует пароль
# def random_password():
#     pas = ''
#     for x in range(5):  # 10 знаков
#         pas = pas + random.choice(list('1234567890'))  # Символы, из которых будет составлен пароль
#     return pas
#

# Профиль пользователя
@login_required()
def user_profile(request):
    curr_user = Profile.objects.get(user=get_current_user())
    form = FormLoadAvatar(request.POST or None, request.FILES or None, instance=curr_user.pk and Profile.objects.get(id=curr_user.pk))

    if request.POST:
        if form.is_valid():
            form.save()

    return render(request, 'accounts/profile.html', {
        'form_avatar': form,
        'profile': Profile.objects.get(user=request.user)}
                  )

#
# # Настройки пользователя
# @login_required()
# def user_settings(request):
#     return redirect('page_error503')
#
#
# # Смена текущей сервисной компании
# @login_required()
# def change_cur_scompany(request):
#     form = change_cur_scompany_form(request.POST, user=request.user)
#     if request.POST:
#         if form.is_valid():
#             cur_scompany = ServiceCompanies.objects.get(id=int(request.POST['cur_scompany']))
#             Profile.objects.filter(user=request.user).update(scompany_current=cur_scompany)
#
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
#
# # Добавление нового пользователя с предмодерацией
# def register_account(request):
#     args = {}
#     args.update(csrf(request))
#
#     if request.POST:
#         form = register_account_form(request.POST)
#
#         if form.is_valid():
#             smsc = SMSC()
#             lastname = form.cleaned_data['last_name']
#             firstname = form.cleaned_data['first_name'].split(' ')[0]
#             middlename = form.cleaned_data['first_name'].split(' ')[1]
#             login = slugify(lastname + firstname[0] + middlename[0])
#             password = form.cleaned_data['pass_new']
#             scompany = form.cleaned_data['scompany']
#             location = form.cleaned_data['location']
#             birthday = form.cleaned_data['birthday']
#             phone = form.cleaned_data['phone']
#             personal_data = form.cleaned_data['personal_data']
#             email = '%s@amulet-secur.ru' % login
#             text = "АРМ Заявки.Пользователь %s зарегестирован в системе" % login
#
#             u = User.objects.create_user(login, email, password)
#             u.save()
#             if u:
#                 # Деактивируем учётку, чтобы сразу после создания, пользователь зайти не смог, а также добавляем ФИО
#                 User.objects.filter(id=u.pk).update(first_name=firstname + ' ' + middlename, last_name=lastname,
#                                                     is_active=False)
#                 # Обновляем профиль
#                 Profile.objects.filter(user=u).update(location=location, birthday=birthday, personal_data=personal_data,
#                                                       phone=clean_phone(phone))
#                 Profile.objects.get(user=u).scompany.add(scompany)
#                 # Надо получить список админов системы с номером телефона
#                 admins = Profile.objects.filter(user__in=User.objects.filter(is_staff=True), phone__isnull=False)
#                 for admin in admins:
#                     # Сообщаем админам, что добавлен новый пользователь и его надо проверить и активировать
#                     smsc.send_sms('7%s' % admin.phone, text, sender="arm_zayavki")
#             # Отправляем нового пользователя на страницу уведомления об успешном создании
#             return render(request, 'success.html',
#                           {'message_type': u'Ваш аккаунт успешно добавлен',
#                            'message_description': u'Системные администраторы уведомлены о добалении Вами учетной записи. '
#                                                   u'В течении суток учетная запись будет проверена и активирована',
#                            'message_ps': u'Для подтверждения права на доступ, необходимо предоставить служебную записку за подписью руководителя.'})
#         else:
#             return render(request, 'register_account.html', {'form': form})
#     else:
#         args['form'] = register_account_form()
#         return render(request, 'register_account.html', args)
#
#
# # Обновление данных профиля
# @login_required()
# def update_profile(request):
#     args = {}
#     args.update(csrf(request))
#
#     if request.method == 'POST':
#         form = update_profile_form(request.POST)
#
#         if form.is_valid():
#             Profile.objects.filter(user=request.user). \
#                 update(birthday=form.cleaned_data['birthday'],
#                        phone=clean_phone(form.cleaned_data['phone']))
#             return redirect('dashboard:index')
#         else:
#             return render(request, 'update_profile.html', {'form': form})
#     else:
#         args['form'] = forgot_password_form()
#         args['user'] = request.user
#     return render(request, 'update_profile.html', args)
#
#
# # Восстановление доступа к программе
# def forgot_password(request):
#     args = {}
#     args.update(csrf(request))
#
#     if request.method == 'POST':
#         form = forgot_password_form(request.POST)
#
#         if form.is_valid():
#             smsc = SMSC()
#             login = form.get_user().user.username
#             random_psw = random_password()
#
#             text = "АРМ 'Заявки'. Пользователь %s, ваш разовый пароль: %s." % (login, random_psw)
#             smsc.send_sms('%s' % request.POST['phone'], text, sender="arm_zayavki")
#             return redirect('change_password', username=login, psw_sms=random_psw)
#         else:
#             return render(request, 'forgot_password.html', {'form': form})
#     else:
#         args['form'] = forgot_password_form()
#     return render(request, 'forgot_password.html', args)
#
#
# # Смена разового пароля на пароль пользователя
# def change_password(request, username, psw_sms):
#     args = {}
#     args.update(csrf(request))
#
#     if request.method == 'POST':
#         form = change_password_form(request.POST)
#
#         if form.is_valid():
#             login = form.cleaned_data['username']
#             password = form.cleaned_data['pass_new']
#             try:
#                 u = User.objects.get(username=login)
#                 u.set_password(password)
#                 u.save()
#             except:
#                 return render(request, 'change_password.html', {'form': form})
#             return redirect('login')
#         else:
#             return render(request, 'change_password.html', {'form': form})
#     else:
#         args['form'] = change_password_form(data={'username': username, 'pass_hidden': psw_sms})
#     return render(request, 'change_password.html', args)
#
#
# # Декоратор для вью. Разрешает доступ в случае нахождения пользователя в одной из указанных групп.
# def group_required(group, login_url=None, raise_exception=False):
#     def in_groups(user):
#         if isinstance(group, six.string_types):
#             groups = (group,)
#         else:
#             groups = group
#         if user.is_superuser or bool(user.groups.filter(name__in=groups)):
#             return True
#         if raise_exception:
#             raise PermissionDenied
#         return False
#
#     return user_passes_test(in_groups, login_url=login_url)
#
#
# @login_required()
# def page_error403(request):
#     error_type = '403'
#     error_description = 'Вам сюда нельзя'
#     return render(request, 'error.html', {'error_type': error_type, 'error_description': error_description})
#
#
# @login_required()
# def page_error423(request):
#     error_type = '423'
#     error_description = 'Вам не назначена группа прав'
#     return render(request, 'error.html', {'error_type': error_type, 'error_description': error_description})
#
#
# @login_required()
# def page_error503(request):
#     error_type = '503'
#     error_description = 'Сервис недоступен'
#     return render(request, 'error.html', {'error_type': error_type, 'error_description': error_description})
