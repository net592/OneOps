#!/usr/bin/env python
#coding=utf-8
import urllib2, urllib
from django.conf import settings
from nodegroups import *

try:
    import json
except ImportError:
    import simplejson as json


class SaltAPI(object):
    __token_id = ''

#初始化API接口
    def __init__(self):
        # type: () -> object获取Setting配置文件
        self.__url = settings.SALT_API_URL
        self.__user = settings.SALT_API_USER
        self.__password = settings.SALT_API_PASSWD
        ''' user login and get token id '''
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        content = self.postRequest(obj, prefix='/login')
        try:
            self.__token_id = content['return'][0]['token']
        except KeyError:
            raise KeyError

#定义Post请求参数
    def postRequest(self, obj, prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token': self.__token_id}
        req = urllib2.Request(url, obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        return content

#定义输出INFO信息
    def postRequest1(self, obj, prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token': self.__token_id}
        req = urllib2.Request(url, obj, headers)
        opener = urllib2.urlopen(req)
        content = opener.info()
        return content

#定义获取所有客户端KEY函数
    def list_all_key(self):
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        # minions = content['return'][0]['data']['return']['minions']
        # minions_pre = content['return'][0]['data']['return']['minions_pre']
        # return minions,minions_pre
        minions = content['return'][0]['data']['return']
        return minions

    def delete_key(self, node_name):
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': node_name}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def accept_key(self, node_name):
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': node_name}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def reject_key(self, node_name):
        params = {'client': 'wheel', 'fun': 'key.reject', 'match': node_name}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

#定义不加参数的命令
    def remote_noarg_execution(self, tgt, fun):
        ''' Execute commands without parameters '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0][tgt]
        return ret

#定义带参数的命令函数
    def remote_execution(self, tgt, fun, arg):
        ''' Command execution with parameters '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0][tgt]
        return ret

#定义CMD命令函数
    def shell_remote_execution(self, tgt, arg):
        ''' Shell command execution with parameters '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'cmd.run', 'arg': arg, 'expr_form': 'list'}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

#定义Grains获取函数
    def grains(self, tgt, arg):
        ''' Grains.item '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'grains.item', 'arg': arg}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

#定义带命令的CMD函数
    def target_remote_execution(self, tgt, fun, arg):
        ''' Use targeting for remote execution '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'nodegroup'}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid

#定义部署SLS编排函数
    def deploy(self, tgt, arg):
        ''' Module deployment '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        return content

#定义异步执行编排函数
    def async_deploy(self, tgt, arg):
        ''' Asynchronously send a command to connected minions '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid

#定义异步列表函数
    def target_deploy(self, tgt, arg):
        ''' Based on the list forms deployment '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'list'}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid

#定义获取Job函数
    def jobs_list(self):
        ''' Get Cache Jobs Defaut 24h '''
        url = self.__url + '/jobs/'
        headers = {'X-Auth-Token': self.__token_id}
        req = urllib2.Request(url, headers=headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        jid = content['return'][0]
        return jid

#定义返回Mange状态函数
    def runner_status(self, arg):
        ''' Return minion status '''
        params = {'client': 'runner', 'fun': 'manage.' + arg}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        jid = content['return'][0]
        return jid

#定义获取状态函数
    def runner(self, arg):
        ''' Return minion status '''
        params = {'client': 'runner', 'fun': arg}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        jid = content['return'][0]
        return jid

#定义主函数
def main():
    # sapi = SaltAPI(url='http://127.0.0.1:8000',username='admin',password='admin')
    sapi = SaltAPI()
    # jid = sapi.target_deploy('echo.example.sinanode.com.cn','nginx-test')
    # jids = sapi.shell_remote_execution('echo','netstat -tnlp')
    # jids = "salt-run jobs.lookup_jid " + jid
    # print jid
    # time.sleep(100)
    # result = os.popen(jids).readlines()
    # if result == "":
    #    result = "Execute time too long, Please Click "  jid + " show it"
    #    print result
    # else:
    #    print result
    status_all = sapi.runner_status('status')
    # b = NodeGroups()

    # b = sapi.runner("status")
    # print a

    up_host = sapi.runner_status('status')['up']
    os_list = []
    os_release = []
    os_all = []
    for hostname in up_host:
        osfullname = sapi.grains(hostname, 'osfullname')[hostname]['osfullname']
        osrelease = sapi.grains(hostname, 'osrelease')[hostname]['osrelease']
        os = osfullname + osrelease
        os_list.append(os)
    os_uniq = set(os_list)

    for release in os_uniq:
        num = os_list.count(release)
        os_dic = {'value': num, 'name': release}
        os_all.append(os_dic)
    os_release = list(set(os_list))

    print os_release
    print os_all


if __name__ == '__main__':
    main()
