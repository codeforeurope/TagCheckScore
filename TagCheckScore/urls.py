"""
Tag. Check. Score. is a program to crowdsource metadata for picture files.  
Copyright (C) 2013  Fraunhofer Institute of Open Communication Systems (FOKUS)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see [http://www.gnu.org/licenses/].

Contact: info [at] fokus [dot] fraunhofer [dot] de
"""
from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crowdsrc.views.home', name='home'),
    # url(r'^crowdsrc/', include('crowdsrc.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/',  include(admin.site.urls)), # admin site
    #url(r'^image/(?P<slug>[-\w]+)/$', 'image.views.detail'),
    (r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^$', 'image.views.index',name="main"),
    url(r'^kontakt/', 'image.views.kontakt',name="kontakt"),
    url(r'^info/', 'image.views.info',name="info"),
    url(r'^impressum/', 'image.views.impressum',name="impressum"),
    url(r'^privacy/', 'image.views.privacy',name="privacy"),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT}),
    (r'^i18n/', include('django.conf.urls.i18n')),
)
