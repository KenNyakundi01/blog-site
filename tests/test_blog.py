import unittest
import datetime
from app.models import Blog

class BlogTest(unittest.TestCase):
   def setUp(self):
       
        self.new_blog = Blog(122, 'Getting various work done')

        def test_instance(self):
            self.assertTrue(isinstance(self.new_blog, Blog))