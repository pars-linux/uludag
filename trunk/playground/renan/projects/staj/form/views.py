#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from django.shortcuts import render_to_response
import MySQLdb
from django.http import HttpResponseRedirect

from django import forms

from staj.form.models import *

from staj.captcha.fields import CaptchaField

from django.forms.util import ErrorList

from django.db.models import F

import os

from django.core.paginator import Paginator

GENDER_CHOICES = (  (u'M', u'Erkek'),
                    (u'F', u'Kadın'))

DATE_CHOICES = (  (u'20 Haziran - 15 Temmuz 2011', u'20 Haziran - 15 Temmuz 2011'),
                  (u'1 Ağustos - 26 Eylül 2011', u'1 Ağustos - 26 Eylül 2011'),
                  (u'Farketmez', u'Farketmez')
                  )

SCORE_CHOICES =  (  (u'1', u'1'),
                    (u'2', u'2'),
                    (u'3', u'3'),
                    (u'4', u'4'),
                    (u'5', u'5'),
                    (u'6', u'6'),
                    (u'7', u'7'),
                    (u'8', u'8'),
                    (u'9', u'9'),
                    (u'10', u'10'),
                    )

GRADE_CHOICES =  (  (u'1', u'1'),
                    (u'2', u'2'),
                    (u'3', u'3'),
                    (u'4', u'4'),
                    )

ENGLISH_CHOICES = ( (u'Başlangıç',u'Başlangıç'),
                    (u'Orta', u'Orta'),
                    (u'İyi', u'İyi'),
                    (u'Çok İyi', u'Çok İyi'),
                    )


YES_NO = (  (u'E', u'Evet'),
            (u'H', u'Hayır'))


"""
class ScoringForm(forms.Form):
    name = forms.CharField()
    surname = forms.CharField()
    birthdate = forms.CharField()
    gender = forms.CharField()
    id_number = forms.CharField()
    address = forms.CharField()
    district = forms.CharField()
    city = forms.CharField()
    email = forms.CharField()
    website = forms.CharField()
    school = forms.CharField()
    department = forms.CharField()
    gpa = forms.CharField()
    programming_languages_and_frameworks = forms.CharField()
    other_programming_languages = forms.CharField()
    awards = forms.CharField()
    why_pardus = forms.CharField()
    projects_done = forms.CharField()
    where_did_you_hear = forms.CharField()
    suitable_date = forms.CharField()
    prefered_projects = forms.CharField()
    commited_before = forms.CharField()
    cv_upload = forms.CharField()
    code_upload = forms.CharField()
"""

