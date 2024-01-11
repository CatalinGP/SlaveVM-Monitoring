$virtualBoxPath = "C:\Program Files\Oracle\VirtualBox\VirtualBox.exe"

if (Test-Path -Path $virtualBoxPath) {
    Write-Host "VirtualBox.exe found."

    $currentPath = [Environment]::GetEnvironmentVariable("PATH", [EnvironmentVariableTarget]::Machine)
    if ($currentPath -notcontains "C:\Program Files\Oracle\VirtualBox") {
        $newPath = $currentPath + ";C:\Program Files\Oracle\VirtualBox"
        [Environment]::SetEnvironmentVariable("PATH", $newPath, [EnvironmentVariableTarget]::Machine)
        Write-Host "VirtualBox directory added to PATH."
    } else {
        Write-Host "VirtualBox directory already in PATH."
    }
} else {
    Write-Host "VirtualBox.exe not found at $virtualBoxPath"
}
