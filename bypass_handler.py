#!/usr/bin/env python3
"""
BYPASS HANDLER MODULE
Cloudflare bypass and proxy management
"""

import requests
import random
import time
import json
from colorama import Fore, Style

class BypassHandler:
    def __init__(self):
        self.proxies = []
        self.user_agents = []
        self.cf_tokens = []
        
    def load_proxies(self):
        """Load proxy list from multiple sources"""
        print(f"{Fore.CYAN}[*] Loading proxies...")
        
        proxy_sources = [
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt"
        ]
        
        all_proxies = []
        
        for source in proxy_sources:
            try:
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    proxies = response.text.strip().split('\n')
                    all_proxies.extend([p.strip() for p in proxies if p.strip()])
                    print(f"{Fore.GREEN}[+] Loaded {len(proxies)} proxies from {source[:30]}...")
            except Exception as e:
                print(f"{Fore.YELLOW}[!] Failed to load from {source[:30]}: {str(e)[:50]}")
        
        # Add some backup proxies
        backup_proxies = [
            '45.77.56.114:8080',
            '138.197.157.32:8080',
            '165.227.36.191:8080',
            '167.71.41.76:8080',
            '45.76.44.175:8080'
        ]
        
        all_proxies.extend(backup_proxies)
        self.proxies = list(set(all_proxies))
        
        print(f"{Fore.GREEN}[✓] Total proxies loaded: {len(self.proxies)}")
        return self.proxies
    
    def detect_cloudflare(self, url):
        """Detect if site uses Cloudflare"""
        try:
            response = requests.get(url, timeout=5)
            
            # Check headers
            headers = response.headers
            server = headers.get('Server', '').lower()
            
            if 'cloudflare' in server or 'cf-ray' in headers:
                return True
            
            # Check for Cloudflare challenge page
            if 'cf-chl-bypass' in response.text.lower():
                return True
                
            return False
            
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Cloudflare detection failed: {str(e)}")
            return False
    
    def bypass_cloudflare_v2_5(self, url):
        """Attempt Cloudflare bypass v2.5"""
        print(f"{Fore.CYAN}[*] Attempting Cloudflare bypass v2.5...")
        
        methods = [
            self._method_js_challenge,
            self._method_header_manipulation,
            self._method_cookie_reuse,
            self._method_websocket_tunnel
        ]
        
        for method in methods:
            try:
                print(f"{Fore.YELLOW}[*] Trying {method.__name__}...")
                success = method(url)
                if success:
                    return True
            except Exception as e:
                continue
        
        return False
    
    def _method_js_challenge(self, url):
        """Method 1: JavaScript challenge solver"""
        try:
            # Simulate browser with JavaScript execution
            headers = self.generate_advanced_headers()
            
            # First request to get challenge
            session = requests.Session()
            response = session.get(url, headers=headers, timeout=10)
            
            if 'cf-browser-verification' in response.text:
                # Parse and solve challenge (simplified)
                time.sleep(2)  # Simulate solving time
                
                # Second request with solved challenge
                headers['Cookie'] = 'cf_clearance=dummy_cf_clearance'
                response2 = session.get(url, headers=headers, timeout=10)
                
                return response2.status_code == 200
                
            return True
            
        except:
            return False
    
    def _method_header_manipulation(self, url):
        """Method 2: Header manipulation"""
        try:
            headers = self.generate_advanced_headers()
            
            # Add Cloudflare bypass headers
            headers.update({
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1'
            })
            
            response = requests.get(url, headers=headers, timeout=10)
            return response.status_code == 200
            
        except:
            return False
    
    def _method_cookie_reuse(self, url):
        """Method 3: Cookie reuse"""
        try:
            # Try to reuse existing clearance cookies
            cookies = {
                'cf_clearance': 'dummy_cf_clearance_value_12345',
                '__cf_bm': 'dummy_cf_bm_value_67890'
            }
            
            headers = self.generate_headers()
            response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
            
            return response.status_code == 200
            
        except:
            return False
    
    def _method_websocket_tunnel(self, url):
        """Method 4: WebSocket tunnel (concept)"""
        print(f"{Fore.YELLOW}[*] WebSocket tunnel method (conceptual)")
        return False  # Placeholder
    
    def generate_headers(self):
        """Generate random headers"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
        ]
        
        accept_languages = [
            'en-US,en;q=0.9',
            'en-GB,en;q=0.8',
            'en;q=0.7',
            'en-US,en;q=0.5'
        ]
        
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': random.choice(accept_languages),
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
    
    def generate_advanced_headers(self):
        """Generate advanced headers for bypass"""
        base_headers = self.generate_headers()
        
        base_headers.update({
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'DNT': '1',
            'TE': 'trailers'
        })
        
        return base_headers
    
    def get_proxy(self):
        """Get random proxy"""
        if self.proxies:
            return random.choice(self.proxies)
        return None
