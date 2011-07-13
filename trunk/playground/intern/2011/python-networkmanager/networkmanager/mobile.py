#!/usr/bin/python
# -*- coding: utf-8 -*-


import piksemel

serviceproviders="/usr/share/mobile-broadband-provider-info/serviceproviders.xml"

doc = piksemel.parse(serviceproviders)
countries = doc.tags('country')


def get_country(code):
    #returns country
    for co in countries:
        if co.getAttribute('code') == code:
            return co

def get_providers(country):
    #returns providers
    providers=[]
    provider=country.tags('provider')
    for pro in provider:
        providers.append(pro)
    return providers

def get_providers_names(providers):
    #returns names
    names=[]
    for pro in providers:
        names.append(pro.getTagData('name'))
    return names

def list_providers_names(providers):
    names=get_providers_names(providers)
    index=1
    for name in names:
        print index , name
        index+=1

def get_providers_gsm(provider):
    #returns gsm
    return provider.getTag('gsm')

def get_gsm_networkid(gsm):
    #returns network-id
    networkids=[]
    for netid in gsm.tags('network-id'):
        networkids.append(netid)
    return networkids

def get_gsm_apn(gsm):
    #return apns
    apns=[]
    for apn in gsm.tags('apn'):
        apns.append(apn)
    return apns

def get_apns_values(apns):
    values=[]
    for apn in apns:
        values.append(apn.getAttribute('value'))
    return values

def get_user_name_pass(apn):
    usr=apn.getTagData('username')
    pss=apn.getTagData('password')
    return (usr,pss)
