import unittest
from flask import current_app
from app import create_app, db 
from app.main import views
from app.models  import TabConfig


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_get_execise_timeout(self):
        timeoutConfig = TabConfig( key='biaodian/execise/time_limit', value='30' )
        db.session.add( timeoutConfig )
        db.session.commit()
        configRow = TabConfig.query.filter_by( key='biaodian/execise/time_limit' ).first()
        self.assertEquals( configRow.value, '30' )
        
        self.assertEquals( views.get_config( 'biaodian/execise/time_limit'), 30 )