class InternForm(forms.Form):
    name = forms.CharField(max_length=50, label="Ad", widget=forms.TextInput(attrs={'class':'validate[required]'}))
    surname = forms.CharField(max_length=50, label="Soyad", widget=forms.TextInput(attrs={'class':'validate[required]'}))
    birthdate = forms.DateField(('%d.%m.%Y',), label="Doğum Tarihi (örnek: 24.03.1988)", widget = forms.DateTimeInput(format='%d.%m.%Y', attrs={'class':'validate[required]','size':'15'}))
    gender = forms.ChoiceField(GENDER_CHOICES,label="Cinsiyet",widget=forms.Select(attrs={'class':'validate[required] short'}))
    id_number = forms.CharField(label="T.C. Kimlik No", max_length=11, widget=forms.TextInput(attrs={'class':'validate[required,custom[number]]'}))
    mobile_phone = forms.CharField(label="Cep Telefonu (örnek: 05001234567)", max_length=11, widget=forms.TextInput(attrs={'class':'validate[required,custom[phone],minSize[11]]'}))
    address = forms.CharField(label="Ev Adresi", max_length=100, widget=forms.TextInput(attrs={'class':'validate[required]'}))
    district = forms.CharField(label="Semt", max_length=50, widget=forms.TextInput(attrs={'class':'validate[required]'}))
    city = forms.CharField(label="Şehir", max_length=50, widget=forms.TextInput(attrs={'class':'validate[required]'})) # SEHIR LISTESI
    email = forms.EmailField(label="E-posta Adresi", max_length=100, widget=forms.TextInput(attrs={'class':'validate[required,custom[email]]'}))
    email_verify = forms.EmailField(label="E-posta Adresi (Tekrar)", max_length=100, widget=forms.TextInput(attrs={'class':'validate[required,custom[email]]'}))
    jabber = forms.EmailField(label="Jabber Hesabı", max_length=100, widget=forms.TextInput(attrs={}), required=False)
    website = forms.URLField(label="Web Sitesi", max_length=100, required=False, widget=forms.TextInput())
    school = forms.CharField(label="Üniversite Adı", max_length=100, widget=forms.TextInput(attrs={'class':'validate[required]'}))
    department = forms.CharField(label="Bölüm", max_length=100, widget=forms.TextInput(attrs={'class':'validate[required]'}))
    grade = forms.ChoiceField(GRADE_CHOICES, label="Kaçıncı Sınıftasınız?", widget=forms.Select(attrs={'class':'validate[required] short'}))
    semester = forms.ChoiceField(SCORE_CHOICES, label="Hazırlık Hariç Toplam Kaç Dönemdir Üniversitedesiniz?", widget=forms.Select(attrs={'class':'validate[required] short'}))
    expected_grad_date = forms.DateField(('%d.%m.%Y',), label="Tahmini Mezuniyet Tarihi (örnek: 17.06.2013)", widget = forms.DateTimeInput(format='%d.%m.%Y', attrs={'class':'validate[required]','size':'15'}))
    gpa = forms.CharField(label="Not Ortalaması (örnek: 2.65)", max_length=10, widget=forms.TextInput(attrs={'class':'validate[required,custom[number]]'}))
    mandatory_internship = forms.ChoiceField(YES_NO,label="Stajınız Zorunlu mu?",widget=forms.Select(attrs={'class':'validate[required] short'}))
    english = forms.ChoiceField(ENGLISH_CHOICES,label="İngilizce Seviyesi",widget=forms.Select(attrs={'class':'validate[required] short'}))
    programming_languages_and_frameworks = forms.ModelMultipleChoiceField(
            queryset = ProgrammingLanguagesAndFrameworks.objects.all(), 
            label="Hakim olduğunuz programlama dilleri ve Frameworkler",
            widget = forms.CheckboxSelectMultiple(attrs={'class':'validate[minCheckbox[2]]'})
            )
    other_programming_languages = forms.CharField(label = "Hakim olduğunuz diğer programlama dilleri", max_length = 100, required=False)
    awards = forms.CharField(label = "Başarı ve Ödüller (En çok 1000 karakter)", widget = forms.Textarea, max_length=1000, required=False)
    why_pardus = forms.CharField(label = "Neden Pardus'ta staj yapmak istediğinizi, Pardus'un size nasıl bir katkı sağlayacağını kısaca yazınız (En çok 1000 karakter)", max_length=1000, widget = forms.Textarea(attrs={'class':'validate[required,maxSize[1000]]'}))
    projects_done = forms.CharField(label = "Projeleriniz (En çok 1000 karakter)", widget=forms.Textarea(attrs={'class':'validate[maxSize[1000]]'}), max_length=1000, required=False)
    where_did_you_hear = forms.CharField(label = "Stajı nereden duydunuz? (En çok 1000 karakter)", max_length=1000, widget = forms.Textarea(attrs={'class':'validate[required,maxSize[1000]]'}))
    linux_experience = forms.CharField(label = "Linux deneyimleriniz (En çok 1000 karakter)", max_length=1000, widget = forms.Textarea(attrs={'class':'validate[required,maxSize[1000]]'}))
    prefered_os = forms.CharField(label = "Bilgisayarınızda aktif olarak bir Linux dağıtımı kullanıyor musunuz? Evet ise hangisi/hangileri?", max_length=100, widget = forms.TextInput(attrs={'class':'validate[required,maxSize[100]]'}))

    more = forms.CharField(label = "Açıklamalar (En çok 1000 karakter)", max_length=1000, widget = forms.Textarea(attrs={'class':'validate[maxSize[1000]]'}), required=False)
    suitable_date = forms.ChoiceField(DATE_CHOICES, label = "Hangi tarih aralıklarında staj yapabileceğinizi belirtiniz")

    #prefered_projects = forms.ModelMultipleChoiceField(queryset = Project.objects.all(),
    #        label = "Staj sırasında üzerinde çalışmak istediğiniz projeler (Birden fazla seçim yapabilirsiniz)",
    #        widget = forms.SelectMultiple(attrs={'class':'validate[required]'})
    #        )

    commited_before = forms.CharField(label="Daha önce Pardus'a katkıda bulundunuz mu? Açıklayınız. (En çok 200 karakter)", max_length = 200, widget = forms.Textarea(attrs={'class':'validate[required,maxSize[200]]'}))
    cv_upload = forms.FileField(label="Özgeçmiş Yükleme. Yüklediğiniz dosya pdf veya odt formatında ve 1 MB'den küçük olmalıdır.", widget = forms.FileInput(attrs={'class':'validate[required]'}))
    code_upload = forms.FileField(label="Kod Yükleme. Yüklediğiniz dosya tar.gz formatında ve 10 MB'den küçük olmalıdır. )", required=False)
    captcha = CaptchaField(label="Doğrulama Metni")

    def clean(self):
        content_types = ('application/pdf', 'application/vnd.oasis.opendocument.text')
        file_exts = ('.odt', '.pdf')

        cleaned_data = self.cleaned_data

        id_number = cleaned_data.get("id_number")
        cv = cleaned_data.get("cv_upload")
        code = cleaned_data.get("code_upload")

        if id_number:
            if not (id_number.isdigit() and len(id_number)==11):
                self._errors["id_number"] = ErrorList(["Lütfen geçerli bir T.C kimlik numarası giriniz."])
            else:
                total = 0
                for i in range(0,10):
                    total += int(id_number[i])

                total = str(total)

                if not total.endswith(id_number[10]):
                    self._errors["id_number"] = ErrorList(["Lütfen geçerli bir T.C kimlik numarası giriniz. no check"])

            if not len(id_number) == 11:
                self._errors["id_number"] = ErrorList(["Lütfen geçerli bir T.C kimlik numarası giriniz."])

        if cv:
            if not cv.content_type in content_types:
                self._errors["cv_upload"] = ErrorList(["Yüklediğiniz dosya odt ya da pdf formatında olmalıdır."])

            if not cv.name.endswith(file_exts):
                self._errors["cv_upload"] = ErrorList(["Yüklediğiniz dosya odt ya da pdf formatında olmalıdır."])

            if cv.size > 1024 * 1024:
                self._errors["cv_upload"] = ErrorList(["Yüklediğiniz dosyanın boyutu 1 Mb'den küçük olmalıdır."])


        if code:
            if code.size > 1024 * 1024 * 10:
                self._errors["code_upload"] = ErrorList(["Yüklediğiniz dosyanın boyutu 10 Mb'den küçük olmalıdır."])

            if not code.name.endswith("tar.gz"):
                self._errors["code_upload"] = ErrorList(["Yüklediğiniz dosya tar.gz formatında olmalıdır."])

            if not code.content_type == "application/x-gzip":
                self._errors["code_upload"] = ErrorList(["Yüklediğiniz dosya tar.gz formatında olmalıdır."])


        return cleaned_data



