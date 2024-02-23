from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render

# Create your views here.
from HumanEvaluationFramework.components.MediaService import MediaService
from HumanEvaluationFramework.components.SessionManager import SessionManager
import json, os, statistics

def vue_app(request):
    # for maintanence:
    # return render(request, 'maintenance.html')

    # for normal state:
    return render(request, 'index.html')

def init(request):
    if 'sessionManager' in request.session:
        del request.session['sessionManager']
    if 'mediaService' in request.session:
        del request.session['mediaService']

    return HttpResponse('')


def login(request):
    name = request.GET.get('name')
    sm = SessionManager(name=name)
    return JsonResponse({'result': sm.query_previous_session()})


def list_datasets(request):
    ms = MediaService()
    return JsonResponse({'datasets': ms.get_datasets()})


def start_new_session(request):
    name = request.GET.get('name')
    sm = SessionManager(name=name)
    sm.register_new_session(request.GET.get('dataset'))

    ms = MediaService()
    samples = ms.select_dataset(request.GET.get('dataset'), int(request.GET.get('sampleSize')))
    sm.start_progress(samples)

    empty, _, full_path = ms.next_sample()
    ms.save()

    return JsonResponse({
        'session_1': sm.session.id,
        'session_2': ms.state.id,
        'isEmpty': empty,
        'nextSample': full_path,
        'current_count': 0,
        'all_count': len(ms.queue) + 1
    })


def load_previous_session(request):
    name = request.GET.get('name')
    sm = SessionManager(name=name)
    sm.set_previous_session()
    samples = sm.get_remaining_samples()

    ms = MediaService()
    ms.load_dataset(sm.dataset, samples)
    empty, _, full_path = ms.next_sample()
    ms.save()

    return JsonResponse({
        'session_1': sm.session.id,
        'session_2': ms.state.id,
        'isEmpty': empty,
        'dataset': sm.dataset,
        'nextSample': full_path,
        'current_count': sm.get_evaluated_count(),
        'all_count': len(ms.queue) + 1 + sm.get_evaluated_count()
    })


def enter_choice(request):
    sm = SessionManager(session_id=request.GET.get('session_1'))
    ms = MediaService(state_id=request.GET.get('session_2'))

    empty, evaluated_sample, full_path = ms.next_sample()
    # player_position, playcount, audio_length
    sm.enter_choice(
        evaluated_sample,
        request.GET.get('result'),
        request.GET.get('difficulty'),
        request.GET.get('time'),
        request.GET.get('player_position'),
        request.GET.get('playcount'),
        request.GET.get('audio_length'))
    ms.save()

    return JsonResponse({
        'isEmpty': empty,
        'nextSample': full_path
    })


def finalize(request):
    sm = SessionManager(session_id=request.GET.get('session_1'))
    acc, sum_time = sm.finalize_session()

    return JsonResponse({
        'accuracy': acc,
        'time': sum_time
    })


def results(request):
    if request.GET.get('v') is not None:
        version = int(request.GET.get('v'))
    else:
        version = False
    folder = 'results/' if not version else f'results/v{version}/'

    jsons = [name for name in os.listdir(folder) if (os.path.isfile(os.path.join(folder, name)) and name.endswith('.json'))]
    results = []
    all_accuracies = []

    for jsonf in jsons:
        with open(f'{folder}{jsonf}', 'r') as f:
            data = json.load(f)
            accuracy, all_time = 0, 0
            for item in data:
                if item["fields"]["result"] == item["fields"]["ground_truth"]:
                    accuracy += 1
                if not version or version > 1:
                    all_time += item["fields"]["time_taken"]

            accuracy /= len(data)
            all_accuracies.append(accuracy)

            results.append({'name': jsonf.split('_')[0], 'accuracy': accuracy, 'time': all_time, 'size': len(data)})

    stats = {
        'min_accuracy': min(all_accuracies),
        'max_accuracy': max(all_accuracies),
        'avg_accuracy': sum(all_accuracies) / len(all_accuracies),
        'median_accuracy': statistics.median(all_accuracies)
    }

    return render(request, 'results.html', context={'results': results, 'stats': stats})
