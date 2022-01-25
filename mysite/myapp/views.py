from typing import Counter
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404,get_list_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic.base import TemplateView

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context, context

############ email verifaction ################
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
# from me
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView ,UpdateView,DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import SingleObjectMixin
from .models import CartUser, Oders, commentModel_1,userProfileModel ,questionModel,ProductModel,itemModel,Cart,CartUser
from .forms import commentForm_1,profileForm,addProductForm,productImageForm, UserRegisterForm, questionForm
from django.utils import timezone

################### to allow paytm to send  post request(send cross post reqeust)#######
from django.views.decorators.csrf import csrf_exempt
################ to genertate checksome #################
from PayTm import Checksum
MERCHANT_KEY = 'kbzk1DSbJiV_03p5'


#################################### electronic all product view #######################################################3
def AllProductView(request,slug=None):
    item = itemModel.objects.filter(slug=slug)[0:5]
    print(type(item))
    if item:
        return render(request,'myapp/about.html',{'item':item})
    
    item = itemModel.objects.filter(item_name__icontains= slug)
    print(type(item))
    if item:
            return render(request,'myapp/about.html',{'item':item})

    item = itemModel.objects.filter(sold_by__icontains= slug)
    if item:
        return render(request,'myapp/about.html',{'item':item})
    
    
    

############################## search view ##########################
def searchView(request):
    if request.method =='GET':
    
        query =  request.GET.get('q')
    # product = ProductModel.objects.all()
    # for itm in product:
    #     if query in itm.product_name:
    #         return redirect(itm.product_name) 
        query.lower()
        try1 =itemModel.objects.filter(slug__icontains=query)
        
        if try1:
              print(try1)
              print('in try2')
        #    pk = try1[0].id
              slug = try1[0].slug
              print(slug)
              return HttpResponseRedirect(reverse('AllProduct',args=(slug,),))
    
        try2 = itemModel.objects.filter(item_name__icontains = query)
        
        if try2:
            print(try2)
            print('in try2')
        #    pk = try2[0].id
            # slug = try2[0].slug
            # print(slug)
            return HttpResponseRedirect(reverse('AllProduct',args=(query,),))
        
        try4 = itemModel.objects.filter(sold_by__icontains=query)
        if try4:
            return HttpResponseRedirect(reverse('AllProduct',args=(query,),))
        
        try3 = itemModel.objects.filter(item_discription__icontains=query)
        if try3:
            slug = try3[0].slug
            return HttpResponseRedirect(reverse('AllProduct',args=(slug,),))




    # electrical=['electronic','electronics','watch','keyboard','speaker','mobile','laptop','tv','computer']
    # if query in electrical:
    #     return redirect('electronics')

    # fashion = ['fashion','cloth','cloths','pant','shirt','shirt-pant','kurta','pajama','kurta-pajama','kurta pajama','shirt pant'] 
    # if query in fashion:
    #     return redirect('fashion')  

    # kitchen=['kitchen','kitchen-stuff','kitchen stuff','cooker','pressure cooker','fridge'] 
    # if query in kitchen:
    #     return redirect('kitchen')
    return redirect('index')



#################### index#######################################
def index(request):

    product = ProductModel.objects.all()
    item1 =  itemModel.objects.filter(slug = product[0])[:4]
    item2 = itemModel.objects.filter(slug = product[1])[:4]
    item3=itemModel.objects.filter(slug = product[2])[0:5]
    return render(request, 'myapp/index.html', {'title':'index','item1':item1,'item2':item2,'item3':item3,'product':product})
  
####################about############################
def about(request):
    return render(request,'myapp/about.html')

#######################item form add product ###########################
def addProductView(request):
    
    if request.method == 'POST':
        item_model = itemModel()
        form = addProductForm(data=request.POST , instance=item_model)
        form1 = productImageForm(data= request.POST , instance=item_model)
        print('post')
        if form.is_valid() and form1.is_valid():
            print('enter')
            id_item = form.cleaned_data.get("item_id")
            itm_name = form.cleaned_data.get("item_name")
            discription = form.cleaned_data.get("item_discription")
            Price = form.cleaned_data.get("item_Price")
            offer = form.cleaned_data.get("item_offer")
            stoke = form.cleaned_data.get("in_stoke")
            sold = form.cleaned_data.get("sold_by")
            
            qlt = form.cleaned_data.get("quality")
            
            obj = itemModel.objects.create(
                                 item_id =id_item,
                                 item_name=itm_name,
                                 item_discription=discription,
                                 item_Price=Price,
                                 item_offer=offer,
                                 in_stoke=stoke,
                                 sold_by=sold,
                                 
                                 quality=qlt,
                                 )
            obj.save()
            # form.save()
            form2 = form1.save(commit=False)
            if 'item_image' in request.FILES:
                print('image')
                form2.item_image = request.FILES['item_image']
            form2.save()
            reverse('electronics',)
        else:
            print(form.errors,form1.errors)
    else:
        form = addProductForm()
        form1 = productImageForm()
 
   
    return render( request,'myapp/addProduct.html',{'form':form,'form1':form1})



