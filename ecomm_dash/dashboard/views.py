from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import FileUploaderSerializer
from .excelReader import handleExcelUpload
from django.conf import settings
# Create your views here.

class ExcelUploadAPI(APIView):

    def post(self,request):
        data = request.data
        serializer = FileUploaderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            file_path = serializer.data['file']
            handleExcelUpload(f"{settings.BASE_DIR}/{file_path}")
            return Response({
                'status' : False,
                "data":serializer.data,
                'message':"file Uploaded"

            })
        return Response({
                'status' : False,
                "data":serializer.errors,
                'message':"File Uploaded Failed"

            })

