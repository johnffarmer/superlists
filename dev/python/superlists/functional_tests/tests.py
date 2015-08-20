from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import sys
import unittest

class NewVisitorTest(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super(StaticLiveServerTestCase, cls).setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super(StaticLiveServerTestCase, cls).tearDownClass() 
         
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()

    def test_layout_and_styling(self):
        # user goes to the homepage
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # she notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        #self.assertAlmostEqual(
        #    inputbox.location['x'] + inputbox.size['width'] / 2, 
        #    512,
        #    delta=5
        #) 
        
        # She starts a new List and sees the input is centered
        inputbox.send_keys('testing\n')
        #self.assertAlmostEqual(
        #    inputbox.location['x'] + inputbox.size['width'] / 2, 
        #    512,
        #    delta=5
        #) 
        
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows],
            "Expected value did not appear in table -- text was \n%s" %
            table.text
        )

    def test_can_start_a_list_and_retrieve_it(self):
        # user goes to web page to see to do app
        self.browser.get(self.server_url)
    
        # check title and header mention to-do
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # user prompted to enter a todo list
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'), 
                'Enter a to-do item'
        )

        # she types "Buy cow" into a text box
	inputbox.send_keys('Buy cow')

        # when she hits enter, the page updates, and
        # now the page lists "1: Buy cow" as an item
        # in a to-do list
	inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertTrue(re.search('/lists/.+', edith_list_url))
        self.check_for_row_in_list_table('1: Buy cow')
        
        # There is still a textbox inviting her to add
        # another item. She enters "Milk the cow"
        inputbox = self.browser.find_element_by_id('id_new_item')
	inputbox.send_keys('Milk the cow')
	inputbox.send_keys(Keys.ENTER)

        # The page updates, now show both items in 
        # her list
        self.check_for_row_in_list_table('1: Buy cow')
        self.check_for_row_in_list_table('2: Milk the cow')

        # The website has generated a unique URL for
        # her list -- there is some explanatory text
        # to that effect

        # user visits that URL - her to-do list still
        # there

        # Now a new user, Frank, comes along to the site

        # get new browser session
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Frank visits the home page. There's no sign of Edith's
        # pag
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy cow', page_text)
        self.assertNotIn('Milk the cow', page_text)

        # Frank starts a new list by entering a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Frank gets his own unique URL
        frank_list_url = self.browser.current_url
        self.assertTrue(re.search('/lists/.+', frank_list_url))
        self.assertNotEqual(frank_list_url, edith_list_url) 

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy cow', page_text)
        self.assertNotIn('Milk the cow', page_text)



