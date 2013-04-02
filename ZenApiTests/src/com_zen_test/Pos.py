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
    # pprint(data)
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
    INCENTIVE_NAME_2 = 'Restaurant.com'
    NAME_1 = 'Road Runner'
    NUMBER_OF_INCENTIVES = 5
    fan_13_incentive = {"incentivevalue": 13, "incentivename": "Fandango"}
    rcom_25_incentive = {"incentivevalue": 25, "incentivename": "Restaurant.com"}
    rcom_100_incentive = {"incentivevalue": 100, "incentivename": "Restaurant.com"}
    shby_10_incentive = {"incentivevalue": 10, "incentivename": "Shoebuy.com"}
    renv_15_incentive = {"incentivevalue": 15, "incentivename": "RedEnvelope"}
    expected_incentive_list = [fan_13_incentive, rcom_25_incentive, rcom_100_incentive, shby_10_incentive, renv_15_incentive]

    
    # Positive1, Group="Sanity" 
    def testPositive1(self):
        print self.TEST_ID_PRINT % "Positive1"
        print self.TEST_DESCRIPTION_PRINT % "Testing if zenclusive's API URL is available!"
        
        response = sendIncentiveRequest(self.INCENTIVE_URL, self.ACME_PASSWORD)
        
        # print "Response from cURL request is \n: \"%s\"" % response
        
        self.assertTrue(not "404 Not Found" in response, "Check if URL is available?")
        data = readJson(response)
        # print "status is %s" % data["status"]
        self.assertTrue(data["status"] == 200, "Check if status is success?")
        # print("\nPositive1 is finished running.")
        pass

    # Positive2, Group="Sanity"
    def testPositive2(self):
        print self.TEST_ID_PRINT % "Positive2"
        print self.TEST_DESCRIPTION_PRINT % "Testing if we can retrieve incentive names for merchant Acme"        

        response = sendIncentiveRequest(self.INCENTIVE_URL, self.ACME_PASSWORD)
        
        self.assertFalse("404 Not Found" in response, "Check if URL is available?")
        data = readJson(response)
        
        
        # print "status is %s" % data["status"]
        self.assertTrue(data["status"] == 200, "Check if status is success?")
        
        self.assertTrue(data["incentives"].__len__() == self.NUMBER_OF_INCENTIVES, "Check if there are five incentives")
        # print("\nPositive2 is finished running.")
        pass
    

    # Positive3, Group="Sanity"
    def testPositive3(self):
        print self.TEST_ID_PRINT % "Positive3"
        print self.TEST_DESCRIPTION_PRINT % "Testing if all of the expected incentives are retrieved."

        response = sendIncentiveRequest(self.INCENTIVE_URL, self.ACME_PASSWORD)
        
        # Making sure connections is good!
        self.assertFalse("404 Not Found" in response, "Check if URL is available?")
        data = readJson(response)        
        
        self.assertTrue(data["status"] == 200, "Check if status is success?")
        self.assertTrue(data["incentives"].__len__() == self.NUMBER_OF_INCENTIVES, "Check if there are five incentives")
        
        i = 0
        while i < self.NUMBER_OF_INCENTIVES:
            self.assertTrue(data["incentives"].count(self.expected_incentive_list[i]) == 1, "Check if expected incentive #%i is present" % i)
            i += 1 
        
        pass


    # Positive4, Group="Sanity"
    def testPositive4(self):
        print self.TEST_ID_PRINT % "Positive4"
        print self.TEST_DESCRIPTION_PRINT % "Testing if we can send a fandango-13 dollar incentive to sanclusive@gmail.com address."
        
        response = sendRewardsRequest(self.REWARDS_URL,
                                                self.ACME_PASSWORD,
                                                self.EMAIL_1,
                                                self.INCENTIVE_NAME_1,
                                                self.INCENTIVE_VALUE_1,
                                                self.NAME_1, None)
        
        print(response)
        # Making sure connections is good!
        self.assertFalse("404 Not Found" in response, "Check if URL is available?")
        data = readJson(response)        
        
        self.assertTrue(data["status"] == 200, "Check if status is success?")        
        pass

    #Positive5, Group="Sanity"
    def testPositive5(self):
        print self.TEST_ID_PRINT % "Positive5"
        print self.TEST_DESCRIPTION_PRINT % "Testing retrieve incentive name & value from GET request and provide it as input to post request."

        response = sendIncentiveRequest(self.INCENTIVE_URL, self.ACME_PASSWORD)
        
        # Making sure connections is good!
        self.assertFalse("404 Not Found" in response, "Check if URL is available?")
        data = readJson(response)        
        
        self.assertTrue(data["status"] == 200, "Check if response-status is success.")
        self.assertTrue(data["incentives"].__len__() > 0, "Check if there is atleast one incentive present.")
        
        FIRST_INCENTIVE_NAME = data["incentives"][0]['incentivename']
        FIRST_INCENTIVE_VALUE = data["incentives"][0]['incentivevalue']
        
        response = sendRewardsRequest(self.REWARDS_URL,
                                                self.ACME_PASSWORD,
                                                self.EMAIL_1,
                                                FIRST_INCENTIVE_NAME,
                                                FIRST_INCENTIVE_VALUE,
                                                self.NAME_1,
                                                None)
        self.assertFalse("404 Not Found" in response, "Check if URL is available?")
        data = readJson(response)        
        
        self.assertTrue(data["status"] == 200, "Status 200 is expected...")        
        pass
    
    # Positive6, Group="Regression"
    def testPositive6(self):
        print self.TEST_ID_PRINT % "Positive6"
        print self.TEST_DESCRIPTION_PRINT % "Testing retrieve all incentive name & value from GET request and provide it as input to post request."

        # GET request
        response = sendIncentiveRequest(self.INCENTIVE_URL, self.ACME_PASSWORD)
        
        # Making sure connections is good!
        self.assertFalse("404 Not Found" in response, "Check if URL is available?")
        incentivesResponse = readJson(response)        
        self.assertTrue(incentivesResponse["status"] == 200, "Check if response-status is success.")
        self.assertTrue(incentivesResponse["incentives"].__len__() > 0, "Check if there is atleast one incentive present.")
        
        # Now send rewards for all the available incentives
        i = 0        
        while i < incentivesResponse["incentives"].__len__():
            FIRST_INCENTIVE_NAME = incentivesResponse["incentives"][i]['incentivename']
            FIRST_INCENTIVE_VALUE = incentivesResponse["incentives"][i]['incentivevalue']
            print "Trying to send incentive: %s with value: %s" % (FIRST_INCENTIVE_NAME, FIRST_INCENTIVE_VALUE)

            # POST request
            response = sendRewardsRequest(self.REWARDS_URL,
                                                    self.ACME_PASSWORD,
                                                    self.EMAIL_1,
                                                    FIRST_INCENTIVE_NAME,
                                                    FIRST_INCENTIVE_VALUE,
                                                    self.NAME_1,
                                                    None)
            self.assertFalse("404 Not Found" in response, "Check if URL is available?")
            sendRewardsResponse = readJson(response)            
            self.assertTrue(sendRewardsResponse["status"] == 200, "Status 200 is expected...")
            i += 1

        pass
    
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testPositive2']
    unittest.main()
