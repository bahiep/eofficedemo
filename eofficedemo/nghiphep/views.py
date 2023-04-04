from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post
from django.views.generic import ListView, DetailView
from .models import Post, Comment
from members.models import Profile
from .forms import CommentForm, AddPostForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.models import User
# Create your views here.
def list(request):
    if request.user.profile.phongban.name == 'BGĐ':
        posts = Post.objects.all().filter(approvalbod=request.user)
        pending = Post.objects.all().filter((Q(approval=request.user) & Q(status='request')) | (Q(approvalbod=request.user) & Q(status='waiting')))
        requesting = Post.objects.get_users_posts(request.user).filter(Q(status='request') | Q(status='waiting') | Q(status='rejected'))
        approved = Post.objects.all().filter(approvalbod=request.user).filter(status='approved')
        myApproved = Post.objects.get_users_posts(request.user).filter(status='approved')
        return render(request, 'blog/blog.html', {'Posts':posts, 'Pending':pending, 'Requesting':requesting, 'Approved':approved, 'MyApproved':myApproved})
    elif request.user.profile.phongban.manager == request.user:
        posts = Post.objects.all().filter(approval=request.user)
        pending = Post.objects.all().filter(approval=request.user).filter(status='request')
        requesting = Post.objects.get_users_posts(request.user).filter(Q(status='request') | Q(status='waiting') | Q(status='rejected'))
        approved = Post.objects.all().filter(approval=request.user).filter(status='approved')
        myApproved = Post.objects.get_users_posts(request.user).filter(status='approved')
        return render(request, 'blog/blog.html', {'Posts':posts, 'Pending':pending, 'Requesting':requesting, 'Approved':approved, 'MyApproved':myApproved})
        # return render(request, 'blog/blog.html', {'Posts':posts, 'MyApproved':myApproved, 'Requesting':requesting, 'Pending':pending, 'sumPending':sumPending, 'Approved':approved})
    else:
        posts = Post.objects.get_users_posts(request.user)
        requesting = Post.objects.get_users_posts(request.user).filter(Q(status='request') | Q(status='waiting') | Q(status='rejected'))
        myApproved = Post.objects.get_users_posts(request.user).filter(status='approved')
        # sumPending = str(pending.count())
        return render(request, 'blog/blog.html', {'Posts':posts, 'Requesting':requesting, 'MyApproved':myApproved})
        # return render(request, 'blog/blog.html', {'Posts':posts, 'Pending':pending, 'sumPending':sumPending, 'Approved':approved})

# def detail(request, id):
#     post = Post.objects.get(id = id)
#     return render(request, 'blog/detail.html', {'post': post})

# class PostListView(ListView):
#     model = Post
#     # queryset = Post.objects.all().order_by('date')
#     template_name = 'blog/blog.html'
#     context_object_name = 'Posts'
#     paginate_by = 3
    

# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/detail.html'

def post(request, pk):
    approvallike = False
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    
    if post.likes.filter(pk=post.approval.pk).exists():
        approvallike = True
    # approvalbodlike = post.likes.filter(post.approvalbod)
    # if request.method == 'POST':
    #     form = CommentForm(request.POST, author = request.user, post = post)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))
    #         # return HttpResponseRedirect(request.path)
    return render(request, 'blog/detail.html', {'post': post, 'form': form, 'Approvallike': approvallike})

@ login_required
def like(request):
    form = CommentForm()
    if request.POST.get('action') == 'post':
        result = ''
        remove = False
        pk = request.POST.get('postid')
        post = get_object_or_404(Post, pk=pk)
        body = request.POST.get('contentbody')
        userid = post.author.profile.id
        profile = get_object_or_404(Profile, pk=userid)
        if request.user == post.author:
            form = CommentForm(request.POST, author = request.user, post = post, body=body, status='Đã cập nhật')
            post.status='request'
            post.save()
            form.save()
        elif post.approval == post.approvalbod:
            form = CommentForm(request.POST, author = request.user, post = post, body=body, status='Đã duyệt')
            post.likes.add(request.user)
            post.status='approved'
            post.like_count += 1
            result = post.like_count
            profile.songaynghiphep += post.numday
            if profile.sophepnam >= profile.songaynghiphep:
                profile.songaynghiphepconlai = profile.sophepnam - profile.songaynghiphep
            else:
                profile.songaynghiphepconlai = 0
                profile.songaynghikhongphep = profile.songaynghiphep - profile.sophepnam
            profile.save()
            post.save()
            form.save()
        else:
            form = CommentForm(request.POST, author = request.user, post = post, body=body, status='Đã duyệt')
            if post.numday < 3:
                if request.user == post.approval:
                    if post.likes.filter(pk=request.user.pk).exists():
                        # post.likes.remove(request.user)
                        # post.like_count -= 1
                        result = post.like_count
                        # remove = True
                        post.save()
                        form.save()
                    else:
                        post.likes.add(request.user)
                        post.status='approved'
                        post.like_count += 1
                        result = post.like_count
                        profile.songaynghiphep += post.numday
                        if profile.sophepnam >= profile.songaynghiphep:
                            profile.songaynghiphepconlai = profile.sophepnam - profile.songaynghiphep
                        else:
                            profile.songaynghiphepconlai = 0
                            profile.songaynghikhongphep = profile.songaynghiphep - profile.sophepnam
                        profile.save()
                        post.save()
                        form.save()
            else:
                if request.user == post.approval:
                    if post.likes.filter(pk=request.user.pk).exists():
                        # post.likes.remove(request.user)
                        # post.like_count -= 1
                        result = post.like_count
                        # remove = True
                        post.save()
                        form.save()
                    else:
                        post.likes.add(request.user)
                        post.status='waiting'
                        post.like_count += 1
                        result = post.like_count
                        post.save()
                        form.save()
                if request.user == post.approvalbod:
                    if post.likes.filter(pk=request.user.pk).exists():
                        # post.likes.remove(request.user)
                        # post.like_count -= 1
                        result = post.like_count
                        # remove = True
                        post.save()
                        form.save()
                    else:
                        post.likes.add(request.user)
                        post.status='approved'
                        post.like_count += 1
                        result = post.like_count
                        profile.songaynghiphep += post.numday
                        if profile.sophepnam >= profile.songaynghiphep:
                            profile.songaynghiphepconlai = profile.sophepnam - profile.songaynghiphep
                        else:
                            profile.songaynghiphepconlai = 0
                            profile.songaynghikhongphep = profile.songaynghiphep - profile.sophepnam
                        profile.save()
                        post.save()
                        form.save()

        return render(request, 'blog/detail.html', {'post': post, 'form': form})

