#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.forms import ModelForm

class ProgrammingLanguagesAndFrameworks(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % (self.name)



class Mentor(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __unicode__(self):
       return u'%s %s' % (self.name, self.surname)


class Project(models.Model):
    name = models.TextField()
    objective = models.TextField()
    todo = models.TextField()
    prerequisites = models.TextField()
    references = models.TextField()
    score = models.TextField()
    mentors = models.ManyToManyField(Mentor)

    def __unicode__(self):
       return u'%s' % (self.name)

    class Meta:
        ordering = ('name',)



class Vote(models.Model):
    vote = models.TextField(max_length=10)
    mentor = models.ForeignKey(Mentor)


class Comment(models.Model):
    comment = models.TextField(max_length=2000)
    timestamp = models.DateTimeField(auto_now = True)
    mentor = models.ForeignKey(Mentor)

    def __unicode__(self):
       return u'%s' % (self.comment)

class Student(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    birthdate = models.DateField(max_length=50)
    gender = models.CharField(max_length=1)
    id_number = models.CharField(max_length=11)
    mobile_phone = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    district = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    jabber = models.EmailField(max_length=100, null=True)
    website = models.URLField(max_length=100, null=True)
    school = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    expected_grad_date = models.EmailField(max_length=100)
    gpa = models.CharField(max_length=10)
    mandatory_internship = models.CharField(max_length=1)
    english = models.CharField(max_length=100)
    programming_languages_and_frameworks = models.ManyToManyField(ProgrammingLanguagesAndFrameworks, max_length=50)

    other_programming_languages = models.CharField(max_length=100, null=True)
    awards = models.CharField(max_length=1000, null=True)
    why_pardus = models.CharField(max_length=1000)
    projects_done = models.CharField(max_length=1000, null=True)
    where_did_you_hear = models.CharField(max_length=1000)
    linux_experience = models.CharField(max_length=1000)
    prefered_os = models.CharField(max_length=1000)

    more = models.CharField(max_length=1000, null=True)
    suitable_date = models.CharField(max_length=50)

    #prefered_projects = models.ManyToManyField(Project, max_length=200)
    commited_before = models.CharField(max_length=100)

    cv_upload = models.FileField(upload_to='attachments')
    code_upload = models.FileField(upload_to='attachments', null=True)

    comment = models.ManyToManyField(Comment, max_length=2000)

    vote = models.ManyToManyField(Vote, max_length=10)
    total_yes_votes = models.IntegerField(null=True)
    total_no_votes = models.IntegerField(null=True)


    def __unicode__(self):
        return u'%s %s' % (self.name, self.surname)

"""
class CommentsAndVotes(models.Model):
    vote = models.TextField(max_length=10)
    comment = models.TextField(max_length=2000)
    student = models.ManyToManyField(Student)
    mentor = models.ManyToManyField(Mentor)

    def __unicode__(self):
        return u'%s %s' % (self.comment, self.vote)
"""

"""
class ScoringModel(models.Model):
"""

"""
Hold score information of the given fields
    student = models.OneToOneField(Student)
    mentor = models.OneToOneField(Mentor)
    score = models.CharField(max_length=5)
    comment = models.CharField(max_length=2000)
"""
