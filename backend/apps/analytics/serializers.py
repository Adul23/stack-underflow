from rest_framework import serializers


class TopQuestionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    title = serializers.CharField(source="question__title")
    slug = serializers.CharField(source="question__slug")
    views = serializers.IntegerField()


class SummarySerializer(serializers.Serializer):
    totals = serializers.DictField(child=serializers.IntegerField())
    top_questions = TopQuestionSerializer(many=True)
