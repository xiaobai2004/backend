import sae
sae.add_vender_dir('site-packages')
from manage import app
application = sae.create_wsgi_app(app);
