from django.conf.urls import patterns, include, url

from blog import views as blogview
from helpdesk import views as helpdeskview

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns



from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sandpit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^admin/', include(admin.site.urls)),
	
	#url(r'^$', helpdeskview.helpdesk),
	url(r'^$', blogview.signin),

	### BLOG ###
	url(r'^blog/$', blogview.blog),
	url(r'^notes/$', blogview.blog),
	
	url(r'^add-note/$', blogview.edit_note),
	url(r'^note/(?P<note_id>\d+)/$', blogview.note),
	url(r'^note/(?P<note_id>\d+)/edit/$', blogview.edit_note),
	url(r'^note/(?P<note_id>\d+)/delete/$', blogview.delete_note),

	url(r'^comment/(?P<comment_id>\d+)/delete/$', blogview.delete_comment),

	url(r'^users/$', blogview.users),
	url(r'^user/(?P<user_id>\d+)/$', blogview.user),
	url(r'^user/(?P<user_id>\d+)/notes/$', blogview.blog),

	url(r'^signup/$', blogview.signup),
	url(r'^user/(?P<user_id>\d+)/edit/$', blogview.edit_user),	
	url(r'^user/(?P<user_id>\d+)/delete/$', blogview.delete_user),	
	url(r'^signin/$', blogview.signin),
	url(r'^logout/$', blogview.logout),

	url(r'^passwd/$', blogview.passwd),

	### HELPDESK ###
	url(r'^helpdesk/$', helpdeskview.helpdesk),

	url(r'^create-ticket/$', helpdeskview.create_ticket),
	url(r'^create-group/$', helpdeskview.edit_group),
	url(r'^groups/$', helpdeskview.groups),
	url(r'^group/(?P<group_id>\d+)/delete/$', helpdeskview.delete_group),
	url(r'^group/(?P<group_id>\d+)/edit/$', helpdeskview.edit_group),
	url(r'^ticket/(?P<ticket_id>\d+)/$', helpdeskview.ticket),

	url(r'^ticket/(?P<ticket_id>\d+)/edit/$', helpdeskview.edit_ticket),
	url(r'^ticket/(?P<ticket_id>\d+)/delete/$', helpdeskview.delete_ticket),

	### THIS STUFF IS FOR SOCIAL AUTH ##################################
	url('', include('social.apps.django_app.urls', namespace='social')),
	url('', include('django.contrib.auth.urls', namespace='auth')),
	###################################################################
)






urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()