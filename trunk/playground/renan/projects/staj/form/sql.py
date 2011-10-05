#!/usr/bin/python
# -*- coding: utf-8 -*-


from form.models import Mentor
from form.models import ProgrammingLanguagesAndFrameworks

def insertMentors():
    mentors = ( ["Onur", "Küçük", "onur@pardus.org.tr"],
                ["Gökmen", "Göksel", "gokmen@pardus.org.tr"],
                ["Ozan", "Çağlayan", "ozan@pardus.org.tr"],
                ["Gökçen", "Eraslan", "gokcen@pardus.org.tr"],
                ["Bahadır", "Kandemir", "bahadir@pardus.org.tr"],
                ["Semen", "Cirit", "scirit@pardus.org.tr"],
                ["Mete", "Alpaslan", "mete@pardus.org.tr"],
                ["Fatih", "Aşıcı", "fatih@pardus.org.tr"],
                ["Serdar", "Dalgıç", "serdar@pardus.org.tr"],
                ["Renan", "Çakırerk", "renan@pardus.org.tr"] )

    for mentor in mentors:
        m = Mentor(name = mentor[0], surname = mentor[1], email = mentor[2], username="none", password="none")
        m.save()

def insertProgrammingLanguages():
    languages = ( "Python", "C", "C++", "Ruby", "Java", "HTML", "Qt", "Django",
                  "Javascript", "Shellscript", "Rails" )

    for language in languages:
        l = ProgrammingLanguagesAndFrameworks(name = language)
        l.save()
