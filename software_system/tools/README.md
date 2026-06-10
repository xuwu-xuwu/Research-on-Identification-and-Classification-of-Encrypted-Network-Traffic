# Local Tools

Optional location for external runtime tools.

To make live capture more portable, copy `tshark.exe` and its required Wireshark
runtime DLL files into this directory, then run:

```powershell
.\software_system\setup_portable_env.ps1 -SkipPackageInstall
```

If this directory is empty, the backend will auto-detect `tshark` from the host.
