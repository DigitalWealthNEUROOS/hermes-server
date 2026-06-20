#!/usr/bin/env python3
'''Hermes Business Browser - Perfect browser for Hermes AI agent'''

import os, json, time, subprocess, tempfile
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

try:
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    HAS_SELENIUM = True
except ImportError:
    HAS_SELENIUM = False

class HermesBrowser:
    def __init__(self, headless=True, proxy=None, user_agent=None):
        self.headless = headless
        self.proxy = proxy
        self.user_agent = user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        self.session_dir = Path('/root/hermes/browser-sessions')
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots_dir = Path('/root/hermes/screenshots')
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
    
    def navigate(self, url, wait=5, screenshot=True):
        if HAS_PLAYWRIGHT:
            return self._playwright_navigate(url, wait, screenshot)
        return self._firefox_navigate(url, wait)
    
    def _playwright_navigate(self, url, wait, screenshot):
        try:
            with sync_playwright() as p:
                browser = p.firefox.launch(headless=True)
                page = browser.new_context(user_agent=self.user_agent).new_page()
                page.goto(url, wait_until='networkidle', timeout=30000)
                time.sleep(wait)
                title = page.title()
                content = page.content()[:5000]
                ss_path = None
                if screenshot:
                    ss_path = str(self.screenshots_dir / f'page_{int(time.time())}.png')
                    page.screenshot(path=ss_path, full_page=True)
                browser.close()
                return {'success': True, 'url': url, 'title': title, 'content': content, 'screenshot': ss_path}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _firefox_navigate(self, url, wait):
        try:
            ss = str(self.screenshots_dir / f'page_{int(time.time())}.png')
            cmd = ['firefox', '--headless', '--screenshot', ss, url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return {'success': result.returncode == 0, 'url': url, 'screenshot': ss}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def scrape(self, url, selectors=None):
        return self._playwright_navigate(url, wait=5, screenshot=False)
    
    def search_google(self, query, num_results=10):
        url = f'https://www.google.com/search?q={query}&num={num_results}'
        return self.navigate(url, wait=5)
    
    def fill_form(self, url, form_data):
        if not HAS_PLAYWRIGHT:
            return {'success': False, 'error': 'Playwright needed'}
        try:
            with sync_playwright() as p:
                browser = p.firefox.launch(headless=True)
                page = browser.new_context(user_agent=self.user_agent).new_page()
                page.goto(url, wait_until='networkidle', timeout=30000)
                filled = []
                for field, value in form_data.items():
                    try:
                        page.fill(field, value)
                        filled.append(field)
                    except:
                        pass
                page.click('button[type=submit], input[type=submit]')
                time.sleep(3)
                ss = str(self.screenshots_dir / f'form_{int(time.time())}.png')
                page.screenshot(path=ss)
                browser.close()
                return {'success': True, 'filled': filled, 'screenshot': ss}
        except Exception as e:
            return {'success': False, 'error': str(e)}

if __name__ == '__main__':
    b = HermesBrowser()
    print(f'Hermes Browser initialized')
    print(f'Playwright: {HAS_PLAYWRIGHT}')
    print(f'Selenium: {HAS_SELENIUM}')
    r = b.navigate('https://example.com')
    print(f'Test: {r.get("success")}')
