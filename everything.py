# Convenience module that loads just about everything from the project into
# its namespace.

# This is to allow "from everything import *" for easy access in the
# interactive shell, but don't use it in production code!

from core.forms import *
from core.models import *
from core.search_indexes import *
from core.tables import *
from core.tests.factories import *
from core.views import *

from projects.forms import *
from projects.models import *
from projects.search_indexes import *
from projects.tables import *
from projects.tests.factories import *
from projects.views import *

# from webarchives.forms import *
from webarchives.models import *
from webarchives.search_indexes import *
# from webarchives.tables import *
# from webarchives.tests.factories import *
from webarchives.views import *
