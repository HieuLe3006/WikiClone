from hashlib import new
from django.shortcuts import render
from . import util
from markdown2 import Markdown
from os import listdir
from os.path import isfile, join
import random
import os
from django.contrib import messages


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def search_entry(request):
    if request.method == "POST":
        title = request.POST['q']
        
        if util.get_entry(title) == None:
            thelist = util.list_entries()
            result = []
            
            for entry in thelist:
                if title.lower() in entry.lower() or entry.lower() in title.lower():
                    result.append(entry)
            
            return render(request, "encyclopedia/search_result.html", {
                "entries": result
            })
        else:
            theMarkdown = Markdown()
            content = util.get_entry(title)
            content = theMarkdown.convert(content)
            
            return render(request, "encyclopedia/entry_page.html", {
                "title": title,
                "content": content
            })

def entry_page(request, title):
    content = util.get_entry(title)
    
    if content == None:
        return render(request, "encyclopedia/entry_error.html")
    else:
        theMarkdown = Markdown()
        content = theMarkdown.convert(content)
        
        return render(request, "encyclopedia/entry_page.html", {
            "title": title, 
            "content": content    
        })
        

def random_page(request):
    # path = os.getcwd()
    # thepath = os.path.dirname(os.path.dirname(path))
    thepath = os.getcwd()
    thepath = thepath + "/entries"
    onlyfiles = [f for f in listdir(thepath) if isfile(join(thepath, f))]
    num = random.randrange(len(onlyfiles))
    
    # Remove the '.MD' at the end
    title = onlyfiles[num][:-3]
    content = util.get_entry(title)
    theMarkdown = Markdown()
    content = theMarkdown.convert(content)
    
    return render(request, "encyclopedia/entry_page.html", {
        "title": title,
        "content": content
    })
    
def edit_page(request, title):
    content = util.get_entry(title)
    theMarkdown = Markdown()
    # content = theMarkdown.convert(content)
    
    return render(request, "encyclopedia/edit_page.html", {
        "title": title, 
        "content": content    
    })

def save_new_entry(request):
    if request.method == "POST":
        new_title = request.POST["new_title"]
        new_content = request.POST["new_content"]
        
        if new_title is not None: 
            check = util.get_entry(new_title)
            if check is None:
                util.save_entry(new_title, new_content)    
                return render(request, "encyclopedia/entry_page.html", {
                    "title": new_title,
                    "content": new_content
                })
            else: 
                return render(request, "encyclopedia/entry_exists.html")
        else:
            return render(request, "encyclopedia/empty_title_error.html")

def save_edit_entry(request, title):
        
    if request.method == "POST":
        new_title = request.POST["new_title"]
        new_content = request.POST["new_content"]
        
        if new_title is not None: 
            check = util.get_entry(new_title)
            if title == new_title: 
                util.save_entry(title, new_content)
                return entry_page(request, title)
            else:
                if check is None:
                    thepath = os.getcwd()
                    thepath = thepath + "/entries/"
                    path = thepath + str(title) + ".md"
                    os.remove(path)
                    util.save_entry(new_title, new_content)    
                    return entry_page(request, new_title)
                else:
                    return render(request, "encyclopedia/entry_exists.html")
        else:
            return render(request, "encyclopedia/empty_title_error.html")

def new_page(request):
    return render(request, "encyclopedia/create_new.html")


    