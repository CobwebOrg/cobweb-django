# Convenience module that loads just about everything from the project into
# its namespace.

# This is to allow "from everything import *" for easy access in the
# interactive shell, but don't use it in production code!

from core.models import *
from core.views import *
from core.forms import *
from core.search_indexes import *
from core.tests import *

from projects.models import *
from projects.views import *
from projects.forms import *
from projects.tests import *

from webarchives.models import *
from webarchives.views import *
