from django.shortcuts import render

import requests as req
import json


def search_food_post(request):
    respons = req.get('https://api.nal.usda.gov/fdc/v1/foods/search?api_key=EVuhK3UbNku53YdTuw044oAUBsIJF0fGDpRhwKhG&query={0}'.format(request.POST.get('data')))
    data = json.loads(respons.text)
    answer = []
    for item in data['foods']:
        answer.append({'name': item['description']})
        for info in item['foodNutrients']:
            if info["nutrientNumber"] == '205':
                answer[-1]['carbohydrate'] = info['value']
            if info["nutrientNumber"] == '208':
                answer[-1]['energy'] = info['value']
            if info["nutrientNumber"] == '204':
                answer[-1]['fat'] = info['value']
            if info["nutrientNumber"] == '203':
                answer[-1]['protein'] = info['value']
    return render(request, "search_food.html", context={'answer': answer[:10]})


def calculator_post(request):
    if request.POST.get('male') == "on":
        BMR = 88.362 + 13.397 * int(request.POST.get('weight')) + 4.799 * int(request.POST.get('height')) - 5.677 * int(request.POST.get('age'))
    elif request.POST.get('female') == "on":
        BMR = 447.593 + 9.247 * int(request.POST.get('weight')) + 3.098 * int(request.POST.get('height')) - 4.330 * int(request.POST.get('age'))

    if request.POST.get('activ') == 'Сидячий образ жизни':
        AMR = 1.2
    elif request.POST.get('activ') == 'Умеренная активность (легкие физические нагрузки либо занятия 1-3 раз в неделю)':
        AMR = 1.375
    elif request.POST.get('activ') == 'Средняя активность (занятия 3-5 раз в неделю)':
        AMR = 1.55
    elif request.POST.get('activ') == 'Активные люди (интенсивные нагрузки, занятия 6-7 раз в неделю)':
        AMR = 1.725
    elif request.POST.get('activ') == 'Спортсмены и люди, выполняющие сходные нагрузки (6-7 раз в неделю)':
        AMR = 1.9

    energy = int(BMR * AMR)
    protein = int(energy * 0.3 / 4)
    fat = int(energy * 0.1 / 9)
    carbohydrate = int(energy * 0.6 / 4)

    return render(request, "calculator.html", context={'energy':energy, 'protein':protein, 'fat':fat, 'carbohydrate':carbohydrate})