#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
from urllib.parse import parse_qsl

from resources.lib.tailscale_manager import TailscaleManager
from resources.lib.wizard import SetupWizard
from resources.lib.nas_manager import NASManager

class TailscaleAddon:
    def __init__(self):
        self.addon = xbmcaddon.Addon()
        self.addon_handle = int(sys.argv[1]) if len(sys.argv) > 1 else -1
        self.addon_path = self.addon.getAddonInfo('path')
        self.addon_id = self.addon.getAddonInfo('id')
        
        self.ts_manager = TailscaleManager(self.addon)
        self.nas_manager = NASManager(self.addon)
        
    def get_string(self, string_id):
        """Get localized string"""
        return self.addon.getLocalizedString(string_id)
    
    def build_main_menu(self):
        """Build the main menu"""
        xbmcplugin.setContent(self.addon_handle, 'files')
        
        # Check if setup is needed
        if not self.ts_manager.is_installed():
            self.add_menu_item(
                self.get_string(30100),  # Setup Wizard
                {'action': 'run_wizard'},
                icon='resources/media/wizard.png'
            )
        else:
            # Connection Status
            self.add_menu_item(
                self.get_string(30101),  # Connection Status
                {'action': 'status'},
                icon='resources/media/status.png'
            )
            
            # Start/Stop based on current state
            if self.ts_manager.is_running():
                self.add_menu_item(
                    self.get_string(30103),  # Stop Tailscale
                    {'action': 'stop'},
                    icon='resources/media/stop.png'
                )
            else:
                self.add_menu_item(
                    self.get_string(30102),  # Start Tailscale
                    {'action': 'start'},
                    icon='resources/media/start.png'
                )
            
            # NAS Management
            self.add_menu_item(
                self.get_string(30104),  # Add NAS Source
                {'action': 'add_nas_source'},
                icon='resources/media/add_source.png'
            )
            
            self.add_menu_item(
                self.get_string(30105),  # Manage NAS Sources
                {'action': 'manage_sources'},
                icon='resources/media/manage_sources.png'
            )
        
        # Settings (always available)
        self.add_menu_item(
            self.get_string(30106),  # Settings
            {'action': 'settings'},
            icon='resources/media/settings.png'
        )
        
        xbmcplugin.endOfDirectory(self.addon_handle)
    
    def add_menu_item(self, label, params, icon=None):
        """Add a menu item"""
        url = self.build_url(params)
        list_item = xbmcgui.ListItem(label=label)
        
        if icon:
            list_item.setArt({'icon': icon, 'thumb': icon})
        
        xbmcplugin.addDirectoryItem(
            handle=self.addon_handle,
            url=url,
            listitem=list_item,
            isFolder=False
        )
    
    def build_url(self, params):
        """Build a plugin URL"""
        if self.addon_handle == -1:
            return ''
        query = '&'.join([f'{k}={v}' for k, v in params.items()])
        return f'{sys.argv[0]}?{query}'
    
    def router(self, params):
        """Route to the appropriate action"""
        action = params.get('action', '')
        
        if action == 'run_wizard':
            wizard = SetupWizard(self.addon, self.ts_manager)
            wizard.run()
        
        elif action == 'start':
            self.start_tailscale()
        
        elif action == 'stop':
            self.stop_tailscale()
        
        elif action == 'restart':
            self.restart_tailscale()
        
        elif action == 'status':
            self.show_status()
        
        elif action == 'add_nas_source':
            self.nas_manager.add_source_wizard()
        
        elif action == 'manage_sources':
            self.nas_manager.manage_sources()
        
        elif action == 'reinstall':
            self.reinstall()
        
        elif action == 'uninstall':
            self.uninstall()
        
        elif action == 'settings':
            self.addon.openSettings()
        
        else:
            # Show main menu
            self.build_main_menu()
    
    def start_tailscale(self):
        """Start Tailscale"""
        if not self.ts_manager.is_installed():
            xbmcgui.Dialog().ok(
                self.get_string(30700),  # Error
                self.get_string(30404)   # Not installed
            )
            return
        
        progress = xbmcgui.DialogProgress()
        progress.create(self.get_string(30800), self.get_string(30801))
        
        success = self.ts_manager.start()
        progress.close()
        
        if success:
            xbmcgui.Dialog().notification(
                self.addon.getAddonInfo('name'),
                self.get_string(30400),  # Started successfully
                xbmcgui.NOTIFICATION_INFO
            )
        else:
            xbmcgui.Dialog().ok(
                self.get_string(30700),  # Error
                self.get_string(30402)   # Failed to start
            )
    
    def stop_tailscale(self):
        """Stop Tailscale"""
        progress = xbmcgui.DialogProgress()
        progress.create(self.get_string(30800), self.get_string(30801))
        
        success = self.ts_manager.stop()
        progress.close()
        
        if success:
            xbmcgui.Dialog().notification(
                self.addon.getAddonInfo('name'),
                self.get_string(30401),  # Stopped successfully
                xbmcgui.NOTIFICATION_INFO
            )
        else:
            xbmcgui.Dialog().ok(
                self.get_string(30700),  # Error
                self.get_string(30403)   # Failed to stop
            )
    
    def restart_tailscale(self):
        """Restart Tailscale"""
        self.stop_tailscale()
        xbmc.sleep(2000)
        self.start_tailscale()
    
    def show_status(self):
        """Show Tailscale status"""
        status = self.ts_manager.get_status()
        
        dialog = xbmcgui.Dialog()
        
        if status['running']:
            message = f"{self.get_string(30305)} {self.get_string(30300)}\n"  # Connected
            if status.get('ip'):
                message += f"{self.get_string(30306)} {status['ip']}\n"
            if status.get('hostname'):
                message += f"{self.get_string(30307)} {status['hostname']}\n"
            if status.get('tailnet'):
                message += f"{self.get_string(30308)} {status['tailnet']}"
        else:
            message = f"{self.get_string(30305)} {self.get_string(30301)}"  # Disconnected
        
        dialog.textviewer(self.get_string(30304), message)  # Connection Status
    
    def reinstall(self):
        """Reinstall Tailscale"""
        if xbmcgui.Dialog().yesno(
            self.get_string(30802),  # Confirm
            "Are you sure you want to reinstall Tailscale?"
        ):
            self.ts_manager.uninstall()
            wizard = SetupWizard(self.addon, self.ts_manager)
            wizard.run()
    
    def uninstall(self):
        """Uninstall Tailscale"""
        if xbmcgui.Dialog().yesno(
            self.get_string(30802),  # Confirm
            "Are you sure you want to uninstall Tailscale? This will remove all configuration."
        ):
            self.ts_manager.uninstall()
            xbmcgui.Dialog().ok(
                self.get_string(30803),  # Success
                "Tailscale has been uninstalled."
            )
    
    def run(self):
        """Main entry point"""
        # Parse parameters
        params = dict(parse_qsl(sys.argv[2][1:]))
        
        # Check if first run and not already in wizard
        if not self.ts_manager.is_installed() and params.get('action') != 'run_wizard':
            # Auto-launch wizard on first run
            if xbmcgui.Dialog().yesno(
                self.get_string(30200),  # Welcome
                self.get_string(30201)   # Description
            ):
                params = {'action': 'run_wizard'}
        
        self.router(params)
