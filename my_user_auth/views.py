from django.shortcuts import render
from django.http import HttpResponse
import base64
from my_user_auth.models import MyUsers
from django.contrib.auth.models import User
from django.utils import timezone
import my_token
from django.core.mail import send_mail
from django.conf import settings


def create_person_id():
	''' функция для определения персоанльного идентификатора пользователя'''
	try:
		last_user = MyUsers.objects.latest('person_id')
		return last_user.person_id + 1
	except:
		#значения персональных id начинается с 1000
		return 1000


# Create your views here.
def reg_page(request, user_referer = None):
	''' функция для отображения страницы регистрации'''
	referer_id = None
	if user_referer:
		try:
			referer_id = base64.urlsafe_b64decode(user_referer)
			referer_id = referer_id.decode('utf-8')
		except:
			return HttpResponse("Неверная ссылка")
	return render(request, 'registration.html', {'referer_id': referer_id})

def user_reg(request):
	''' функция для регистрации пользователя в системе'''
	if request.method == 'POST':
		referer_id = request.POST["referer_id"]
		user_name = request.POST["user_name"]
		email = request.POST["user_email"]
		password = request.POST["user_password1"]

		#создаем пользователя
		user = User(username = user_name, email = email, password = password)
		user.is_active = False
		user.save()

		try:
			#определяем персональный id
			new_person_id = str(create_person_id())
			b_person_id = bytes(new_person_id, 'utf-8')
			uid = base64.urlsafe_b64encode(b_person_id).decode('utf-8')
			#определяем токен для активации аккаунта
			user_token, url_token = my_token.create_token()
			current_datetime = timezone.now()
			#определяем реферальную ссылку
			referal_link = "http://{0}/registration_from_{1}".format(request.META['HTTP_HOST'], uid)

			#создаём пользователя с дополнительными возможностями
			my_user = MyUsers(
				user = user, 
				person_id = new_person_id,
				 token = user_token, 
				 time_activation = current_datetime, 
				 user_rating = 0, 
				 referal_link = referal_link
				 )
			#если пользователь зарегистрировался по реферальной ссылке
			if referer_id != 'None':
				referer = MyUsers.objects.get(person_id = referer_id)
				my_user.referer = referer
			my_user.save()

			#сообщение для активационного письма
			mail_text = '''Hello, {0}.
			Confirm email for activation your account to host {1}.
			<a href="http://{1}/confirm_email_{2}/{3}">http://{1}/confirm_email_{2}/{3}</a>'''.format(user_name, request.META['HTTP_HOST'], uid, url_token)

			#отправка письма пользователю
			send_mail(
				'Confirm your email',
				mail_text,
				settings.EMAIL_HOST_USER,
				[email],
				html_message = mail_text
				)
			message = "На указанную вами почту, было выслано письмо для активации аккаунта"
		except Exception as err:
			print(err)
			user.delete()
			message = "Что-то не так"
	else:
		message = "Попробуйте по-другому"

	
	return render(request, 'message.html', {'message':message})

def main_page(request):
	users = MyUsers.objects.all().order_by('-user_rating')
	return render(request, 'main.html', {'users':users})



def email_confirm(request, uid, token):
	''' функция для активации аккаунта'''

	b_user_id = base64.urlsafe_b64decode(uid)
	user_id = b_user_id.decode('utf-8')
	try:
		my_user = MyUsers.objects.get(person_id = user_id)
	except:
		message = "Неверная ссылка"
	else:
		b_token = base64.urlsafe_b64decode(token)
		token = b_token.decode('utf-8')
		#определяем равен ли полученный токен токену пользователя
		if token == my_user.token:
			date = timezone.now() - my_user.time_activation
			#проверяем не просрочен ли токен
			if date.days > 0:
				message = "Время активации просрочено"
			else:
				#проверяем переходил ли пользователь уже по ссылке
				if not my_user.user.is_active:
					my_user.user.is_active = True
					my_user.user.save()
					if my_user.referer:
						current_rating = my_user.referer.user_rating
						my_user.referer.user_rating = current_rating + 10
						print(my_user.referer.user_rating)
						my_user.referer.save()
					message = "Активация прошла успешно"
				else:
					message = "Ссылка уже была использована"
		else:
			message = "Неверная ссылка"

	return render(request, 'message.html', {'message':message})



def activate_account(request):
	''' функция для активации аккаунта'''
	if request.method == 'POST':

		user_name = request.POST["user_name"]
		email = request.POST["user_email"]
		password = request.POST["user_password1"]

		try: 
			user = User.objects.get(
				username = user_name, 
				email = email, 
				password = password
				)
		except:
			message = "Пользователь с такими данными не зарегистрирован, проверьте введенные данные."
		else:
			my_user = MyUsers.objects.get(user = user)
			if my_user.user.is_active:
				message = "Данный аккаунт уже активирован"
			else:
				b_person_id = bytes(str(my_user.person_id), 'utf-8')
				uid = base64.urlsafe_b64encode(b_person_id).decode('utf-8')
				#определяем токен для активации аккаунта
				user_token, url_token = my_token.create_token()
				current_datetime = timezone.now()

				my_user.token = user_token
				my_user.time_activation = current_datetime
				my_user.save()

				#сообщение для активационного письма
				mail_text = '''Hello, {0}.
				Confirm email for activation your account to host {1}.
				<a href="http://{1}/confirm_email_{2}/{3}">http://{1}/confirm_email_{2}/{3}</a>'''.format(user_name, request.META['HTTP_HOST'], uid, url_token)

				#отправка письма пользователю
				send_mail(
					'Confirm your email',
					mail_text,
					settings.EMAIL_HOST_USER,
					[email],
					html_message = mail_text
					)
				message = "На указанную вами почту, было выслано письмо для активации аккаунта"

		return render(request, 'message.html', {'message':message})
	else:
		return render(request, 'activate_account.html')
	