################################ user profile #######################3
def userView(request):
    post = User.objects.get(username= request.user)
    detail = userProfileModel.objects.filter(name=request.user)
    if detail:
        return render(request,'myapp/user_profile.html',{'title':'user profile','post':post,'detail':detail})
    else:
        form = profileForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                user_name = request.user                
                form = form.save(commit=False)
                form.name=user_name
                if 'userpic' in request.FILES:
                   form.userpic = request.FILES['userpic']
                form.save()
                redirect('user-profile',)
            else:
                messages.info(f'invalid input!')
    

    # print(userProfileModel.objects.get(name=request.user))
    
    return render(request,'myapp/user_profile.html',{'title':'user profile','post':post,'form':form})


def kitchenView(request,pk=None):
    print("kitchen")
    qust = None
    if pk:
       item = get_list_or_404(itemModel,pk=pk)

       for it in item:
            related_item = itemModel.objects.filter(slug=it.slug).exclude(pk=pk)[0:5]
            item_total = it.item_Price - it.item_offer
            offer_perent = (item_total/it.item_Price)*100
       offer_perent =round(offer_perent,2)
    form1 = commentForm_1(request.POST or None)
    form = questionForm(request.POST or None)
    # cart form 
    # form3 = Cart(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            
            q = form.cleaned_data.get('question')
            qust = questionModel.objects.filter(question__icontains = q)[0:1]
            if qust:
                for ans in qust:
                    # print(ans.answer)
                    if ans.answer is  None:
                        form = form.save(commit=False)
                        form.user_name = request.user
                        form.save()
            else:
                form = form.save(commit=False)
                form.user_name = request.user
                form.save()

            
        if form1.is_valid():
            form1 = form1.save(commit=False)
            form1.author =request.user
            form1.save()
        # cart form is valid or not
        # if form3.is_valid():
        cart_post = request.POST.get("cartItm")
        # print(cart_post)
        if cart_post:
            if request.user.is_authenticated:
                it = itemModel.objects.filter(id=cart_post)
                cart = CartUser.objects.filter(cart_holder=request.user)
                # print(it)
                # # print(it.item_name)
                if cart:
                    item_in_cart=Cart.objects.filter(id=cart_post)
                    if item_in_cart:
                           for itm in it:
                                if itm.in_stoke>=1:
                                    for cat in item_in_cart:
                                        cat.cart_item_quantity+=1
                                        cat.save()
                                    itm.in_stoke-=1
                                    itm.save()
                                else:
                                    print("item out of stoke")
                    else:
                        c = Cart()
                        for itm in it:
                          for crt in cart:
                           c.id =cart_post
                           c.cart_user=crt
                           c.cart_item=itm.item_name
                           c.cart_product =str(itm.item_id)
                           c.cart_item_quantity=1
                           c.cart_item_quality=itm.quality
                           c.cart_item_price=itm.item_Price
                        # cart=Cart(cart_user=request.user,id=itm.id, cart_item=itm.item_name,cart_product =str(itm.item_id), cart_item_quantity=1,cart_item_quality=itm.quality  ,cart_item_price=itm.item_Price)
                           itm.in_stoke-=1
                           c.save()
                           itm.save()
                else:
                    c = Cart()
                    d=CartUser()
                    for itm in it:
                       
                        d.cart_holder=request.user
                        d.save()
                        c.id =cart_post
                        c.cart_user=d
                        c.cart_item=itm.item_name
                        c.cart_product =str(itm.item_id)
                        c.cart_item_quantity=1
                        c.cart_item_quality=itm.quality
                        c.cart_item_price=itm.item_Price
                        # cart=Cart(cart_user=request.user,id=itm.id, cart_item=itm.item_name,cart_product =str(itm.item_id), cart_item_quantity=1,cart_item_quality=itm.quality  ,cart_item_price=itm.item_Price)
                        itm.in_stoke-=1
                        c.save()
                      
                        itm.save()
                    # cart=cart.save(commit=False)
                    # cart.cart_product =it.item_id
                    
                    
                    
            return redirect('cart')
        reverse('kitchen',args=(pk,),)
    if qust:
            return render(request,'myapp/kitchen.html',{'item':item,'related_item':related_item,'item_total':item_total,'form':form,'form1':form1,'offer_perent':offer_perent,'qust':qust})
    
    else:
        return render(request,'myapp/kitchen.html',{'item':item,'related_item':related_item,'item_total':item_total,'form':form,'form1':form1,'offer_perent':offer_perent})


