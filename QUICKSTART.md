# Quick Start Guide

Get up and running with Tailscale on Kodi in 5 minutes!

## Prerequisites

- Kodi 21 (Omega) installed
- Internet connection
- A Tailscale account (free at https://tailscale.com)

## Installation (2 minutes)

1. **Download** the addon ZIP file
2. In Kodi: **Settings** → **Add-ons** → **Install from zip file**
3. Select the downloaded **plugin.program.tailscale-1.0.0.zip**
4. Wait for "Add-on installed" notification

## First Run Setup (3 minutes)

Launch the addon from **Add-ons** → **Program add-ons** → **Tailscale VPN Manager**

The Setup Wizard will automatically start:

### Step 1: System Detection ✓
The wizard detects your system automatically. Just wait a moment.

### Step 2: Download Tailscale ✓
Binary downloads automatically. Watch the progress bar.

**Windows Users:** You'll need to run the installer manually after this step.

### Step 3: Start Tailscale ✓
The daemon starts automatically on Linux/LibreELEC.

### Step 4: Auto-Start ✓
Choose **Yes** if you want Tailscale to start with Kodi (recommended).

### Step 5: Authentication ✓
1. You'll see a URL like: `https://login.tailscale.com/a/xxxxx`
2. **Copy this URL** (write it down or take a photo)
3. On your phone or computer, visit that URL
4. Log in with your Tailscale account
5. Authorize the device
6. Click **OK** in Kodi

Done! 🎉

## Using Your NAS (1 minute)

Now connect to your NAS over Tailscale:

1. In the addon, select **Add NAS Source**
2. Choose **SMB/CIFS (Windows Share)**
3. Enter your NAS **Tailscale hostname** (e.g., `my-nas`)
   - Find this in your Tailscale admin panel
4. Enter your share name (e.g., `media`)
5. Enter username and password if needed
6. Give it a name (e.g., "Home NAS")
7. Choose **Videos** (or your content type)

Your NAS is now available in Kodi! Browse to **Videos** → **Files** → **Home NAS**

## Quick Reference

| Action | Location |
|--------|----------|
| View connection status | Main menu → Connection Status |
| Start/Stop Tailscale | Main menu → Start/Stop Tailscale |
| Add NAS source | Main menu → Add NAS Source |
| Manage sources | Main menu → Manage NAS Sources |
| Settings | Main menu → Settings |

## Common Tasks

### Check if Connected
Main menu → **Connection Status**
- Should show "Connected" with your IP address

### Stop Tailscale Temporarily
Main menu → **Stop Tailscale**
- Stops the VPN connection

### Start Tailscale Again
Main menu → **Start Tailscale**
- Reconnects to your Tailnet

### Find Your NAS Hostname
1. Visit https://login.tailscale.com
2. Look at your devices list
3. Find your NAS device name (e.g., "synology-nas")
4. Use that name when adding sources

## Troubleshooting

**"Not Installed" appears**
→ Run the Setup Wizard from Settings

**"Not Authenticated" shows**
→ The auth URL expired. Stop and restart Tailscale to get a new one.

**Can't connect to NAS**
→ Check both Kodi device and NAS are connected in Tailscale admin panel

**Windows: "Please run installer manually"**
→ Find the installer at: `%APPDATA%\Kodi\addons\plugin.program.tailscale\bin\tailscale-setup.exe`
→ Right-click and "Run as administrator"

## Tips

💡 **Use Tailscale hostnames** instead of IP addresses for your NAS (they don't change!)

💡 **Enable auto-start** so Tailscale connects when Kodi starts

💡 **Check status regularly** to ensure you're connected

💡 **Test the connection** using the "Test Connection" feature in Manage Sources

## What's Next?

- Add multiple NAS sources (home, work, friend's server)
- Configure exit nodes in Settings for routing all traffic
- Explore advanced Tailscale features at https://tailscale.com/kb

## Need Help?

- Check the full **README.md** for detailed information
- Review **INSTALL.md** for platform-specific guidance
- Report issues on GitHub: https://github.com/yourusername/Kodi-Tailscale
- Check logs: `/storage/.kodi/temp/kodi.log` on LibreELEC

---

**Enjoy secure, easy access to your media from anywhere! 🎬**
