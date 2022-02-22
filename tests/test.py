import requests

def simulate(mes, user):
    '''
        Simulaion d'envoie des données
    '''
    data_json = {
        "object": "page",
        "entry": [
            {
                "messaging": [
                    {
                        "message":
                            {
                                "text": mes,
                            },
                        "sender":
                            {
                                "id": user
                            }
                    }
                ]
            }
        ]
    }
    header = {'content-type': 'application/json; charset=utf-8'}
    return requests.post(
        'http://127.0.0.1:4555',
        json=data_json,
        headers=header,
        params={"TEST": '1'}
    )


simulate("Gaetan", "155454")