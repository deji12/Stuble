from django.shortcuts import render
from .books import books
from .bible_versions import versions
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings

API_BIBLE_BASE_URL = "https://rest.api.bible/v1"

def home(request):

    return render(request, 'home.html')

def bible(request):

    context = {
        "books": books,
        "bible_versions": versions
    }
    return render(request, "bible.html", context)

@require_GET
def get_chapter_passage(request):
    bible_id = request.GET.get("bibleId")
    chapter_id = request.GET.get("chapterId")
    verse_id = request.GET.get("verseId")

    if not bible_id or not chapter_id:
        return JsonResponse(
            {"error": "bibleId and chapterId are required"},
            status=400
        )

    if not verse_id:
        url = f"{API_BIBLE_BASE_URL}/bibles/{bible_id}/passages/{chapter_id}"
    else:
        url = f"{API_BIBLE_BASE_URL}/bibles/{bible_id}/verses/{chapter_id}.{verse_id}"

    headers = {
        "api-key": settings.API_BIBLE_KEY    
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)

        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        return JsonResponse(
            {
                "error": "Failed to fetch passage",
                "detail": str(e),
            },
            status=502
        )

    return JsonResponse(response.json(), safe=False)
