from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

from Health_App.views import Message


urlpatterns = [
				
				path('',views.Home,name='Home'),
				path('Admin_Login/',views.Admin_Login,name='Admin_Login'),
				path('User_Login/',views.User_Login,name='User_Login'),
				path('User_Registeration/',views.User_Registeration,name='User_Registeration'),
				path('Change_Password/',views.Change_Password,name='Change_Password'),
				path('View_Users/',views.View_Users,name="View_Users"),
				path('Manage_Question/',views.Manage_Question,name="Manage_Question"),
				path('Add_Question/',views.Add_Question,name="Add_Question"),
				path('Update_Question/',views.Update_Question,name="Update_Question"),
				path('Delete_Question/<int:id>',views.Delete_Question,name="Delete_Question"),
				path('U_NearbyHospitals/',views.U_NearbyHospitals,name='U_NearbyHospitals'),
				path('maps/',views.maps,name='maps'),
				path('Profile/',views.Profile,name='Profile'),
				path('Message/', Message.as_view(),name='Message'),
				path('train_model/', views.train_chatbot_model, name='train_model'),
				path('Demo/', views.Demo, name='Demo'),
				path('Example/', views.Example, name='Example'),
				path('run_training_and_redirect/', views.run_training_and_redirect, name='run_training_and_redirect'),
				path('Logout/',views.Logout,name='Logout'),
					
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)