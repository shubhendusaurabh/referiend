from django.conf.urls import patterns, url

urlpatterns = patterns('userprofile.views',
        url(r'^profile/(?P<pk>\d+)/$', 'userprofile_detail', name='userprofile_detail'),
        url(r'^profile/edit/(?P<pk>\d+)/$', 'userprofile_edit', name='userprofile_edit'),
        url(
            regex=r'^$',
            view='userprofile_list',
            name='userprofile_list'
        ),
)
