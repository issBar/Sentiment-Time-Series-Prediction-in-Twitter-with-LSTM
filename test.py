# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 14:03:00 2019

@author: itsba
"""
import unittest


class Tests(unittest.TestCase):

    def check_predicted_Values(self,score):
        self.assertTrue(-1 <= score <= 1)
    
    
    
if __name__ == '__main__':
    unittest.main()

