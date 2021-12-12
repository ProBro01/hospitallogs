from django.urls import path
from allapps import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="mainpage"),
    path("register/", views.register, name="registration"),
    path("login/", views.login, name="login"),
    path("registerdocs/", views.registerdoc, name="doctorregister"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout, name="logout"),
    path("imageupload/", views.imageUpload, name="imageupload"),
    path("registrationdone/", views.regdone, name="registrationdone"),
    path("editprofile/", views.editprofile, name="editprofile"),
    path("searchresult/", views.search, name="search"),
    path("gethospitaldetails/<int:number>/", views.getdetails, name="getdetails"),
    path("adddoctor/", views.adddoctor, name="adddocs"),
    path("removedoctor/", views.removedoctor, name="removedocs"),
    path("forgotpassword/", views.forgotpassword, name="forgotpassword"),
    path("resetpassword/<str:resetid>/", views.resetpassword, name="resetpassword"),
    path("otppage/", views.otppage, name="otppage"),
    path("searchform/", views.searchform, name="searchform"),
    path("aboutus/", views.aboutus, name="aboutus"),
    path("editdoctorprofile/<int:docid>/", views.editdoctorprofile, name="editdoctor")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
