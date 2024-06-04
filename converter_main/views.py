from django.http import FileResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import tempfile
import os
from django.shortcuts import render
import requests
from openpyxl import load_workbook 
from yattag import Doc, indent 


# Create your views here.
def home_page(request):
    return render(request, 'converter_main/index.html')

@csrf_exempt
def import_file(request):
    if request.method == 'POST':
        # Check if file is included in the request
        if 'import_file' not in request.FILES:
            return HttpResponseBadRequest("No file provided")
        
        import_file = request.FILES['import_file']
        
        # Load Excel File 
        try:
            workBook=load_workbook(import_file)
        except Exception as e:
            return HttpResponseBadRequest(f"Error reading file: {str(e)}")

        # Getting an object of active sheet 1 
        workSheet = workBook.worksheets[0]

        # Returning returns a triplet 
        doc, tag, text = Doc().tagtext() 
        
        xml_schema = 'xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.09" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:iso:std:iso:20022:tech:xsd:pain.001.001.09"'

        with tag('Document', xml_schema):
            with tag('CstmrCdtTrfInitn'):
                    for row in workSheet.iter_rows(min_row=2, min_col=1): 
                        row = [cell.value for cell in row]
                        with tag("GrpHdr"): 
                            with tag("CreDtTm"): 
                                text(str(row[0])) 
                            with tag("NbOfTxs"): 
                                text(row[1]) 
                            with tag("CtrlSum"): 
                                text(row[2]) 
                        with tag('PmtInf'):
                            with tag('PmtInfId'):
                                text(row[3])
                            with tag('NbOfTxs'):
                                text(str(row[4]))
                            with tag('ReqdExctnDt'):
                                with tag('Dt'):
                                    text(row[5])
                            with tag('DbtrAcct'):
                                with tag('Id'):
                                    with tag('IBAN '):
                                        text(row[6])


        # Generate XML string
        result = indent( 
            doc.getvalue(), 
            indentation='   ', 
            indent_text=True
        )    

        # Create a temporary file to save the XML
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as tmp_file:
            tmp_file.write(result.encode('utf-8'))
            tmp_file_path = tmp_file.name
        
        # Create a file response
        response = HttpResponse(open(tmp_file_path, 'rb'), content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename="pain001.xml"'
        
        # Clean up the temporary file
        os.remove(tmp_file_path)
        
        return response
    else:
        return HttpResponseBadRequest("Only POST method is allowed")
