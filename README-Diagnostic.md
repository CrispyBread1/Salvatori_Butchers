# ManageMeStock Diagnostic

Copy diagnostic.spec and diagnostic_hook.py beside main.py. Copy the supplied
.github/workflows/build-windows-diagnostic.yml into that exact folder in your repo.
Keep your existing main.spec and Build and Release workflow.

Commit the files. GitHub normally needs this manual workflow on the default branch
before it appears in Actions. Open Actions > Build Windows Diagnostic > Run workflow,
select the branch containing all three files, then run it. Download the
ManageMeStock-Diagnostic artifact from the completed run and extract it on Server 69.
Double-click ManageMeStock-Diagnostic.exe using your normal account.

This build uses your existing GitHub production secrets and explicitly sets
APP_ENV=production. It is NOT a dummy-data or read-only build: normal app actions can
change live data. It does not alter TLS certificate verification.

The console shows Python startup output. Logs are saved to
%LOCALAPPDATA%\ManageMeStock-Diagnostic\logs (paste into File Explorer's address bar).
If unavailable, the logger tries the same subfolder under the user's temporary
directory. The console waits for Enter after ordinary Python shutdown, including
most unhandled Python exceptions.

The executable contains the bundled .env, including production credentials and
the service-role key, matching your current packaging approach. Keep the download
restricted to trusted operators; Actions artifacts are not a secret vault and
access depends on repository permissions. Do not publish this EXE publicly.
Review logs for credentials or customer data before sharing: existing application
code may print sensitive values. The hook itself does not print configuration values.

Logging starts once the Python runtime and this hook are reached. It cannot log
Windows execution-policy blocks or earlier bootloader/extraction failures. Native
crashes may produce a partial log and may close the console. This is not a way to
bypass server restrictions; if execution is blocked, the administrator must review it.

The build uses Python 3.9 as in your existing workflow and pins PyInstaller 6.20.0.
It installs your listed dependencies plus requirements.txt when present; failed
requirements installation stops the build. The spec uses PyInstaller 6 syntax.
It does not launch the live app during CI.

Validation here: Python/spec syntax and workflow YAML checked; startup-hook normal
exit and exception logging checked in a local subprocess. The actual Windows build
and full app need to be verified in your GitHub run and on Server 69, since the
application source and Windows server are not available in this workspace.
