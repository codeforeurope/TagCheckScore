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
from django.shortcuts import render_to_response
from django.template import RequestContext
from image.models import Image, Category, Tag_image, Tag, Category_image, Highscore, Blacklist, Freetext_image, Licence_image
from random import randint
from django.conf import settings

licence = Licence_image.objects.all()

def index(request):
    #indicates if the user tagges something on the picture
    userTag = False
    #generates which page should be shown (choose or decide)
    randomPage =  randint(0,1)
    #get first 10 people from highscore list
    highscores = Highscore.objects.all().order_by('-points')[0:10]
    #placeholder for page that should be delivered
    page = ""
    #placeholder for the image search
    images = ""
    
    #imageTags = ""
    
    #placeholder for the seach results
    noImage = False
    #placeholder for the user search
    search = ""
    
    #If there are no points for this session yet
    if (request.session.get('points') == None) or (request.session.get('points') == {}):
        pointCount = 0
    else:
        pointCount = request.session.get('points')
    
    #If the Add Score button was pressed
    if (request.method == 'POST') and ('AddScore' == request.GET.get('button')):
        highscoreName = request.POST.get('name')
        if highscoreName != '':
            highscore = Highscore(name=highscoreName, points = pointCount)
            highscore.save()
            pointCount = 0
            
    #if the search button was pressed
    elif (request.method == 'POST') and ('Search' == request.GET.get('button')):
        search = request.POST.get('search').lower()
        images = Tag_image.objects.filter(tag__tag=search)
        if images.exists() == False:
            noImage = True
    
    #If the Yes or No button on the "Yes or No" page was pressed
    elif (request.method == 'POST') and (('Yes' == request.GET.get('button')) or ('No' == request.GET.get('button'))):
        if 'Yes' == request.GET.get('button'):
            newCount = Tag_image.objects.filter(image=request.session['image']).filter(tag=request.session['question']).values_list('tCount')[0][0] + 1
            #Modify DB entry for counter
            newEntry = Tag_image.objects.filter(image=request.session['image']).filter(tag=request.session['question'])[0]
            newEntry.tCount = newCount
            newEntry.save()
        if 'No' == request.GET.get('button'):
            newCount = Tag_image.objects.filter(image=request.session['image']).filter(tag=request.session['question']).values_list('tCount')[0][0] - 1
            #Modify DB entry for counter
            newEntry = Tag_image.objects.filter(image=request.session['image']).filter(tag=request.session['question'])[0]
            newEntry.tCount = newCount
            newEntry.save()

        request.session['image'] = Image.objects.order_by('?')[0]
        if Tag_image.objects.filter(tag__language=request.LANGUAGE_CODE).filter(image=request.session['image']).values_list('tag').exists():
            request.session['question'] = Tag_image.objects.filter(tag__language=request.LANGUAGE_CODE).filter(image=request.session['image']).values_list('tag').order_by('?')[0][0]
        else:
            while Tag_image.objects.filter(image=request.session['image']).exists() == False:
                request.session['image'] = Image.objects.order_by('?')[0]
        pointCount = pointCount + 5
    
    #If the skip button the the choose page was pressed
    elif (request.method == 'POST') and ('TagNo' == request.GET.get('button')):
        request.session['image'] = Image.objects.order_by('?')[0]
        if Tag_image.objects.filter(tag__language=request.LANGUAGE_CODE).filter(image=request.session['image']).values_list('tag').exists():
            request.session['question'] = Tag_image.objects.filter(tag__language=request.LANGUAGE_CODE).filter(image=request.session['image']).values_list('tag').order_by('?')[0][0]
        else:
            while Tag_image.objects.filter(image=request.session['image']).exists() == False:
                request.session['image'] = Image.objects.order_by('?')[0]
    
    #If the submit button on the choose page was pressed
    elif request.method == 'POST' and ('TagYes' == request.GET.get('button')):
        tagList = request.POST.getlist('tags')
        chosenCategory = request.POST.get('category')
        typedFreetext = request.POST.get('freetext')
        
        #If the user put in some freetext
        if typedFreetext != '':
            userTag = True
            freetextImage = Freetext_image(image=request.session['image'], text=typedFreetext, language=request.LANGUAGE_CODE)
            freetextImage.save()
        
        #if the user has choosen a category
        if chosenCategory != '':
            userTag = True
            #If the Category for this Image exists already
            if Category_image.objects.filter(image=request.session['image']).filter(category=Category.objects.filter(language=request.LANGUAGE_CODE).filter(category=chosenCategory)[0].id).exists():
                #take the current count and increment by 1
                countC = Category_image.objects.filter(image=request.session['image']).filter(category=Category.objects.filter(language=request.LANGUAGE_CODE).filter(category=chosenCategory)[0].id).values_list('cCount')[0][0] + 1
                #the current category that should be incremented
                modC = Category_image.objects.filter(image=request.session['image']).filter(category=Category.objects.filter(language=request.LANGUAGE_CODE).filter(category=chosenCategory)[0].id)[0]
                #save the new count
                modC.cCount = countC
                modC.save()
            #if the Category does not exist yet
            else:
                #save the new category with the counter starting by 1
                categoryImage = Category_image(image=request.session['image'], category=Category.objects.get(category=chosenCategory, language=request.LANGUAGE_CODE), cCount=1)
                categoryImage.save()
                
                
        #iterate over all tags from the textbox
        for singleTag in tagList:
            userTag = True       
            singleTag = singleTag.lower()
            singleTag.encode('utf-8')
            #if the tag exists
            blacklist = False
            for word in Blacklist.objects.all():
                if word.word in singleTag:
                    blacklist = True
                    
            #if the word is not on the blacklist        
            if blacklist == False:
                #if Tag.objects.filter(tag=singleTag).filter(language=request.LANGUAGE_CODE).exists():
                if Tag.objects.filter(language=request.LANGUAGE_CODE).filter(tag=singleTag).exists():
                    #If the Tag exists for this image
                    if Tag_image.objects.filter(image=request.session['image']).filter(tag=Tag.objects.filter(language=request.LANGUAGE_CODE).filter(tag=singleTag)[0].id).exists():
                            
                        newCount = Tag_image.objects.filter(image=request.session['image']).filter(tag=Tag.objects.filter(language=request.LANGUAGE_CODE).filter(tag=singleTag)[0].id).values_list('tCount')[0][0] + 1
                            
                            #hier db entry modifizieren
                        newEntry = Tag_image.objects.filter(image=request.session['image']).filter(tag=Tag.objects.filter(language=request.LANGUAGE_CODE).filter(tag=singleTag)[0].id)[0]
                        newEntry.tCount = newCount
                        newEntry.save()
                    else:
                        print(Tag.objects.filter(language=request.LANGUAGE_CODE).filter(tag=singleTag)[0].id)
                        tagImage = Tag_image(image=request.session['image'], tag=Tag.objects.get(tag=Tag.objects.filter(language=request.LANGUAGE_CODE).filter(tag=singleTag)[0].tag, language=request.LANGUAGE_CODE), tCount=1)
                        tagImage.save()
                #if the tag does not exist yet            
                else:
                    tag = Tag(tag = singleTag, language=request.LANGUAGE_CODE)
                    tag.save()
                    tagImage = Tag_image(image=request.session['image'], tag=Tag.objects.get(tag=singleTag, language=request.LANGUAGE_CODE), tCount=1)
                    tagImage.save()

        request.session['image'] = Image.objects.order_by('?')[0]
        if Tag_image.objects.filter(tag__language=request.LANGUAGE_CODE).filter(image=request.session['image']).values_list('tag').exists():
            request.session['question'] = Tag_image.objects.filter(tag__language=request.LANGUAGE_CODE).filter(image=request.session['image']).values_list('tag').order_by('?')[0][0]
        else:
            while Tag_image.objects.filter(image=request.session['image']).exists() == False:
                request.session['image'] = Image.objects.order_by('?')[0]
        if userTag == True:
            pointCount = pointCount + 5

    else:
        request.session['image'] = Image.objects.order_by('?')[0]
        if Tag_image.objects.filter(tag__language=request.LANGUAGE_CODE).filter(image=request.session['image']).values_list('tag').exists():
            request.session['question'] = Tag_image.objects.filter(tag__language=request.LANGUAGE_CODE).filter(image=request.session['image']).values_list('tag').order_by('?')[0][0]
        else:
            request.session['image'] = Image.objects.order_by('?')[0]
    
    if (request.method == 'POST') and ('Search' == request.GET.get('button')):
        page = 'image/search_a.html'
    else:
        if (request.method == 'POST'):
            if Tag_image.objects.filter(tag__language=request.LANGUAGE_CODE).filter(image=request.session['image']).values_list('tag').exists() == False:
                page = 'image/choose_a.html'
            #if a tag exists
            else:
                if randomPage == 0:
                    request.session['image'] = Image.objects.order_by('?')[0]
                    page = 'image/choose_a.html'
                elif randomPage == 1:
                    #if tags are exsisting for this image
                    if Tag_image.objects.filter(tag__language=request.LANGUAGE_CODE).filter(image=request.session['image']).values_list('tag').exists():
                        #order the tags randomly and give the first element without braces
                        request.session['question'] = Tag_image.objects.filter(tag__language=request.LANGUAGE_CODE).filter(image=request.session['image']).values_list('tag').order_by('?')[0][0]
                    else:
                        #if no tags exist for this image
                        while Tag_image.objects.filter(image=request.session['image']).exists() == False:
                            #generate a new random image
                            request.session['image'] = Image.objects.order_by('?')[0]
                    page = 'image/decide_a.html'
        else:
            #if no tag exsists yet
            if Tag_image.objects.filter(tag__language=request.LANGUAGE_CODE).filter(image=request.session['image']).values_list('tag').exists() == False:
                page = 'image/choose.html'
            #if a tag exists
            else:
                if randomPage == 0:
                    request.session['image'] = Image.objects.order_by('?')[0]
                    page = 'image/choose.html'
                elif randomPage == 1:
                    #if tags are exsisting for this image
                    if Tag_image.objects.filter(tag__language=request.LANGUAGE_CODE).filter(image=request.session['image']).values_list('tag').exists():
                        #order the tags randomly and give the first element without braces
                        request.session['question'] = Tag_image.objects.filter(tag__language=request.LANGUAGE_CODE).filter(image=request.session['image']).values_list('tag').order_by('?')[0][0]
                    else:
                        #if no tags exist for this image
                        while Tag_image.objects.filter(image=request.session['image']).exists() == False:
                            #generate a new random image
                            request.session['image'] = Image.objects.order_by('?')[0]
                    page = 'image/decide.html'
    request.session['points'] = pointCount
    if Tag.objects.filter(id=request.session.get('question')).exists():
        question = Tag.objects.get(id=request.session.get('question'))
    else:
        question = ''
    return render_to_response(page,context_instance=RequestContext(request, {'highscores': highscores, 'image': request.session['image'], 'categories': Category.objects.all(), 'question': question, 'points': pointCount, 'images': images, 'tags': Tag.objects.all(), 'noimage': noImage, 'licence': licence, 'search': search, 'WEB_PREFIX': settings.WEB_PREFIX}))

def kontakt(request):
    return render_to_response('image/kontakt.html',context_instance=RequestContext(request, {'WEB_PREFIX': settings.WEB_PREFIX}))

def info(request):
    return render_to_response('image/info.html',context_instance=RequestContext(request, {'WEB_PREFIX': settings.WEB_PREFIX}))

def impressum(request):
    return render_to_response('image/impressum.html',context_instance=RequestContext(request, {'WEB_PREFIX': settings.WEB_PREFIX}))

def privacy(request):
    return render_to_response('image/privacy.html',context_instance=RequestContext(request, {'WEB_PREFIX': settings.WEB_PREFIX}))