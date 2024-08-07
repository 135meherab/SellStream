from django.shortcuts import render
from rest_framework import viewsets
from .models import DesignationModel, EmployeeModel, AttendanceModel, LeaveModel, SpecialOccasionModel,Shop
from .serializers import DesignationSerializers, EmployeeSerializers, AttendanceSerializers, LeaveSerializers, SpecialOccasionSerializers
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend 
from shop.models import Branch  
# Create your views here.

# Designation
class DesignationViews(viewsets.ModelViewSet):
    queryset = DesignationModel.objects.all()
    serializer_class = DesignationSerializers

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        try:
            # Get the current user's shop
            shop_user = Shop.objects.get(user = self.request.user)
            # Filter the designations by the user's shop
            return DesignationModel.objects.filter(owner = shop_user)
        except Shop.DoesNotExist:
            return DesignationModel.objects.none()



# Employee
class EmployeeViews(viewsets.ModelViewSet):
    queryset = EmployeeModel.objects.all()
    serializer_class = EmployeeSerializers

    # Only allow access if the user is authenticated
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the current user making the request
        user = self.request.user

        try:
            # Try to find a branch linked to this user
            branch = Branch.objects.get(user=user)
            # If found, return employees from this branch
            return EmployeeModel.objects.filter(branch = branch)
        except Branch.DoesNotExist:
            # If no branch is found, try to find a shop linked to this user
            try:
                shop = Shop.objects.get(user=user)
                # If found, get all branches of this shop
                branches = Branch.objects.filter(shop=shop)
                # Return employees from all these branches
                return EmployeeModel.objects.filter(branch__in = branches)
            except Shop.DoesNotExist:
                # If no branch or shop is found, return an empty list
                return EmployeeModel.objects.none()



# Attendance
class Attendanceview(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = AttendanceModel.objects.all()
    serializer_class = AttendanceSerializers

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['employee__branch__name', 'date']

    def get_queryset(self):
        user = self.request.user   # Get the current user

        try:
            # Try to find branches for this user
            branch = Branch.objects.get(user = user)  
             # Get attendance records for these branches
            return AttendanceModel.objects.filter(employee__branch = branch)
        
        except Branch.DoesNotExist:
            try:
                # If no branches, try to find a shop for this user
                shop = Shop.objects.get(user=user)
                 # Find all branches for this shop
                branches = Branch.objects.filter(shop = shop)
                # Get attendance records for these branches
                return AttendanceModel.objects.filter(employee__branch__in=branches)
            except Shop.DoesNotExist:
                # If no branches or shop, return no records
                return AttendanceModel.objects.none()
        


    def get(self, request, *args, **kwargs):
         # Handle GET requests, list leave records
        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        # Handle POST requests, create a leave record
        return self.create(request, *args, **kwargs)

class AttendanceviewRetrive(GenericAPIView, RetrieveModelMixin):
    queryset = AttendanceModel.objects.all()
    serializer_class = AttendanceSerializers

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# Employee leave view
class Leaveview(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = LeaveModel.objects.all()
    serializer_class = LeaveSerializers

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user   # Get the current user

        try:
            # Try to find branches for this user
            branch = Branch.objects.get(user = user)  
             # Get leave records for these branches
            return LeaveModel.objects.filter(employee__branch = branch)
        
        except Branch.DoesNotExist:
            try:
                # If no branches, try to find a shop for this user
                shop = Shop.objects.get(user=user)
        
                # Get leave records for employees in all branches of this shop
                branches = Branch.objects.filter(shop = shop)
                return LeaveModel.objects.filter(employee__branch__in = branches)
            except Shop.DoesNotExist:
                # If no branches or shop, return no records
                return LeaveModel.objects.none()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# Special occassion
#####################
# for email send
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

def send_transaction_email(designation, fullname, email, description_occation, start_occation, end_occation):
    message = render_to_string('email.html', {
        'designation' : designation,
        'fullname' : fullname,
        'description_occation': description_occation, 
        'start_occation': start_occation, 
        'end_occation': end_occation,
    })
    send_email = EmailMultiAlternatives("Special Occasion Start", '', to=[email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

#####################

class SpecialOccasionView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        data = SpecialOccasionModel.objects.all()
        pythondata = SpecialOccasionSerializers(data, many=True)
        return Response(pythondata.data)



    def post(self, request, format=None):
        serializerdata = SpecialOccasionSerializers(data=request.data)
        if serializerdata.is_valid():
            branch = serializerdata.validated_data.get('branch')
            description_occation = serializerdata.validated_data.get('description')
            start_occasion = serializerdata.validated_data.get('start_occasion')
            end_occasion = serializerdata.validated_data.get('end_occasion')

            if branch.id is not None:
                employeedata = EmployeeModel.objects.filter(branch=branch.id)
                for i in employeedata:
                    send_transaction_email(i.designation, i.fullname, i.email, description_occation, start_occasion, end_occasion)
                    print(i.email)

            serializerdata.save()
            return Response({'msg' : 'Successfully create data'})
        return Response(serializerdata.errors)