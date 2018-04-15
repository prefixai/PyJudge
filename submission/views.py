from datetime import datetime

from VirtualJudgeSpider import Config
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from submission.models import Submission
from submission.serializers import SubmissionListSerializer, VerdictSerializer, SubmissionSerializer
from submission.tasks import submit_task
from utils.response import res_format, Message


class VerdictAPI(APIView):
    def post(self, request, submission_id, *args, **kwargs):
        try:
            submission = Submission.objects.get(id=submission_id)
            return Response(res_format(VerdictSerializer(submission).data), status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(res_format('submission not exist', status=Message.ERROR),
                            status=status.HTTP_400_BAD_REQUEST)


class SubmissionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        last_submit_time = request.session.get('last_submit_time', None)
        if last_submit_time and (datetime.now() - datetime.fromtimestamp(last_submit_time)).seconds < 5:
            return Response(res_format("Cannot be resubmitted within five seconds", status=Message.ERROR),
                            status=status.HTTP_400_BAD_REQUEST)
        request.session['last_submit_time'] = datetime.now().timestamp()

        serializer = SubmissionSerializer(data=request.data)
        if serializer.is_valid():
            submission = serializer.save(str(request.user))
            if submission is not None:
                submit_task.delay(submission.id)
                return Response(res_format(submission.id), status=status.HTTP_200_OK)
            return Response(res_format('submit error', status=Message.ERROR), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(res_format(serializer.errors, status=Message.ERROR), status=status.HTTP_400_BAD_REQUEST)


class SubmissionListAPI(APIView):
    def post(self, request, *args, **kwargs):
        try:
            submissions = Submission.objects.filter(contest_id=None).order_by('-create_time')[:100]
            return Response(res_format(SubmissionListSerializer(submissions, many=True).data),
                            status=status.HTTP_200_OK)
        except DatabaseError:
            return Response(res_format('System error', status=Message.ERROR),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReJudgeAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, submission_id, *args, **kwargs):
        try:
            submission = Submission.objects.get(id=submission_id)
            if submission.status in {Config.Result.Status.STATUS_NO_ACCOUNT.value,
                                     Config.Result.Status.STATUS_NETWORK_ERROR.value}:
                submission.status = Config.Result.Status.STATUS_PENDING.value
                submission.save()
                submit_task.delay(submission_id)
                return Response(res_format('rejudge submit success'), status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(res_format('System error', status=Message.ERROR),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except DatabaseError:
            return Response(res_format('rejudge failed', status=Message.ERROR), status=status.HTTP_400_BAD_REQUEST)
