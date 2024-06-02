from django.http import FileResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import tempfile
import os
from django.shortcuts import render
import requests
import xlrd
from django.http import HttpResponseBadRequest
from pain001 import __main__

# Create your views here.
def home_page(request):
    return render(request, 'converter_main/index.html')
    
@csrf_exempt
def import_file(request):
    if request.method == 'POST':
        # Ensure the file is included in the request
        if 'import_file' not in request.FILES:
            return HttpResponseBadRequest("No file provided")
        
        import_file = request.FILES['import_file']
        
        # Check if the uploaded file is an Excel file
        if not import_file.name.endswith(('.xls', '.xlsx')):
            return HttpResponseBadRequest("Invalid file type")
        
        # Read the Excel file
        try:
            df = pd.read_excel(import_file)
        except Exception as e:
            return HttpResponseBadRequest(f"Error reading Excel file: {e}")
        
        # Create a temporary file to save the CSV
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            csv_path = tmp_file.name
            df.to_csv(csv_path, index=False)
        
        # Return the CSV file as a response
        response = FileResponse(open(csv_path, 'rb'), as_attachment=True, filename='converted_file.csv')
        
        # Clean up the temporary file after the response is complete
        response['X-Accel-Buffering'] = 'no'
        response['X-Accel-Expires'] = '0'
        response['Content-Disposition'] = f'attachment; filename="converted_file.csv"'
        response['Content-Length'] = os.path.getsize(csv_path)
        
        return response

    return HttpResponseBadRequest("Invalid request method")