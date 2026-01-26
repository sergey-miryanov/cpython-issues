import cProfile
import sys

class _MonitoringStub:
    MISSING = object()

sys.monitoring = _MonitoringStub()

prof = cProfile.Profile()
