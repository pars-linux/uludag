from security.advisory.models import Advisory, Language
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import translation
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.feedgenerator import Rss201rev2Feed
from django.contrib.sites.models import Site

def advisory_details(request, lang_code, plsa_id):
    translation.activate(lang_code)
    other_languages = Language.objects.exclude(code=lang_code)
    advisory = get_object_or_404(Advisory, publish=True, language__code=lang_code, plsa_id=plsa_id)
    years = [x.year for x in Advisory.objects.dates("release_date", "year")]

    return render_to_response("advisory/advisory_details.html", {"advisory": advisory,
                                                                 "language": lang_code,
                                                                 "years": years,
                                                                 "other_languages": other_languages})

def advisory_text(request, lang_code, plsa_id):
    translation.activate(lang_code)
    advisory = get_object_or_404(Advisory, language__code=lang_code, plsa_id=plsa_id)

    return render_to_response("advisory/advisory_text.html", {"advisory": advisory})

def archive_year(request, lang_code, year):
    translation.activate(lang_code)
    other_languages = Language.objects.exclude(code=lang_code)
    advisories = [x for x in Advisory.objects.filter(publish=True, language__code=lang_code) if x.release_date.year == int(year)]
    years = [x.year for x in Advisory.objects.dates("release_date", "year")]

    return render_to_response("advisory/archive_year.html", {"advisories": advisories,
                                                             "year": year,
                                                             "language": lang_code,
                                                             "years": years,
                                                             "other_languages": other_languages})

def index_language(request, lang_code):
    translation.activate(lang_code)
    advisories = Advisory.objects.filter(publish=True, language__code=lang_code)[:10]
    years = [x.year for x in Advisory.objects.dates("release_date", "year")]
    other_languages = Language.objects.exclude(code=lang_code)

    return render_to_response("advisory/index_language.html", {"advisories": advisories,
                                                               "language": lang_code,
                                                               "years": years,
                                                               "other_languages": other_languages})

def index(request):
    """
    languages = [x.code for x in Language.objects.all()]
    for lang in request.META["HTTP_ACCEPT_LANGUAGE"].split(","):
        lang = lang.split("-")[0]
        if lang in languages:
            return HttpResponseRedirect("/%s/" % lang)
    """
    return HttpResponseRedirect("/en/")

def feed(request, lang_code):
    translation.activate(lang_code)
    advisories = Advisory.objects.filter(publish=True, language__code=lang_code)[:25]
    site = Site.objects.get_current()

    rss = Rss201rev2Feed(title=unicode(_("Pardus Linux Security Advisories")),
                         link="http://%s/%s/rss/" % (site.domain, lang_code),
                         description=unicode(_("Pardus Linux Security Advisories")),
                         language=lang_code)

    for adv in advisories:
        rss.add_item(title="[PLSA %s] %s" % (adv.plsa_id, adv.title),
                     link="http://%s/%s/%s/" % (site.domain, lang_code, adv.plsa_id),
                     description=adv.summary,
                     pubdate=adv.release_date,
                     unique_id=adv.plsa_id)

    return HttpResponse(rss.writeString("utf-8"))
