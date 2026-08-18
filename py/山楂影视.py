# -*- coding: utf-8 -*-
# by @嗷呜
import json
import random
import sys
import base64
from base64 import b64encode, b64decode
from concurrent.futures import ThreadPoolExecutor, TimeoutError

try:
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5
except ImportError:
    raise RuntimeError("请安装依赖: pip install pycryptodome")

sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    def init(self, extend=""):
        try:
            did = self.getdid()
            self.headers.update({'deviceId': did})
            token = self.gettk()
            if token:
                self.headers.update({'token': token})
        except Exception as e:
            print(f"init初始化异常:{e}")

    def getName(self):
        return "趣看影视"

    def isVideoFormat(self, url):
        return False

    def manualVideoCheck(self):
        return False

    def destroy(self):
        pass

    host = 'http://qkys.qukanwh.com'
    headers = {
        'Host': 'qkys.qukanwh.com',
        'User-Agent': 'okhttp/4.12.0',
        'client': 'app',
        'deviceType': 'Android',
        'Referer': ''
    }

    publicKey_str = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCoYt0BP77U+DM08BiI/QbSRIfxijXo85BTPqIM1Ow8BNwhLETzRIZ+dEwdWDbydG/PspgBAfRpGaYVdJYtvaC2JnoO8+Ik6qMWojfEJxSFLa0Pb0A892tun4gsxoEMjcreZ+YGyaBxAfqX0BSMfdrOgIYaZQjYrw9TRLlUT31QoQIDAQAB
-----END PUBLIC KEY-----"""

    privateKey_str = """-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCquQQ5r6+yJI8CDFkXRp8vUsdD45ov8EP12ooLs56ca2DQXaSNGS9910bAPVA9chkp0mKIvKqjAsHz5Tl9EeNPblarGEeJUIxpxZtiSqNTpvtiD/TjhpzuHYic7RAfQ/h7p/ypE8ymU42pYjsB5t26Mv6XgkLV+jzrSf73HlCuS0iMyLmt6zz3Mw9izM13EpB8iFLtfbbYymycKTx4RAmPQLwhNGex/AlUIYxXP4R2yyaa4W6mEtc6aME2QuzJFxPgP3HJ9NBx/LWVn4skxWjZ7zg+VRQRHnjyVaSLu3Z5gN5ITWCyE32qaHJa6WBahZj5jWhRyAG1bQ+xKJa8lBL5AgMBAAECggEAUwv9SjJ0PSwbhNuM2w23kcWquROWhYtTA91zGY4esehqB/IFgb2mpIh8Gje5OKqwIu/8jpd4SiOlRYdUF8sD0DfUYRZGdj2AkFNX6tBz8tVfo6wvbB6naA1lzzBij1L5JO3qsjS3cJFkb+kg2yP66AC2Z+0tpfk8eRhdtshAZwfcd1DEGt1uAvYL1eaUK9HRvpt9lPeGcHERDl2hBd4uyaF0K1O+zF9y59nYbTySWPxRZq3sFEE85xRMlstD7YZi7W2gKvMFRD4/FKmrZ3m7aKJRITtyKOyyPcYmepNv3Qv7kk59Pg38n2WWQ0Ra/bCH3E48YNCnQvZMpitkTfJhoQKBgQDbnROOYTP8OTJ6f/qhoGjxeO3x1VOaOp8l0x7b0SCfoqNGS0Cyiqj72BmJtPMPqSTjn6MmNzqbg1KOdhXyzNozs+i5ccW1M56j96mr5I/Z0FpE3oyIHNfDDBlf9M8YQqEF9oYxniYYft9oapO7cRQkHER6qpvnHTavwlv4m78CXwKBgQDHAjs2YlpKDdI1lcbZJCc7TwtH+Pd2bUki8YXafWNcPhITQHbOZjr310eK1QJC6GJncjkOqbX7yv3ivvTO35FZTQhuA1xEG1P00FG8bE0tHYPIwQHi9y0eA5cieMdo8E6XYria1mw/3fqSQEsfZyJlR32JQIoGAipM8iO1X2nZpwKBgDkMFIhnt5lNQk+P7wsNIDWZtDWdtJnboHuy29E+Abt2A/O+mI/IdRz2hau/1WO8DFkUnszOi+rZshhPlGP90rCbi1igtTrcrdjp/KkqNjPea5R4OwkgdOu1uOG0NheXNzzVTQaWjk7Opjn5dWa7eP/oV+GFb/oZHJuLYVizHGsBAoGADA7rjZEKDYCm4w5PPSr+oY5ZjaPdQrS+gLqHtMRyN82fBMGcMUdqfUfzEstzVqCEDeaS5HuOBlK3bXzKkppjUTjksN3NQmcxgBz7RuJ9DqXCLXDcb2cwuafYCYOt+YLOEEgwDVm+t2P44dG5e46hO+fICH/7nP+WlpD5buz4GfMCgYB57r3g/6hi9WUDnfc7ZAzWMqR0EhJVYKYy+KFEtdIPzhkkIHq5RASe88E9kzoGoZFdb3tIjvGZWcHerirrqWkMsuQtP/Qi0zjieid5tAPj+r4kbiCVTw0E0jnmPBzGInQi7lpeTTKnG1fbyS5lBS+WmHfIuzpECgCkxhaT+LJJkg==
