from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
                       (r'^$', 'application1.views.home'),
                       #(r'^timeline$', 'application1.views.timeline'),
                       #(r'^timeline_dynamic', 'application1.views.timeline_dynamic'),

                       (r'^createUser', 'application1.views.createUser'),
                       (r'^login', 'application1.views.login_view'),
                       (r'^logout', 'application1.views.logout_view'),
                       #(r'^load_timeline', 'application1.views.get_timeline_ajax'),
                       (r'^load_dynamic', 'application1.views.get_classification'),
                       (r'^new_timeline', 'application1.views.html5_timeline'),
                       (r'^get_relevant_articles', 'application1.views.get_relevant_articles'),
#    'psets.views',
#    (r'^$', 'index'),
#    (r'^create/$', 'create_pset'),
#    (r'^pset/(?P<pset_id>\d+)/$', 'pset_detail'),
#    (r'^pset/(?P<pset_id>\d+)/add_question/$', 'add_question'),
)




