from rest_framework import serializers

from polis.models import PolicyFile

class PolicyFileSerializer(serializers.ModelSerializer):
    class Meta:

        model = PolicyFile
        fields = ['id', 'name', 'file', 'file_hash']
        read_only_fields = ['file_hash']

    def create(self, validated_data):
        return super().create(validated_data)