import os
import requests


# définition de l'adresse de l'API
api_address = os.environ.get('ip_address')
# port de l'API
api_port = 8000

sentences = ['life is beautiful', 'that sucks']


for sentence in sentences:
    r = requests.get(
        url='http://{address}:{port}/sentiment'.format(address=api_address, port=api_port),
        params= {
            'username': 'alice',
            'password': 'wonderland',
            'sentence': sentence
        }
    )


    output = '''
        ============================
            Content test
        ============================

        request done at "/sentiment" 
        | username="Alice"
        | sentence={sentence}
        | classz: {classe} (0 négative et 1 positive)

        expected result = 200
        actual restult = {status_code}

        ==>  {test_status}


        '''

    # statut de la requête
    status_code = r.status_code

    # affichage des résultats
    if status_code == 200:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'
        
    # resultat de le rêquette
    data = r.json()

    print(output.format(status_code=status_code, test_status=test_status,sentence=sentence, classe=data['class']))


    # impression dans un fichier
    if os.environ.get('LOG') == "1":
        with open('api_test.log', 'a') as file:
            file.write(output.format(status_code=status_code, test_status=test_status,sentence=sentence, classe=data['class']))