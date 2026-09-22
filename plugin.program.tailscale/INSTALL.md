# Installation Guide

## Quick Start

### Option 1: Install from ZIP (Recommended for first-time users)

1. **Download the addon**
   - Download `plugin.program.tailscale-1.0.0.zip` from the releases page

2. **Enable Unknown Sources** (if not already enabled)
   - Open Kodi
   - Go to **Settings** (gear icon) → **System** → **Add-ons**
   - Enable **Unknown sources**
   - Click **Yes** when warned

3. **Install the addon**
   - Go to **Settings** → **Add-ons**
   - Click **Install from zip file**
   - Navigate to where you downloaded the ZIP
   - Select `plugin.program.tailscale-1.0.0.zip`
   - Wait for the "Add-on installed" notification

4. **Launch the addon**
   - Go to **Add-ons** → **Program add-ons**
   - Click **Tailscale VPN Manager**
   - The setup wizard will start automatically

### Option 2: Manual Installation

If you're developing or testing:

1. **Clone or download the repository**
   ```bash
   git clone https://github.com/yourusername/Kodi-Tailscale.git
   cd Kodi-Tailscale
   ```

2. **Copy to Kodi addons directory**
   
   **LibreELEC:**
   ```bash
   cp -r plugin.program.tailscale /storage/.kodi/addons/
   ```
   
   **Windows:**
   ```
   Copy the plugin.program.tailscale folder to:
   %APPDATA%\Kodi\addons\
   ```
   
   **Linux:**
   ```bash
   cp -r plugin.program.tailscale ~/.kodi/addons/
   ```

3. **Restart Kodi** or update the addon database:
   - Settings → Add-ons → My add-ons → Program add-ons
   - Right-click on Tailscale VPN Manager
   - Select **Information** → **Update**

## First Run Setup

When you first launch the addon, the Setup Wizard will guide you through:

### Step 1: System Detection
The wizard automatically detects your:
- Operating system (LibreELEC, Windows, Linux)
- CPU architecture (x86_64, ARM, etc.)

### Step 2: Download Tailscale
- Downloads the correct Tailscale binary for your system
- Shows progress during download
- Extracts and installs binaries

**Note for Windows users:** The wizard downloads the installer but requires manual installation with administrator privileges.

### Step 3: Start Tailscale
- Starts the Tailscale daemon
- Verifies it's running correctly

### Step 4: Auto-start Configuration
Choose whether Tailscale should start automatically when Kodi starts.

### Step 5: Authentication
- Displays a Tailscale authentication URL
- Visit the URL on any device to authenticate
- Once authenticated, your Kodi device joins your Tailnet

## Post-Installation

### Verify Installation
1. Open the addon
2. Select **Connection Status**
3. You should see:
   - Status: Connected
   - Your Tailscale IP address
   - Your device hostname
   - Your Tailnet name

### Add Your First NAS Source
1. From the main menu, select **Add NAS Source**
2. Choose your protocol (SMB recommended for most NAS devices)
3. Enter your NAS Tailscale hostname (e.g., `my-nas`)
4. Enter the share name (e.g., `media`)
5. Provide credentials if needed
6. Give it a display name
7. Select content type

The source will be added to Kodi and accessible immediately!

## Troubleshooting Installation

### "Unknown sources is disabled"
Enable it in Settings → System → Add-ons → Unknown sources

### "Add-on installed" but not appearing
- Restart Kodi completely
- Or go to Settings → Add-ons → My add-ons and look under Program add-ons

### Download fails during setup
- Check your internet connection
- Try running the wizard again from Settings
- Manually download Tailscale and place in the addon's bin directory

### Permission errors on LibreELEC
The addon uses `/storage/.kodi/addons/` which should have correct permissions.
If issues persist, check:
```bash
ls -la /storage/.kodi/addons/plugin.program.tailscale/
```

### Windows requires administrator
The Tailscale installer needs admin rights. Run it manually:
1. Navigate to the downloaded installer (shown in wizard)
2. Right-click → Run as administrator
3. Complete installation
4. Restart Kodi and run wizard again

## Updating the Addon

### Automatic Updates (if using repository)
Updates will appear in Settings → Add-ons → My add-ons

### Manual Update
1. Download the new version ZIP
2. Install from ZIP (it will update the existing installation)
3. Your settings and sources will be preserved

## Uninstalling

### Complete Removal
1. Open the addon
2. Go to Settings
3. Select **Uninstall Tailscale** (removes Tailscale binaries and config)
4. In Kodi, go to Settings → Add-ons → My add-ons
5. Find Tailscale VPN Manager
6. Select **Uninstall**

### Keep Tailscale, Remove Addon
If you want to keep Tailscale running but remove the addon:
1. Just uninstall the addon from Kodi
2. Tailscale will continue running in the background

## Support

If you encounter issues:
1. Check the logs: `/storage/.kodi/addons/plugin.program.tailscale/logs/tailscaled.log`
2. Enable Kodi debug logging: Settings → System → Logging → Enable debug logging
3. Check Kodi's log: `/storage/.kodi/temp/kodi.log`
4. Report issues on GitHub with relevant log excerpts
