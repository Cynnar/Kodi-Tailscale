#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import xbmc
import xbmcgui
import xbmcvfs

class NASManager:
    """Manages NAS sources in Kodi"""
    
    def __init__(self, addon):
        self.addon = addon
        
        # Translate Kodi's special:// path to real filesystem path
        profile_path = xbmcvfs.translatePath(addon.getAddonInfo('profile'))
        
        self.sources_file = os.path.join(
            profile_path,
            'nas_sources.json'
        )
        
        # Ensure profile directory exists
        if not os.path.exists(profile_path):
            os.makedirs(profile_path, exist_ok=True)
    
    def get_string(self, string_id):
        """Get localized string"""
        return self.addon.getLocalizedString(string_id)
    
    def load_sources(self):
        """Load saved NAS sources"""
        if not os.path.exists(self.sources_file):
            return []
        
        try:
            with open(self.sources_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            xbmc.log(f"NAS Manager: Failed to load sources: {e}", xbmc.LOGERROR)
            return []
    
    def save_sources(self, sources):
        """Save NAS sources"""
        try:
            with open(self.sources_file, 'w') as f:
                json.dump(sources, f, indent=2)
            return True
        except Exception as e:
            xbmc.log(f"NAS Manager: Failed to save sources: {e}", xbmc.LOGERROR)
            return False
    
    def add_source_wizard(self):
        """Wizard to add a new NAS source"""
        dialog = xbmcgui.Dialog()
        
        # Step 1: Select protocol
        protocols = [
            self.get_string(30600),  # SMB/CIFS
            self.get_string(30601),  # NFS
            self.get_string(30602),  # WebDAV
        ]
        
        protocol_idx = dialog.select(
            self.get_string(30505),  # Select Source Type
            protocols
        )
        
        if protocol_idx < 0:
            return
        
        protocol_map = ['smb', 'nfs', 'webdav']
        protocol = protocol_map[protocol_idx]
        
        # Step 2: Get hostname/IP
        hostname = dialog.input(
            self.get_string(30501),  # Enter NAS Hostname or IP
            type=xbmcgui.INPUT_ALPHANUM
        )
        
        if not hostname:
            return
        
        # Step 3: Get share name/path
        share = dialog.input(
            self.get_string(30502),  # Enter Share Name
            type=xbmcgui.INPUT_ALPHANUM
        )
        
        if not share:
            return
        
        # Step 4: Get credentials (if needed)
        username = None
        password = None
        
        if protocol in ['smb', 'webdav']:
            needs_auth = dialog.yesno(
                "Authentication",
                "Does this share require authentication?"
            )
            
            if needs_auth:
                username = dialog.input(
                    self.get_string(30503),  # Enter Username
                    type=xbmcgui.INPUT_ALPHANUM
                )
                
                if username:
                    password = dialog.input(
                        self.get_string(30504),  # Enter Password
                        type=xbmcgui.INPUT_ALPHANUM,
                        option=xbmcgui.ALPHANUM_HIDE_INPUT
                    )
        
        # Step 5: Get display name
        default_name = f"{hostname} - {share}"
        display_name = dialog.input(
            self.get_string(30506),  # Enter Display Name
            defaultt=default_name,
            type=xbmcgui.INPUT_ALPHANUM
        )
        
        if not display_name:
            display_name = default_name
        
        # Step 6: Select content type
        content_types = [
            "Videos",
            "Music",
            "Pictures",
            "Programs",
            "Files"
        ]
        
        content_idx = dialog.select(
            "Select Content Type",
            content_types
        )
        
        if content_idx < 0:
            content_idx = 4  # Default to Files
        
        content_type = content_types[content_idx].lower()
        
        # Build source path
        source_path = self.build_source_path(
            protocol, hostname, share, username, password
        )
        
        # Create source entry
        source = {
            'name': display_name,
            'path': source_path,
            'protocol': protocol,
            'hostname': hostname,
            'share': share,
            'username': username,
            'content_type': content_type
        }
        
        # Add to Kodi sources
        if self.add_to_kodi(source):
            # Save to our list
            sources = self.load_sources()
            sources.append(source)
            self.save_sources(sources)
            
            dialog.notification(
                self.addon.getAddonInfo('name'),
                self.get_string(30507),  # Source added successfully
                xbmcgui.NOTIFICATION_INFO
            )
        else:
            dialog.ok(
                self.get_string(30700),  # Error
                self.get_string(30508)   # Failed to add source
            )
    
    def build_source_path(self, protocol, hostname, share, username=None, password=None):
        """Build the source path based on protocol"""
        if protocol == 'smb':
            if username and password:
                return f"smb://{username}:{password}@{hostname}/{share}/"
            else:
                return f"smb://{hostname}/{share}/"
        
        elif protocol == 'nfs':
            return f"nfs://{hostname}/{share}/"
        
        elif protocol == 'webdav':
            if username and password:
                return f"webdav://{username}:{password}@{hostname}/{share}/"
            else:
                return f"webdav://{hostname}/{share}/"
        
        return None
    
    def add_to_kodi(self, source):
        """Add source to Kodi's sources.xml"""
        try:
            import xml.etree.ElementTree as ET
            
            # Get Kodi userdata path
            userdata_path = xbmcvfs.translatePath('special://userdata/')
            sources_xml = os.path.join(userdata_path, 'sources.xml')
            
            # Load or create sources.xml
            if os.path.exists(sources_xml):
                tree = ET.parse(sources_xml)
                root = tree.getroot()
            else:
                root = ET.Element('sources')
                tree = ET.ElementTree(root)
            
            # Find or create appropriate section based on content type
            section_map = {
                'videos': 'video',
                'music': 'music',
                'pictures': 'pictures',
                'programs': 'programs',
                'files': 'files'
            }
            
            section_name = section_map.get(source['content_type'], 'files')
            section = root.find(section_name)
            
            if section is None:
                section = ET.SubElement(root, section_name)
            
            # Check if source already exists
            for existing in section.findall('source'):
                path_elem = existing.find('path')
                if path_elem is not None and path_elem.text == source['path']:
                    xbmc.log(f"NAS Manager: Source already exists: {source['path']}", xbmc.LOGINFO)
                    return True
            
            # Add new source
            source_elem = ET.SubElement(section, 'source')
            
            name_elem = ET.SubElement(source_elem, 'name')
            name_elem.text = source['name']
            
            path_elem = ET.SubElement(source_elem, 'path')
            path_elem.text = source['path']
            
            allowsharing_elem = ET.SubElement(source_elem, 'allowsharing')
            allowsharing_elem.text = 'true'
            
            # Write back to file
            tree.write(sources_xml, encoding='utf-8', xml_declaration=True)
            
            xbmc.log(f"NAS Manager: Added source: {source['name']}", xbmc.LOGINFO)
            
            # Refresh Kodi
            xbmc.executebuiltin('UpdateLocalAddons')
            
            return True
        
        except Exception as e:
            xbmc.log(f"NAS Manager: Failed to add source to Kodi: {e}", xbmc.LOGERROR)
            return False
    
    def manage_sources(self):
        """Show and manage existing NAS sources"""
        sources = self.load_sources()
        
        if not sources:
            xbmcgui.Dialog().ok(
                self.get_string(30105),  # Manage Sources
                self.get_string(30509)   # No sources configured
            )
            return
        
        # Build list
        source_names = [s['name'] for s in sources]
        
        dialog = xbmcgui.Dialog()
        selected = dialog.select(
            self.get_string(30105),  # Manage Sources
            source_names
        )
        
        if selected < 0:
            return
        
        source = sources[selected]
        
        # Show options
        options = [
            "View Details",
            "Test Connection",
            "Remove Source"
        ]
        
        action = dialog.select(
            source['name'],
            options
        )
        
        if action == 0:  # View Details
            details = f"Name: {source['name']}\n"
            details += f"Path: {source['path']}\n"
            details += f"Protocol: {source['protocol']}\n"
            details += f"Hostname: {source['hostname']}\n"
            details += f"Share: {source['share']}\n"
            details += f"Content Type: {source['content_type']}"
            
            dialog.textviewer("Source Details", details)
        
        elif action == 1:  # Test Connection
            self.test_connection(source)
        
        elif action == 2:  # Remove
            if dialog.yesno(
                self.get_string(30510),  # Remove this source?
                f"Are you sure you want to remove '{source['name']}'?"
            ):
                sources.pop(selected)
                self.save_sources(sources)
                self.remove_from_kodi(source)
                
                dialog.notification(
                    self.addon.getAddonInfo('name'),
                    "Source removed",
                    xbmcgui.NOTIFICATION_INFO
                )
    
    def test_connection(self, source):
        """Test connection to NAS source"""
        dialog = xbmcgui.Dialog()
        progress = xbmcgui.DialogProgress()
        progress.create("Testing Connection", f"Connecting to {source['hostname']}...")
        
        try:
            # Try to list directory
            dirs, files = xbmcvfs.listdir(source['path'])
            progress.close()
            
            message = f"Connection successful!\n\n"
            message += f"Found {len(dirs)} directories and {len(files)} files."
            
            dialog.ok("Connection Test", message)
        
        except Exception as e:
            progress.close()
            dialog.ok(
                "Connection Failed",
                f"Could not connect to {source['hostname']}\n\n"
                f"Error: {str(e)}"
            )
    
    def remove_from_kodi(self, source):
        """Remove source from Kodi's sources.xml"""
        try:
            import xml.etree.ElementTree as ET
            
            userdata_path = xbmcvfs.translatePath('special://userdata/')
            sources_xml = os.path.join(userdata_path, 'sources.xml')
            
            if not os.path.exists(sources_xml):
                return
            
            tree = ET.parse(sources_xml)
            root = tree.getroot()
            
            # Find and remove the source
            for section in root:
                for source_elem in section.findall('source'):
                    path_elem = source_elem.find('path')
                    if path_elem is not None and path_elem.text == source['path']:
                        section.remove(source_elem)
                        break
            
            tree.write(sources_xml, encoding='utf-8', xml_declaration=True)
            
            xbmc.executebuiltin('UpdateLocalAddons')
        
        except Exception as e:
            xbmc.log(f"NAS Manager: Failed to remove source from Kodi: {e}", xbmc.LOGERROR)
