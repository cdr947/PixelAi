# from django.conf import settings
# from django.shortcuts import render
# from pathlib import Path

# from .inference import run_inference


# def _parse_threshold(threshold_str, default=0.5):
#     try:
#         threshold = float(threshold_str)
#         if 0 <= threshold <= 1:
#             return threshold
#     except (ValueError, TypeError):
#         return default  # Return default threshold if parsing fails
#     return max(0.0, min(threshold, 1.0))  # Ensure threshold is within [0, 1]

# def upload_view(request):
#     if request.method == 'POST':
#         uploaded_file = request.FILES.get('image')
#         threshold_str = request.POST.get('threshold', '0.5')
#         threshold = _parse_threshold(threshold_str)

#         if uploaded_file:
#             input_path = Path(settings.MEDIA_ROOT) / uploaded_file.name
#             output_path = Path(settings.MEDIA_ROOT) / 'output'
#             output_path.mkdir(parents=True, exist_ok=True)

#             with open(input_path, 'wb+') as destination:
#                 for chunk in uploaded_file.chunks():
#                     destination.write(chunk)

#             # Run inference on the uploaded file
#             inference_results = run_inference(str(input_path), str(output_path), threshold)

#             # Save the inference results to the database
#             result_entry = {
#                 'file_name': uploaded_file.name,
#                 'threshold': threshold,
#                 'results': inference_results
#             }

#             request.session['latest_inference_result'] = result_entry

#             return render(request, 'upload.html', {
#                 'inference_results': inference_results,
#                 'file_name': uploaded_file.name,
#                 'threshold': threshold
#             })

#     return render(request, 'upload.html')

# def results_view(request, pk):
#     result_entry = request.session.get('latest_inference_result')

#     if not result_entry:
#         return render(request, 'result.html', {
#             'error': 'Result not found.',
#             'pk': pk,
#         })

#     return render(request, 'result.html', {
#         'instance': {
#             'file_name': result_entry.get('file_name'),
#             'threshold': result_entry.get('threshold'),
#             'result': result_entry.get('results', {}),
#         },
#         'pk': pk,
#     })


from django.shortcuts import render,get_object_or_404, redirect
from django.conf import settings
from pathlib import Path
from .inference import run_inference
from .models import ImageUpload

def _parse_threshold(threshold_str, default=0.5):
    try:
        threshold = float(threshold_str)
        if 0 <= threshold <= 1:
            return threshold
    except (ValueError, TypeError):
        return default  # Return default threshold if parsing fails
    return max(0.0, min(threshold, 1.0))  # Ensure threshold is within [0, 1]


def upload_view(request):
    if request.method == 'POST' :
        f = request.FILES.get('image')
        if f :
            inst = ImageUpload.objects.create(image=f)
            original_path = Path(settings.MEDIA_ROOT) / inst.image.name
            output_path = Path(settings.MEDIA_ROOT) / f'predicted/{inst.id}'
            threshold = _parse_threshold(request.POST.get('threshold', '0.5'))
            predicted_path = output_path / Path(inst.image.name).name

            result = run_inference(
                str(original_path),
                str(output_path),
                threshold
            )

            if predicted_path.exists():
                inst.predicted.name = str(predicted_path.relative_to(settings.MEDIA_ROOT))
            else:
                inst.predicted = None

            inst.results = result
            inst.save()
            return redirect('webapp:results', pk=inst.id, )
    recent_images = ImageUpload.objects.all().order_by('-created_at')[:10]
    return render(request, 'upload.html', {'recent_images': recent_images})

def results_view(request, pk):
    inst = get_object_or_404(ImageUpload, pk=pk)
    return render(request, 'results.html', {'instance': inst},)



def current_models_view(request):
    return render(request, 'current_models.html')

def api_view(request):
    return render(request, 'api.html')

def about_view(request):
    return render(request, 'about.html')

