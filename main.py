import requests


def intelligent_superhero(url_api):
    dist_superhero = {}
    response = requests.get(url_api)
    if response.status_code == 200:
        superhero_specification = response.json()
        for superhero in superhero_specification:
            dist_superhero[superhero['name']] = superhero['powerstats']['intelligence']
    return dist_superhero


if __name__ == '__main__':

    # task 1
    url = 'https://akabab.github.io/superhero-api/api/all.json'
    dict_superhero = intelligent_superhero(url)
    list_superhero = {'Hulk', 'Captain America', 'Thanos'}
    max_intelligent = 0
    for name_superhero in list_superhero:
        if max_intelligent < dict_superhero[name_superhero]:
             max_intelligent = dict_superhero[name_superhero]
             cleverest_superhero = name_superhero
    print(cleverest_superhero + ' is the intelligent superhero')
