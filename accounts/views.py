from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
# Create your views here.
from .models import * 
from .forms import *
from .filters import *
import zipfile36 as zipfile
import os
import boto
import io

import xlwt


def loginPage(request):
	if request.user.is_authenticated:
		return redirect('Download')
	else:
		if request.method == "POST":
			username = request.POST.get("username")
			password = request.POST.get("password")
			
			user = authenticate(request, username = username, password = password)

			if user is not None:
				login(request, user)
				return redirect('Download')
			else:
				messages.info(request, 'Username or Password was not correct')

		context = {}
		return render(request, 'accounts/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')


def registerPage(request):
	if request.user.is_authenticated:
		return redirect('Download')
	else:
		form = CreateUserForm()
		if request.method == "POST":
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, 'Account was successful created')
				return redirect('login')

		context = {'form': form}
		return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
def upload(request):
	submit = UploadPres()
	
	if request.method == 'POST':
		submit = UploadPres(request.POST, request.FILES)
		if submit.is_valid():
			submit.save()
			messages.info(request, 'Presentation Uploaded Successfully!')
			return redirect('Download')
	context = {'submit': submit}
	return render(request, 'accounts/upload.html', context)


@login_required(login_url='login')
def download (request):
	presentations = Presentation.objects.all()

	myFilter = Presentationfilter(request.GET, queryset=presentations)
	presentations = myFilter.qs
	request.session['presies'] = [f.id for f in presentations]

	display = presentations.count()

	context = {'presentations': presentations, 'myFilter': myFilter, 'display': display}
	return render(request, 'accounts/download.html', context)


def getfiles(request):
	ids = request.session['presies']
	presies = Presentation.objects.filter(id__in = ids)
	file_names = []
	for x in presies:
		file_names.append(x.pptx)

	zip_subdir = "presentation_folder"
	zip_filename = zip_subdir + ".zip"
	byte_stream = io.BytesIO()
	zf = zipfile.ZipFile(byte_stream, "w")  


	for filename in file_names:  
		conn = boto.connect_s3('AKIAVH6CVLPUTAWB5U4P', 'BF/zeRdEm5sEtzKymAMpJ6heO19Bv3XgSbvjkF85')
		bucket = conn.get_bucket('danielsantander-uldl')
		s3_file_path = bucket.get_key(filename)
		response_headers = {
		'response-content-type': 'application/force-download',
		'response-content-disposition':'attachment;filename="%s"'% filename
		}
		url = s3_file_path.generate_url(60, 'GET',
			response_headers=response_headers,
			force_http=True)

		# download the file
		file_response = requests.get(url)  

		if file_response.status_code == 200:

		# create a copy of the file
			string = str(filename)[10:]
			f1 = open(string , 'wb')
			f1.write(file_response.content)
			f1.close()

			# write the file to the zip folder
			fdir, fname = os.path.split(string)
			zip_path = os.path.join(zip_subdir, fname)
			zf.write(string, zip_path)    

	# close the zip folder and return
	zf.close()
	response = HttpResponse(byte_stream.getvalue(), content_type="application/x-zip-compressed")
	response['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
	return response 


def export_xls(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="PresentationData.xls"'
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('presentations')
	# Sheet header, first row
	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Title','Author','Protocol','AI','Crop','Year','Status','Country']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()

	ids = request.session['presies']
	
	presies = Presentation.objects.filter(id__in = ids)

	for x in presies:
		row_num += 1

		title = x.title
		aid = str(x.author)
		status = x.status
		cid2 = str(x.country)
		yid = str(x.year)

		protocols = x.protocol.all()
		pid = ""
		for a in range(len(protocols)):
			if a == 0:
				pid += str(protocols[a])
			else:
				pid += ", " + str(protocols[a]) 

		ais = x.ai.all()
		aid2 = ""
		for b in range(len(ais)):
			if b == 0:
				aid2 += str(ais[b])
			else :
				aid2 += ", " + str(ais[b])

		crops = x.crop.all()
		cid = []
		for c in range(len(crops)):
			if c == 0:
				cid += str(crops[c])
			else:
				cid += ", " + str(crops[c])

		edit = (title,aid,pid,aid2,cid,yid,status,cid2)
		for col_num in range(len(edit)):
			ws.write(row_num, col_num, edit[col_num], font_style)

	wb.save(response)
	return response



"""
		row_num += 1

		aindex = row[1]
		for a in authors:
			if a['id'] == aindex:
				aid = a['name']

		pindex = row[2]
		for p in protocols:
			if p['id'] == pindex:
				pid = p['name']

		a2index = row[3]
		for a2 in ais:
			if a2['id'] == a2index:
				aid2 = a2['name']

		cindex = row[4]
		for c in countries:
			if c['id'] == cindex:
				cid = c['name']

		c2index = row[7]
		for c2 in countries:
			if c2['id'] == c2index:
				cid2 = c2['name']

		yindex = row[5]
		for yr in years:
			if yr['id'] == yindex:
				yid = yr['name']
"""