#!/usr/bin/env python3
"""
UTILITY FUNCTIONS MODULE
Helper functions for DDoS system
"""

import random
import string
import time
import sys
from colorama import Fore, Style

def generate_random_string(length=10):
    """Generate random string"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def calculate_rps(start_time, request_count):
    """Calculate requests per second"""
    elapsed = time.time() - start_time
    return request_count / elapsed if elapsed > 0 else 0

def format_number(num):
    """Format large numbers with commas"""
    return f"{num:,}"

def print_status(message, status_type="info"):
    """Print status message with color coding"""
    colors = {
        "info": Fore.CYAN,
        "success": Fore.GREEN,
        "warning": Fore.YELLOW,
        "error": Fore.RED,
        "debug": Fore.MAGENTA
    }
    
    color = colors.get(status_type, Fore.WHITE)
    timestamp = time.strftime("%H:%M:%S")
    
    print(f"{Fore.WHITE}[{timestamp}] {color}{message}{Style.RESET_ALL}")

def check_internet():
    """Check internet connection"""
    import socket
    
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def validate_url(url):
    """Validate URL format"""
    from urllib.parse import urlparse
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def get_terminal_width():
    """Get terminal width"""
    try:
        import os
        return os.get_terminal_size().columns
    except:
        return 80

def animate_text(text, delay=0.05):
    """Animate text printing"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()
