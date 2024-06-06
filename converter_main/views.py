from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from openpyxl import load_workbook
from lxml import etree as et
import pandas as pd
from datetime import datetime
import tempfile

# Create your views here.
def home_page(request):
    return render(request, 'converter_main/index.html')

def parseToXml(workBook):
        root = et.Element('Document', xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.09", 
                             xmlns_xsi="http://www.w3.org/2001/XMLSchema-instance", 
                             xsi_schemaLocation="urn:iso:std:iso:20022:tech:xsd:pain.001.001.09")

        for index,row in workBook.iterrows():
            # Replace None values with empty strings
            try:
                cstmrCdtTrfInitn = et.SubElement(root, 'CstmrCdtTrfInitn')
                grpHdr = et.SubElement(cstmrCdtTrfInitn, 'GrpHdr')

                creDtTm = et.SubElement(grpHdr, 'CreDtTm')
                if isinstance(row[0], datetime):
                    creDtTm.text = row[0].strftime('%Y-%m-%d')
                else:
                    creDtTm.text = str(row[0])

                nbOfTxs = et.SubElement(grpHdr, 'NbOfTxs')
                nbOfTxs.text = str(row[1])

                ctrlSum = et.SubElement(grpHdr, 'CtrlSum')
                ctrlSum.text = str(row[2])

                initgPty = et.SubElement(grpHdr, 'InitgPty')
                nm = et.SubElement(initgPty, 'Nm')
                nm.text = str(row[3])
                
                id_tag = et.SubElement(initgPty, 'Id')
                orgId = et.SubElement(id_tag, 'OrgId')
                othr = et.SubElement(orgId, 'Othr')
                id_othr = et.SubElement(othr, 'Id')
                id_othr.text = str(row[4])
                schmeNm = et.SubElement(othr, 'SchmeNm')
                et.SubElement(schmeNm, 'Prtry')

                pmtInf = et.SubElement(cstmrCdtTrfInitn, 'PmtInf')

                pmtInfId = et.SubElement(pmtInf, 'PmtInfId')
                pmtInfId.text = str(row[5])
                nbOfTxs_pmt = et.SubElement(pmtInf, 'NbOfTxs')
                nbOfTxs_pmt.text = str(row[6])
                pmtMtd = et.SubElement(pmtInf, 'PmtMtd')
                pmtMtd.text = str(row[7])

                dbtr = et.SubElement(pmtInf, 'Dbtr')
                nm_dbtr = et.SubElement(dbtr, 'Nm')
                nm_dbtr.text = str(row[9])

                id_dbtr = et.SubElement(dbtr, 'Id')
                prvtId = et.SubElement(id_dbtr, 'PrvtId')
                othr_dbtr = et.SubElement(prvtId, 'Othr')
                id_othr_dbtr = et.SubElement(othr_dbtr, 'Id')
                id_othr_dbtr.text = str(row[10])
                schmeNm_dbtr = et.SubElement(othr_dbtr, 'SchmeNm')
                prtry_dbtr = et.SubElement(schmeNm_dbtr, 'Prtry')
                # prtry_dbtr.text = str(row[10])

                dbtrAgt = et.SubElement(pmtInf, 'DbtrAgt')
                finInstnId = et.SubElement(dbtrAgt, 'FinInstnId')
                clrSysMmbId = et.SubElement(finInstnId, 'ClrSysMmbId')
                clrSysId = et.SubElement(clrSysMmbId, 'ClrSysId')
                prtry_clr = et.SubElement(clrSysId, 'Prtry')
                prtry_clr.text = str(row[12])
                mmbId = et.SubElement(clrSysMmbId, 'MmbId')
                mmbId.text = str(row[13])

                reqdExctnDt = et.SubElement(pmtInf, 'ReqdExctnDt')
                dt = et.SubElement(reqdExctnDt, 'Dt')
                if isinstance(row[14], datetime):
                    dt.text = row[14].strftime('%Y-%m-%d')
                else:
                    dt.text = str(row[14])

                dbtrAcct = et.SubElement(pmtInf, 'DbtrAcct')
                id_dbtrAcct = et.SubElement(dbtrAcct, 'Id')
                iban_dbtrAcct = et.SubElement(id_dbtrAcct, 'IBAN')
                iban_dbtrAcct.text = str(row[15])

                cdtTrfTxInf = et.SubElement(pmtInf, 'CdtTrfTxInf')
                pmtId = et.SubElement(cdtTrfTxInf, 'PmtId')
                endToEndId = et.SubElement(pmtId, 'EndToEndId')
                # endToEndId.text = str(row[15])

                amt = et.SubElement(cdtTrfTxInf, 'Amt')
                instdAmt = et.SubElement(amt, 'InstdAmt', Ccy="UAH")
                instdAmt.text = str(row[17])

                cdtr = et.SubElement(cdtTrfTxInf, 'Cdtr')
                nm_cdtr = et.SubElement(cdtr, 'Nm')
                nm_cdtr.text = str(row[19])

                pstlAdr = et.SubElement(cdtr, 'PstlAdr')
                et.SubElement(pstlAdr, 'StrtNm').text = str(row[20])
                et.SubElement(pstlAdr, 'BldgNb').text = str(row[21])
                et.SubElement(pstlAdr, 'Room').text = str(row[22])
                et.SubElement(pstlAdr, 'PstCd').text = str(row[23])
                et.SubElement(pstlAdr, 'TwnNm').text = str(row[24])
                et.SubElement(pstlAdr, 'DstrctNm').text = str(row[25])
                et.SubElement(pstlAdr, 'CtrySubDvsn').text = str(row[26])
                et.SubElement(pstlAdr, 'Ctry').text = str(row[27])

                id_cdtr = et.SubElement(cdtr, 'Id')
                orgId_cdtr = et.SubElement(id_cdtr, 'OrgId')
                othr_cdtr = et.SubElement(orgId_cdtr, 'Othr')
                id_othr_cdtr = et.SubElement(othr_cdtr, 'Id')
                id_othr_cdtr.text = str(row[28])
                schmeNm_cdtr = et.SubElement(othr_cdtr, 'SchmeNm')
                prtry_cdtr = et.SubElement(schmeNm_cdtr, 'Prtry')
                prtry_cdtr.text = str(row[29])

                ctryOfRes = et.SubElement(cdtr, 'CtryOfRes')
                ctryOfRes.text = str(row[30])

                cdtrAcct = et.SubElement(cdtTrfTxInf, 'CdtrAcct')
                id_cdtrAcct = et.SubElement(cdtrAcct, 'Id')
                iban_cdtrAcct = et.SubElement(id_cdtrAcct, 'IBAN')
                iban_cdtrAcct.text = str(row[31])

                rmtInf = et.SubElement(cdtTrfTxInf, 'RmtInf')
                strd = et.SubElement(rmtInf, 'Strd')
                taxRmt = et.SubElement(strd, 'TaxRmt')
                rcrd = et.SubElement(taxRmt, 'Rcrd')
                tp = et.SubElement(rcrd, 'Tp')
                tp.text = str(row[32])
                ctgy = et.SubElement(rcrd, 'Ctgy')
                ctgy.text = str(row[33])
                ctgyDtls = et.SubElement(rcrd, 'CtgyDtls')
                ctgyDtls.text = str(row[34])
                certId = et.SubElement(rcrd, 'CertId')
                certId.text = str(row[35])
                taxAmt = et.SubElement(rcrd, 'TaxAmt')
                ttlAmt = et.SubElement(taxAmt, 'TtlAmt', Ccy="UAH")
                ttlAmt.text = str(row[36])
                addtlInf = et.SubElement(rcrd, 'AddtlInf')
                addtlInf.text = str(row[37])

            except Exception as e:
                return HttpResponseBadRequest(f"Error processing row: {str(e)}")

        # Generate XML string
        xml_string = et.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        return xml_string

@csrf_exempt
def import_file(request):
    if request.method == 'POST':
        # Check if file is included in the request
        if 'import_file' not in request.FILES:
            return HttpResponseBadRequest("No file provided")
        
        import_file = request.FILES['import_file']
        
        # Load Excel File 
        try:
            workBook = pd.read_excel(import_file, header=None)
        except Exception as e:
            return HttpResponseBadRequest(f"Error reading file: {str(e)}")

        xml_string = parseToXml(workBook)

        # Create a temporary file to save the XML
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as tmp_file:
                tmp_file.write(xml_string)
                tmp_file_path = tmp_file.name
        except Exception as e:
            return HttpResponseBadRequest(f"Error creating temporary file: {str(e)}")
        
        # Create a file response
        try:
            response = HttpResponse(open(tmp_file_path, 'rb'), content_type='application/xml')
            response['Content-Disposition'] = 'attachment; filename="pain001.xml"'
            return response
        except Exception as e:
            return HttpResponseBadRequest(f"Error creating response: {str(e)}")

    return HttpResponseBadRequest("Invalid request method")