class MentorForm(forms.Form):
    name = forms.CharField(label="Proje Adı")
    objective = forms.CharField(widget=forms.Textarea, label="Amaç")
    todo = forms.CharField(widget=forms.Textarea, label="Yapılacaklar")
    prerequisites = forms.CharField(widget=forms.Textarea, label="Ön Şartlar")
    references = forms.CharField(widget=forms.Textarea, label="Referanslar")
    score = forms.ChoiceField(SCORE_CHOICES, label="Zorluk Derecesi")
    mentors = forms.ModelMultipleChoiceField(queryset=Mentor.objects.all(), label="Danışman (Birden fazla seçim yapılabilir)")



ext = { 'application/pdf':'pdf', 'text/html':'html', 'application/vnd.oasis.opendocument.text':'odt', 'text/plain':'txt'}



def scoring_form(request):

    # Messages to inform the user about processes
    messages = []

    # Logout

    if request.POST.get('logout') == "true":
        request.session.__delitem__("mentor_id")
        return render_to_response('login.html')


    # Login Failed

    if not request.session.__contains__("mentor_id"):
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == None or password == None:
            return render_to_response('login.html')

        mentor = None

        try:
            mentor = Mentor.objects.get(username = username, password = password)
        except:
            return render_to_response('login.html')

        request.session['mentor_id'] = mentor.id
        request.session['mentor_name'] = mentor.name
        request.session['mentor_surname'] = mentor.surname

    # Login Successfull

        if request.session['mentor_id'] == 47:
            return HttpResponseRedirect("http://pardus.org.tr")

    studentList = Student.objects.all()
    student_id = request.GET.get('student')

    mentor_id = request.session['mentor_id']
    mentor_name = request.session['mentor_name']
    mentor_surname = request.session['mentor_surname']

    # ana tabloya gelecek verileri modifiye ediyoruz
    for s in studentList:
        total = 0
        for v in s.vote.select_related():
            total += int(v.vote)

        score = float(total) / float(len(s.vote.select_related()))
        score = "%.3f" % score
        s.score = score

        s.gpa = str(s.gpa).replace(",",".")

    # End session after 5 minutes
    #request.session.set_expiry(600)

    # Request Student Details
    if (student_id):
        current_student = None

        try:
            student_id = int(student_id)
        except:
            student_id = 1

        # Select Current Student From Database
        try:
            current_student = Student.objects.get(id=student_id)
        except:
            messages.append("Öğrenci Bulunamadı")

            return render_to_response('scoringform.html', {'studentList': studentList,
                                                           'mentor_id': mentor_id,
                                                           'mentor_name':mentor_name ,
                                                           'mentor_surname':mentor_surname,
                                                           'messages':messages
                                                           }
                                     )

        mentor_has_voted_before = False
        for vote in current_student.vote.select_related():
            if vote.mentor.id == mentor_id:
                mentor_has_voted_before = True


        if request.method == "POST":
            comment = request.POST.get('comment')
            vote = request.POST.get('vote')
            mentor = request.POST.get('mentor')

            if not comment == None and comment != "":
                comment_to_add = Comment.objects.create(comment = comment, mentor_id = mentor_id)

                # Save Comment
                current_student.comment.add(comment_to_add)
                current_student.save()
                messages.append("Yorumunuz Eklendi.")


            if not vote == None:

                if not mentor_has_voted_before:

                    # Save Vote
                    try:
                        vote_to_add = Vote.objects.create(vote = vote, mentor_id = mentor_id)
                        current_student.vote.add(vote_to_add)

                        current_student.save()

                        messages.append("Oyunuz Gönderildi.")
                        mentor_has_voted_before = True

                    except:
                        messages.append("Oylamada hata var.")
                        return render_to_response('scoringform.html', {'studentList': studentList,
                            'mentor_id': mentor_id, 'mentor_name':mentor_name , 'mentor_surname':mentor_surname, 'messages':messages})

        comments = current_student.comment.select_related()
        votes = current_student.vote.select_related()

        # Get Vote List
        mentor_votes_mentor = []
        mentor_votes_vote = []


        # Count Total Votes
        total_votes = 0
        total_score = 0.0

        for vote in votes:
            mentor_votes_mentor.append("%s %s" % (vote.mentor.name, vote.mentor.surname))
            mentor_votes_vote.append("%s" % vote.vote)

            try:
                total_score += int(vote.vote)
            except:
                pass

            total_votes += 1

        avarage_score = 0

        try:
            avarage_score = total_score / total_votes
            avarage_score = "%.3f" % avarage_score
        except:
            pass

        total_score = int(total_score)

        # Has uploaded code
        path = "/home/pars/workspace/staj/uploads/code/%s.tar.gz" % current_student.id_number
        code_uploaded = os.path.exists(path)

        # Display Student Details
        return render_to_response('scoringform.html', {'student':current_student, 'studentList': studentList,
            'mentor_id': mentor_id, 'mentor_name':mentor_name , 'mentor_surname':mentor_surname, 'comments':comments,
            'votes':votes, 'mentor_has_voted_before':mentor_has_voted_before, 'mentor_votes_mentor':mentor_votes_mentor, 'mentor_votes_vote':mentor_votes_vote,
            'total_votes':total_votes,'avarage_score':avarage_score, 'total_score':total_score, 'code_uploaded':code_uploaded, 'messages':messages})

    else:
        test = 0
        return render_to_response('scoringform.html', {'studentList': studentList,
            'mentor_id': mentor_id, 'mentor_name':mentor_name , 'mentor_surname':mentor_surname, 'test':test, 'messages':messages})


    """
    if request.GET.get('student'):
        try:
            page = int(request.GET.get('student','1'))
            if page > paginator.num_pages or page==0:
                return render_to_response('scoringform.html', {'error': 'Student not found'})
        except ValueError:
            page = 1

        try:
            list = paginator.page(page)
        except(EmptyPage, InvalidPage):
            list = paginator.page(paginator.num_pages)

        return render_to_response('scoringform.html', {'list': list})
    else:
        return render_to_response('scoringform.html', {'studentList': studentList})
    """

