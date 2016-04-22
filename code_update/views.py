from django.shortcuts import render
from django.contrib.auth.decorators import login_required


#定义客户端状态页面
@login_required(login_url="/account/login/")
def code_up(request):
    status = Minions_status.objects.all()
    return render(request, 'code_update/codeup.html', {'status': status})

# Create your views here.
