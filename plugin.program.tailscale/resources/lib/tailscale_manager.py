#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import platform
import subprocess
import json
import xbmc
import xbmcvfs

class TailscaleManager:
    """Manages Tailscale installation and operations"""
    
    TAILSCALE_URLS = {
        'x86_64': 'https://pkgs.tailscale.com/stable/tailscale_latest_amd64.tgz',
        'aarch64': 'https://pkgs.tailscale.com/stable/tailscale_latest_arm64.tgz',
        'armv7l': 'https://pkgs.tailscale.com/stable/tailscale_latest_arm.tgz',
        'i686': 'https://pkgs.tailscale.com/stable/tailscale_latest_386.tgz',
    }
    
    WINDOWS_URL = 'https://pkgs.tailscale.com/stable/tailscale-setup-latest.exe'
    
    def __init__(self, addon):
        self.addon = addon
        self.addon_path = addon.getAddonInfo('path')

        # Use Kodi's per-addon profile directory. translatePath() resolves
        # this correctly on every platform (Linux, Windows, macOS, Android,
        # LibreELEC/CoreELEC), instead of assuming a specific OS layout.
        self.base_path = xbmcvfs.translatePath(addon.getAddonInfo('profile'))

        self.bin_path = os.path.join(self.base_path, 'bin')
        self.state_path = os.path.join(self.base_path, 'state')
        self.log_path = os.path.join(self.base_path, 'logs')
        
        # Ensure directories exist
        self._ensure_directories()
        
        # Update addon setting
        self.addon.setSetting('tailscale_path', self.bin_path)
    
    def _ensure_directories(self):
        """Ensure all required directories exist"""
        for path in [self.bin_path, self.state_path, self.log_path]:
            if not os.path.exists(path):
                try:
                    os.makedirs(path, exist_ok=True)
                except Exception as e:
                    xbmc.log(f"Tailscale: Failed to create directory {path}: {e}", xbmc.LOGERROR)
    
    def is_windows(self):
        """Check if running on Windows"""
        return platform.system() == 'Windows'
    
    def get_architecture(self):
        """Detect system architecture"""
        machine = platform.machine().lower()
        
        # Map various architecture names to our supported ones
        arch_map = {
            'x86_64': 'x86_64',
            'amd64': 'x86_64',
            'x64': 'x86_64',
            'aarch64': 'aarch64',
            'arm64': 'aarch64',
            'armv7l': 'armv7l',
            'armv7': 'armv7l',
            'i686': 'i686',
            'i386': 'i686',
        }
        
        return arch_map.get(machine, machine)
    
    def get_download_url(self):
        """Get the appropriate download URL for the system"""
        if self.is_windows():
            return self.WINDOWS_URL
        
        arch = self.get_architecture()
        return self.TAILSCALE_URLS.get(arch, None)
    
    def download_tailscale(self, progress_callback=None):
        """Download Tailscale binary"""
        import requests
        import tarfile
        import tempfile
        
        url = self.get_download_url()
        if not url:
            xbmc.log(f"Tailscale: Unsupported architecture: {self.get_architecture()}", xbmc.LOGERROR)
            return False
        
        try:
            xbmc.log(f"Tailscale: Downloading from {url}", xbmc.LOGINFO)
            
            # Download file
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            if self.is_windows():
                # For Windows, just download the installer
                installer_path = os.path.join(self.bin_path, 'tailscale-setup.exe')
                with open(installer_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if progress_callback and total_size:
                                progress = int((downloaded / total_size) * 100)
                                progress_callback(progress)
                
                xbmc.log("Tailscale: Windows installer downloaded. Please run manually.", xbmc.LOGINFO)
                return True
            
            else:
                # For Linux, extract tar.gz
                with tempfile.NamedTemporaryFile(suffix='.tgz', delete=False) as tmp_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            tmp_file.write(chunk)
                            downloaded += len(chunk)
                            if progress_callback and total_size:
                                progress = int((downloaded / total_size) * 100)
                                progress_callback(progress)
                    
                    tmp_path = tmp_file.name
                
                # Extract tarball
                xbmc.log(f"Tailscale: Extracting to {self.bin_path}", xbmc.LOGINFO)
                with tarfile.open(tmp_path, 'r:gz') as tar:
                    # Extract tailscale and tailscaled binaries
                    for member in tar.getmembers():
                        if member.name.endswith('tailscale') or member.name.endswith('tailscaled'):
                            member.name = os.path.basename(member.name)
                            tar.extract(member, self.bin_path)
                
                # Make binaries executable
                tailscale_bin = os.path.join(self.bin_path, 'tailscale')
                tailscaled_bin = os.path.join(self.bin_path, 'tailscaled')
                
                if os.path.exists(tailscale_bin):
                    os.chmod(tailscale_bin, 0o755)
                if os.path.exists(tailscaled_bin):
                    os.chmod(tailscaled_bin, 0o755)
                
                # Clean up temp file
                os.unlink(tmp_path)
                
                xbmc.log("Tailscale: Download and extraction complete", xbmc.LOGINFO)
                self.addon.setSetting('tailscale_installed', 'true')
                return True
        
        except Exception as e:
            xbmc.log(f"Tailscale: Download failed: {e}", xbmc.LOGERROR)
            return False
    
    def is_installed(self):
        """Check if Tailscale is installed"""
        if self.is_windows():
            # Check if Windows Tailscale is installed in standard location
            common_paths = [
                os.path.join(os.getenv('ProgramFiles', ''), 'Tailscale', 'tailscale.exe'),
                os.path.join(os.getenv('ProgramFiles(x86)', ''), 'Tailscale', 'tailscale.exe'),
            ]
            return any(os.path.exists(path) for path in common_paths)
        else:
            tailscale_bin = os.path.join(self.bin_path, 'tailscale')
            tailscaled_bin = os.path.join(self.bin_path, 'tailscaled')
            return os.path.exists(tailscale_bin) and os.path.exists(tailscaled_bin)
    
    def start(self):
        """Start Tailscale daemon"""
        if not self.is_installed():
            return False
        
        if self.is_running():
            xbmc.log("Tailscale: Already running", xbmc.LOGINFO)
            return True
        
        try:
            if self.is_windows():
                # On Windows, use the service
                subprocess.run(['net', 'start', 'Tailscale'], check=True, 
                             capture_output=True, text=True)
            else:
                # Start tailscaled daemon
                tailscaled_bin = os.path.join(self.bin_path, 'tailscaled')
                log_file = os.path.join(self.log_path, 'tailscaled.log')
                
                cmd = [
                    tailscaled_bin,
                    '--state', os.path.join(self.state_path, 'tailscaled.state'),
                    '--socket', os.path.join(self.state_path, 'tailscaled.sock'),
                ]
                
                # Start daemon in background
                with open(log_file, 'a') as log:
                    subprocess.Popen(cmd, stdout=log, stderr=log, 
                                   start_new_session=True)
                
                # Wait a moment for daemon to start
                xbmc.sleep(2000)
            
            xbmc.log("Tailscale: Started successfully", xbmc.LOGINFO)
            return True
        
        except Exception as e:
            xbmc.log(f"Tailscale: Failed to start: {e}", xbmc.LOGERROR)
            return False
    
    def stop(self):
        """Stop Tailscale daemon"""
        try:
            if self.is_windows():
                subprocess.run(['net', 'stop', 'Tailscale'], check=True,
                             capture_output=True, text=True)
            else:
                # Find and kill tailscaled process
                result = subprocess.run(['pgrep', '-f', 'tailscaled'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    pids = result.stdout.strip().split('\n')
                    for pid in pids:
                        subprocess.run(['kill', pid])
            
            xbmc.log("Tailscale: Stopped successfully", xbmc.LOGINFO)
            return True
        
        except Exception as e:
            xbmc.log(f"Tailscale: Failed to stop: {e}", xbmc.LOGERROR)
            return False
    
    def is_running(self):
        """Check if Tailscale daemon is running"""
        try:
            if self.is_windows():
                result = subprocess.run(['sc', 'query', 'Tailscale'],
                                      capture_output=True, text=True)
                return 'RUNNING' in result.stdout
            else:
                result = subprocess.run(['pgrep', '-f', 'tailscaled'],
                                      capture_output=True, text=True)
                return result.returncode == 0
        except Exception:
            return False
    
    def authenticate(self):
        """Get authentication URL"""
        if not self.is_installed() or not self.is_running():
            return None
        
        try:
            tailscale_bin = os.path.join(self.bin_path, 'tailscale')
            
            if self.is_windows():
                tailscale_bin = 'tailscale'  # Use system tailscale on Windows
            
            # Set socket environment variable for Linux
            env = os.environ.copy()
            if not self.is_windows():
                env['TAILSCALE_SOCKET'] = os.path.join(self.state_path, 'tailscaled.sock')
            
            result = subprocess.run([tailscale_bin, 'up', '--auth-key='],
                                  capture_output=True, text=True, env=env)
            
            # Parse output for auth URL
            for line in result.stderr.split('\n'):
                if 'https://login.tailscale.com' in line:
                    # Extract URL
                    import re
                    match = re.search(r'https://login\.tailscale\.com[^\s]+', line)
                    if match:
                        url = match.group(0)
                        self.addon.setSetting('tailscale_authenticated', 'true')
                        return url
            
            return None
        
        except Exception as e:
            xbmc.log(f"Tailscale: Authentication failed: {e}", xbmc.LOGERROR)
            return None
    
    def get_status(self):
        """Get Tailscale status"""
        status = {
            'running': False,
            'authenticated': False,
            'ip': None,
            'hostname': None,
            'tailnet': None,
        }
        
        if not self.is_installed():
            return status
        
        status['running'] = self.is_running()
        
        if not status['running']:
            return status
        
        try:
            tailscale_bin = os.path.join(self.bin_path, 'tailscale')
            
            if self.is_windows():
                tailscale_bin = 'tailscale'
            
            env = os.environ.copy()
            if not self.is_windows():
                env['TAILSCALE_SOCKET'] = os.path.join(self.state_path, 'tailscaled.sock')
            
            result = subprocess.run([tailscale_bin, 'status', '--json'],
                                  capture_output=True, text=True, env=env,
                                  timeout=5)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                status['authenticated'] = True
                
                # Get self info
                if 'Self' in data:
                    self_data = data['Self']
                    if 'TailscaleIPs' in self_data and self_data['TailscaleIPs']:
                        status['ip'] = self_data['TailscaleIPs'][0]
                    if 'HostName' in self_data:
                        status['hostname'] = self_data['HostName']
                    if 'DNSName' in self_data:
                        # Extract tailnet from DNS name
                        dns = self_data['DNSName']
                        if '.' in dns:
                            status['tailnet'] = dns.split('.')[-2] if dns.count('.') > 1 else None
        
        except Exception as e:
            xbmc.log(f"Tailscale: Failed to get status: {e}", xbmc.LOGERROR)
        
        return status
    
    def uninstall(self):
        """Uninstall Tailscale"""
        self.stop()
        
        # Remove files
        import shutil
        try:
            if os.path.exists(self.bin_path):
                shutil.rmtree(self.bin_path)
            if os.path.exists(self.state_path):
                shutil.rmtree(self.state_path)
            
            self.addon.setSetting('tailscale_installed', 'false')
            self.addon.setSetting('tailscale_authenticated', 'false')
            
            xbmc.log("Tailscale: Uninstalled successfully", xbmc.LOGINFO)
            return True
        
        except Exception as e:
            xbmc.log(f"Tailscale: Uninstall failed: {e}", xbmc.LOGERROR)
            return False