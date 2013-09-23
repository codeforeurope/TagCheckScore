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
from django.db import models
from django.conf import settings


        
class Category(models.Model):
    category = models.TextField(u'Category', primary_key=False)
    language = models.CharField(max_length=5, blank=False)
    def __unicode__(self):
        return self.category
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
class Tag(models.Model):
    tag = models.TextField(u'Tag', primary_key=False)
    language = models.CharField(max_length=5, blank=False)
    def __unicode__(self):
        return self.tag
    class Meta:
        verbose_name = "Crowdsourced Tags"
        verbose_name_plural = "Crowdsourced Tags"
        
class Image(models.Model):
    #id = models.IntegerField(u'ID')
    image = models.ImageField(upload_to='images')
    tags = models.ManyToManyField(Tag, through='Tag_image')
    def __unicode__(self):
        return self.image.__str__()
    def image_thumb(self):
        return '<img src="' + settings.MEDIA_URL + '%s" width="100" height="100" />' % (self.image)
    image_thumb.allow_tags = True
    
class Tag_image(models.Model):
    image = models.ForeignKey(Image)
    tag = models.ForeignKey(Tag)
    tCount = models.IntegerField(u'Tag Count')
    def __unicode__(self):
        return self.image.__str__()
    def image_thumb(self):
        return '<img src="' + settings.MEDIA_URL + '%s" width="100" height="100" />' % (self.image)
    image_thumb.allow_tags = True
    def tag_language(self):
        return self.tag.language
    class Meta:
        verbose_name = "Crowdsourced Imagetag"
        verbose_name_plural = "Crowdsourced Imagetags"
    
class Freetext_image(models.Model):
    image = models.ForeignKey(Image)
    text = models.TextField(u'Freetext')
    language = models.CharField(max_length=5, blank=False)
    def __unicode__(self):
        return self.image.__str__()
    def image_thumb(self):
        return '<img src="' + settings.MEDIA_URL + '%s" width="100" height="100" />' % (self.image)
    image_thumb.allow_tags = True
    
    class Meta:
        verbose_name = "Crowdsourced Freetext"
        verbose_name_plural = "Crowdsourced Freetexts"
        
class Licence_image(models.Model):
    title = models.TextField(u'Licencetitle')
    text = models.TextField(u'Licencetext')
    def __unicode__(self):
        return self.title.__str__()
    class Meta:
        verbose_name = "Licence"
        verbose_name_plural = "Licences"
    
class Category_image(models.Model):
    image = models.ForeignKey(Image)
    category = models.ForeignKey(Category, related_name='categories_category')
    cCount = models.IntegerField(u'Category Count')
    def __unicode__(self):
        return self.image.__str__()
    def image_thumb(self):
        return '<img src="' + settings.MEDIA_URL + '%s" width="100" height="100" />' % (self.image)
    image_thumb.allow_tags = True
    def category_language(self):
        return self.category.language
    class Meta:
        verbose_name = "Crowdsourced Imagecategory"
        verbose_name_plural = "Crowdsourced Imagecategories"
    
class Highscore(models.Model):
    name = models.TextField()
    points = models.IntegerField()
    
class Blacklist(models.Model):
    word = models.TextField()