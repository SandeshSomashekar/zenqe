'''
Created on Apr 3, 2013

@author: sandesh
'''
import unittest
import json
import pycurl
import cStringIO
import urllib
import time
import logging
import threading

########### UTIL FUNCTIONS START ###########
def IsNotNull(value):
    return value is not None and len(value) > 0

def sendIncentiveRequest(URL, PASSWORD):
    # Variables created   
    response = cStringIO.StringIO()
    c = pycurl.Curl()
    
    c.setopt(c.URL, URL)
    c.setopt(c.HTTPHEADER, ['Accept: text/html', 'Accept-Charset: UTF-8'])
    c.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
    c.setopt(pycurl.USERPWD, PASSWORD)
    c.setopt(pycurl.SSL_VERIFYPEER, False)
    c.setopt(pycurl.SSL_VERIFYHOST, False)
    c.setopt(pycurl.WRITEFUNCTION, response.write)

    c.perform()
    c.close()    
    return response.getvalue()


def sendRewardsRequest(URL, PASSWORD, EMAIL, INCENTIVE_NAME, INCENTIVE_VALUE, NAME, CELLPHONE):
    # Variables created   
    response = cStringIO.StringIO()
    c = pycurl.Curl()
    
    c.setopt(c.URL, URL)
    c.setopt(c.HTTPHEADER, ['Accept: text/html', 'Accept-Charset: UTF-8'])
    c.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
    c.setopt(pycurl.USERPWD, PASSWORD)
    c.setopt(pycurl.SSL_VERIFYPEER, False)
    c.setopt(pycurl.SSL_VERIFYHOST, False)
    c.setopt(pycurl.WRITEFUNCTION, response.write)
    
    # URL encodings of form data
    login_form_seq = []
    login_form_seq.append(('email', EMAIL))
    login_form_seq.append(('incentivename', INCENTIVE_NAME))
    login_form_seq.append(('incentivevalue', INCENTIVE_VALUE))
    if IsNotNull(NAME):
        login_form_seq.append(('name', NAME))
    if IsNotNull(CELLPHONE):
        login_form_seq.append(('cellphone', CELLPHONE))
    
    login_form_data = urllib.urlencode(login_form_seq)
    
    # Option -d/--data <data>   HTTP POST data
    c.setopt(pycurl.POSTFIELDS, login_form_data)
                    
    c.perform()
    c.close()    
    return response.getvalue()

def readJson(JSON):
    data = json.loads(JSON)
    return data
########### UTIL FUNCTIONS END ###########

class Test(unittest.TestCase):
    TEST_ID_PRINT = 'Test ID: %s'
    TEST_DESCRIPTION_PRINT = 'Test Description: %s'
    INCENTIVE_URL = 'https://www.zenclusive.com/zencl/web/v1/incentives'
    REWARDS_URL = 'https://www.zenclusive.com/zencl/web/v1/rewards'
    ACME_PASSWORD = 'test_id_288d66052715858d38492bb8e2d32d:test_pwd_1b5683c5f80ec139dfc8e8f387b50b'
    EMAIL_1 = 'sanclusive@gmail.com'
    INCENTIVE_VALUE_1 = '13'
    INCENTIVE_NAME_1 = 'Fandango'
    INCENTIVE_VALUE_2 = '50'
    RESTAURANT_COM = 'Restaurant.com'
    INCENTIVE_VALUE_50 = '50'
    INCENTIVE_VALUE_25 = '25'
    NAME_1 = 'Road Runner'
    NUMBER_OF_INCENTIVES = 5
    fan_13_incentive = {"incentivevalue": 13, "incentivename": "Fandango"}
    rcom_25_incentive = {"incentivevalue": 25, "incentivename": "Restaurant.com"}
    rcom_100_incentive = {"incentivevalue": 100, "incentivename": "Restaurant.com"}
    shby_10_incentive = {"incentivevalue": 10, "incentivename": "Shoebuy.com"}
    renv_15_incentive = {"incentivevalue": 15, "incentivename": "RedEnvelope"}
    expected_incentive_list = [fan_13_incentive, rcom_25_incentive, rcom_100_incentive, shby_10_incentive, renv_15_incentive]


    def sendRewardsWorker(self):
        t_start =time.time()
        t_lastCall=time.time()
        response = sendRewardsRequest(self.REWARDS_URL,
                                            self.ACME_PASSWORD,
                                            self.EMAIL_1,
                                            self.RESTAURANT_COM,
                                            self.INCENTIVE_VALUE_25,
                                            self.NAME_1, None)
        # Making sure connections is good!
        self.assertFalse("404 Not Found" in response, "Check if URL is available?")
        data = readJson(response)
        self.assertTrue(data["status"] == 200, "Check if status is success?")
        print "%3.3f" % (time.time()-t_lastCall)
        t_lastCall=time.time()
        
        
    def testMe(self):
        COUNT=0
        MAX=50
        threads=[]
        while COUNT < MAX:
            t = threading.Thread(target=self.sendRewardsWorker)
            threads.append(t)
            t.start()
            COUNT += 1


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()