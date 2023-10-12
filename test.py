import requests
import urllib.request 


# search something from google
def search_google(query):
    url = "https://www.google.com/search?q={}".format(query+' lang:tw,en')
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    text = response.text
    print(text[:100])
    # open('text.html', 'w').write(text)
    text = text[text.find('id="search"'):]
    text = text[text.find('<a jsname', 2):]
    text = text[text.find('href')+6:]
    text = text[:text.find('"')]
    
    if 'http' not in text:
        return '抱歉我盡力了，我找不到相關資訊耶'
    elif 'porn' in text:
        return '抱歉我盡力了，我找不到相關資訊耶'
    elif 'xvideo' in text:
        return '抱歉我盡力了，我找不到相關資訊耶'


    return text


print(search_google('cnn neural network'))