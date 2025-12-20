# Keylights

Control Elgato Key Lights from the command line with a simple Python script and a JSON config.

## Files

- `keylights.py`: entry point wrapper (runs the package in `src/`)
- `src/keylights/`: implementation modules
- `keylights.conf`: JSON config with your light aliases

Example config:

```json
{
  "lights": [
    { "alias": "one", "host": "192.168.1.50", "port": 9123 },
    { "alias": "two", "host": "192.168.1.51" }
  ]
}
```

## Quick start

```bash
git clone <your-repo-url>
cd pykeylight
```

Create `keylights.conf`:

```json
{
  "lights": [
    { "alias": "left", "host": "192.168.1.50", "port": 9123 },
    { "alias": "right", "host": "192.168.1.51" }
  ]
}
```

Run it:

```bash
python keylights.py on
python keylights.py left -a on
python keylights.py toggle
```

## Usage

```bash
keylights
keylights on
keylights off
keylights toggle
keylights left -a on
keylights right off
```

## Add a global command

### Windows Terminal (PowerShell profile)

Edit your PowerShell profile and add a function that calls the script. Replace the paths.

```powershell
function keylights {
    & py -3 "C:\path\to\keylights.py" --config "C:\path\to\keylights.conf" @args
}
```

Apply changes:

```powershell
. $PROFILE
```

### kitty (macOS/Linux)

Add a shell function in your profile (for bash/zsh). Replace the paths.

```bash
keylights() {
  /path/to/keylights.py --config /path/to/keylights.conf "$@"
}
```

Reload your shell:

```bash
source ~/.bashrc
```

If you use zsh, replace `~/.bashrc` with `~/.zshrc`.

you may need to make the keylights executable on linux `chmod +x keylights.py`
