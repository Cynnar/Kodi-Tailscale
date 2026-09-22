# Development Guide

This guide covers development, testing, and contribution guidelines for the Kodi Tailscale addon.

## Development Setup

### Prerequisites

- Python 3.8+ (matches Kodi 21 requirement)
- Git
- Access to:
  - Windows 11 machine for testing
  - LibreELEC device (or VM) for testing
- Kodi 21 (Omega) installed on test machines

### Local Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Kodi-Tailscale.git
   cd Kodi-Tailscale
   ```

2. **Install development dependencies** (optional, for testing outside Kodi)
   ```bash
   pip install requests
   ```

3. **Symlink to Kodi addons directory** (for live development)
   
   **Linux:**
   ```bash
   ln -s $(pwd)/plugin.program.tailscale ~/.kodi/addons/
   ```
   
   **Windows (Administrator PowerShell):**
   ```powershell
   New-Item -ItemType SymbolicLink -Path "$env:APPDATA\Kodi\addons\plugin.program.tailscale" -Target "$(pwd)\plugin.program.tailscale"
   ```

## Project Structure

```
plugin.program.tailscale/
├── addon.xml                    # Addon metadata and dependencies
├── default.py                   # Entry point - minimal, imports addon.py
├── LICENSE                      # MIT License
├── README.md                    # User documentation
├── INSTALL.md                   # Installation instructions
├── CHANGELOG.md                 # Version history
├── package.sh                   # Build script
│
├── resources/
│   ├── settings.xml             # Settings UI definition
│   │
│   ├── language/                # Localization
│   │   └── resource.language.en_gb/
│   │       └── strings.po       # English strings (30000-30999)
│   │
│   ├── lib/                     # Core addon logic
│   │   ├── __init__.py
│   │   ├── addon.py             # Main addon class (menu, routing)
│   │   ├── tailscale_manager.py # Tailscale operations (install, start, stop)
│   │   ├── wizard.py            # Setup wizard (multi-step UI)
│   │   └── nas_manager.py       # NAS source management (Kodi integration)
│   │
│   └── media/                   # Icons and images
│       ├── icon.png             # 512x512 addon icon
│       ├── fanart.jpg           # 1920x1080 background
│       ├── screenshot-01.jpg    # Screenshots for Kodi repo
│       ├── screenshot-02.jpg
│       └── *.png                # Menu item icons
```

## Code Architecture

### Module Responsibilities

**default.py**
- Entry point called by Kodi
- Instantiates and runs TailscaleAddon
- Minimal code to avoid blocking Kodi UI

**addon.py - TailscaleAddon**
- URL routing (`router()` method)
- Menu building (`build_main_menu()`)
- Coordinates between manager classes
- Handles user notifications

**tailscale_manager.py - TailscaleManager**
- Architecture detection
- Binary download and extraction
- Daemon lifecycle (start/stop/restart)
- Status checking
- Authentication URL generation
- Cross-platform path handling

**wizard.py - SetupWizard**
- Multi-step guided setup
- Progress dialogs
- User input collection
- Error handling with user feedback

**nas_manager.py - NASManager**
- NAS source wizard
- Kodi sources.xml manipulation
- JSON persistence for addon sources
- Connection testing

### Key Design Patterns

1. **Manager Pattern**: Separate managers for distinct concerns (Tailscale, NAS, Wizard)
2. **Dependency Injection**: Addon reference passed to managers
3. **Cross-Platform Abstraction**: OS detection with platform-specific code paths
4. **Progressive Enhancement**: Works without all features (e.g., can manage pre-installed Tailscale)

## Testing Strategy

### Test Matrix

| Platform | Architecture | Status |
|----------|-------------|---------|
| Windows 11 | x86_64 | Primary test platform |
| LibreELEC | x86_64 | Production target |
| LibreELEC | aarch64 | Secondary target |
| LibreELEC | armv7l | Tertiary target |

### Testing Workflow

#### Phase 1: Windows Development
1. Develop on Windows 11 with Kodi 21
2. Test all UI flows and wizards
3. Verify menu navigation
4. Test settings integration
5. Validate error handling

#### Phase 2: LibreELEC x86_64
1. Deploy to test device
2. Test binary download
3. Verify daemon starts correctly
4. Test authentication flow
5. Verify NAS source addition
6. Test connection management
7. Check log files for errors

#### Phase 3: ARM Testing
1. Deploy to ARM device (if available)
2. Verify correct binary download
3. Test all functionality
4. Check for architecture-specific issues

### Manual Test Cases

**Setup Wizard**
- [ ] First run automatically launches wizard
- [ ] System detection shows correct architecture
- [ ] Binary downloads successfully
- [ ] Progress bar updates during download
- [ ] Daemon starts (Linux only)
- [ ] Auto-start preference is saved
- [ ] Authentication URL displays correctly
- [ ] Completion message shows

**Connection Management**
- [ ] Start button starts Tailscale
- [ ] Stop button stops Tailscale
- [ ] Restart works correctly
- [ ] Status shows correct information
- [ ] Status updates when state changes

**NAS Source Management**
- [ ] Add source wizard guides through all steps
- [ ] Source appears in Kodi file manager
- [ ] Connection test works
- [ ] Source removal works
- [ ] Sources persist across restarts

**Settings**
- [ ] All settings are accessible
- [ ] Settings changes are saved
- [ ] Action buttons trigger correct functions
- [ ] Settings survive addon updates

### Logging

Enable Kodi debug logging for development:
```python
xbmc.log(f"Tailscale: Your message here", xbmc.LOGINFO)
xbmc.log(f"Tailscale: Error message", xbmc.LOGERROR)
```

View logs:
- **LibreELEC:** `tail -f /storage/.kodi/temp/kodi.log`
- **Windows:** `%APPDATA%\Kodi\kodi.log`

### Debugging Tips

1. **Check Kodi log first** - Most issues show up here
2. **Test outside wizard** - Use main menu actions to isolate issues
3. **Verify paths** - Print paths before file operations
4. **Test subprocess calls** - Verify commands work in terminal first
5. **Check permissions** - Especially on LibreELEC

## Adding Features

### Adding a New Menu Item

1. **Add string to `strings.po`**
   ```xml
   <string id="30XXX">My New Feature</string>
   ```

2. **Add menu item in `addon.py`**
   ```python
   self.add_menu_item(
       self.get_string(30XXX),
       {'action': 'my_new_action'},
       icon='resources/media/my_icon.png'
   )
   ```

3. **Add router case in `addon.py`**
   ```python
   elif action == 'my_new_action':
       self.my_new_action()
   ```

4. **Implement the action**
   ```python
   def my_new_action(self):
       # Your implementation
       pass
   ```

### Adding a New Setting

1. **Add to `settings.xml`**
   ```xml
   <setting id="my_setting" type="bool" label="30XXX" default="false"/>
   ```

2. **Access in code**
   ```python
   value = self.addon.getSetting('my_setting')
   self.addon.setSetting('my_setting', 'true')
   ```

### Adding Language Support

1. Create new language directory:
   ```bash
   mkdir -p resources/language/resource.language.de_de
   ```

2. Copy and translate `strings.po`

3. Test with Kodi set to that language

## Building for Distribution

### Create Release Package

```bash
cd plugin.program.tailscale
./package.sh
```

This creates `plugin.program.tailscale-X.X.X.zip` ready for distribution.

### Version Numbering

Follow Semantic Versioning (semver.org):
- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)
- Increment MAJOR for breaking changes
- Increment MINOR for new features
- Increment PATCH for bug fixes

Update version in:
1. `addon.xml` - version attribute
2. `CHANGELOG.md` - new version section

## Contributing

### Pull Request Process

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```
3. **Make your changes**
4. **Test thoroughly** on at least Windows and LibreELEC
5. **Update documentation** (README, CHANGELOG)
6. **Commit with clear messages**
   ```bash
   git commit -m "Add feature: description of feature"
   ```
