import requests
from pprint import pprint
import datetime


def intelligent_superhero(url_api):
    dist_superhero = {}
    response = requests.get(url_api)
    if response.status_code == 200:
        superhero_specification = response.json()
        for superhero in superhero_specification:
            dist_superhero[superhero['name']] = superhero['powerstats']['intelligence']
    return dist_superhero


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def get_files_list(self):
        url_files_list = 'https://cloud-api.yandex.net:443/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(url_files_list, headers=headers)
        return response.json()

    def _get_upload_link(self, disk_file_path):
        url_upload = 'https://cloud-api.yandex.net:443/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(url_upload, headers=headers, params=params)
        pprint(response.json())
        return response.json()

    def upload(self, disk_file_path, file_local):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        href_upload = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href_upload, data=open(file_local, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print('Success!')


def questions_for_two_days(url_api, tagged):
    # получаем данные за 2 предыдущих дня
    delta_day = datetime.timedelta(2)
    today = datetime.datetime.now()
    day_before_yesterday = today - delta_day
    todate = str(int(today.timestamp()))
    fromdate = str(int(day_before_yesterday.timestamp()))

    headers = {'Content-Type': 'application/json'}
    params = {"fromdate": fromdate, "todate": todate, "order": "asc",
              "sort": "activity", "tagged": tagged, "site": "stackoverflow"}
    response_api = requests.get(url_api, headers=headers, params=params)
    pprint(response_api.json())


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

    # task 2
    file_local = 'result.txt'
    TOKEN = ''
    uploader = YaUploader(TOKEN)
    uploader.upload("/result.txt", file_local)

    # task 3
    url_api = 'https://api.stackexchange.com/2.3/questions'
    tag_api = 'Python'
    questions_for_two_days(url_api, tag_api)