@ login_required
def dislike(request):
    form = CommentForm()
    if request.POST.get('action') == 'post':
        result = ''
        remove = False
        pk = request.POST.get('postid')
        post = get_object_or_404(Post, pk=pk)
        body = request.POST.get('contentbody')
        if request.user == post.author:
            form = CommentForm(request.POST, author = request.user, post = post, body=body, status='Hủy')
            if post.likes.filter(pk=request.user.pk).exists():
                post.likes.remove(request.user)
                post.like_count = 0
                post.status='canceled'
                result = post.like_count
                remove = True
                post.save()
                form.save()
            else:
                # post.likes.add(request.user)
                # post.like_count += 1
                
                post.like_count = 0
                post.status='canceled'
                result = post.like_count
                post.save()
                form.save()
        else:
            form = CommentForm(request.POST, author = request.user, post = post, body=body, status='Trả về')
            if post.likes.filter(pk=request.user.pk).exists():
                post.likes.remove(request.user)
                post.like_count = 0
                post.status='rejected'
                result = post.like_count
                remove = True
                post.save()
                form.save()
            else:
                # post.likes.add(request.user)
                # post.like_count += 1
                
                post.like_count = 0
                post.status='rejected'
                result = post.like_count
                post.save()
                form.save()
        
        return render(request, 'blog/detail.html', {'post': post, 'form': form})
def AddPost(request):
    # post = get_object_or_404(Post, pk=pk)
    form = AddPostForm()
    if request.method =='POST':
        if request.user == request.user.profile.phongban.bod:
            form = AddPostForm(request.POST, author=request.user, approval=request.user.profile.phongban.gd,approvalbod=request.user.profile.phongban.gd)
            if form.is_valid():
                # post = form.save(commit=False)
                form.save()
        elif request.user == request.user.profile.phongban.manager:
            form = AddPostForm(request.POST, author=request.user, approval=request.user.profile.phongban.bod,approvalbod=request.user.profile.phongban.gd)
            if form.is_valid():
                # post = form.save(commit=False)
                form.save()
        else:
            form = AddPostForm(request.POST, author=request.user, approval=request.user.profile.phongban.manager,approvalbod=request.user.profile.phongban.bod)
            if form.is_valid():
                # post = form.save(commit=False)
                form.save()
            # comment = Comment.objects.create(post=form, author=request.user, body='')
        return HttpResponseRedirect(reverse('blog'))
    return render(request, "blog/addpost.html", {"form":form})

def EditPost(request,pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    if request.method == 'POST':
        if request.user == request.user.profile.phongban.bod:
            edit_form = AddPostForm(instance=post,data=request.POST, author=request.user, approval=request.user.profile.phongban.gd,approvalbod=request.user.profile.phongban.gd)
            if edit_form.is_valid():
                # post = form.save(commit=False)
                edit_form.save()
        elif request.user == request.user.profile.phongban.manager:
            edit_form = AddPostForm(instance=post,data=request.POST, author=request.user, approval=request.user.profile.phongban.bod,approvalbod=request.user.profile.phongban.gd)
            if edit_form.is_valid():
                # post = form.save(commit=False)
                edit_form.save()
        else:
            edit_form = AddPostForm(instance=post,data=request.POST,author=request.user,approval=request.user.profile.phongban.manager,approvalbod=request.user.profile.phongban.bod)
            if edit_form.is_valid():
                # post = form.save(commit=False)
                edit_form.save()
        
        return redirect('editpost', pk=post.pk)
    else:
        edit_form = AddPostForm(instance=post)
    return render(request,'blog/editpost.html',{'post': post,'editform': edit_form,'form': form})