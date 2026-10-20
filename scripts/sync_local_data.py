"""
Local Data Sync Script for Hosseiny Kala (hosseinykala.ir)
Fetches all products, posts/articles, product categories, post categories, and tags
via the WordPress REST API and updates the local data files.
"""

import os
import sys

# Add current directory to path if needed
sys.path.insert(0, os.path.dirname(__file__))

from sync_database import main

if __name__ == '__main__':
    main()
