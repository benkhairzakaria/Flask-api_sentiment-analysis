from fastapi import FastAPI, HTTPException
from MLSentiment import sentimens_analysis_predict


app = FastAPI()

users = {
    'alice': 'wonderland',
    'bob': 'builder'
}


def authenticate_user(username, password):
    authenticated_user = False
    if username in users.keys():
        if users[username] == password:
            authenticated_user = True
    return authenticated_user



@app.get('/status')
async def return_status():
    '''
    returns 1 if the app is up
    '''
    return 1


@app.get('/permissions')
async def return_permission(username: str = 'username', password: str = 'password'):
    if authenticate_user(username=username, password=password):
        return {'username': username}
    else:
        raise HTTPException(status_code=403, detail='Authentication failed')


@app.get('/sentiment')
async def return_sentiment(username: str="username", password: str="password", sentence: str="sentence"):
    if not authenticate_user(username = username, password = password):
        raise HTTPException(status_code=403, detail='Authentication failed')
    
    pred = sentimens_analysis_predict(sentence)

    return {
        'username': username,
        'sentence': sentence,
        'class': pred.tolist()
    }

    

