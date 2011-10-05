#!/usr/bin/python
# -*- coding: utf-8 -*-

from form.models import Student
import datetime

students = Student.objects.all()

def get_age(student):
    today = datetime.date.today()
    age = today.year - student.birthdate.year

    return age


def average_age():
    total = 0
    average = 0

    for s in students:
        total += get_age(s)

    average = total / students.count()

    return average


def maximum_age():
    max_age = 0
    for s in students:
        if get_age(s) > max_age:
            max_age = get_age(s)

    return max_age


def minimum_age():
    min_age = maximum_age()
    for s in students:
        if get_age(s) < min_age:
            min_age = get_age(s)

    return min_age


def count_distinct_ages():
    age_table = {}

    for s in students:
        if get_age(s) in age_table:
            age_table[get_age(s)] += 1
        else:
            age_table[get_age(s)] = 1

    return age_table


def count_distinct_universities():
    uni_table = {}

    for s in students:
        if s.school in uni_table:
            uni_table[s.school] += 1
        else:
            uni_table[s.school] = 1

    return uni_table


def pretty_distinct_universities():
    uni = count_distinct_universities()
    for u in uni:
        print "%s-%s" % (u.title(), uni[u])

    print len(count_distinct_universities())


def count_distinct_departments():
    dep_table = {}
    departments = Student.objects.values('department').distinct()

    for d in departments:
        if departments[d] in dep_table:
            dep_table[d.department] += 1
        else:
            dep_table[d.department] = 1

    return dep_table




print average_age(), maximum_age(), minimum_age()
print count_distinct_ages()
print pretty_distinct_universities()
print count_distinct_departments()
