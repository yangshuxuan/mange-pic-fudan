from django.http import HttpResponseBadRequest,HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from pathology.models import Patient
from pathlib import PurePath
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_BREAK_TYPE, WD_UNDERLINE
from docx.shared import RGBColor,Pt
from docx.shared import Inches
from datetime import date
from io import BytesIO
from docx.oxml.ns import qn
from  django.http import HttpResponse
import re


@login_required(login_url='/login/')
def protected_serve_patient(request, path, document_root=None, show_indexes=False):
    # patientId = request.GET.get("patient__id")
    patientId = str(PurePath(path).parent)
    if re.compile(r"\d+").fullmatch(patientId) is None:
        return HttpResponseBadRequest("<h3>非本病例剖验医生,无权查看</h3>")
    p = get_object_or_404(Patient, pk=patientId)
    if p.doctors.filter(id = request.user.id).exists():
        return serve(request, path, document_root, show_indexes)
    else:
        return HttpResponseForbidden("<h3>非本病例剖验医生,无权查看</h3>")

@login_required(login_url='/login/')
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)



@login_required(login_url='/login/')
def generateDocument(request):
    patientId = request.GET.get("patient__id")
    if patientId is None:
        return HttpResponseBadRequest("<h3>非本病例剖验医生,无权查看诊断报告</h3>")
    p = get_object_or_404(Patient, pk=patientId)
    if p.doctors.filter(id = request.user.id).exists():
        document = Document()
        document.styles['Normal'].font.name = u'宋体'
        document.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
        docx_title=f"{p.operateSeqNumber}诊断报告.docx"
        


        paragraph = document.add_paragraph("")
        run = paragraph.add_run("复旦大学上海医学院病理学系")
        run.font.size = Pt(15)
        paragraph_format = paragraph.paragraph_format
        paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        paragraph = document.add_paragraph("")
        paragraph_format = paragraph.paragraph_format
        paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run("电话 54237009　　　　　　　　　　　　　　　　　地址 上海医学院路138号")
        run.font.size = Pt(12)
        run.font.underline = WD_UNDERLINE.THICK

        # run = document.add_paragraph().add_run(" ")
        # run.font.size = Pt(12)



        
        paragraph = document.add_paragraph("")
        paragraph.add_run("姓名 ").font.size = Pt(12)
        run = paragraph.add_run(f"{p.name} ")
        run.font.underline = True
        run.font.size = Pt(12)
        paragraph.add_run("      性别").font.size = Pt(12)
        run = paragraph.add_run(f" {p.sex} ")
        run.font.underline = True
        run.font.size = Pt(12)
        paragraph.add_run("       年龄").font.size = Pt(12)
        run = paragraph.add_run(f" {p.age}  ")
        run.font.underline = True
        run.font.size = Pt(12)


        paragraph = document.add_paragraph("")
        paragraph.add_run("剖验号数").font.size = Pt(12)
        run = paragraph.add_run(f"　 {p.operateSeqNumber} ")
        run.font.underline = True
        run.font.size = Pt(12)
        paragraph.add_run("                死亡时日").font.size = Pt(12)
        run = paragraph.add_run(f"　{p.deathDate.strftime('%Y/%m/%d')}     ")
        run.font.underline = True
        run.font.size = Pt(12)


        paragraph = document.add_paragraph("")
        paragraph.add_run("解剖时日").font.size = Pt(12)
        run = paragraph.add_run(f"　   {p.operateDate.strftime('%Y/%m/%d')}　    ")
        run.font.underline = True
        run.font.size = Pt(12)
        paragraph.add_run("    剖验医生").font.size = Pt(12)
        run = paragraph.add_run(f"　{' '.join([ d.username for d in list(p.doctors.all())])}　  ")
        run.font.underline = True
        run.font.size = Pt(12)


        run = document.add_paragraph().add_run(" ")
        run.font.size = Pt(10.5)

        paragraph = document.add_paragraph("")
        run = paragraph.add_run("  解  剖  诊  断  ")
        run.font.bold = True
        run.font.size = Pt(15)
        paragraph_format = paragraph.paragraph_format
        paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        
        
        run = document.add_paragraph().add_run(" ")
        run.font.size = Pt(15)

        for i in p.operateDiagose.split("\r\n"):
            paragraph = document.add_paragraph("")
            run = paragraph.add_run(i)
            run.font.size = Pt(14)
            paragraph_format = paragraph.paragraph_format
            paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT



        run = document.add_paragraph().add_run(" ")
        run.font.size = Pt(14)

        paragraph = document.add_paragraph("")
        run = paragraph.add_run('死亡原因：')
        run.font.bold = True
        run.font.size = Pt(14)
        
        run = paragraph.add_run(p.deadReason)
        run.font.size = Pt(14)

        for i in range(1):
            run = document.add_paragraph().add_run(" ")
            run.font.size = Pt(9)
        
        paragraph = document.add_paragraph("")
        run = paragraph.add_run('（此报告专供医师参考用请勿给与病家）')
        run.font.size = Pt(9)
        paragraph_format = paragraph.paragraph_format
        paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

        

        # Prepare document for download        
        # -----------------------------
        f = BytesIO()
        document.save(f)
        length = f.tell()
        f.seek(0)
        response = HttpResponse(
            f.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = 'attachment; filename=' + docx_title
        response['Content-Length'] = length
        return response
    else:
        return HttpResponseForbidden("<h3>非本病例剖验医生,无权查看</h3>")

    