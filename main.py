# -*- coding: utf-8 -*-

import webbrowser

import requests
import simplejson as json

from wox import Wox, WoxAPI


class Mojidict(Wox):

    def query(self, keyword):
        proxies = {}
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies = {
              "http": "http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
              "http": "https://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))
            }
            #self.debug(proxies)

        headers = {
            'origin': 'https://www.mojidict.com',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'content-type': 'text/plain',
            'accept': '*/*',
            'referer': 'https://www.mojidict.com/',
            'authority': 'www.mojidict.com',
        }

        data_form = {
            'searchText': keyword.encode('utf-8'),
            '_ApplicationId': "E62VyFVLMiW7kvbtVq3p",
            "_ClientVersion":"js2.4.0",
            "_InstallationId":"648c0a83-f303-ec2b-93d6-245aa9b95752"
        }

        data = json.dumps(data_form)

        response = requests.post('https://www.mojidict.com/parse/functions/search', headers=headers, data=data, proxies=proxies).json()

        search_results = response['result']['searchResults']
        words = response['result']['words']

        results = []
        for search_result in search_results:
            tar_id = search_result['tarId']
            for word in words:
                if word['identity'] == tar_id:
                    url = 'https://www.mojidict.com/details/{}'.format(tar_id)
                    results.append({
                        'Title': '{} | {}'.format(word['spell'], word['pron']),
                        'SubTitle': word['excerpt'],
                        'IcoPath': 'assets/moji.jpg',
                        'JsonRPCAction': {
                            "method": "openUrl",
                            "parameters":[url],
                            "dontHideAfterAction": False
                        }
                    })

        return results

    def openUrl(self,url):
        webbrowser.open(url)
        #todo:doesn't work when move this line up 
        WoxAPI.change_query(url)

if __name__ == '__main__':
    Mojidict()
