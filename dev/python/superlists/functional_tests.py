from selenium import webdriver
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
        self.fail('Finish the test!')

        # user prompted to enter a todo list

        # she types "Buy cow" into a text box

        # when she hits enter, the page updates, and
        # now the page lists "1: Buy cow" as an item
        # in a to-do list

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


if __name__ == '__main__':
    unittest.main()

