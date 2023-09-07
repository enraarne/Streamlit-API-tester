import requests

def trines_get_tidID():
    """ Some explanation for the function """
    url      = "https://api.statistikkbanken.udir.no/api/rest/v2/Eksport/151/filterVerdier"
    response = requests.get(url)
    tidID = response.json()["TidID"][0]["kode"]
    return tidID
