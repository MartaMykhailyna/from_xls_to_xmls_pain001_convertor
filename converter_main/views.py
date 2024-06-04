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
                    for row in workSheet.iter_rows(min_row=1, min_col=1): 
                        row = [cell.value for cell in row]
                        with tag("GrpHdr"): 
                            with tag("CreDtTm"): 
                                text(str(row[0])) 
                            with tag("NbOfTxs"): 
                                text(row[1]) 
                            with tag("CtrlSum"): 
                                text(row[2]) 
                        with tag('InitgPty'):
                            doc.stag('Nm')
                            with tag('Id'):
                                with tag('OrgId'):
                                    with tag('Othr'):
                                        doc.stag('Id')
                                        with tag('SchmeNm'):
                                            doc.stag('Prtry')
                        with tag('PmtInf'):
                            doc.stag('PmtInfId')
                            doc.stag('NbOfTxs')
                            doc.stag('PmtMtd')
                            with tag('Dbtr'):
                                with tag('Nm'):
                                    text(row[9])
                                with tag('Id'):
                                    with tag('PrvtId'):
                                        with tag('Othr'):
                                            with tag('Id'):
                                                text(row[10])
                                            with tag('SchmeNm'):
                                                doc.stag('Prtry') 
                            with tag('DbtrAgt'):
                                with tag('FinInstnId'):            
                                    with tag('ClrSysMmbId'):            
                                        with tag('ClrSysId'):  
                                            with tag('Prtry'):
                                                text(str(row[11]))
                                        with tag('MmbId'):
                                            text(row[12])         
                                with tag('ReqdExctnDt'):
                                    with tag('Dt'):
                                        text(row[13])
                                with tag('DbtrAcct'):
                                    with tag('Id'):
                                        with tag('IBAN'):
                                            text(str(row[14]))
                                with tag('CdtTrfTxInf'):
                                    with tag('PmtId'):
                                        doc.stag('EndToEndId')
                                    with tag('Amt'):
                                        with tag('InstdAmt', Ccy="UAH"):
                                            text(row[15])
                                    with tag('Cdtr'):
                                        with tag('Nm'):
                                            text(str(row[16]))
                                        with tag('PstlAdr'):
                                            doc.stag('StrtNm')
                                            doc.stag('BldgNb')
                                            doc.stag('Room')
                                            doc.stag('PstCd')
                                            doc.stag('TwnNm')
                                            doc.stag('DstrctNm')
                                            doc.stag('CtrySubDvsn')
                                            with tag('Ctry'):
                                                text(row[17])
                                        with tag('Id'):
                                            with tag('OrgId'):
                                                with tag('Othr'):
                                                    with tag('Id'):
                                                        text(row[18])
                                                    with tag('SchmeNm'):
                                                        doc.stag('Prtry')
                                        with tag('CtryOfRes'):
                                            text(row[19])
                                    with tag('DbtrAcct'):
                                        with tag('Id'):
                                            with tag('IBAN'):
                                                text(str(row[20]))
                                    with tag('RmtInf'):
                                        with tag('Strd'):
                                            with tag('TaxRmt'):
                                                with tag('Rcrd'):
                                                    doc.stag('Tp')
                                                    with tag('Ctgy'):
                                                        text(str(row[21]))
                                                    doc.stag('CtgyDtls')
                                                    with tag('CertId'):
                                                        text(str(row[22]))
                                                    with tag('TaxAmt'):
                                                        doc.stag('TtlAmt', Ccy="UAH")
                                                    with tag('AddtlInf'):
                                                        text(str(row[23]))




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
