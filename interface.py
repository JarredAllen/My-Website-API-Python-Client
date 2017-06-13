###############################################################################
# !/user/local/bin/python3
#
# This file defines a class that stores a stateful interface.
#
###############################################################################

from http.client import HTTPConnection
import json

__all__ = ['Interface']


class MyJSONEncoder(json.JSONEncoder):
    def __init__(self):
        super(MyJSONEncoder, self).__init__(default=lambda x: x.__dict__)

json_decode = json.JSONDecoder().decode
json_encode = MyJSONEncoder().encode


class Credentials:
    def __init__(self, token, user, password):
        self.token = token
        if isinstance(user, int):
            self.userid = user
        else:
            self.email = user
        self.password = password


class Interface:
    def __init__(self, address='localhost'):
        self.__logged_in = False
        self.__address = address
        self.__connection = HTTPConnection(address)
        self.__token = self.__get_token()
    
    def get_token(self):
        return self.__token
    
    def __get_token(self):
        conn = self.__connection
        conn.request('POST', '/api.php/token')
        return json_decode(conn.getresponse().read().decode('utf-8'))['token']
    
    def login(self, user, password):
        body = json_encode(Credentials(self.__token, user, password))
        conn = self.__connection
        conn.connect()
        conn.request('POST', '/api.php/login', body=body)
        response = conn.getresponse()
        if response.status == 200:
            self.__token = json_decode(response.read().decode('utf-8'))['token']
            self.__logged_in = True
            return True
        return False
    
    def logout(self):
        pass
        self.__logged_in = False
    
    def get_calculation_history(self, user="current", sortby="Timestamp",
                                page=-1, pagesize=10):
        body = '{"token":"'+self.__token+'"}'
        conn = self.__connection
        conn.connect()
        url = '/api.php/calculations?user='+str(user)+'&sortby='+str(sortby)\
              +'&page='+str(page)+'&pagesize='+str(pagesize)
        conn.request('POST', url, body=body)
        response = conn.getresponse()
        return json_decode(response.read().decode('utf-8'))
    
    def __repr__(self):
        string = 'interface pointing to '+self.__address
        string += ' with session token '+self.__token
        if self.__logged_in:
            string += ' and logged in on the server'
        return string
    
    def __del__(self):
        if self.__logged_in:
            self.logout()
        self.__connection.close()


if __name__ == '__main__':
    # Only run this if you are testing the interface class
    pass
