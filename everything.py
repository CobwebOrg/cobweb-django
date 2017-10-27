# Convenience module that loads just about everything from the project into
# its namespace. 

# This is to allow "from everything import *" for easy access in the 
# interactive shell, but don't use it in production code!

from archives.models import *
from archives.views import *
# from archives.search_indexes import *
from archives.tests import *

from core.models import *
from core.views import *
from core.forms import *
# from core.search_indexes import *
from core.tests import *

from projects.models import *
from projects.views import *
from projects.forms import *
# from projects.search_indexes import *
from projects.tests import *

from datasources.models import *
from datasources.views import *
from datasources.tests import *

from webresources.models import *
from webresources.views import *
from webresources.tests import *

from metadata.models import *
from metadata.views import *
from metadata.forms import *
from metadata.tests import *