import os

from socorrolib.app.generic_app import main
from socorrolib.webapi.servers import ApacheModWSGI

from collector.collector_app import CollectorApp
import collector.collector_app

from configman import ConfigFileFutureProxy

if os.path.isfile('/etc/socorro/collector.ini'):
    config_path = '/etc/socorro'
else:
    config_path = ApacheModWSGI.get_socorro_config_path(__file__)

# invoke the generic main function to create the configman app class and which
# will then create the wsgi app object.
main(
    CollectorApp,  # the socorro app class
    config_path=config_path
)

application = socorrolib.collector.collector_app.application
