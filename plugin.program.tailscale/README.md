# Kodi-Tailscale

A Kodi addon to manage Tailscale VPN connections and easily add NAS sources over your Tailnet.

## Features

- **Easy Installation**: Automated download and installation of Tailscale binary
- **Setup Wizard**: Guided setup process for first-time configuration
- **Connection Management**: Start, stop, and monitor Tailscale connections
- **NAS Integration**: Wizard-based NAS source addition with support for SMB, NFS, and WebDAV
- **Cross-Platform**: Supports LibreELEC (x86_64, ARM) and Windows
- **Status Monitoring**: Visual connection status and Tailscale information

## Requirements

- Kodi 21 (Omega) or later
- Internet connection for initial download
- LibreELEC or Windows operating system

## Installation

### From ZIP file

1. Download the latest release ZIP file
2. In Kodi, go to **Settings** → **Add-ons** → **Install from zip file**
3. Select the downloaded ZIP file
4. The addon will be installed and available in **Programs**

### From Repository

1. Add the Cynnar repository to Kodi
2. Go to **Settings** → **Add-ons** → **Install from repository**
3. Select **Cynnar Repository** → **Program add-ons**
4. Select **Tailscale VPN Manager** and click Install

## First Run

When you launch the addon for the first time, it will automatically start the Setup Wizard:

1. **System Detection**: Detects your system architecture
2. **Download Tailscale**: Downloads the appropriate Tailscale binary
3. **Start Service**: Starts the Tailscale daemon
4. **Configure Autostart**: Choose whether to start Tailscale automatically
5. **Authentication**: Displays authentication URL to complete login

### Authentication

During the authentication step, you'll receive a URL like:
```
https://login.tailscale.com/a/xxxxxxxxxxxxxx
```

Visit this URL on any device (phone, computer) to authenticate your Kodi device with your Tailscale account.

## Usage

### Main Menu

After setup, the addon provides the following options:

- **Connection Status**: View current connection details (IP, hostname, tailnet)
- **Start/Stop Tailscale**: Control the Tailscale service
- **Add NAS Source**: Wizard to add network sources
- **Manage NAS Sources**: View, test, and remove existing sources
- **Settings**: Configure addon preferences

### Adding a NAS Source

1. Select **Add NAS Source** from the main menu
2. Choose protocol (SMB/CIFS, NFS, or WebDAV)
3. Enter NAS hostname or IP address (use Tailscale hostname for secure access)
4. Enter share name/path
5. Provide credentials if required
6. Set a display name
7. Choose content type (Videos, Music, Pictures, etc.)

The source will be automatically added to Kodi's file manager.

### Managing Sources

Use **Manage NAS Sources** to:
- View source details
- Test connections
- Remove sources

## Configuration

Access settings through the addon menu or Kodi's addon settings:

### Tailscale Control

- **Tailscale Path**: Location of Tailscale binaries (read-only)
- **Auto-start Tailscale**: Start Tailscale when Kodi starts
- **Exit Node**: Optional exit node for routing traffic
- **Start/Stop/Restart**: Manual service control
- **Show Status**: Display connection information

### NAS Sources

- **Add NAS Source**: Launch the source wizard
- **Manage Sources**: Manage existing sources
- **Default Protocol**: Set preferred protocol for new sources
- **Default Credentials**: Store default username/password

### Setup & Maintenance

- **Run Setup Wizard**: Re-run the initial setup
- **Reinstall Tailscale**: Download and reinstall Tailscale
- **Uninstall Tailscale**: Remove Tailscale and configuration

## Platform-Specific Notes

### LibreELEC

Tailscale is installed to `/storage/.kodi/addons/plugin.program.tailscale/bin/`

The addon handles all installation and configuration automatically.

### Windows

On Windows, the addon downloads the Tailscale installer but requires manual installation:

1. The wizard downloads `tailscale-setup.exe`
2. Run the installer manually (Administrator rights required)
3. After installation, restart Kodi and run the wizard again

Alternatively, you can install Tailscale normally on Windows and use the addon for connection management and NAS integration.

## Troubleshooting

### Tailscale won't start

- Check logs at: `/storage/.kodi/addons/plugin.program.tailscale/logs/tailscaled.log`
- Ensure you have sufficient disk space
- Try running **Reinstall Tailscale** from settings

### Authentication URL not working

- Copy the URL exactly as shown
- Try the URL on a different device/browser
- Check your Tailscale account status at https://login.tailscale.com

### NAS source won't connect

- Verify Tailscale is connected (check status)
- Use the Tailscale hostname instead of IP (e.g., `nas-device`)
- Test the connection using **Test Connection** in source management
- Check credentials if authentication is required

### Permission errors

- On LibreELEC, the addon uses `/storage` which should have proper permissions
- If issues persist, check system logs: `dmesg` or `/var/log/messages`

## File Structure

```
plugin.program.tailscale/
├── addon.xml                          # Addon metadata
├── default.py                         # Entry point
├── resources/
│   ├── settings.xml                   # Settings definition
│   ├── language/
│   │   └── resource.language.en_gb/
│   │       └── strings.po             # English strings
│   ├── lib/
│   │   ├── __init__.py
│   │   ├── addon.py                   # Main addon class
│   │   ├── tailscale_manager.py       # Tailscale operations
│   │   ├── wizard.py                  # Setup wizard
│   │   └── nas_manager.py             # NAS source management
│   └── media/
│       ├── icon.png                   # Addon icon
│       ├── fanart.jpg                 # Background art
│       └── *.png                      # Menu icons
```

## Development

### Building from Source

```bash
git clone https://github.com/yourusername/Kodi-Tailscale.git
cd Kodi-Tailscale
zip -r plugin.program.tailscale.zip plugin.program.tailscale/
```

### Testing

Test on Windows 11 first, then deploy to LibreELEC device.

### Architecture Support

Currently supports:
- x86_64 (Intel/AMD 64-bit)
- aarch64 (ARM 64-bit)
- armv7l (ARM 32-bit)
- i686 (Intel/AMD 32-bit)

## License

MIT License - See LICENSE file for details

## Credits

- **Provider**: Cynnar
- **Tailscale**: https://tailscale.com
- **Kodi**: https://kodi.tv

## Support

For issues, feature requests, or contributions, please visit:
https://github.com/yourusername/Kodi-Tailscale

## Changelog

### Version 1.0.0 (Initial Release)
- Automated Tailscale installation
- Setup wizard with step-by-step guidance
- Start/Stop/Restart Tailscale service
- Connection status monitoring
- NAS source management (SMB, NFS, WebDAV)
- Multi-architecture support
- Windows and LibreELEC support
