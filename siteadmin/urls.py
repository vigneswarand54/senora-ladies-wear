from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.admin_register, name='adminregister' ),
    path('login/',views.admin_login, name= 'adminlogin'),
    path('logout/',views.admin_logout, name= 'adminlogout'),
    
    path('',views.dashboard, name= 'dashboard'),
    path('user-management/',views.usermanagement, name= 'usermanagement'),
    path('product-management/',views.productmanagement, name= 'productmanagement'),
    path('filter-management/',views.filtermanagement, name= 'filtermanagement'),
    path('add_filters/add_category',views.addcategory, name= 'addcategory'),
    path('add_filters/add_subcategory',views.addsubcategory, name= 'addsubcategory'),
    path('add_filters/',views.addfilters,name= 'addfilters'),
    path('add_product/',views.addproduct,name= 'addproduct'),
    path('variation-management/',views.variationmanagement, name= 'variationmanagement'),
    path('add_variation/',views.addvariation,name= 'addvariation'),
    path('order-management/',views.ordermanagement, name='ordermanagement'),
    
    path('user-management/block_user/<int:id>/',views.blockuser, name ='blockuser'),
    path('user-management/unblock_user/<int:id>/',views.unblockuser, name ='unblockuser'),
    path('filter-management/delete-category/<int:id>/',views.deletecategory, name ='deletecategory'),
    path('filter-management/delete-subcategory/<int:id>/',views.deletesubcategory, name ='deletesubcategory'),
    path('product-management/edit-product/<int:id>/',views.editproduct, name ='editproduct'),
    path('product-management/delete-product/<int:id>/',views.deleteproduct, name ='deleteproduct'),
    path('variation-management/delete-variation/<int:id>/',views.deletevariation, name ='deletevariation'),
    path('order-management/order-status/<int:id>/',views.orderstatus, name='orderstatus'),
    
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
]
