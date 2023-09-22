from django.urls import path
from . import views # (. means root)

urlpatterns = [
    path('',views.index,name= 'list'),
    path('update_task/<str:pk>', views.updateTask,name = "update_task"),
    path('delete_task/<str:pk>', views.deleteTask,name='delete_task'),
    path('clear_all',views.clear_all_tasks,name = 'clear_all'),
]
