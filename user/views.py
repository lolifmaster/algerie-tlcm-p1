from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import urllib
import json
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import Dot, Cmp, Information, InformationDot
from rest_framework.decorators import api_view
from rest_framework import status
from . import serializers
import datetime


@login_required(login_url='login')
def homePage(request):
    return render(request, 'chartjs.html')


@never_cache
def loginPage(request):
    form = UserForm()
    if request.method == 'POST':
        if not request.POST.get('g-recaptcha-response'):
            context = {
                'form': form,
            }
            messages.info(request, 'The captcha is required')
            return render(request, 'Login.html', context)

        username = request.POST.get('username')
        password = request.POST.get('password')
        captcha_rs = request.POST.get('g-recaptcha-response')

        url = 'https://www.google.com/recaptcha/api/siteverify'
        params = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': captcha_rs
        }
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())['success']

        if result and (user := authenticate(request, username=username, password=password)) is not None:
            login(request, user)
            messages.success(request, "Username or Password is incorrect")
            return redirect('home')
        else:
            messages.warning(request, "Username or Password is incorrect")
    context = {
        'form': form,

    }

    return render(request, 'Login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

# Dot Data


@api_view(['GET'])
@login_required
def getDotInformations(request):
    try:
        dot = Dot.objects.get(name=request.user.dot)
    except ObjectDoesNotExist:
        return Response({'Error': 'failed to fetch data'}, status=status.HTTP_401_UNAUTHORIZED)
    month = request.query_params.get('month', datetime.date.today().month)
    year = request.query_params.get('year', datetime.date.today().year)
    data = InformationDot.objects.filter(dot=dot, date__month=month, date__year=year).order_by('date')
    srl = serializers.InformationDotSerializer(data, many=True)
    return Response(srl.data)


@api_view(['GET'])
@login_required
def getDotInformation(request, pk):
    try:
        dot = Dot.objects.get(id=pk)
        month = request.query_params.get('month', datetime.date.today().month)
        year = request.query_params.get('year', datetime.date.today().year)
        data = InformationDot.objects.filter(dot=dot, date__month=month, date__year=year).order_by('date')
    except ValidationError:
        return Response({'Error': 'not a valid id'}, status=status.HTTP_404_NOT_FOUND)
    except ObjectDoesNotExist:
        return Response({'Error': 'failed to fetch data'}, status=status.HTTP_401_UNAUTHORIZED)
    srl = serializers.InformationDotSerializer(data, many=True)
    return Response(srl.data)

# Cmp data


@api_view(['GET'])
@login_required
def getCmpInformations(request):
    try:
        dot = Dot.objects.get(name=request.user.dot)
        cmp = Cmp.objects.filter(dot=dot).all()
    except ObjectDoesNotExist:
        return Response({'Error': 'failed to fetch data'}, status=status.HTTP_401_UNAUTHORIZED)
    month = request.query_params.get('month', datetime.date.today().month)
    year = request.query_params.get('year', datetime.date.today().year)
    data = Information.objects.filter(cmp__in=cmp, date__month=month, date__year=year).order_by('date')
    srl = serializers.InformationSerializer(data, many=True)
    h=list()
    p= dict()
    date=datetime.datetime(1,1,1)
    for i in srl.data:
        if date==i["date"]:
            p["total_raccordement_client"]=i["total_raccordement_client"]+p["total_raccordement_client"]
            p["auto"]=i["auto"]+p["auto"]
            p["binome"]=i["binome"]+p["binome"]
            p["dhdb"]=i["dhdb"]+p["dhdb"]
            p["ftth"]=i["ftth"]+p["ftth"]
            p["la_ls"]=i["la_ls"]+p["la_ls"]
            p["sans_specialite"]=i["sans_specialite"]+p["sans_specialite"]
            p["total"]=i["total"]+p["total"]
            p["q_o_s"]=i["q_o_s"]+p["q_o_s"]
            p["norme"]=i["norme"]+p["norme"]
            p["objectif"]=i["objectif"]+p["objectif"]
        else:
            if len(h)== 0:
                date=i["date"]
                p["date"]=i["date"]
                p["total_raccordement_client"]=i["total_raccordement_client"]
                p["auto"]=i["auto"]
                p["binome"]=i["binome"]
                p["dhdb"]=i["dhdb"]
                p["ftth"]=i["ftth"]
                p["la_ls"]=i["la_ls"]
                p["sans_specialite"]=i["sans_specialite"]
                p["total"]=i["total"]
                p["q_o_s"]=i["q_o_s"]
                p["norme"]=i["norme"]
                p["objectif"]=i["objectif"]
            else:
                h.append(p)
                date=i["date"]
                p["date"]=i["date"]
                p["total_raccordement_client"]=i["total_raccordement_client"]
                p["auto"]=i["auto"]
                p["binome"]=i["binome"]
                p["dhdb"]=i["dhdb"]
                p["ftth"]=i["ftth"]
                p["la_ls"]=i["la_ls"]
                p["sans_specialite"]=i["sans_specialite"]
                p["total"]=i["total"]
                p["q_o_s"]=i["q_o_s"]
                p["norme"]=i["norme"]
                p["objectif"]=i["objectif"]

    h.append(p)
    return Response(h)



@api_view(['GET'])
@login_required
def getCmpInformation(request, pk):
    try:
        cmp = Cmp.objects.get(id=pk)
        month = request.query_params.get('month', datetime.date.today().month)
        year = request.query_params.get('year', datetime.date.today().year)
        data = Information.objects.filter(cmp=cmp, date__month=month, date__year=year).order_by('date')
    except ValidationError:
        return Response({'Error': 'not a valid id'}, status=status.HTTP_404_NOT_FOUND)
    except ObjectDoesNotExist:
        return Response({'Error': 'failed to fetch data'}, status=status.HTTP_404_NOT_FOUND)
    srl = serializers.InformationSerializer(data, many=True)
    h=list()
    p= dict()
    date=datetime.datetime(1,1,1)
    for i in srl.data:
        if date==i["date"]:
            p["total_raccordement_client"]=i["total_raccordement_client"]+p["total_raccordement_client"]
            p["auto"]=i["auto"]+p["auto"]
            p["binome"]=i["binome"]+p["binome"]
            p["dhdb"]=i["dhdb"]+p["dhdb"]
            p["ftth"]=i["ftth"]+p["ftth"]
            p["la_ls"]=i["la_ls"]+p["la_ls"]
            p["sans_specialite"]=i["sans_specialite"]+p["sans_specialite"]
            p["total"]=i["total"]+p["total"]
            p["q_o_s"]=i["q_o_s"]+p["q_o_s"]
            p["norme"]=i["norme"]+p["norme"]
            p["objectif"]=i["objectif"]+p["objectif"]
        else:
            if len(h)== 0:
                date=i["date"]
                p["date"]=i["date"]
                p["total_raccordement_client"]=i["total_raccordement_client"]
                p["auto"]=i["auto"]
                p["binome"]=i["binome"]
                p["dhdb"]=i["dhdb"]
                p["ftth"]=i["ftth"]
                p["la_ls"]=i["la_ls"]
                p["sans_specialite"]=i["sans_specialite"]
                p["total"]=i["total"]
                p["q_o_s"]=i["q_o_s"]
                p["norme"]=i["norme"]
                p["objectif"]=i["objectif"]
            else:
                h.append(p)
                date=i["date"]
                p["date"]=i["date"]
                p["total_raccordement_client"]=i["total_raccordement_client"]
                p["auto"]=i["auto"]
                p["binome"]=i["binome"]
                p["dhdb"]=i["dhdb"]
                p["ftth"]=i["ftth"]
                p["la_ls"]=i["la_ls"]
                p["sans_specialite"]=i["sans_specialite"]
                p["total"]=i["total"]
                p["q_o_s"]=i["q_o_s"]
                p["norme"]=i["norme"]
                p["objectif"]=i["objectif"]

    h.append(p)
    return Response(h)


@api_view(['GET'])
@login_required
def getCmpsName(request):
    try:
        dot = Dot.objects.get(name=request.user.dot)
        cmp = Cmp.objects.filter(dot_id=dot).all()
    except ObjectDoesNotExist:
        return Response({'Error': 'failed to fetch data'}, status=status.HTTP_401_UNAUTHORIZED)
    srl = serializers.CmpSerializer(cmp, many=True)
    return Response(srl.data)


@api_view(['GET'])
@login_required
def getCmpName(request, pk):
    try:
        cmp = Cmp.objects.get(id=pk)
    except ValidationError:
        return Response({'Error': 'not a valid id'}, status=status.HTTP_404_NOT_FOUND)
    except ObjectDoesNotExist:
        return Response({'Error': 'failed to fetch data'}, status=status.HTTP_404_NOT_FOUND)
    srl = serializers.CmpSerializer(cmp, many=False)
    return Response(srl.data)
