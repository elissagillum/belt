from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def index(request):
	return render(request, "main/index.html")

def register(request):
	errors_or_user = User.objects.validate_registration(request.POST)

	if errors_or_user[0]:
		for fail in errors_or_user[0]:
			messages.error(request, fail)
		return redirect('/')
	messages.success(request, "Successfully registered.  Please login")
	request.session['id'] = errors_or_user[1].id
	return redirect('/')

def login(request):
	errors_or_user = User.objects.validate_login(request.POST)

	if errors_or_user[0]:
		for fail in errors_or_user[0]:
			messages.error(request, fail)
		return redirect('/')
	request.session['id'] = errors_or_user[1].id
	return redirect('/success')

def success(request):
	try:
		context = {
			"user": User.objects.get(id=request.session['id']),
			"appointments": Appointment.objects.filter(task_date=datetime.date.today()).order_by("task_time"), 
			"other_appointments": Appointment.objects.filter(task_date__gt=datetime.date.today()).order_by("task_date"),
		}
	except KeyError:
		return redirect('/')
	return render(request, "main/appointments.html", context)

def add(request):
	Appointment.objects.create(
		task_date = request.POST['date'],
		task_time = request.POST['time'],
		task = request.POST['task'],
		task_creator_id = request.session['id']
	)
	return redirect('/success')


def logout(request):
	del request.session['id']
	return redirect('/')

def destroy(request, appointment_id):
	appointment_to_delete = Appointment.objects.get(id=appointment_id)
	appointment_to_delete.delete()
	return redirect('/success')

def edit(request, appointment_id):
	context = {
		"appointments": Appointment.objects.get(id=appointment_id)
	}
	return render(request, "main/edit.html", context)

def update(request, appointment_id):
	
	appointments = Appointment.objects.get(id=appointment_id)
	appointments.task = request.POST["task"]
	appointments.task_status = request.POST["task_status"]
	appointments.task_date = request.POST["date"]
	appointments.task_time = request.POST["task_time"]
	appointments.save(force_update=True)
	return redirect('/success')