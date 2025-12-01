from rest_framework import serializers

def validate_no_profanity(value):
    profane_words = ['spam', 'badword']
    if any( word in value.lower() for word in profane_words):
        raise serializers.ValidationError("Content containes inappropriate words")
    return value