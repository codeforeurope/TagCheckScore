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
from image.models import Image, Category, Category_image, Tag_image, Highscore, Blacklist, Freetext_image, Licence_image
from django.contrib import admin
import csv
from django.http import HttpResponse
from multiupload.admin import MultiUploadAdmin
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
BaseFileUploadAdmin = admin.ModelAdmin
class BaseFileUploadAdmin(MultiUploadAdmin):

    change_form_template = 'multiupload/change_form.html'
    change_list_template = 'multiupload/change_list.html'
    multiupload_template = 'multiupload/upload.html'

    multiupload_list = True

    multiupload_form = False
    # max allowed filesize for uploads in bytes
    multiupload_maxfilesize = 3 * 2 ** 20 # 3 Mb
    # min allowed filesize for uploads in bytes
    multiupload_minfilesize = 0
    # tuple with mimetype accepted
    multiupload_acceptedformats = ( "image/jpeg",
                                    "image/pjpeg",
                                    "image/png",)

    def process_uploaded_file(self, uploaded, object, request):

        f = self.model(image=uploaded)
        f.save()
        return {
            'url': f.image_thumb(),
            'thumbnail_url': f.image_thumb(),
            'id': f.id,
            'name': f.id
        }

    def delete_file(self, pk, request):

        obj = get_object_or_404(self.queryset(request), pk=pk)
        obj.delete()

#Code from http://djangosnippets.org/snippets/2369/
def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        writer = csv.DictWriter(response,fields)
        writer.writeheader()
        if header:
            writer.writerow(list(field_names))
        for obj in queryset:
            writer.writerow(dict(zip(fields,[unicode(getattr(obj, field)).encode("utf-8","replace") for field in fields])))
        return response
    export_as_csv.short_description = description
    return export_as_csv


def generate_value(obj, column):
    """Get fields value and convert to ASCIC for string type"""
    row = getattr(obj, column)
    if isinstance(row, basestring):
        row = row.encode('ascii', 'ignore')
    return row

class ImageAdmin(BaseFileUploadAdmin):
    list_display = ('image', 'image_thumb')
    search_fields = ['image']
    
class Tag_imageAdmin(admin.ModelAdmin):
    list_display = ('image', 'tag', 'tCount', 'tag_language', 'image_thumb')
    search_fields = ['image__image', 'tag__tag', 'tag__language']
    list_filter = ('tag__language', )
    list_max_show_all = 10000
    actions = [export_as_csv_action("Export selected items as CSV file", fields=['image', 'tag', 'tCount'], header=False),]
    
class Category_imageAdmin(admin.ModelAdmin):
    list_display = ('image', 'category', 'cCount', 'category_language', 'image_thumb')
    search_fields = ['image__image', 'category__category', 'category__language']
    list_filter = ('category__language', )
    list_max_show_all = 10000
    actions = [export_as_csv_action("Export selected items as CSV file", fields=['image', 'category', 'cCount'], header=False),]
    
class Freetext_imageAdmin(admin.ModelAdmin):
    list_display = ('image', 'text', 'language', 'image_thumb')
    search_fields = ['image__image']
    list_filter = ('language', )
    list_max_show_all = 10000
    actions = [export_as_csv_action("Export selected items as CSV file", fields=['image', 'text'], header=False),]
    
class Licence_imageAdmin(admin.ModelAdmin):
    list_display = ('title', 'text')
    
class Highscore_imageAdmin(admin.ModelAdmin):
    list_display = ('name', 'points')
    search_fields = ['name']
    
class Blacklist_imageAdmin(admin.ModelAdmin):
    list_display = ('word',)
    search_fields = ['word']
    
#class TagAdmin(admin.ModelAdmin):
#    search_fields = ['tag']
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'language')
    search_fields = ['category']

admin.site.register(Image, ImageAdmin)
#admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Category_image, Category_imageAdmin)
admin.site.register(Freetext_image, Freetext_imageAdmin)
admin.site.register(Licence_image, Licence_imageAdmin)
admin.site.register(Tag_image, Tag_imageAdmin)
admin.site.register(Highscore, Highscore_imageAdmin)
admin.site.register(Blacklist, Blacklist_imageAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Site)