class CheckoutError(Exception):
    '''
    Creates a custom exception that inherits from the Exception class
    '''
    pass

class Checkout:
    '''
    A checkout class that allows people to add items to a basket, calculate totals and
    apply discounts
    '''

    def __init__(self):
        self.products = {}
        self.total = 0

    def add_item_price(self, item, price, quantity):
        if item == "" or type(item) != str:
            raise TypeError("Item description can't be empty and has to be a string")
        elif price < 0 or type(price) != int:
            raise CheckoutError("Price has to be a positive number")
        else:
            if item not in self.products:
                self.products[item] = {}
                self.products[item]['price'] = price
                self.products[item]['quantity'] = quantity
            else:
                self.products[item]['quantity'] += quantity
        
    def remove_item(self, item):
        if item in self.products and self.products[item]['quantity'] > 0:
            self.products[item]['quantity'] -= 1
        else:
            raise CheckoutError("Item not found in your basket or not enough items")

    def calculate_total(self):
        # reset total to 0
        self.total = 0
        
        if not self.products:
            raise CheckoutError("Basket is empty. Try adding some items first")
        else:
            for item in self.products:
                self.total += self.products[item]['price']*self.products[item]['quantity']
            return self.total
    
    def apply_discount(self, item, discount):
        '''
        For calculating discounts of type 20%
        '''
        if type(discount) != int:
            raise TypeError("Discount should be an integer")
        else:
            if item in self.products:
               self.products[item]['price'] = self.products[item]['price']-(self.products[item]['price']*discount/100)
            else:
               raise CheckoutError("Item couldn't be found in your basket. Add it first")
        
    
    def apply_special_offer(self, item, initial_amount, final_amount):
        '''
        For calculating special offers of type 2 for 1
        '''
        if item not in self.products:
            raise CheckoutError("Item not found in your basket")
        if self.products[item]['quantity'] >= initial_amount:
            if self.products[item]['quantity'] % 2 == 0:
                self.products[item]['quantity'] = self.products[item]['quantity']/2
            elif self.products[item]['quantity'] % 3 == 0:
                self.products[item]['quantity']  = (self.products[item]['quantity']+1)/2
        else:
            raise CheckoutError("Offer can't be applied. Not enough items in basket")
