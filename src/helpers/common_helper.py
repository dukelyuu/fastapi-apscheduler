from typing import Tuple


class  CommonHelper():
    @staticmethod
    def get_url(base_url:str,endpoint:str) ->str:
        url = None
        if base_url and not base_url.endswith('/') and endpoint and not endpoint.startswith('/'):
            url = base_url + '/' + endpoint
        else:
            url = (base_url or '') + (endpoint or '')
        return url
    @staticmethod
    def convert_cronstr_to_params(cron_str:str):
        tmp = cron_str.split(" ")
        FIELD_NAMES = ( 'year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second')
        res = []
        index_val = len(FIELD_NAMES) -1
        for v in FIELD_NAMES:
            if v == 'year':
                res.append('*')
                # print('year')
            else:
                res.append(tmp[index_val])
                # res[v] = tmp[index_val]
            index_val = index_val - 1
        return res
    @staticmethod
    def base64_encode(in_str:str):
        from pybase64 import b64encode_as_string
        res = b64encode_as_string(in_str)
        return res
    @staticmethod
    def base64_decode(in_str:str):
        from pybase64 import b64decode
        res = b64decode(in_str)
        return res
    
    