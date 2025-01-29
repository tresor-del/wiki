import random 
import markdown2
import textwrap
import re
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import util



entries = util.list_entries()
entries_range = range(0,len(entries))
search_list = []

def checker(search):
     search_list.clear()
     for entry_position in entries_range:
         entry = entries[entry_position]
         if search in entry and entry not in search_list:
             search_list.append(entry)


def index(request):
    searchs = request.POST
    entries = util.list_entries()
    for search in searchs:
        search = searchs['q']
        if search in entries:
            entry = util.get_entry(search)
            entry_content = markdown2.markdown(entry, extras=["footnotes"])
            return render(request, f"encyclopedia/entry.html",{
        "entry": entry_content
        })
        elif search not in entries:
                search_list.clear()
                checker(search)
                return render(request, "encyclopedia/liste.html",{
                            'entries':search_list,
                            'title': search,
                            'result': len(search_list)
                        })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
                    

def article(request, page):
    path = request.path
    edit_page = path[16:]
    entries = util.list_entries()
    if page in entries:
        entry_content = util.get_entry(page)
        entry_content_to_html = markdown2.markdown(entry_content)
        return render(request, f"encyclopedia/entry.html", {
            "entry": entry_content_to_html,
            "page": page
        })
    elif page == "randomfile":
        randomfile = random.choice(entries)
        return HttpResponseRedirect(reverse(random_page, args=(randomfile,)))
    elif page == "Edit":
        return HttpResponseRedirect(reverse(edit, args=(edit_page,)))
    return render(request, "encyclopedia/page_not_found.html")

def newpage(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        entries = util.list_entries()
        if title not in entries:
            util.save_entry(title, content)
            entry_content = util.get_entry(title)
            entry_content_to_html = markdown2.markdown(entry_content)
            return render(request, 'encyclopedia/entry.html',{
                "entry": entry_content_to_html,
                'page': title
            })
        else:
            return render(request, 'encyclopedia/newpage.html', {
                "message": "Entry with this title is already saved"
            })
    return render(request, "encyclopedia/newpage.html" )
 


def edit(request, edit_page):
    path = request.path
    edit_page = path.removeprefix("/wiki/Edit/")
    if request.method == "POST":
        edited_content = request.POST
        title = edited_content["title"]
        content = edited_content["content"]
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse(article, args=(title,)))
    md_text = util.get_entry(edit_page)
    return render(request, 'encyclopedia/edit.html',{
        "title": edit_page,
        "content": md_text,
    })

def random_page(request, randomfile):
    randomfile = random.choice(entries)
    return HttpResponseRedirect(reverse(article, args=(randomfile,)))
