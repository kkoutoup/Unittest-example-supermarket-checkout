import unittest
from checkout import Checkout, CheckoutError

class TestCheckout(unittest.TestCase):
    
    
    @staticmethod
    def test_can_instantiate_class():
        checkout = Checkout()

    def setUp(self):
        '''
        setup instance of class for tests that follow
        '''
        self.checkout = Checkout()

    def test_item_description(self):
        '''
        Raise exception if description is empty string or not string
        '''
        with self.assertRaises(TypeError):
            self.checkout.add_item_price("", 2, 1)

    def test_item_price(self):
        '''
        Raise exception if price is negative, not an int or float
        '''
        with self.assertRaises(CheckoutError):
            self.checkout.add_item_price('item', -2, 1)

        with self.assertRaises(CheckoutError):
            self.checkout.add_item_price('item', True, 1)

    def test_items_are_added(self):
        '''
        Should add items and prices
        '''
        #add some items
        self.checkout.add_item_price('bread', 2, 1)
        self.checkout.add_item_price('bread', 2, 1)
        self.checkout.add_item_price('milk', 1, 1)

        #check values are added
        self.assertEqual(self.checkout.products, {'bread': {'price': 2, 'quantity': 2}, 'milk': {'price': 1, 'quantity': 1}})
        
    def test_remove_item_if_item_not_there(self):
        '''
        Raise an exception if item is not in basket
        '''
        with self.assertRaises(CheckoutError):
            self.checkout.remove_item('peanut butter')

    def test_remove_item(self):
        '''
        Check the correct remaining amount
        '''
        #add item
        self.checkout.add_item_price('bread', 2, 2)
        #remove item
        self.checkout.remove_item('bread')

        #check remaining amount
        self.assertEqual(self.checkout.products, {'bread': {'price': 2, 'quantity': 1}})

    def test_calculate_total_empty_basket(self):
        '''
        Raise an exception if basket is empty
        '''
        with self.assertRaises(CheckoutError):
            self.checkout.calculate_total()

    def calculate_total(self):
        '''
        Test total is working properly
        '''

        #add items
        self.checkout.add_item_price('bread', 2, 2)
        self.checkout.add_item_price('milk', 1, 1)
        self.checkout.add_item_price('honey', 4, 1)
        self.checkout.add_item_price('eggs', 2, 1)

        #test total
        self.assertEqual(self.calculate_total(), 11)

    def test_apply_discount_wrong_type(self):
        '''
        Raise exception if discount is not of type int
        '''
        with self.assertRaises(TypeError):
            self.checkout.apply_discount('item','item')

    def test_apply_discount_to_non_existing_item(self):
        '''
        Raise exception if item not in basket
        '''
        with self.assertRaises(CheckoutError):
            self.checkout.apply_discount('toothpaste', 20)

    def test_apply_discount(self):
        '''
        Test discount is applied to items
        '''
        
        #add items
        self.checkout.add_item_price('bread', 2, 1)
        self.checkout.add_item_price('honey', 4, 1)
        
        #apply discount
        self.checkout.apply_discount('bread', 50)
        self.checkout.apply_discount('honey', 20)
        
        #check discount is applied correctly
        self.assertEqual(self.checkout.products['bread']['price'], 2-(2*50/100))
        self.assertEqual(self.checkout.products['honey']['price'], 4-(4*20/100))

    def test_apply_special_offer_to_item_not_in_basket(self):
        '''
        Raise exception if item has not been added to basket
        '''
        with self.assertRaises(CheckoutError):
            self.checkout.apply_special_offer('item', 2, 1)
       
    def test_apply_special_offer_not_enough_items(self):
        '''
        Raise exception if amount of items lower than necessary
        '''
        #add items
        self.checkout.add_item_price('bread', 2, 1)
        
        with self.assertRaises(CheckoutError):
            self.checkout.apply_special_offer('bread', 2, 1)

    def test_apply_special_offer_item_not_there(self):
        '''
        Raise exception if not enough items in the basket
        '''       
        with self.assertRaises(CheckoutError):
            self.checkout.apply_special_offer('bread', 2, 1)
        
    def test_apply_special_offer_even_quantity(self):
        '''
        Testing for even quantities
        '''
        #add items
        self.checkout.add_item_price('bread', 2, 2)
        self.checkout.add_item_price('milk', 1, 4)

        #test offer is applied
        self.checkout.apply_special_offer('bread', 2, 1)
        self.checkout.apply_special_offer('milk', 2, 1)

        self.assertEqual(self.checkout.products['bread']['quantity'], 1)
        self.assertEqual(self.checkout.products['milk']['quantity'], 2)
        
    def test_apply_special_offer_odd_quantity(self):
       '''
       Testing for odd quantities
       '''
       #add items
       self.checkout.add_item_price('bread', 2, 3)
       self.checkout.add_item_price('milk', 1, 9)
       self.checkout.add_item_price('chewing gum', 1, 27)

       #test offer is applied
       self.checkout.apply_special_offer('bread', 2, 1)
       self.checkout.apply_special_offer('milk', 2, 1)
       self.checkout.apply_special_offer('chewing gum', 2, 1)

       self.assertEqual(self.checkout.products['bread']['quantity'], 2)
       self.assertEqual(self.checkout.products['milk']['quantity'], 5)
       self.assertEqual(self.checkout.products['chewing gum']['quantity'], 14)
            
if __name__ == '__main__':
    unittest.main()
