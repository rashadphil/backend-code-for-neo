from posts.models.poll import Poll, PollChoice
from rest_framework import serializers


class PollChoiceSerializer(serializers.ModelSerializer):
    vote_count = serializers.SerializerMethodField(read_only=True)

    def get_vote_count(self, obj) -> int:
        return obj.votes

    class Meta:
        model = PollChoice
        fields = ("id", "body", "vote_count")


class PollSerializer(serializers.ModelSerializer):
    options = PollChoiceSerializer(many=True, source="pollchoice_set")

    class Meta:
        model = Poll
        fields = (
            "id",
            "options",
        )


class PollReadSerializer(PollSerializer):
    total_votes = serializers.SerializerMethodField()
    options = PollChoiceSerializer(many=True, source="pollchoice_set")
    user_selection = serializers.SerializerMethodField()

    def get_total_votes(self, obj) -> int:
        return obj.votes

    def get_user_selection(self, obj) -> int:
        if not hasattr(obj, "user_poll_selections"):
            return None
        user_selection = (
            obj.user_poll_selections[0].id if obj.user_poll_selections else None
        )
        return user_selection

    class Meta:
        model = Poll
        fields = (
            "id",
            "created_at",
            "ends_at",
            "total_votes",
            "user_selection",
            "options",
        )


class PollCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = (
            "id",
            "ends_at",
            "options",
        )

    def create(self, validated_data):
        options = validated_data.pop("options")
        poll = Poll.objects.create(**validated_data)
        for option in options:
            PollChoice.objects.create(poll=poll, **option)
        return poll
