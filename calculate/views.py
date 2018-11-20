# -*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views import generic
from django.views.decorators import csrf
import os, sys
from coursearrangement import solve
from calculate.models import Applicant
from calculate.forms import ContactForm,SwapForm
from coursearrangement.display import writecontent
from django.core.mail import send_mail, BadHeaderError
import random
from calculate.match import match



def mainpage(request):
    return render(request,'home.html')

def contact(request):
    if request.method == 'GET':
        return render(request,"contact.html",{})
    else:
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        send_mail("course arrangement web","from: "+email+"\n"+"name: "+name+"\n message:"+ message,"chentaoyu802x@gmail.com",['chentaoyu802x@gmail.com'])
        return HttpResponseRedirect('/contact/success/')


def successView(request):
    return render(request,'success.html',{})


def timetable(request):
    return render(request,'timetable.html')


def search(request):
    request.encoding = 'utf-8'
    content = {}
    list = []

    if request.method == "POST":
        list = request.POST.getlist('text')
        names = request.POST.getlist('checkbox')

        j = 0
        n = len(list)
        for i in range(n):
            if list[i-j] == '':
                list.remove(list[i-j])
                j=j+1

        list1=[]
        for i in range(len(list)):
            list[i] = list[i].lower()
            if(list[i] not in list1):
                list1.append(list[i])
        list = list1
        if(len(list)==0):
            return timetable(request)


        for element in names:
            name = 'check'+element
            content[name] = "checked="

        n = len(names)
        for i in range(n):
            names[i] = int(names[i])

        print(names)


        name = 'a'
        i=0
        for element in list:
            content[name] = list[i]
            name = chr(ord(name)+1)
            i = i+1

        list.reverse()
        answer = solve.allCombination(list,names)
        if answer:
            n = len(answer)
            if n==1:
                content['outcome'] = str(n) + " result is available!"
            else:
                content['outcome'] = str(n) + " results are available!"
            if n>10:
                content['suggestion'] = "We’ve curated 10 timetables for you. More index combinations are available at the bottom."
                base = random.randint(0, n)
                dif = n//10
                i=0
                while(i<10):
                    writecontent(i+1,answer[(base+i*dif)%n],content,list)
                    i = i+1
            else:
                i = 0
                while(i<n):
                    writecontent(i+1,answer[i],content,list)
                    i = i+1
            content['result'] = str(answer)
        else:
            content["outcome"] = "Opps! No result!"
            content["suggestion"] = "We suggest you to unclick some time slots or change the courses you select."
            content['result'] = ""

    return render(request, 'timetablelist.html',content)

def temp(request):

    if request.method == 'POST':
        form = SwapForm(request.POST)
        if form.is_valid():
            form.save()

        name = request.POST['name']
        code = request.POST['code']
        current = request.POST['current']
        expected = request.POST['expected']
        email = request.POST['email']
        # id = request.POST['id']

        result = match(code,current,expected,email)

        # for keys in result:
        #     print("{}: {}".format(keys,result[keys]))

        if result["match"]:
            #send mail to both of the ppl
            # send_mail(subject, message, from_email, recipient_list)
            send_mail("Course Swapping MATCH!",message(name,code,current,expected,result["name"],result["email"]),"ntucourseplanner@gmail.com",[email,])
            send_mail("Course Swapping MATCH!",message(result["name"],code,expected,current,name,email),"ntucourseplanner@gmail.com",[result["email"],])

            #delte ppl from both of the database
            p1 = Applicant.objects.get(name=name,code=code,current=current,expected=expected,email=email)
            p1.delete()
            p2 = Applicant.objects.get(id=result["id"])
            p2.delete()

            return redirect("match")

        else:
            return redirect("nomatch")

    else:
        form = SwapForm()

    return render(request,'comming.html',{'form':form})

def message(name,code,current,expected,match_name,match_email):
    return ("Congratulations {}!\nWe have found you a match for {}, to swap {} with {}."
    "\nThe persons name is {}, and you can contact him or her @: {}."
    "\nYour request will now be deleted from our database, "
    "should this swap not work out feel free to submit another request.\nCheers! :)"
    ).format(name,code,current,expected,match_name,match_email)

# def matchsuccess(request):
#     if request.method == 'POST':
#         form = SwapForm(request.POST)
#         if form.is_valid():
#             form.save()

