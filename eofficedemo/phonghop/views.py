from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from .models import LichHop, PhanQuyen
from . forms import FormLichHop, FormGhiChuLichHop
from django.contrib import messages
from django.core import serializers

# Create your views here.

def get_posts(request):
    posts = LichHop.objects.all().values()
    return JsonResponse({'posts': list(posts)})

def get_post(request, post_id):
    post = LichHop.objects.get(pk=post_id)
    data = {
        'id': post.pk,
        'title': post.title,
        'time_from': post.time_from,
        'time_end': post.time_end,
    }
    return JsonResponse(data)

def phonghop(request):
    posts = LichHop.objects.all().filter(author=request.user).filter(Q(status='request') | Q(status='rejected'))
    requesting = LichHop.objects.all().filter(author=request.user).filter(Q(status='request') | Q(status='rejected'))
    
    approved = LichHop.objects.all().filter(author=request.user).filter(status='approved')
    opal = LichHop.objects.all().filter(room='OPAL')
    ruby = LichHop.objects.all().filter(room='RUBY')
    amber = LichHop.objects.all().filter(room='AMBER')
    saphire = LichHop.objects.all().filter(room='SAPHIRE')
    diamond = LichHop.objects.all().filter(room='DIAMOND')
    form = FormLichHop()
    phanquyen = PhanQuyen.objects.first().qlphonghop
    if request.user == phanquyen:
        pending = LichHop.objects.all().filter(approval=request.user).filter(status='request')
        myapproved = LichHop.objects.all().filter(status='approved')
    else:
        pending = 0
        myapproved = 0
    if request.method =='POST':
        form = FormLichHop(request.POST, author=request.user, approval=phanquyen)
        if form.is_valid():
            # post = form.save(commit=False)
            form.save()
            messages.success(request,("Đăng ký thành công"))
        return HttpResponseRedirect(reverse('phonghop'))
    return render(request, 'phonghop.html', {'Requesting':requesting,'Approved':approved,'Pending':pending,'MyApproved':myapproved,'Posts':posts,"form":form,'Opal':opal,'Ruby':ruby,'Amber':amber,'Saphire':saphire,'Diamond':diamond,})

def chitietphonghop(request, pk):
    approvallike = False
    post = get_object_or_404(LichHop, pk=pk)
    form = FormGhiChuLichHop()
    
    # if post.likes.filter(pk=post.approval.pk).exists():
    #     approvallike = True
    # approvalbodlike = post.likes.filter(post.approvalbod)
    # if request.method == 'POST':
    #     form = CommentForm(request.POST, author = request.user, post = post)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))
    #         # return HttpResponseRedirect(request.path)
    return render(request, 'chitietphonghop.html', {'post': post,'form': form})

def DangKyPhongHop(request):
    phanquyen = PhanQuyen.objects[1]
    form = FormLichHop()
    if request.method =='POST':
        form = FormLichHop(request.POST, author=request.user, approval=phanquyen.qlphonghop)
        if form.is_valid():
            # post = form.save(commit=False)
            form.save()
        return HttpResponseRedirect(reverse('phonghop'))
    return render(request, "phonghop.html", {"form":form})

@ login_required
def like(request):
    form = FormGhiChuLichHop()
    if request.POST.get('action') == 'post':
        pk = request.POST.get('postid')
        post = get_object_or_404(LichHop, pk=pk)
        body = request.POST.get('contentbody')
        
        if request.user == post.author:
            if post.author == post.approval:
                form = FormGhiChuLichHop(request.POST, author = request.user, post = post, body=body, status='Đã duyệt')
                post.status='approved'
                post.save()
                form.save()
            else:
                form = FormGhiChuLichHop(request.POST, author = request.user, post = post, body=body, status='Gửi yêu cầu')
                post.status='request'
                post.save()
                form.save()
        else:
            if request.user == post.approval:
                form = FormGhiChuLichHop(request.POST, author = request.user, post = post, body=body, status='Đã duyệt')
                post.status='approved'
                post.save()
                form.save()
        return render(request, 'chitietphonghop.html', {'post': post, 'form': form})

@ login_required
def dislike(request):
    form = FormGhiChuLichHop()
    if request.POST.get('action') == 'post':
        pk = request.POST.get('postid')
        post = get_object_or_404(LichHop, pk=pk)
        body = request.POST.get('contentbody')
        if request.user == post.author:
            form = FormGhiChuLichHop(request.POST, author = request.user, post = post, body=body, status='Hủy')
            post.status='canceled'
            post.save()
            form.save()
        else:
            form = FormGhiChuLichHop(request.POST, author = request.user, post = post, body=body, status='Trả về')
            post.status='rejected'
            post.save()
            form.save()   
        return render(request, 'chitietphonghop.html', {'post': post, 'form': form})

def EditPost(request,pk):
    post = get_object_or_404(LichHop, pk=pk)
    phanquyen = PhanQuyen.objects.first().qlphonghop
    form = FormGhiChuLichHop()
    if request.method == 'POST':
        if request.user == post.author:
            edit_form = FormLichHop(instance=post,data=request.POST, author=request.user, approval=phanquyen)
            if edit_form.is_valid():
                # post = form.save(commit=False)
                edit_form.save()
        if request.user == phanquyen:
            edit_form = FormLichHop(instance=post,data=request.POST, author=post.author, approval=phanquyen)
            if edit_form.is_valid():
                # post = form.save(commit=False)
                edit_form.save()
        return redirect('dangkyphonghop', pk=post.pk)
    else:
        edit_form = FormLichHop(instance=post)
    return render(request,'dangkyphonghop.html',{'post': post,'editform': edit_form,'form': form})