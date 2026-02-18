import requests
import json
API_KEY = #TMDB API_KEY NEEDED HERE
query = "15"
def getMovie():
    res = requests.get(f"https://api.themoviedb.org/3/movie/{query}",params={"api_key":API_KEY})
    print(res.status_code)
    if(res.status_code==200):
        file = open(file="text.txt",mode="w")
        file.write(json.dumps(res.json()))
        file.close()

getMovie()