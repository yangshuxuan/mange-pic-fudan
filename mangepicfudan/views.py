from django.http import HttpResponseBadRequest,HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from pathology.models import Patient
from pathlib import PurePath
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