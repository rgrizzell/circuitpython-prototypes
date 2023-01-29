"""Ensure that local storage can be written to."""
import storage
import supervisor

# Disable reload when writing to the filesystem.
supervisor.runtime.autoreload = False
if storage.getmount("/").readonly:
    print("Read-only Filesystem")
    try:
        # Ensure that the Microcontroller can write to the filesystem
        storage.remount("/", disable_concurrent_write_protection=True)
    except:
        print("Could not remount filesystem.")
