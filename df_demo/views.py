from django.shortcuts import render

# Create your views here.
def mce(request):
    return render(request,'df_demo/mce.html')

def mce2(request):
    dict=request.POST
    mce1=dict.get('mce')
    return render(request,'df_demo/mce2.html',{'mce':mce1})