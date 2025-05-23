import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class YouTubeSearchView(APIView):
    def get(self, request):
        q = request.query_params.get("q", "")
        max_results = request.query_params.get("maxResults", 15)
        if not q:
            return Response(
                {"error": "q 파라미터가 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        params = {
            "part": "snippet",
            "q": q,
            "type": "video",
            "maxResults": max_results,
            "key": settings.YOUTUBE_API_KEY,
        }
        try:
            r = requests.get(
                "https://www.googleapis.com/youtube/v3/search", params=params, timeout=5
            )
            r.raise_for_status()
        except requests.RequestException as e:
            return Response(
                {"error": "YouTube API 호출 실패", "detail": str(e)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(r.json())


class YouTubeVideoDetailView(APIView):
    def get(self, request):
        vid = request.query_params.get("id")
        if not vid:
            return Response(
                {"error": "id 파라미터가 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        params = {
            "part": "snippet,contentDetails,statistics",
            "id": vid,
            "key": settings.YOUTUBE_API_KEY,
        }
        try:
            r = requests.get(
                "https://www.googleapis.com/youtube/v3/videos", params=params, timeout=5
            )
            r.raise_for_status()
        except requests.RequestException as e:
            return Response(
                {"error": "YouTube API 호출 실패", "detail": str(e)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(r.json())


class YouTubeChannelDetailView(APIView):
    def get(self, request):
        ids = request.query_params.get("id", "")
        if not ids:
            return Response(
                {"error": "id 파라미터가 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        params = {
            "part": "snippet",
            "id": ids,
            "key": settings.YOUTUBE_API_KEY,
        }
        try:
            r = requests.get(
                "https://www.googleapis.com/youtube/v3/channels",
                params=params,
                timeout=5,
            )
            r.raise_for_status()
        except requests.RequestException as e:
            return Response(
                {"error": "YouTube API 호출 실패", "detail": str(e)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(r.json())