#         name = request.POST['name']
#         code = request.POST['code']
#         current = request.POST['current']
#         expected = request.POST['expected']
#         email = request.POST['email']
#         # id = request.POST['id']

#         result = match(code,current,expected,email)

#         # for keys in result:
#         #     print("{}: {}".format(keys,result[keys]))

#         if result["match"]:
#             #send mail to both of the ppl
#             # send_mail(subject, message, from_email, recipient_list)
#             send_mail("Course Swapping MATCH!",message(name,code,current,expected,result["name"],result["email"]),"ntucourseplanner@gmail.com",[email,])
#             send_mail("Course Swapping MATCH!",message(result["name"],code,expected,current,name,email),"ntucourseplanner@gmail.com",[result["email"],])

#             #delete ppl from both of the database
#             p1 = Applicant.objects.get(name=name,code=code,current=current,expected=expected,email=email)
#             p1.delete()
#             p2 = Applicant.objects.get(id=result["id"])
#             p2.delete()

#             return redirect("match")

#         else:
#             return redirect("nomatch")

#     else:
#         form = SwapForm()

#     return render(request,'match.html',{'form':form})

# def nomatch(request):
#     if request.method == 'POST':
#         form = SwapForm(request.POST)
#         if form.is_valid():
#             form.save()

#         name = request.POST['name']
#         code = request.POST['code']
#         current = request.POST['current']
#         expected = request.POST['expected']
#         email = request.POST['email']
#         # id = request.POST['id']

#         result = match(code,current,expected,email)

#         # for keys in result:
#         #     print("{}: {}".format(keys,result[keys]))

#         if result["match"]:
#             #send mail to both of the ppl
#             # send_mail(subject, message, from_email, recipient_list)
#             send_mail("Course Swapping MATCH!",message(name,code,current,expected,result["name"],result["email"]),"ntucourseplanner@gmail.com",[email,])
#             send_mail("Course Swapping MATCH!",message(result["name"],code,expected,current,name,email),"ntucourseplanner@gmail.com",[result["email"],])

#             #delte ppl from both of the database
#             p1 = Applicant.objects.get(name=name,code=code,current=current,expected=expected,email=email)
#             p1.delete()
#             p2 = Applicant.objects.get(id=result["id"])
#             p2.delete()

#             return redirect("match")

#         else:
#             return redirect("nomatch")

#     else:
#         form = SwapForm()

#     return render(request,'nomatch.html',{'form':form})

def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

def get_coursecode_list(max_results=0, starts_with=''):
    coursecode_list = []
    if starts_with:
        coursecode_list = CourseCode.objects.filter(name__startswith=starts_with)
    else:
        coursecode_list = CourseCode.objects.all()

    if max_results > 0:
        if (len(coursecode_list) > max_results):
            coursecode_list = coursecode_list[:max_results]

    for coursecode in coursecode_list:
        coursecode.url = encode_url(coursecode.code)

    return coursecode_list


def forum(request):

    top_coursecode_list = CourseCode.objects.order_by('-views')[:10]

    for coursecode in top_coursecode_list:
        coursecode.url = encode_url(coursecode.code)

    context_dict = {'coursecodes': top_coursecode_list}

    coursecode_list = get_coursecode_list()
    context_dict['coursecode_list'] = coursecode_list

    # Render and return the rendered response back to the user.
    return render(request,'forum.html', context_dict)


def coursecode(request,coursecode1_name_url):
    top_coursecode_list = CourseCode.objects.order_by('-views')[:10]

    for coursecode in top_coursecode_list:
        coursecode.url = encode_url(coursecode.code)

    context_dict = {'coursecodes': top_coursecode_list}

    coursecode_list = get_coursecode_list()
    context_dict['coursecode_list'] = coursecode_list

    # Render and return the rendered response back to the user.


    coursecode1_name = decode_url(coursecode1_name_url)
    context_dict = {'coursecode1_name':coursecode1_name,'coursecode1_name_url':coursecode1_name_url}

    try:
        coursecode1 = CourseCode.objects.get(code=coursecode1_name)
        context_dict['coursecode1'] = coursecode1
        indexnumbers = IndexNumber.objects.filter(course=coursecode1)
        for indexnumber in indexnumbers:
            print(indexnumber.index)
        print(indexnumbers)
        context_dict['indexnumbers'] = indexnumbers
    except CourseCode.DoesNotExist:
        pass

    return  render(request,'coursecode.html', context_dict)