def intern_form(request):

    title = "Pardus Staj 2011 Başvuru Formu"

    if request.method == 'POST': # If the form has been submitted...
        form = InternForm(request.POST, request.FILES) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass

            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            birthdate = form.cleaned_data['birthdate']
            gender = form.cleaned_data['gender']
            id_number = form.cleaned_data['id_number']
            mobile_phone = form.cleaned_data['mobile_phone']
            address = form.cleaned_data['address']
            district = form.cleaned_data['district']
            city = form.cleaned_data['city']
            email = form.cleaned_data['email']
            jabber = form.cleaned_data['jabber']
            website = form.cleaned_data['website']
            school = form.cleaned_data['school']
            department = form.cleaned_data['department']
            grade = form.cleaned_data['grade']
            semester = form.cleaned_data['semester']
            expected_grad_date = form.cleaned_data['expected_grad_date']
            gpa = form.cleaned_data['gpa']
            mandatory_internship = form.cleaned_data['mandatory_internship']
            english = form.cleaned_data['english']
            programming_languages_and_frameworks = form.cleaned_data['programming_languages_and_frameworks']
            other_programming_languages = form.cleaned_data['other_programming_languages']
            awards = form.cleaned_data['awards']
            why_pardus = form.cleaned_data['why_pardus']
            projects_done = form.cleaned_data['projects_done']
            where_did_you_hear = form.cleaned_data['where_did_you_hear']
            linux_experience = form.cleaned_data['linux_experience']
            prefered_os = form.cleaned_data['prefered_os']
            more = form.cleaned_data['more']
            suitable_date = form.cleaned_data['suitable_date']
            #prefered_projects = form.cleaned_data['prefered_projects']
            commited_before = form.cleaned_data['commited_before']
            cv = form.cleaned_data['cv_upload']
            code = form.cleaned_data['code_upload']

            name = name.split()
            name = " ".join(name)
            surname = surname.split()
            surname = " ".join(surname)

            filename = "%s.%s" % (id_number, ext[cv.content_type])
            save_cv(cv, filename)

            if code:
                save_code(code, id_number)

            s = Student(name=name,
                        surname=surname,
                        birthdate=birthdate,
                        gender=gender,
                        id_number=id_number,
                        mobile_phone=mobile_phone,
                        address=address,
                        district=district,
                        city=city,
                        email=email,
                        jabber=jabber,
                        website=website,
                        school=school,
                        department=department,
                        grade=grade,
                        semester=semester,
                        expected_grad_date=expected_grad_date,
                        gpa=gpa,
                        mandatory_internship=mandatory_internship,
                        english=english,
                        other_programming_languages=other_programming_languages,
                        awards=awards,
                        why_pardus=why_pardus,
                        projects_done=projects_done,
                        where_did_you_hear=where_did_you_hear,
                        linux_experience=linux_experience,
                        prefered_os=prefered_os,
                        more=more,
                        suitable_date=suitable_date,
                        commited_before=commited_before,
                        cv_upload = filename)
            s.save()

            #for project in prefered_projects:
            #    s.prefered_projects.add(project)

            for pl in programming_languages_and_frameworks:
                s.programming_languages_and_frameworks.add(pl)


            return HttpResponseRedirect('/kayit/') # Redirect after POST
    else:
        form = InternForm(label_suffix=' ') # An unbound form

    return render_to_response('form.html', {'form': form, 'title': title})


