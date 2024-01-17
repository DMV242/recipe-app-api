"""
Sample test
"""
from django.test import SimpleTestCase
from app import calc


class CalcTests(SimpleTestCase):
    "Test calc module"
    
    def test_add_numbers(self):
        """Test add numbers function with positive numbers"""
        res = calc.add(5, 6)
        
        self.assertEqual(11, res)
        
    
    def test_substract_numbers(self):
        """Test substracting numbers"""
        res = calc.substract(10,15)
    
        self.assertEqual(res,5)
