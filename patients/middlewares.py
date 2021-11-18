from .models import Patient
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User


class SetOrGetPatientMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not any(request.path.startswith(url) for url in settings.NO_PATIENT_REQUIRED_URLS):
            p_code = request.headers.get('p-code')
            user_token = request.headers.get('Authorization')
            if p_code:
                if user_token:
                    user_token = user_token[6:]
                    user_qs = User.objects.filter(auth_token__key=user_token)
                    if user_qs:
                        user = user_qs.get()
                    else:
                        return JsonResponse({'message': 'invalid token'}, status=403)
                else:
                    return JsonResponse({'message': 'authentication credentials not provided'}, status=403)
                query_set = Patient.objects.filter(code=int(p_code), user=user)
                if query_set:
                    request.patient = query_set.get()
                else:
                    return JsonResponse({'message': 'invalid patient code'}, status=403)
            else:
                return JsonResponse({'message': 'patient code not provided'}, status=403)

        response = self.get_response(request)
        return response
