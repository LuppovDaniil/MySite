from django.shortcuts import render
from django.core.cache import cache
from . import terms_work
import pandas as pd


def index(request):
    return render(request, "index.html")


def terms_list(request):
    terms = terms_work.get_terms_for_table()
    return render(request, "term_list.html", context={"terms": terms})


def add_term(request):
    return render(request, "term_add.html")


def send_term(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_term = request.POST.get("new_term", "")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "Описание должно быть не пустым"
        elif len(new_term) == 0:
            context["success"] = False
            context["comment"] = "Термин должен быть не пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваш термин принят"
            terms_work.write_term(new_term, new_definition)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "term_request.html", context)
    else:
        add_term(request)


def show_stats(request):
    stats = terms_work.get_terms_stats()
    return render(request, "stats.html", stats)


def show_review(request):
    return render(request, "review.html")


def send_review(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        grade = request.POST.get('grade')
        review = request.POST.get("review", "")
        reviews = pd.read_csv('./data/reviews.csv', sep=';')
        reviews.loc[len(reviews)] = [user_name, grade, review]
        print(len(reviews))
        #reviews = reviews.append({'user_name': user_name, 'grade': int(grade), 'review': review}, ignore_index=True)
        reviews.set_index('user_name').to_csv('./data/reviews.csv', sep=';')
    return render(request, "index.html")
