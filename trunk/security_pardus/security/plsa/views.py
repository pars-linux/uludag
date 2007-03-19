from security.plsa.models import PLSA, Language
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import translation
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.feedgenerator import Rss201rev2Feed
from django.contrib.sites.models import Site

def details(request, lang, plsa_id):
    translation.activate(lang)
    lang = Language.objects.get(code=lang)
    plsa = get_object_or_404(PLSA, publish=True, language=lang, plsa_id=plsa_id)
    year_list = [x.year for x in PLSA.objects.dates("release_date", "year")]
    language_list = Language.objects.exclude(code=lang.code)

    return render_to_response("plsa/plsa_detail.html", {"object": plsa,
                                                        "lang": lang.code,
                                                        "year_list": year_list,
                                                        "language_list": language_list})

def details_text(request, lang, plsa_id):
    translation.activate(lang)
    lang = Language.objects.get(code=lang)
    plsa = get_object_or_404(PLSA, publish=True, language=lang, plsa_id=plsa_id)
    language_list = Language.objects.exclude(code=lang.code)

    return render_to_response("plsa/plsa_detail_text.html", {"object": plsa})

def list_year(request, lang, year):
    translation.activate(lang)
    lang = Language.objects.get(code=lang)
    object_list = [x for x in PLSA.objects.filter(publish=True, language=lang) if x.release_date.year == int(year)]
    year_list = [x.year for x in PLSA.objects.dates("release_date", "year")]
    language_list = Language.objects.exclude(code=lang.code)

    return render_to_response("plsa/plsa_archive_year.html", {"object_list": object_list,
                                                              "year": year,
                                                              "lang": lang.code,
                                                              "year_list": year_list,
                                                              "language_list": language_list})

def page_lang(request, lang):
    translation.activate(lang)
    lang = Language.objects.get(code=lang)
    object_list = PLSA.objects.filter(publish=True, language=lang)[:10]
    year_list = [x.year for x in PLSA.objects.dates("release_date", "year")]
    language_list = Language.objects.exclude(code=lang.code)

    return render_to_response("plsa/plsa_archive.html", {"object_list": object_list,
                                                         "lang": lang.code,
                                                         "year_list": year_list,
                                                         "language_list": language_list})

def page_index(request):
    languages = [x.code for x in Language.objects.all()]
    for lang in request.META["HTTP_ACCEPT_LANGUAGE"].split(","):
        lang = lang.split("-")[0]
        if lang in languages:
            return HttpResponseRedirect("/%s/" % lang)
    return HttpResponseRedirect("/en/")

def feed(request, lang):
    translation.activate(lang)
    lang = Language.objects.get(code=lang)
    object_list = PLSA.objects.filter(publish=True, language=lang)[:15]

    site = Site.objects.get_current()
    rss = Rss201rev2Feed(title=unicode(_("Pardus Linux Security Advisories")),
                         link="http://%s/%s/rss/" % (site.domain, lang.code),
                         description=unicode(_("Pardus Linux Security Advisories")),
                         language=lang.code)

    for adv in object_list:
        rss.add_item(title=adv.title,
                     link="http://%s/%s/%s/" % (site.domain, lang.code, adv.plsa_id),
                     description=adv.summary,
                     pubdate=adv.release_date,
                     unique_id=adv.plsa_id)

    return HttpResponse(rss.writeString("utf-8"))
