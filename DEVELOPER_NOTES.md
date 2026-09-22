# Developer Notes - Important Information

## Critical Items to Complete Before Release

### 1. Replace Placeholder Images ⚠️
All image files are currently empty placeholders. You need to create:

- **icon.png** (512x512): Main addon icon
  - Should represent Tailscale + Kodi
  - Use Tailscale's logo guidelines if including their branding
  
- **fanart.jpg** (1920x1080): Background image
  - High quality, relevant to networking/VPN
  
- **screenshot-01.jpg**: Screenshot of main menu
- **screenshot-02.jpg**: Screenshot of connection status or wizard

- **Menu icons** (64x64 or 128x128 recommended):
  - wizard.png
  - status.png
  - start.png
  - stop.png
  - add_source.png
  - manage_sources.png
  - settings.png

### 2. Update GitHub URLs
Throughout the code and documentation, replace:
- `https://github.com/yourusername/Kodi-Tailscale`

With your actual GitHub repository URL.

Files to update:
- addon.xml (website, source)
- README.md (support link)
- QUICKSTART.md (issues link)
- DEVELOPMENT.md (resources section)

### 3. Test on Your Platforms

**Windows 11 Testing Checklist:**
- [ ] Addon installs from ZIP
- [ ] Wizard launches on first run
- [ ] Download works (but manual install required)
- [ ] All menu items appear
- [ ] Settings are accessible
- [ ] Can manage Tailscale after manual installation

**LibreELEC x86_64 Testing Checklist:**
- [ ] Addon installs from ZIP
- [ ] Wizard completes successfully
- [ ] Binary downloads correctly
- [ ] Daemon starts and stays running
- [ ] Authentication URL displays
- [ ] After auth, status shows connected
- [ ] NAS source wizard works
- [ ] Sources appear in Kodi
- [ ] Can access NAS files
- [ ] Start/Stop functions work
- [ ] Settings persist across restarts
- [ ] Auto-start works (if enabled)

### 4. Permissions on LibreELEC

The addon uses `/storage/.kodi/addons/plugin.program.tailscale/` which *should* have correct permissions by default. However, if you encounter permission issues:

**Check permissions:**
```bash
ssh root@libreelec-ip
ls -la /storage/.kodi/addons/plugin.program.tailscale/
```

**Fix if needed:**
```bash
chmod -R 755 /storage/.kodi/addons/plugin.program.tailscale/bin/
chmod 755 /storage/.kodi/addons/plugin.program.tailscale/bin/tailscale
chmod 755 /storage/.kodi/addons/plugin.program.tailscale/bin/tailscaled
```

### 5. Code Improvements to Consider

**Security:**
- Passwords are stored in plain text in settings and sources.json
- Consider encryption or using Kodi's secure storage
- Document this security consideration for users

**Error Handling:**
- Add more specific error messages for network failures
- Implement retry logic for downloads
- Add timeout handling for daemon operations

**Features to Add Later:**
- Automatic binary updates when new Tailscale versions release
- Backup/restore for NAS sources configuration
- Integration with Kodi's built-in VPN settings (if possible)
- Support for multiple Tailnets
- Advanced networking options (subnet routes, etc.)

## Architecture-Specific Notes

### x86_64 (Your Primary Platform)
- Download URL: `https://pkgs.tailscale.com/stable/tailscale_latest_amd64.tgz`
- Well tested by Tailscale
- Should work perfectly on Beelink mini PC

### aarch64 (Raspberry Pi 4 64-bit)
- Download URL: `https://pkgs.tailscale.com/stable/tailscale_latest_arm64.tgz`
- Common platform, well supported

### armv7l (Raspberry Pi 32-bit)
- Download URL: `https://pkgs.tailscale.com/stable/tailscale_latest_arm.tgz`
- Older devices, test if possible

### i686 (Legacy 32-bit)
- Download URL: `https://pkgs.tailscale.com/stable/tailscale_latest_386.tgz`
- Uncommon, low priority

## LibreELEC-Specific Considerations

1. **Read-only filesystem**: Most of the OS is read-only, but `/storage` is writable
2. **No systemd in standard way**: That's why we manage the daemon directly
3. **Limited tools**: Not all Linux utilities available
4. **Python version**: Kodi 21 uses Python 3.11.x
5. **No sudo**: Root access available via SSH but Kodi runs as root anyway

## Windows-Specific Considerations

1. **Manual installation required**: Windows installer needs admin rights
2. **Service management**: Uses Windows services, not direct process management
3. **Different paths**: Uses APPDATA instead of /storage
4. **Tailscale typically installed system-wide**: May already be installed

