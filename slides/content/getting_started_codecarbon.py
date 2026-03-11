from codecarbon import EmissionsTracker

tracker = EmissionsTracker()
tracker.start()

# Your training code here
# ...

# Stop tracking
emissions = tracker.stop()
