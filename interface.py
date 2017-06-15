###############################################################################
# !/user/local/bin/python3
#
# This file defines a class that stores a stateful interface to the webserver.
#
###############################################################################

from http.client import HTTPConnection
from functools import lru_cache
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
    """A client for interfacing with my web server's API."""
    def __init__(self, address='localhost'):
        """Creates a new client with its own internal state."""
        self.__logged_in = False
        self.__address = address
        self.__connection = HTTPConnection(address)
        self.__token = self.__get_token()
    
    def get_token(self):
        """Return the session token used by the client."""
        return self.__token
    
    def __get_token(self):
        """Connect to the server and get a token."""
        conn = self.__connection
        conn.request('POST', '/api.php/token')
        return json_decode(conn.getresponse().read().decode('utf-8'))['token']
    
    def login(self, user, password):
        """Log in to the server with the given credentials.
        
        User can be the userid or the email address of the user. This gets a new
        session token from the server, as well.
        """
        body = json_encode(Credentials(self.__token, user, password))
        conn = self.__connection
        conn.connect()
        conn.request('POST', '/api.php/login', body=body)
        response = conn.getresponse()
        if response.status == 200:
            self.__token = json_decode(response.read().decode('utf-8'))['token']
            self.__logged_in = True
            self.get_operations.cache_clear()
            return True
        return False
    
    def logout(self):
        """Log out from the server."""
        conn = self.__connection
        conn.connect()
        conn.request('POST', '/api.php/logout',
                     body=json_encode({"token": self.__token}))
        conn.getresponse().read()
        self.__logged_in = False
        self.get_operations.cache_clear()
    
    def get_calculation_history(self, user="current", sortby="Timestamp",
                                page=-1, pagesize=10):
        """Return the user's calculation history as a JSON object"""
        body = json_encode({"token": self.__token})
        conn = self.__connection
        conn.connect()
        url = ('/api.php/calculations?user=' + str(user) + '&sortby='
               + str(sortby) + '&page=' + str(page) + '&pagesize='
               + str(pagesize))
        conn.request('POST', url, body=body)
        response = conn.getresponse()
        return json_decode(response.read().decode('utf-8'))
    
    @lru_cache()
    def get_operations(self):
        body = json_encode({"token": self.__token})
        conn = self.__connection
        conn.connect()
        conn.request("POST", '/api.php/calculate/operations', body)
        response = conn.getresponse()
        out = json_decode(response.read().decode('utf-8'))
        ops = []
        for op in out:
            if 'requiredCredentials' in out[op]:
                if out[op]['requiredCredentials'] == 'login':
                    if self.__logged_in:
                        ops.append(op)
            else:
                ops.append(op)
        return ops
    
    def calculate(self, operator, *nums):
        body = json_encode({"token": self.__token})
        conn = self.__connection
        conn.connect()
        uri = '/api.php/calculate/'+operator+'/'+'/'.join(str(i) for i in nums)
        conn.request("POST", uri, body)
        response = conn.getresponse()
        return json_decode(response.read().decode('utf-8'))["result"]
    
    def get_id(self):
        if not self.__logged_in:
            return None
        body = json_encode({"token": self.__token})
        conn = self.__connection
        conn.connect()
        conn.request("POST", '/api.php/userid', body)
        return int(json_decode(conn.getresponse().read().decode('utf-8'))["id"])
    
    def __repr__(self):
        string = 'interface pointing to '+self.__address
        string += ' with session token '+self.__token
        if self.__logged_in:
            string += ' and logged as user with id='+str(self.get_id())
        return string
    
    def __del__(self):
        if self.__logged_in:
            self.logout()
        self.__connection.close()


if __name__ == '__main__':
    # Only run this if you are testing the interface class
    pass
