from django.urls import path
from buyerseller import views

app_name = 'buyerseller'

urlpatterns = [
	path('uploadcontract/', views.upload, name='upload'),
	path('deploycontract/<int:pk>', views.deploy, name='deploy'),
	path('confirmagreement/<int:pk>', views.confirmAgreement, name='confirm-agreement'),
	path('pay/<int:pk>', views.pay, name='pay'),
	path('terminate/<int:pk>', views.terminateContract, name='terminate'),
	path('shift_next/<int:pk>', views.shift_next, name='shift_next'),
	path('shift_prev/<int:pk>', views.shift_prev, name='shift_previous'),
	path('deploy_next/<int:pk>', views.deploy_next, name='deploy_next'),
	path('deploylink/<int:doc_id>/<int:c_id>', views.deploy_with_confirmation, name='deploy_with_confirmation'),
]