## Known Limitations

1. **Windows**: Requires manual Tailscale installer execution
2. **Authentication**: User must visit URL on another device (Tailscale limitation)
3. **No offline mode**: Requires internet for initial setup
4. **Single Tailnet**: Currently supports only one Tailnet per device
5. **Password storage**: Plain text in settings and JSON files

## Testing Scenarios to Cover

1. **Fresh Install**
   - First run wizard
   - Complete setup flow
   - Add first NAS source

2. **Existing Tailscale**
   - Skip download if already installed
   - Use existing authentication
   - Import existing state

3. **Network Issues**
   - Download failure handling
   - Connection timeout handling
   - Recovery from failed state

4. **User Errors**
   - Invalid NAS hostname
   - Wrong credentials
   - Cancelled wizard mid-flow

5. **Upgrade Path**
   - Install new version over old
   - Settings preservation
   - Sources preservation

## Before Committing to GitHub

- [ ] Remove any debugging code or print statements
- [ ] Remove any API keys or credentials (none should exist)
- [ ] Test the package.sh script
- [ ] Verify .gitignore excludes bin/, state/, logs/
- [ ] Add proper icon.png (not placeholder)
- [ ] Update all GitHub URLs
- [ ] Write a clear commit message for initial commit

## Initial Commit Suggestion

```bash
git init
git add .
git commit -m "Initial release: Kodi Tailscale addon v1.0.0

Features:
- Automated Tailscale installation wizard
- Multi-architecture support (x86_64, ARM)
- Start/Stop/Restart Tailscale service
- Connection status monitoring
- NAS source management (SMB, NFS, WebDAV)
- Kodi 21 (Omega) compatible
- LibreELEC and Windows support

Provider: Cynnar
License: MIT"

git remote add origin https://github.com/yourusername/Kodi-Tailscale.git
git branch -M main
git push -u origin main
```

## Documentation to Review Before Release

1. **README.md** - Make sure all features are documented
2. **INSTALL.md** - Test installation steps yourself
3. **QUICKSTART.md** - Verify it's truly quick (< 5 minutes)
4. **DEVELOPMENT.md** - Ensure dev setup instructions work
5. **CHANGELOG.md** - Accurate version history

## Future Version Ideas (v1.1+)

- [ ] Tailscale binary auto-update check
- [ ] Multiple language support (German, French, Spanish)
- [ ] Backup/Restore configuration
- [ ] Import sources from file
- [ ] Dark mode icons
- [ ] Integration with Kodi skin themes
- [ ] Subnet router configuration
- [ ] Exit node selection UI
- [ ] MagicDNS configuration
- [ ] Tailscale SSH feature integration

## Support Considerations

Users will likely ask about:
1. How to find their NAS Tailscale hostname
2. Why Windows requires manual installation
3. Authentication URL expiration
4. Connection troubleshooting
5. Performance impact

Have clear answers ready in documentation or FAQ.

## License Compliance

- **Your code**: MIT License ✓
- **Tailscale binary**: BSD-3-Clause (separate, not included in addon package)
- **Kodi**: GPL v2 (your addon is compatible as MIT)
- **Dependencies**: Check licenses for script.module.requests

No conflicts detected.

## Final Pre-Release Checklist

- [ ] All placeholder images replaced with real assets
- [ ] Tested on Windows 11
- [ ] Tested on LibreELEC x86_64
- [ ] All URLs updated to real GitHub repo
- [ ] CHANGELOG.md has v1.0.0 entry
- [ ] README.md reviewed and accurate
- [ ] package.sh creates working ZIP
- [ ] Fresh install from ZIP works
- [ ] Upgrade from previous version works (for v1.1+)
- [ ] No debugging code left in
- [ ] All files have proper copyright headers (optional but nice)
- [ ] GitHub repository created and code pushed
- [ ] GitHub Release created with ZIP attached
- [ ] README has installation instructions pointing to Releases

## Contact Information for Users

Consider adding a support section:
- GitHub Issues for bugs
- GitHub Discussions for questions
- Email or Discord for direct contact (optional)
- Kodi forum thread (consider creating one)

---

**Good luck with your Kodi Tailscale addon!**

This is a solid foundation for a useful tool. The architecture is extensible, the code is well-organized, and the documentation is comprehensive. Focus on testing thoroughly on your target platforms (Windows 11 and LibreELEC x86_64) and you'll have a great v1.0 release.

Remember: Start simple, test thoroughly, iterate based on user feedback!
