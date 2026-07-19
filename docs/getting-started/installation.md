## Endstone

ChatTriggers uses the Endstone modloader for Minecraft bedrock.

??? question "Why Endstone?"
    You can return any product within 30 days of purchase.
    Please ensure the item is in its original packaging.

## Installation Methods

### Method 1: PyPI Installation (Recommended)

The easiest way to install endstone-chat-triggers is through PyPI using pip.

#### Step 1: Install via pip

Open your terminal/command prompt and run:

```bash
pip install endstone-chat-triggers
```

#### Step 2: Copy to Plugins Folder

After installation, locate your Endstone server directory and copy the plugin to the plugins folder:

```bash
# The plugin should be copied to:
# {bedrock_server_path}/plugins/
```

On Windows, this might look like:
```
C:\path\to\bedrock_server\plugins\
```

On Linux, this might look like:
```
/path/to/bedrock_server/plugins/
```

#### Step 3: Start Your Server

Restart your Endstone server. The plugin will be automatically loaded during startup:

```bash
endstone
```

### Method 2: GitHub Releases (.whl Files)

For users who prefer to manually download releases or need a specific version.

#### Step 1: Download the .whl File

1. Visit the [Endstone Chat Triggers releases page](https://github.com/niko-at-chalupa/endstone-chat-triggers/releases)
2. Download the latest `.whl` file for your Python version
3. Choose the appropriate wheel file for your platform (Windows or Linux)

**Wheel naming convention:**
- `endstone_chat_triggers-X.X.X-cpXXX-cpXXX-*.whl`

Example files:
- `endstone_chat_triggers-1.0.1-cp311-cp311-win_amd64.whl` (Windows, Python 3.11)
- `endstone_chat_triggers-1.0.1-cp311-cp311-manylinux_x86_64.whl` (Linux, Python 3.11)

#### Step 2: Place in Plugins Folder

1. Navigate to your Endstone server directory
2. Locate the `plugins` folder (create it if it doesn't exist)
3. Copy the downloaded `.whl` file directly into the plugins folder

```
bedrock_server/
├── plugins/
│   └── endstone_chat_triggers-1.0.1-cp311-cp311-*.whl
├── server.properties
└── ...
```

#### Step 3: Start Your Server

Restart your Endstone server:

```bash
endstone
```

The plugin loader will automatically detect and load the `.whl` file.

## Installation Verification

After starting your server, check the console output for successful plugin loading. You should see:

```
[INFO] Loading plugin: Chat Triggers
[INFO] Chat Triggers v1.0.1 successfully loaded!
```

If the plugin doesn't load:
1. Verify the `.whl` file is in the correct plugins folder
2. Check that your Python version matches the wheel file (e.g., cp311 for Python 3.11)
3. Ensure Endstone version is v0.9.4 or later
4. Check server logs for error messages

## Updating the Plugin

### Via PyPI

To update to the latest version:

```bash
pip install --upgrade endstone-chat-triggers
```

Then restart your server.

### Via GitHub Releases

1. Download the new `.whl` file from releases
2. Remove the old `.whl` file from the plugins folder
3. Copy the new `.whl` file into the plugins folder
4. Restart your server

## Troubleshooting Installation Issues

### "Module not found" Error

**Problem:** Plugin fails to load with module not found error.

**Solutions:**
- Verify the `.whl` file is not corrupted by re-downloading it
- Ensure you're using the correct Python version for the wheel file
- Try installing dependencies: `pip install endstone`

### "Python 3.x is not supported" Error

**Problem:** Plugin reports incompatible Python version.

**Solution:**
- Upgrade to Python 3.10 or later
- Verify your Python installation: `python --version`

### Plugin Doesn't Load on Linux

**Problem:** Plugin loads on Windows but not on Linux.

**Solutions:**
- Verify you're using the `manylinux` wheel version
- Ensure Endstone is properly installed on Linux
- Check file permissions: `chmod +r endstone_chat_triggers-*.whl`

### Outdated Endstone Version

**Problem:** "Incompatible with Endstone version"

**Solution:**
- Update Endstone: `pip install --upgrade endstone`
- Verify installation: `endstone --version`

## Next Steps

After successful installation:

1. **Configure Workflows**: See [Configuration Guide](./CONFIGURATION.md) for setup instructions
2. **Create Your First Workflow**: Learn to create event-driven workflows in the configuration guide
3. **Connect to Twitch**: Configure your Twitch credentials for event handling
4. **Review Examples**: Check the documentation for workflow examples and best practices

## Getting Help

- **Official Documentation**: [https://niko-at-chalupa.github.io/endstone-chat-triggers/](https://niko-at-chalupa.github.io/endstone-chat-triggers/)
- **GitHub Issues**: Report problems at [https://github.com/niko-at-chalupa/endstone-chat-triggers/issues](https://github.com/niko-at-chalupa/endstone-chat-triggers/issues)
- **Endstone Documentation**: [https://endstone.dev/](https://endstone.dev/)

## Supported Endstone Versions

- Endstone 0.9.4+
- Python 3.10, 3.11, 3.12, 3.13+

The plugin follows Endstone's compatibility guidelines and is tested against the latest stable releases.