##################  add to cart ############################
def addcartView(request):
    if request.user.is_authenticated:
        user_cart = CartUser.objects.get( cart_holder=request.user)
        cart_items = Cart.objects.filter(cart_user=user_cart)
        lst={}
        sum=0
        related_item=[]
        total_item=0;
        for i in cart_items:
            item=itemModel.objects.filter(id=i.id)
           
            num=i.cart_item_quantity 
            lst[num]=item
            sum=sum+i.cart_item_quantity*i.cart_item_price
            total_item+=1
            related = itemModel.objects.filter(slug=i.cart_product)
        
            related_item.append(related)
       
        
        if user_cart:
            
            return render(request,'myapp/Cart.html',{'cart_items':cart_items,'item':lst,'sum':sum,'total_item':total_item,'related_item':related_item})
        else:
            return render(request,'myapp/Cart.html')
    else:
        return redirect('login')

############################  Delete cart item ######################################### 
def deleteCartView(request):
    if request.method=="POST":
        
        del_req = request.POST.get("del")
        add_req = request.POST.get("add")
        
        if del_req:
            item_cart = Cart.objects.filter(id=del_req)
            item_in_stoke =itemModel.objects.filter(id=del_req)
            print(item_cart )
            for ct in item_cart:
               
               if ct.cart_item_quantity >1:
                    for tm in item_in_stoke :
                      ct.cart_item_quantity-=1;
                      tm.in_stoke+=1
                      tm.save()
                      ct.save()
               else:
                    del_cart_item = Cart.objects.filter(id=del_req)
                    del_cart_item.delete()
        if add_req:
            add_cart_item=Cart.objects.get(id=add_req)
            item_stoke =itemModel.objects.get(id=add_req)
            if item_stoke.in_stoke>=1:
                        add_cart_item.cart_item_quantity+=1
                        item_stoke.in_stoke-=1
                        add_cart_item.save()
                        item_stoke.save()
    return redirect('cart')

############################### oder an item ###########################
def orderView(request,pk=None):
  if request.user.is_authenticated:
    next_order = Oders.objects.filter(oder_user=request.user)[0:1]
    item_price = itemModel.objects.filter(id=pk)
    cart_user = CartUser.objects.filter(cart_holder=request.user)
    cart_item = Cart.objects.filter(id=pk )
    customer =User.objects.filter(username=request.user)
    print(next_order)
    in_cart=0
    for it in cart_item:
        if it.cart_user==cart_user:
           in_cart=it.cart_item
    
    for i in item_price:
        price=i.item_Price
        offer = i.item_offer
        in_stoke=i.in_stoke
    price = price-offer
    in_stoke = in_stoke+in_cart
    
    if request.method=="POST":
        country = request.POST.get('country')
        city = request.POST.get('city')
       
        state = request.POST.get('state')
        landmark = request.POST.get('landmark')
        pincode   =request.POST.get('pincode')
        name  = request.POST.get('fullname')
        mobile_no = request.POST.get('mobile_no')
        amount = request.POST.get('amount')
        address = request.POST.get('address')
        # item_amount = request.POST.get('max_items')
        # amount_total = item_amount *price
        # if str(item_amount)<= str(in_stoke):
        
        order = Oders(country=country,state=state,city=city,landmark=landmark,pincode=pincode,oder_user=name,
                                   mobile_no=mobile_no,address=address,amount=price)
        order.save()
        for a in item_price:
           a.in_stoke -=1
        
        #
    #################request paytm to transfer the amount to your account after payment by user##############
        ##################### generte dictionary to send user details and transfer money into our account ########
        param_dict={

            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(order.id),
            'TXN_AMOUNT': str(price),
            'CUST_ID': customer[0].email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            # url at which paytm send you a post request
            'CALLBACK_URL':'http://127.0.0.1:8000/myapp/handelrequest/',

        }
        param_dict['CHECKSUMHASH']=Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return  render(request, 'myapp/paytm.html', {'param_dict': param_dict})
        
        return render(request,'myapp/sucess.html')
    if next_order:
        return render(request,'myapp/order.html',{'next_order':next_order,'price':price,'in_stoke':in_stoke})
    else:
        return render(request,'myapp/order.html',{'price':price,'in_stoke':in_stoke })
    

  else:
      return redirect('login')

###################### paytm send a post request #################33
@csrf_exempt
def handelrequest(request):
    return HttpResponse('done')
  
  
  
  
####################electronic############################
# class electronicView(TemplateView):
#     template_name ='sale/electronic.html'

