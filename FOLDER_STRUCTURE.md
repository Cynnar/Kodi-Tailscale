# Kodi Tailscale Addon - Complete Folder Structure

```
plugin.program.tailscale/
│
├── addon.xml                           # Addon metadata, dependencies, and Kodi integration
├── default.py                          # Main entry point called by Kodi
├── LICENSE                             # MIT License file
├── README.md                           # Main documentation for users
├── INSTALL.md                          # Detailed installation instructions
├── DEVELOPMENT.md                      # Guide for developers
├── CHANGELOG.md                        # Version history and changes
├── package.sh                          # Script to create distribution ZIP
├── .gitignore                          # Git ignore rules
│
├── resources/
│   │
│   ├── settings.xml                    # Addon settings UI definition
│   │
│   ├── icon.png                        # 512x512 addon icon (placeholder)
│   ├── fanart.jpg                      # 1920x1080 background art (placeholder)
│   ├── screenshot-01.jpg               # Screenshot for Kodi repository (placeholder)
│   ├── screenshot-02.jpg               # Screenshot for Kodi repository (placeholder)
│   │
│   ├── language/                       # Localization files
│   │   └── resource.language.en_gb/
│   │       └── strings.po              # English language strings (IDs 30000-30999)
│   │
│   ├── lib/                            # Python modules for addon logic
│   │   ├── __init__.py                 # Package initialization
│   │   ├── addon.py                    # Main addon class (menu, routing, coordination)
│   │   ├── tailscale_manager.py        # Tailscale operations (download, install, control)
│   │   ├── wizard.py                   # Setup wizard (multi-step guided setup)
│   │   └── nas_manager.py              # NAS source management (Kodi integration)
│   │
│   └── media/                          # Icons for menu items
│       ├── wizard.png                  # Setup wizard icon (placeholder)
│       ├── status.png                  # Connection status icon (placeholder)
│       ├── start.png                   # Start Tailscale icon (placeholder)
│       ├── stop.png                    # Stop Tailscale icon (placeholder)
│       ├── add_source.png              # Add NAS source icon (placeholder)
│       ├── manage_sources.png          # Manage sources icon (placeholder)
│       └── settings.png                # Settings icon (placeholder)
│
└── [Runtime directories - created automatically]
    ├── bin/                            # Tailscale binaries (tailscale, tailscaled)
    ├── state/                          # Tailscale state (tailscaled.state, socket)
    └── logs/                           # Log files (tailscaled.log)
```

## File Descriptions

### Root Level Files

- **addon.xml**: Defines addon metadata including ID, name, version, provider (Cynnar), dependencies, and platform support. Required by Kodi.

- **default.py**: Entry point executed when addon starts. Minimal code that imports and runs the main addon class.

- **LICENSE**: MIT License for the project.

- **README.md**: Primary documentation for end users. Covers features, installation, usage, and troubleshooting.

- **INSTALL.md**: Step-by-step installation guide including first-run setup and platform-specific instructions.

- **DEVELOPMENT.md**: Comprehensive guide for developers including setup, architecture, testing, and contribution guidelines.

- **CHANGELOG.md**: Version history with all changes, additions, and fixes.

- **package.sh**: Bash script to create a distributable ZIP file excluding development files.

- **.gitignore**: Git ignore patterns for Python cache, binaries, logs, and temporary files.

### Resources Directory

**settings.xml**
- Defines the settings UI with three categories:
  1. Tailscale Control (installation, configuration, service control)
  2. NAS Sources (source management, default settings)
  3. Setup & Maintenance (wizard, reinstall, uninstall)

**icon.png** (512x512)
- Main addon icon displayed in Kodi's addon browser
- Currently a placeholder - replace with actual Tailscale-themed icon

**fanart.jpg** (1920x1080)
- Background artwork shown when addon is selected
- Currently a placeholder - replace with custom artwork

**screenshot-01.jpg, screenshot-02.jpg**
- Screenshots for Kodi addon repository listing
- Currently placeholders - replace with actual UI screenshots

### Language Directory

**resources/language/resource.language.en_gb/strings.po**
- All user-facing text strings with IDs 30000-30999
- Categories:
  - 30001-30099: Settings labels
  - 30100-30199: Menu items
  - 30200-30299: Wizard strings
  - 30300-30399: Status strings
  - 30400-30499: Action messages
  - 30500-30599: NAS source strings
  - 30600-30699: Protocol names
  - 30700-30799: Error messages
  - 30800-30899: Dialog strings

### Library (lib) Directory

