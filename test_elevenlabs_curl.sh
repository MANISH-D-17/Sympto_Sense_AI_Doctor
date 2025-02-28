API_KEY="sk_000446a51d6878455ed82f7e927731060ead838c7d7f3fcf"  

curl -X GET "https://api.elevenlabs.io/v1/voices?show_legacy=true" \
-H "Authorization: Bearer $API_KEY"
