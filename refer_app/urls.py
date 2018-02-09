from django.conf.urls import include, url
from django.contrib import admin

from my_user_auth import views


urlpatterns = [
    # Examples:
    # url(r'^$', 'refer_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.main_page),
    #регистрация
    url(r'^registration(_from_)?(?P<user_referer>[a-zA-Z0-9_\-+/=]+)?', views.reg_page),
    url(r'^user_reg$', views.user_reg),
    #проверка почты
    url(r'^confirm_email_(?P<uid>[a-zA-Z0-9_\-+/=]+)/(?P<token>[a-zA-Z0-9_\-+/=]+)$', views.email_confirm),
    #активация аккаунта
    url(r'^activate$', views.activate_account),
]