**addon.py - TailscaleAddon Class**
- Main addon logic and coordination
- Methods:
  - `build_main_menu()`: Creates dynamic menu based on install state
  - `router()`: Routes actions to appropriate handlers
  - `add_menu_item()`: Helper for menu construction
  - `start_tailscale()`, `stop_tailscale()`, `restart_tailscale()`: Service control
  - `show_status()`: Display connection information
  - Action handlers for wizard, NAS management, settings

**tailscale_manager.py - TailscaleManager Class**
- Handles all Tailscale operations
- Methods:
  - `get_architecture()`: Detect CPU architecture
  - `get_download_url()`: Get correct binary URL for platform
  - `download_tailscale()`: Download and extract binaries
  - `is_installed()`, `is_running()`: Status checks
  - `start()`, `stop()`: Daemon lifecycle management
  - `authenticate()`: Generate auth URL
  - `get_status()`: Retrieve detailed status information
  - `uninstall()`: Remove Tailscale and configuration
- Platform-aware with separate logic for Windows and Linux

**wizard.py - SetupWizard Class**
- Multi-step guided setup process
- Steps:
  1. Welcome and confirmation
  2. System detection (architecture, OS)
  3. Binary download with progress
  4. Daemon startup
  5. Auto-start configuration
  6. Authentication with URL display
  7. Completion message
- Progress dialog management
- Error handling with user feedback

**nas_manager.py - NASManager Class**
- NAS source management and Kodi integration
- Methods:
  - `add_source_wizard()`: Step-by-step source addition
  - `build_source_path()`: Construct protocol-specific URLs
  - `add_to_kodi()`: Manipulate Kodi's sources.xml
  - `manage_sources()`: View, test, and remove sources
  - `test_connection()`: Verify source accessibility
  - `load_sources()`, `save_sources()`: JSON persistence
- Supports SMB/CIFS, NFS, and WebDAV protocols

### Media Directory

All .png files are menu item icons:
- **wizard.png**: Setup Wizard
- **status.png**: Connection Status
- **start.png**: Start Tailscale
- **stop.png**: Stop Tailscale
- **add_source.png**: Add NAS Source
- **manage_sources.png**: Manage NAS Sources
- **settings.png**: Settings

Currently placeholders - should be replaced with actual icons (64x64 or 128x128 recommended).

### Runtime Directories

These are created automatically during installation:

**bin/**
- Location: `/storage/.kodi/addons/plugin.program.tailscale/bin/` (LibreELEC)
- Contents:
  - `tailscale`: Command-line client
  - `tailscaled`: Daemon binary
- Permissions: 0755 (executable)

**state/**
- Location: `/storage/.kodi/addons/plugin.program.tailscale/state/`
- Contents:
  - `tailscaled.state`: Tailscale state database
  - `tailscaled.sock`: Unix socket for communication
- Managed by Tailscale daemon

**logs/**
- Location: `/storage/.kodi/addons/plugin.program.tailscale/logs/`
- Contents:
  - `tailscaled.log`: Daemon log output
- Used for troubleshooting

## Architecture Support

The addon detects and supports:
- **x86_64**: Intel/AMD 64-bit (primary platform)
- **aarch64**: ARM 64-bit (Raspberry Pi 3/4 with 64-bit OS)
- **armv7l**: ARM 32-bit (Raspberry Pi with 32-bit OS)
- **i686**: Intel/AMD 32-bit (legacy systems)

## Platform-Specific Paths

### LibreELEC (Linux)
- Base: `/storage/.kodi/addons/plugin.program.tailscale/`
- Binaries: `bin/tailscale`, `bin/tailscaled`
- State: `state/tailscaled.state`
- Socket: `state/tailscaled.sock`
- Logs: `logs/tailscaled.log`

### Windows
- Base: `%APPDATA%\Kodi\addons\plugin.program.tailscale\`
- Installer: `bin\tailscale-setup.exe`
- Note: Windows requires manual installer execution with admin rights

## Dependencies

As specified in addon.xml:
- **xbmc.python**: version 3.0.0+ (Kodi 21)
- **script.module.requests**: version 2.31.0+ (for HTTP downloads)

## Next Steps

1. **Replace Placeholder Images**: Create proper icons and artwork
2. **Test on All Platforms**: Verify functionality on Windows and LibreELEC
3. **Create GitHub Repository**: Upload to your Kodi-Tailscale repo
4. **Package for Distribution**: Run `./package.sh`
5. **Test Installation**: Install from ZIP on fresh Kodi instance
6. **Document Findings**: Update README with any platform-specific notes
