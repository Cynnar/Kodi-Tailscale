#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xbmc
import xbmcgui

class SetupWizard:
    """Setup wizard for Tailscale installation and configuration"""
    
    def __init__(self, addon, ts_manager):
        self.addon = addon
        self.ts_manager = ts_manager
        self.progress = None
    
    def get_string(self, string_id):
        """Get localized string"""
        return self.addon.getLocalizedString(string_id)
    
    def show_welcome(self):
        """Show welcome dialog"""
        dialog = xbmcgui.Dialog()
        return dialog.yesno(
            self.get_string(30200),  # Welcome to Tailscale Setup
            self.get_string(30201)   # Description
        )
    
    def detect_system(self):
        """Detect and show system information"""
        self.progress = xbmcgui.DialogProgress()
        self.progress.create(
            self.get_string(30200),  # Wizard title
            self.get_string(30214)   # Detecting system architecture
        )
        
        xbmc.sleep(1000)
        
        arch = self.ts_manager.get_architecture()
        is_windows = self.ts_manager.is_windows()
        
        self.progress.update(20, self.get_string(30215) % arch)  # Architecture: %s
        xbmc.sleep(1500)
        
        return arch, is_windows
    
    def download_step(self):
        """Step 1: Download Tailscale"""
        if not self.progress:
            self.progress = xbmcgui.DialogProgress()
        
        self.progress.update(30, self.get_string(30202))  # Step 1: Download
        xbmc.sleep(1000)
        
        self.progress.update(35, self.get_string(30203))  # Downloading...
        
        def progress_callback(percent):
            if self.progress:
                self.progress.update(35 + int(percent * 0.25), 
                                   f"{self.get_string(30203)} {percent}%")
        
        success = self.ts_manager.download_tailscale(progress_callback)
        
        if success:
            self.progress.update(60, self.get_string(30204))  # Download Complete
            xbmc.sleep(1500)
            return True
        else:
            self.progress.close()
            xbmcgui.Dialog().ok(
                self.get_string(30700),  # Error
                self.get_string(30701)   # Download failed
            )
            return False
    
    def start_step(self):
        """Step 2: Start Tailscale"""
        if not self.progress:
            self.progress = xbmcgui.DialogProgress()
        
        # Skip if Windows (requires manual installation)
        if self.ts_manager.is_windows():
            self.progress.update(70, "Windows detected. Please run the installer manually.")
            xbmc.sleep(3000)
            
            xbmcgui.Dialog().ok(
                "Manual Installation Required",
                f"Please run the Tailscale installer at:\n{self.ts_manager.bin_path}\\tailscale-setup.exe\n\n"
                "After installation, restart Kodi and run this wizard again."
            )
            self.progress.close()
            return False
        
        self.progress.update(65, self.get_string(30205))  # Step 2: Start
        xbmc.sleep(1000)
        
        self.progress.update(70, self.get_string(30206))  # Starting daemon...
        
        success = self.ts_manager.start()
        
        if success:
            self.progress.update(75, self.get_string(30207))  # Started!
            xbmc.sleep(1500)
            return True
        else:
            self.progress.close()
            xbmcgui.Dialog().ok(
                self.get_string(30700),  # Error
                self.get_string(30402)   # Failed to start
            )
            return False
    
    def autostart_step(self):
        """Step 3: Configure autostart"""
        if not self.progress:
            self.progress = xbmcgui.DialogProgress()
        
        self.progress.update(80, self.get_string(30208))  # Step 3: Auto-start
        xbmc.sleep(1000)
        
        dialog = xbmcgui.Dialog()
        autostart = dialog.yesno(
            self.get_string(30208),  # Auto-start Configuration
            self.get_string(30209)   # Would you like Tailscale to start automatically?
        )
        
        self.addon.setSetting('autostart_tailscale', 'true' if autostart else 'false')
        
        self.progress.update(85, "Auto-start configured")
        xbmc.sleep(1000)
        
        return True
    
    def authentication_step(self):
        """Step 4: Authentication"""
        if not self.progress:
            self.progress = xbmcgui.DialogProgress()
        
        self.progress.update(90, self.get_string(30210))  # Step 4: Authentication
        xbmc.sleep(1000)
        
        auth_url = self.ts_manager.authenticate()
        
        if auth_url:
            self.progress.close()
            
            # Show authentication URL in a text viewer dialog
            dialog = xbmcgui.Dialog()
            message = f"{self.get_string(30211)}\n\n{auth_url}\n\n"
            message += "Once you've authenticated on another device, click OK to continue."
            
            dialog.textviewer(
                self.get_string(30210),  # Authentication
                message
            )
            
            # Wait for user confirmation
            dialog.ok(
                self.get_string(30210),
                "Please authenticate using the URL shown.\n\n"
                "Click OK when you've completed authentication on another device."
            )
            
            # Verify authentication
            if self.progress:
                self.progress = xbmcgui.DialogProgress()
            self.progress.create(self.get_string(30200), "Verifying authentication...")
            
            xbmc.sleep(2000)
            
            status = self.ts_manager.get_status()
            if status.get('authenticated'):
                self.progress.update(100, "Authentication successful!")
                xbmc.sleep(1500)
                return True
            else:
                self.progress.close()
                # Continue anyway - user might need more time
                xbmcgui.Dialog().ok(
                    self.get_string(30804),  # Warning
                    "Authentication could not be verified immediately.\n"
                    "You can complete authentication later from the addon settings."
                )
                return True
        else:
            self.progress.close()
            xbmcgui.Dialog().ok(
                self.get_string(30700),  # Error
                "Failed to generate authentication URL.\n"
                "You can try again from the addon settings."
            )
            return True  # Continue anyway
    
    def show_completion(self):
        """Show completion message"""
        if self.progress:
            self.progress.close()
        
        dialog = xbmcgui.Dialog()
        dialog.ok(
            self.get_string(30212),  # Setup Complete!
            self.get_string(30213)   # Ready to use
        )
    
    def run(self):
        """Run the complete wizard"""
        # Welcome
        if not self.show_welcome():
            return False
        
        # Detect system
        arch, is_windows = self.detect_system()
        
        # Step 1: Download
        if not self.download_step():
            return False
        
        # Step 2: Start. start_step() itself detects Windows and shows the
        # manual-installation dialog in that case, returning False — no
        # need to duplicate that check here.
        if not self.start_step():
            return False
        
        # Step 3: Autostart
        if not self.autostart_step():
            return False
        
        # Step 4: Authentication
        if not self.authentication_step():
            return False
        
        # Completion
        self.show_completion()
        
        if self.progress:
            self.progress.close()
        
        return True