7. **Push and create PR**
   ```bash
   git push origin feature/my-new-feature
   ```

### Code Style

- Follow PEP 8 for Python code
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use meaningful variable names
- Add comments for complex logic
- Document functions with docstrings

Example:
```python
def my_function(param1, param2):
    """
    Brief description of function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    """
    # Implementation
    pass
```

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Example:
```
feat: Add support for ARM architecture

- Detect ARM architecture variants
- Download correct binary for ARM devices
- Test on Raspberry Pi 4

Closes #123
```

## Release Checklist

- [ ] Update version in `addon.xml`
- [ ] Update `CHANGELOG.md`
- [ ] Test on Windows 11
- [ ] Test on LibreELEC x86_64
- [ ] Test wizard flow completely
- [ ] Test all menu functions
- [ ] Test settings changes
- [ ] Verify NAS source addition
- [ ] Check all strings display correctly
- [ ] Review logs for errors
- [ ] Run `package.sh`
- [ ] Test installation from ZIP
- [ ] Create GitHub release
- [ ] Upload ZIP to release
- [ ] Update README if needed

## Common Issues During Development

### Import Errors
- Ensure `__init__.py` exists in `resources/lib/`
- Check Python path if testing outside Kodi

### Dialog Not Showing
- Check for exceptions in Kodi log
- Verify string IDs exist in `strings.po`

### Settings Not Saving
- Verify setting ID matches in `settings.xml` and code
- Check addon profile directory exists

### Binary Download Fails
- Test URL manually with `curl` or browser
- Check network connectivity
- Verify architecture detection is correct

### Daemon Won't Start
- Check binary has execute permissions
- Verify paths are correct
- Look for errors in `tailscaled.log`
- Test command manually in terminal

## Resources

- **Kodi Addon Development:** https://kodi.wiki/view/Add-on_development
- **Kodi Python API:** https://codedocs.xyz/xbmc/xbmc/
- **Tailscale Documentation:** https://tailscale.com/kb/
- **LibreELEC Documentation:** https://wiki.libreelec.tv/

## Getting Help

- **Issues:** GitHub Issues for bug reports
- **Discussions:** GitHub Discussions for questions
- **Kodi Forums:** forum.kodi.tv for general Kodi questions