# def electronicView(request):
#     post = commentModel_1.objects.order_by('-published_date')[:5]
#     qst = questionModel.objects.all()[0:1]

#     form2 = questionForm(request.POST or None)
    
#     if request.method == 'POST':
#         form = commentForm_1(request.POST )
#         username = request.user
#         if form.is_valid():
            
            
#             # if username not in post:
#             #     print('post')
#             # if request.user.is_authenticated():
#                 # username = request.user
#                 # print(form.cleaned_data)
#             # print(form.data)
#             # user= User.username
#             # print(user)
#             # print(commentModel_1.pk)
#                 # print(request.user)
#             form=form.save(commit=False)
#                 # print("not save yet")
#             form.author =username
#             print(form.author)
#             form.save()

#             print('save')

#             reverse('electronics',)
#                 # heree reverse('name_in_urls')
#             # return redirect('listView')
#         else:
#                 messages.info(request,f'responce Invalid!')
            
#         if form2.is_valid():
#                 # q= form2.question
#                 # q = request.GET.get('question')
#                 # print(form2)
#                 form2=form2.save(commit=False)
#                 form2.user_name =username
#                 form2.save()
#                 # q1= questionModel.objects.all()[0:1]
#                 # print(q1)
#                 # qs = questionModel.objects.all()[1:]

#                 # if q1 in qs:
#                 #     qst=q1
                    
#                 reverse('electronics',)
#         else:
#              messages.info(request,f'responce Invalid!')

        


#         # else:
#         #     messages.info(request,f'invalid form!')
         
#     else:
      
#             form = commentForm_1()
#     return render(request,'myapp/electronic.html',{'title':'Electronic-Items' ,'form':form, 'post':post,'post2':qst,'form':form,'form2':form2})
                 

################################## logout view##########################################
@login_required
def logoutView(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")
    

########### register here #####################################
def register(request):
    
    if request.method == 'POST':
      
        form= UserRegisterForm(request.POST)
        if  form.is_valid():
            # all_ready = User.objects.all()
            form.save(commit=False)
            form.is_active=False
            
            # print(form)
            em = form.cleaned_data.get('username')
            # print(em)
            # print(form)
            
            form.save()
            user = User.objects.get(username=em)
            
            # lst=[]
            # for it in all_ready:
            #     lst.append(it.email)
            #     lst.append(it.username)
            # print(user)
            # print(all_ready)
            # if user.email in lst and user.username in lst:
            #     # return HttpResponse("Username and email already exist !")
            #     pass
            # else:
            
            # if len(user)>1:
            #     pass
            # else:
            
            user.is_active=False
            # user.is_active = False
            ### get current site ######
            current_site= get_current_site(request)
            mail_subject ='Activate your account on Amazon.'
            token = account_activation_token.make_token(user)
            # token = account_activation_token.token_generator(user)
            print(token)
            print(user.pk)
            print(urlsafe_base64_encode(force_bytes(user.pk)))
            message = render_to_string('myapp/acc_active_email.html',{
                'form':form,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':token,
                })
            # username =  form.cleaned_data.get('username')
            
            to_email =  form.cleaned_data.get('email')
            to = [to_email,]
            print(to)
            send_mail(mail_subject,message,'pooja8jan1999@gmail.com',to,)
            # email = EmailMessage(
            #     mail_subject,message,to=[to_email],
            # )
            # email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
            ######################## mail system ####################################
            # htmly = get_template('sale/Email.html')
            # print("1")
            # d = { 'username': username }
            # subject, from_email, to = 'welcome', 'your_email@gmail.com', email
            # html_content = htmly.render(d)
            # print("2")
            # msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            # print("3")
            # msg.attach_alternative(html_content, "text/html")
            # print("4")
            # msg.send()
            # print("5")
            #################################################################
            # messages.success(request, f'Your account has been created ! You are now able to log in')
            # # print("6")
            # return redirect('login')
            # print("7")
    else:
        form = UserRegisterForm()
        # print("8")
    return render(request, 'myapp/register.html', {'form': form, 'title':'reqister here'})

############################# user activation function invoke when user fill vaild token #############
def activate(request,uidb64,token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
        # print(uid)
        user = User.objects.get(pk=uid)
        # print(uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    print(account_activation_token.check_token(user,token))
    print(uid)
    print(user)
    print(token)
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active =True
        user.save()
        # login(request, user)
        # return redirect('login')
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        # print(account_activation_token(user,token))
        # return redirect('index')
        return HttpResponse('Activation link is invalid!')
    # return render(request,'myapp/index.html')
  
################ login forms###################################################
def Login(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' wecome {username} !!')
            return redirect('index')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form':form, 'title':'log in'})
