# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-07

### Added
- Initial release
- Automated Tailscale binary download and installation
- Multi-architecture support (x86_64, aarch64, armv7l, i686)
- Setup wizard with guided installation process
  - System detection
  - Binary download with progress indicator
  - Tailscale daemon startup
  - Auto-start configuration
  - Authentication URL display
- Tailscale service management
  - Start/Stop/Restart functionality
  - Connection status monitoring
  - Status display with IP, hostname, and tailnet information
- NAS source management
  - Wizard-based source addition
  - Support for SMB/CIFS, NFS, and WebDAV protocols
  - Credential management
  - Source testing and validation
  - Integration with Kodi's sources.xml
- Configuration settings
  - Auto-start option
  - Exit node configuration
  - Default NAS credentials
  - Protocol preferences
- Windows support with installer download
- LibreELEC support with /storage directory usage
- Comprehensive logging
- English language strings
- Settings interface

### Technical Details
- Python 3 compatible (Kodi 21+)
- Uses script.module.requests for HTTP operations
- XML manipulation for Kodi sources integration
- JSON storage for addon-specific data
- Subprocess management for Tailscale daemon
- Cross-platform path handling

## [Unreleased]

### Planned Features
- Additional language support
- Automatic updates for Tailscale binary
- Advanced networking options
- Export/import source configurations
- Network diagnostics tools
- Integration with Kodi's built-in VPN settings
