import json, os, subprocess, time, sys
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.utils import timezone
from .models import Post

def index(request):
    posts = Post.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'core/index.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        path = os.path.join(settings.BASE_DIR, 'userlist.json')
        with open(path, 'r') as f:
            users = json.load(f)
        if any(u['username'] == username for u in users):
            return render(request, 'core/login.html', {
                'error_register': '用户名已存在',
                'show_register': True
            })
        users.append({
            'username': username,
            'password_hash': make_password(password),
            'permission_level': 4
        })
        with open(path, 'w') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        return redirect('login')
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        path = os.path.join(settings.BASE_DIR, 'userlist.json')
        with open(path, 'r') as f:
            users = json.load(f)
        for u in users:
            if u['username'] == username and check_password(password, u['password_hash']):
                request.session['username'] = username
                return redirect('index')
        return render(request, 'core/login.html', {'error_login': '用户名或密码错误'})
    return render(request, 'core/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('index')

def create_post(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.permission_level >= 5:
        return redirect('index')
    if request.method == 'POST':
        is_official = request.user.username == 'mcytd'
        post = Post.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            author=request.user.username,
            approved=is_official
        )
        if not is_official:
            print(f"\n[审核申请] 新帖待审：ID={post.id} 标题={post.title} 作者={request.user.username}")
            print("请在另一终端执行: python manage.py review 来审核帖子\n")
        return redirect('index')
    return render(request, 'core/create_post.html')

def review_list(request):
    if not request.user.is_authenticated or request.user.permission_level > 3:
        return redirect('index')
    posts = Post.objects.filter(approved=False)
    return render(request, 'core/review_list.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, approved=True)
    return render(request, 'core/post_detail.html', {'post': post})

def user_panel(request):
    if not request.user.is_authenticated:
        return redirect('login')
    posts = Post.objects.filter(author=request.user.username).order_by('-created_at')
    return render(request, 'core/panel.html', {'posts': posts})

def delete_post(request, post_id):
    if not request.user.is_authenticated or request.user.permission_level != 1:
        return redirect('index')
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('user_panel')

def system_status(request):
    if not request.user.is_authenticated or request.user.permission_level > 2:
        return redirect('index')
    # 收集系统信息
    info = {
        'python_version': sys.version,
        'django_version': __import__('django').get_version(),
        'user_count': len(json.load(open(os.path.join(settings.BASE_DIR, 'userlist.json')))),
        'post_count': Post.objects.count(),
        'approved_count': Post.objects.filter(approved=True).count(),
        'pending_count': Post.objects.filter(approved=False).count(),
        'db_size': os.path.getsize(os.path.join(settings.BASE_DIR, 'db.sqlite3')) // 1024,
        'server_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    return render(request, 'core/status.html', {'info': info})

def about(request):
    return render(request, 'core/about.html')
