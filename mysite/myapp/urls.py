from django.conf.urls import url
from django.db.models import query
from django.views.generic.base import View
from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
 
urlpatterns = [
         url(r'^$', views.index, name ='index'),
         url(r'^about/$', views.about, name ='about'),
         url(r'^kitchen/<slug:slug>/$', views.kitchenView, name ='kitchen-items'),
         path('kitchen/<int:pk>/', views.kitchenView, name ='kitchen'),
         path('AllProductView/<slug:slug>/', views.AllProductView, name ='AllProduct'),
         path('addProduct/',views.addProductView,name ='addProduct'),
         path('search/',views.searchView,name='search'),
        #  lofin logout
        path('login/', views.Login, name ='login'),
        # path('logout/', auth.LogoutView.as_view(template_name ='myapp/login.html'), name ='logout'),
        path('logout/',views.logoutView,name="logout"),

        ############ oder #############
        path('order/<int:pk>/',views.orderView,name='order'),

        #  path('electronic/',views.electronicView,name='electronics'),
         path('cart/',views.addcartView,name='cart'),
         path('addDelCartItem/',views.deleteCartView,name="add-del"),
         path('user-profile/',views.userView,name='user-profile'),
     

        #  url(r'^cloths/$', views.clothsView, name ='fashion'),
         url(r'^$', views.index, name ='index'),
         
        # token url
        # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        # views.activate, name='activate'), 
        path('activate/<uidb64>/<token>/', views.activate, name='activate'),


         
         # paytm
         path('handelrequest/',views.handelrequest,name='handelrequest')
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)