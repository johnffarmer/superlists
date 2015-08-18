from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it(self):
        # user goes to web page to see to do app
        self.browser.get('http://localhost:8000')

        # check title and header mention to-do
        self.assertIn('To-Do', self.browser.title)

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
        
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy cow' for row in rows)
        )

        # There is still a textbox inviting her to add
        # another item. She enters "Milk the cow"

        # The page updates, now show both items in 
        # her list

        # The website has generated a unique URL for
        # her list -- there is some explanatory text
        # to that effect

        # user visits that URL - her to-do list still
        # there

        # user done
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main()
