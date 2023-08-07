"""This is an automation program which was used to download all the icons for the app.
Many of the images are unused as the icons are from a different website and the API is different"""
import requests

img_urls = []
for i in range(1, 45):
    if i < 10:
        img_urls.append(f"https://developer.accuweather.com/sites/default/files/0{i}-s.png")
    else:
        img_urls.append(f"https://developer.accuweather.com/sites/default/files/{i}-s.png")

    try:
        res = requests.get(img_urls[i-1])
    except FileNotFoundError:
        continue
    else:
        if i < 10:
            with open(f"./Icons/0{i}-s.png", "wb") as file:
                file.write(res.content)
        else:
            with open(f"./Icons/{i}-s.png", "wb") as file:
                file.write(res.content)
