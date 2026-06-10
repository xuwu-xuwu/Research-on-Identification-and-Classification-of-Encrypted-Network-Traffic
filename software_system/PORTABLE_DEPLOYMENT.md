# Portable Deployment

This software runtime keeps Python dependencies inside `software_system/.venv`.
Use this when moving the project to another Windows host.

## Install Local Dependencies

Run from the project root:

```powershell
.\software_system\setup_portable_env.ps1
```

The script will:

- create `software_system/.venv`
- install packages from `software_system/requirements.txt`
- create or update `software_system/.env`
- auto-detect the host `tshark` executable

Start the backend with:

```powershell
.\software_system\start_backend.ps1
```

## tshark Discovery Order

The backend and setup script search for `tshark` in this order:

- `software_system\tools\tshark.exe`
- `software_system\bin\tshark.exe`
- `EIM_TSHARK_PATH` or `TSHARK_PATH`
- system `PATH`
- Windows App Paths registry
- host Wireshark install folders

For a more portable package, put `tshark.exe` and the required Wireshark DLL files
under `software_system\tools\`, then rerun:

```powershell
.\software_system\setup_portable_env.ps1 -SkipPackageInstall
```

If no `tshark` is detected, live capture will stay unavailable until Wireshark,
Npcap, or a local `software_system\tools\tshark.exe` is available.