-----END PRIVATE KEY-----"""

    def rsa_encrypt(self, text):
        try:
            key = RSA.import_key(self.publicKey_str)
            cipher = PKCS1_v1_5.new(key)
            cipher_text = cipher.encrypt(text.encode('utf-8'))
            return b64encode(cipher_text).decode('utf-8')
        except Exception as e:
            print(f"RSA加密失败: {e}")
            return ""

    def rsa_decrypt(self, text):
        try:
            from Crypto import Random
            key = RSA.import_key(self.privateKey_str)
            cipher = PKCS1_v1_5.new(key)
            raw_bytes = b64decode(text.encode('utf-8'))
            sentinel = Random.new().read(256)
            decrypted = b""
            offset = 0
            step = key.size_in_bytes()
            while offset < len(raw_bytes):
                chunk = raw_bytes[offset:offset + step]
                part = cipher.decrypt(chunk, sentinel)
                if part == sentinel:
                    return ""
                decrypted += part
                offset += step
            return decrypted.decode('utf-8')
        except Exception as e:
            print(f"RSA解密失败: {e}")
            return ""

    def homeContent(self, filter):
        result = {}
        try:
            resp = self.post(f"{self.host}/api/v1/app/screen/screenType", headers=self.headers)
            data = resp.json()
        except Exception as e:
            print(f"首页分类请求异常:{e}")
            return {"class":[], "filters":{}}

        cate = {
            "类型": "type",
            "地区": "area",
            "年份": "year"
        }
        sort = {
            'key': 'sort',
            'name': '排序',
            'value': [{'n': '最新', 'v': 'NEWEST'}, {'n': '热门', 'v': 'HOT'}, {'n': '收藏', 'v': 'COLLECT'}]
        }
        classes = []
        filters = {}
        for k in data.get('data', []):
            tid = str(k.get('id',''))
            if not tid:
                continue
            classes.append({
                'type_name': k.get('name',''),
                'type_id': tid
            })
            filters[tid] = []
            for v in k.get('children', []):
                if v.get('name') in cate:
                    filters[tid].append({
                        'name': v['name'],
                        'key': cate[v['name']],
                        'value': [{'n': i.get('name',''), 'v': i.get('name','')} for i in v.get('children', []) if i.get('name')]
                    })
            filters[tid].append(sort)
        result['class'] = classes
        result['filters'] = filters
        return result

    def homeVideoContent(self):
        jdata = {
            "condition": {
                "sreecnTypeEnum": "NEWEST"
            },
            "pageNum": 1,
            "pageSize": 40
        }
        try:
            data = self.post(f"{self.host}/api/v1/app/screen/screenMovie", headers=self.headers, json=jdata).json()
            records = data.get('data', {}).get('records', [])
        except Exception as e:
            print(f"首页内容异常:{e}")
            records = []
        return {'list': self.getlist(records)}

    def categoryContent(self, tid, pg, filter, extend):
        condition = {
            'sreecnTypeEnum': 'NEWEST',
            'typeId': int(tid) if str(tid).isdigit() else tid
        }
        if extend:
            if 'sort' in extend:
                condition['sreecnTypeEnum'] = extend.pop('sort')
            condition.update(extend)
        jdata = {
            'condition': condition,
            'pageNum': int(pg),
            'pageSize': 40,
        }
        try:
            data = self.post(f"{self.host}/api/v1/app/screen/screenMovie", headers=self.headers, json=jdata).json()
            records = data.get('data', {}).get('records', [])
            res_list = self.getlist(records)
        except Exception as e:
            print(f"分类获取错误: {e}")
            res_list = []
        result = {
            'list': res_list,
            'page': int(pg),
            'pagecount': 9999,
            'limit': 40,
            'total': 999999
        }
        return result

    def detailContent(self, ids):
        vod = {
            'type_name': '',
            'vod_year': '',
            'vod_area': '',
            'vod_actor': '',
            'vod_director': '',
            'vod_content': '',
            'vod_play_from': '',
            'vod_play_url': ''
        }
        try:
            ids = ids[0].split('@@')
            mid = int(ids[0])
            tid = ids[-1]
            jdata = {"id": mid, "typeId": tid}
            v = self.post(f"{self.host}/api/v1/app/play/movieDesc", headers=self.headers, json=jdata).json()
            v = v.get('data', {})
            vod['type_name'] = v.get('typeName', '')
            vod['vod_year'] = v.get('year', '')
            vod['vod_area'] = v.get('area', '')
            vod['vod_actor'] = v.get('star', '')
            vod['vod_director'] = v.get('director', '')
            vod['vod_content'] = v.get('introduce', '')

            play_params = {"id": mid, "source": 0, "typeId": tid}
            encrypt_payload = {"key": self.rsa_encrypt(json.dumps(play_params))}
            c_res = self.post(f"{self.host}/api/v1/app/play/movieDetails", headers=self.headers, json=encrypt_payload).json()
            decrypted_play_str = self.rsa_decrypt(c_res.get('data', ''))
            if not decrypted_play_str:
                return {'list': [vod]}
            decrypted_play_data = json.loads(decrypted_play_str)
            l = decrypted_play_data.get('moviePlayerList', [])
            if not l:
                return {'list': [vod]}
            n = {str(i['id']): i.get('moviePlayerName','未知线路') for i in l}
            m = play_params.copy()
            m.update({'playerId': l[0]['id']})
            first_source_payload = {"key": self.rsa_encrypt(json.dumps(m))}
            first_res = self.post(f"{self.host}/api/v1/app/play/movieDetails", headers=self.headers, json=first_source_payload).json()
            decrypted_first_str = self.rsa_decrypt(first_res.get('data', ''))
            pd = {}
            if decrypted_first_str:
                decrypted_first_episode = json.loads(decrypted_first_str)
                pd = self.getv(m, decrypted_first_episode.get('episodeList', []))
            if len(l) > 1:
                with ThreadPoolExecutor(max_workers=min(4, len(l)-1)) as executor:
                    futures = []
                    for pl in l[1:]:
                        futures.append(executor.submit(self.getd, play_params, pl))
                    for fu in futures:
                        try:
                            o,p = fu.result(timeout=8)
                            if p:
                                pd.update(self.getv(o,p))
                        except TimeoutError:
                            print("线路请求超时")
                        except Exception as e:
                            print(f"多线路请求失败: {e}")
            w, e = [], []
            for ki,val in pd.items():
                if val:
                    w.append(n.get(ki,'未知线路'))
                    e.append(val)
            vod['vod_play_from'] = '$$$'.join(w)
            vod['vod_play_url'] = '$$$'.join(e)
        except Exception as e:
            print(f"详情页解析异常:{e}")
        return {'list': [vod]}

    def searchContent(self, key, quick, pg="1"):
        jdata = {
            "condition": {
                "value": str(key)
            },
            "pageNum": int(pg),
            "pageSize": 40
        }
        try:
            data = self.post(f"{self.host}/api/v1/app/search/searchMovie", headers=self.headers, json=jdata).json()
            records = data.get('data', {}).get('records', [])
        except Exception as e:
            print(f"搜索请求失败: {e}")
            records = []
        return {'list': self.getlist(records), 'page': int(pg)}

    def playerContent(self, flag, id, vipFlags):
        try:
            raw_id_str = self.d64(id)
            if not raw_id_str:
                return {'parse': 0, 'url': '', 'header': {'User-Agent': 'okhttp/4.12.0'}}
            jdata = json.loads(raw_id_str)
            encrypt_payload = {"key": self.rsa_encrypt(json.dumps(jdata))}
            data = self.post(f"{self.host}/api/v1/app/play/movieDetails", headers=self.headers, json=encrypt_payload).json()
            dec = self.rsa_decrypt(data.get('data',''))
            if not dec:
                return {'parse': 0, 'url': '', 'header': {'User-Agent': 'okhttp/4.12.0'}}
            decrypted_url_data = json.loads(dec)
            playerUrl = decrypted_url_data.get('url', '')
            if not playerUrl:
                return {'parse': 0, 'url': '', 'header': {'User-Agent': 'okhttp/4.12.0'}}
            params = {'playerUrl': playerUrl, 'playerId': jdata['playerId']}
            pd = self.fetch(f"{self.host}/api/v1/app/play/analysisMovieUrl", headers=self.headers, params=params).json()
            url = pd.get('data', '')
            return {
                'parse':0,
                'url':url,
                'header':{'User-Agent':'okhttp/4.12.0'}
            }
        except Exception as e:
            print(f"解析流媒体直链失败: {e}")
            return {'parse':0, 'url':'', 'header':{'User-Agent':'okhttp/4.12.0'}}

    def localProxy(self, param):
        return None

    def liveContent(self, url):
        return None

    def gettk(self):
        try:
            self.headers.update({'deviceId': self.getdid()})
            data = self.fetch(f"{self.host}/api/v1/app/user/visitorInfo", headers=self.headers).json()
            return data.get('data', {}).get('token', '')
        except Exception as e:
            print(f"获取token失败:{e}")
            return ""

    def getdid(self):
        did = self.getCache('ldid')
        if not did:
            hex_chars = '0123456789abcdef'
            did = ''.join(random.choice(hex_chars) for _ in range(16))
            self.setCache('ldid', did)
        return did

    def getd(self, jdata, player):
        x = jdata.copy()
        x.update({'playerId': player['id']})
        encrypt_payload = {"key": self.rsa_encrypt(json.dumps(x))}
        response = self.post(f"{self.host}/api/v1/app/play/movieDetails", headers=self.headers, json=encrypt_payload).json()
        decrypted_str = self.rsa_decrypt(response.get('data', ''))
        if decrypted_str:
            decrypted_episode = json.loads(decrypted_str)
            return x, decrypted_episode.get('episodeList', [])
        return x, []

    def getv(self, d, c):
        f = {str(d['playerId']): ''}
        g = []
        for i in c:
            j = d.copy()
            j.update({'episodeId': i.get('id','')})
            ep_name = i.get('episode','')
            g.append(f"{ep_name}${self.e64(json.dumps(j))}")
        f[str(d['playerId'])] = '#'.join(g)
        return f

    def getlist(self, data):
        videos = []
        for i in data:
            vid = i.get('id')
            if not vid:
                continue
            videos.append({
                'vod_id': f"{vid}@@{i.get('typeId', '')}",
                'vod_name': i.get('name', ''),
                'vod_pic': i.get('cover', ''),
                'vod_year': i.get('year', ''),
                'vod_remarks': i.get('totalEpisode', '')
            })
        return videos

    def e64(self, text):
        try:
            return b64encode(text.encode('utf-8')).decode('utf-8')
        except:
            return ""

    def d64(self, encoded_text):
        try:
            return b64decode(encoded_text.encode('utf-8')).decode('utf-8')
        except:
            return ""
