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