def save_cv(cv, filename):
    path = "/home/pars/workspace/staj/uploads/cv/" + filename
    destination = open(path, 'wb+')
    for chunk in cv.chunks():
        destination.write(chunk)
    destination.close()

def save_code(code, id_number):
    path = "/home/pars/workspace/staj/uploads/code/" + id_number + ".tar.gz"
    destination = open(path, 'wb+')
    for chunk in code.chunks():
        destination.write(chunk)
    destination.close()

def thanks(request):
    return render_to_response('kayit.html', None)

def end(request):
    return render_to_response('thanks.html', None)

def makale(request):
    return render_to_response('index.html', None)

def mentor_form(request):

    title = "Fikir Toplama Robotu"

    if request.method == 'POST': # If the form has been submitted...
        form = MentorForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            name = form.cleaned_data['name']
            objective = form.cleaned_data['objective']
            todo = form.cleaned_data['todo']
            prerequisites = form.cleaned_data['prerequisites']
            score = form.cleaned_data['score']
            references = form.cleaned_data['references']
            mentors = form.cleaned_data['mentors']


            p = Project(name=name, objective=objective, todo=todo, prerequisites=prerequisites, score=score, references=references)
            p.save()
            for mentor in mentors:
                p.mentors.add(mentor)

            return HttpResponseRedirect('/mentor/done') # Redirect after POST
    else:
        form =MentorForm(label_suffix=' ') # An unbound form

    return render_to_response('mentor.html', {'form': form, 'title': title})


def mentor_done(request):
    return render_to_response('mentor_done.html', None)

def process_intern_form():
    pass


def projeler(request):
    list = Project.objects.all()
    details = "details"
    return render_to_response('projects.html', {'list': list, 'details':details})



