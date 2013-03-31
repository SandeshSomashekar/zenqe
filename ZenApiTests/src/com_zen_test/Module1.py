'''
Created on Mar 24, 2013

@author: sandesh
@copyright: property of zenclusive inc.
'''

import unittest
import json
import pycurl
import cStringIO
import urllib

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
    c.setopt(pycurl.USERPWD,  PASSWORD)
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
    c.setopt(pycurl.USERPWD,  PASSWORD)
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
    data=json.loads(JSON)
    #pprint(data)
    return data
########### UTIL FUNCTIONS END ###########


class Test(unittest.TestCase):
    INCENTIVE_URL = 'https://www.zenclusive.com/zencl/web/v1/incentives'
    REWARDS_URL = 'https://www.zenclusive.com/zencl/web/v1/rewards'
    ACME_PASSWORD = 'test_id_288d66052715858d38492bb8e2d32d:test_pwd_1b5683c5f80ec139dfc8e8f387b50b'
    EMAIL_1='sanclusive@gmail.com'
    INCENTIVE_VALUE_1='13'
    INCENTIVE_NAME_1='Fandango'
    INCENTIVE_VALUE_2='50'
    INCENTIVE_NAME_2='Restaurant.com'
    NAME_1='Road Runner'
    NUMBER_OF_INCENTIVES = 5
    fan_13_incentive = {"incentivevalue": 13, "incentivename": "Fandango"}
    rcom_25_incentive = {"incentivevalue": 25, "incentivename": "Restaurant.com"}
    rcom_100_incentive = {"incentivevalue": 100, "incentivename": "Restaurant.com"}
    shby_10_incentive = {"incentivevalue": 10, "incentivename": "Shoebuy.com"}
    renv_15_incentive = {"incentivevalue": 15, "incentivename": "RedEnvelope"}
    expected_incentive_list = [fan_13_incentive, rcom_25_incentive, rcom_100_incentive, shby_10_incentive, renv_15_incentive]


    #Positive1 ; Connnection check test, 
    def testPositive1(self):
        print("\nPositive1 is running\n") 
        
        response=sendIncentiveRequest(self.INCENTIVE_URL, self.ACME_PASSWORD)
        
        print "Response from cURL request is \n: \"%s\"" % response
        
        self.assertTrue(not "404 Not Found" in response, "Check if URL is available?")
        data=readJson(response)
        print "status is %s" % data["status"]
        self.assertTrue(data["status"] == 200, "Check if status is success?")
        print("\nPositive1 is finished running.")
        pass        


    #Negative2
    def testNegative2(self):
        #Providing wrong URL
        print("Negative2 is running\n")
        response=sendIncentiveRequest(self.INCENTIVE_URL+"BadURL", self.ACME_PASSWORD)
        
        self.assertTrue("404 Not Found" in response, "Check if URL is available?")
        print("\nNegative2 is finished running.")
        pass
    

    #Positive2
    def testPositive2(self):
        print("Positive2 is running\n")
        response=sendIncentiveRequest(self.INCENTIVE_URL, self.ACME_PASSWORD)
        
        self.assertFalse("404 Not Found" in response, "Check if URL is available?")
        data=readJson(response)
        
        
        print "status is %s" % data["status"]
        self.assertTrue(data["status"] == 200, "Check if status is success?")
        
        self.assertTrue(data["incentives"].__len__() == self.NUMBER_OF_INCENTIVES, "Check if there are five incentives")
        print("\nPositive2 is finished running.")
        pass
    

    #Positive3
    def testPositive3(self):
        print("\nPositive3 is running...")
        response=sendIncentiveRequest(self.INCENTIVE_URL, self.ACME_PASSWORD)
        
        #Making sure connections is good!
        self.assertFalse("404 Not Found" in response, "Check if URL is available?")
        data=readJson(response)        
        
        self.assertTrue(data["status"] == 200, "Check if status is success?")
        self.assertTrue(data["incentives"].__len__() == self.NUMBER_OF_INCENTIVES, "Check if there are five incentives")
        
        i = 0
        while i < self.NUMBER_OF_INCENTIVES:
            self.assertTrue(data["incentives"].count(self.expected_incentive_list[i]) == 1, "Check if expected incentive #%i is present"%i)
            i += 1 
        
        print("\nPositive3 is finished running.\n")
        pass


    #Positive4
    def testPositive4(self):
        print("\nPositive4 is running...")
        response=sendRewardsRequest(self.REWARDS_URL, 
                                                self.ACME_PASSWORD, 
                                                self.EMAIL_1, 
                                                self.INCENTIVE_NAME_1, 
                                                self.INCENTIVE_VALUE_1, 
                                                self.NAME_1, None)
        
        print(response)
        #Making sure connections is good!
        self.assertFalse("404 Not Found" in response, "Check if URL is available?")
        data=readJson(response)        
        
        self.assertTrue(data["status"] == 200, "Check if status is success?")
        
        print("\nPositive4 is finished running.\n")
        pass

    
    #Negative3
    def testNegative3(self):
        print("\nNegative3 is running...")
        response=sendRewardsRequest(self.REWARDS_URL, 
                                                self.ACME_PASSWORD, 
                                                self.EMAIL_1, 
                                                self.INCENTIVE_NAME_2, 
                                                self.INCENTIVE_VALUE_2, 
                                                self.NAME_1, 
                                                None)
        
        print(response)
        #Making sure connections is good!
        self.assertFalse("404 Not Found" in response, "Check if URL is available?")
        data=readJson(response)        
        
        self.assertTrue(data["status"] == 400, "Email must not be sent, status 400 is expected...")
        
        print("\nNegative3 is finished running.\n")
        pass

    
    
    def testPositive5(self):
        print("\nPositive5 is running...")
        response=sendIncentiveRequest(self.INCENTIVE_URL, self.ACME_PASSWORD)
        
        #Making sure connections is good!
        self.assertFalse("404 Not Found" in response, "Check if URL is available?")
        data=readJson(response)        
        
        self.assertTrue(data["status"] == 200, "Check if status is success?")
        self.assertTrue(data["incentives"].__len__() > 0, "Check if is atleast one incentive")
        
        FIRST_INCENTIVE_NAME = data["incentives"][0]['incentivename']
        FIRST_INCENTIVE_VALUE = data["incentives"][0]['incentivevalue']
        
        response=sendRewardsRequest(self.REWARDS_URL, 
                                                self.ACME_PASSWORD, 
                                                self.EMAIL_1, 
                                                FIRST_INCENTIVE_NAME, 
                                                FIRST_INCENTIVE_VALUE, 
                                                self.NAME_1, 
                                                None)
        self.assertFalse("404 Not Found" in response, "Check if URL is available?")
        data=readJson(response)        
        
        self.assertTrue(data["status"] == 200, "Status 200 is expected...")        
        print("\nPositive5 is finished running.\n")
        pass


    #Negative4
    def testNegative4(self):
        print("\nNegative4 is running...\n")
        EMAIL="sanclusive@G@mail.com"
        ERROR_STR="This value is not a valid email address"
        response=sendRewardsRequest(self.REWARDS_URL, 
                                                self.ACME_PASSWORD, 
                                                EMAIL, 
                                                self.INCENTIVE_NAME_2, 
                                                self.INCENTIVE_VALUE_2, 
                                                self.NAME_1, 
                                                None)
        
        print(response)
        #Making sure connections is good!
        self.assertFalse("404 Not Found" in response, "Check if URL is available?")
        data=readJson(response)        
        
        self.assertTrue(data["status"] == 400, "Email must not be sent, status 400 is expected...")
        self.assertTrue(response.find(ERROR_STR)>0, "Checking for error string: 'This value is not a valid email address' in the response.")
        
        print("\nNegative4 is finished running.\n")
        pass



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testPositive2']
    unittest.main()