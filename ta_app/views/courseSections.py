from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from ta_app.models import Course, Section, User
from ta_app.Classes.UserClass import UserClass


class courseSections(View):
    def get(self, request, course_pk):
        usr_role = request.session["role"]
        pk = request.session["pk"]
        curr_usr = User.objects.get(pk=pk)
        course = Course.objects.get(pk=course_pk)
        sections = Section.objects.filter(course_parent=course)
        teacherassistant_pool = User.objects.filter(role="Teacher-Assistant")
        instructor_pool = User.objects.filter(role="Instructor")
        is_assigned = False
        ta_pool = []
        assigned_users={}
        for section in sections:
            tas = User.objects.filter(role="Teacher-Assistant", assigned_section__in=[section]).distinct()
            ins = User.objects.filter(role="Instructor", assigned_section__in=[section]).distinct()
            if User.objects.filter(pk=pk,role="Instructor",assigned_section__in=[section]).exists():
                is_assigned = True
            for inst in ins:
                if inst not in assigned_users:
                    assigned_users[inst] = "True"
            for ta in tas:
                if ta not in ta_pool:
                    if not ta.assigned_section.filter(type="LAB", course_parent=section.course_parent).exists:
                        assigned_users[ta] = "True"
                    else:
                        assigned_users[ta] = "False"
                    ta_pool.append(ta)
        course_lecture = None
        for secs in sections:
            if secs.type == "LEC":
                course_lecture = secs.pk

        check = "False"
        for usrs in assigned_users:
            print(usrs.role)
            if usrs.role == "Instructor":
                check = "True"
        print(check)
        instructor_message = 'None'
        if curr_usr not in assigned_users:
            instructor_message = "Your are not assigned to this course"
        return render(request, "course_sections.html", {"course": course, "sections": sections,
                                                        "ta_all": teacherassistant_pool, "ins_all": instructor_pool,
                                                        "usr_role": usr_role, "ta_pool": ta_pool, "assigned_users":assigned_users,
                                                        "course_lecture":course_lecture,"instructor_message":instructor_message,
                                                        "check":check,"is_assigned":is_assigned, "curr_usr":curr_usr},)

    def post(self, request, course_pk):
        usr_role = request.session["role"]
        pk = request.session["pk"]
        curr_usr = User.objects.get(pk=pk)
        course = Course.objects.get(pk=course_pk)
        sections = Section.objects.filter(course_parent=course)
        teacherassistant_pool = User.objects.filter(role="Teacher-Assistant")
        instructor_pool = User.objects.filter(role="Instructor")
        # get pool of users for sections
        ta_pool = []
        assigned_users={}
        for section in sections:
            tas = User.objects.filter(role="Teacher-Assistant", assigned_section__in=[section]).distinct()
            ins = User.objects.filter(role="Instructor", assigned_section__in=[section]).distinct()
            for inst in ins:
                if inst not in assigned_users:
                    assigned_users[inst]="True"
            for ta in tas:
                if ta not in ta_pool:
                    if not ta.assigned_section.filter(type="LAB", course_parent=section.course_parent).exists:
                        assigned_users[ta] = "True"
                    else:
                        assigned_users[ta] = "False"
                    ta_pool.append(ta)
        course_lecture = None
        for secs in sections:
            if secs.type == "LEC":
                course_lecture = secs.pk
        check = "False"
        for usrs in assigned_users:
            if usrs.role == "Instructor":
                check = "True"
        dict = {}
        for key,values in request.POST.lists():
            if key != "csrfmiddlewaretoken" and key != "remove_section":
                if key in dict:
                    dict[key].extend(values)
                else:
                    dict[key] = values
        assigned = False
        instructor_message = 'None'

        if curr_usr not in assigned_users:
            instructor_message = "You are not assigned to this course"
        for key, value in dict.items():
            for val in value:
                if val != 'None':
                    try:
                        acc = User.objects.get(pk=val)
                        sec = Section.objects.get(pk=key)
                        newacc = UserClass(username=acc.username, password=acc.password, name=acc.name, role=acc.role,
                                           email=acc.email,
                                           phone_number=acc.phone_number, address=acc.address, assigned=acc.assigned,
                                           assigned_sections=acc.assigned_section.all())
                        newacc.add_section(sec)
                        assigned = True

                    except ValueError as failure:
                        return render(request, "course_sections.html", {"course": course, "sections": sections,"curr_usr":curr_usr,
                                                                        "ta_all": teacherassistant_pool, "ins_all": instructor_pool, "usr_role": usr_role,
                                                                        "ta_pool": ta_pool, "assigned_users":assigned_users,"check":check,
                                                                        "course_lecture":course_lecture,check:"check","instructor_message":instructor_message,"message": failure.__str__()})
        success = ""
        to_remove = request.POST.get('remove_section')
        if to_remove:
            keys = to_remove.split()
            try:
                remove = User.objects.get(pk=int(keys[0]))
                s = None
                try:
                    s = Section.objects.get(pk=int(keys[1]))
                except Section.DoesNotExist:
                    # this will be caught by the remove_section so can just pass right now
                    pass
                u = UserClass(username=remove.username, password=remove.password, name=remove.name, role=remove.role,
                              email=remove.email, phone_number=remove.phone_number, skills=remove.skills,
                              address=remove.address, assigned=remove.assigned,
                              assigned_sections=remove.assigned_section.all())
                try:
                    u.remove_section(s)
                    success = "Successfully removed " + u.__str__() + " from " + s.__str__()
                except ValueError as failure:
                    # changes the error message, then proceeds, removing need for another return
                    success = failure.__str__()
            except User.DoesNotExist:
                success = "User does not exist"

        # get pool of users for sections
        ta_pool = []
        assigned_users = {}
        for section in sections:

            tas = User.objects.filter(role="Teacher-Assistant", assigned_section__in=[section]).distinct()
            ins = User.objects.filter(role="Instructor", assigned_section__in=[section]).distinct()
            for inst in ins:
                if inst not in assigned_users:
                    assigned_users[inst] = "True"
            for ta in tas:
                if ta not in ta_pool:
                    if not ta.assigned_section.filter(type="LAB", course_parent=section.course_parent).exists:
                        assigned_users[ta] = "True"
                    else:
                        assigned_users[ta] = "False"
                    ta_pool.append(ta)
        course_lecture = None
        for secs in sections:
            if secs.type == "LEC":
                course_lecture = secs.pk

        check = "False"
        for usrs in assigned_users:
            print(usrs)

            if usrs.role == "Instructor":
                check = "True"
        if success == "":
            success = "Nothing was Submitted"
        if assigned:
            success = "Successfully assigned user(s) to section(s)"

            instructor_message = 'None'
            if curr_usr not in assigned_users:
                instructor_message = "Your are not assigned to this course"


        return render(request, "course_sections.html", {"course": course, "sections": sections,"curr_usr":curr_usr,
                                                        "ta_all": teacherassistant_pool, "ins_all": instructor_pool,
                                                        "usr_role": usr_role, "ta_pool": ta_pool, "assigned_users":assigned_users,
                                                        "course_lecture":course_lecture,"check":check,"instructor_message":instructor_message,
                                                        "message": success})
