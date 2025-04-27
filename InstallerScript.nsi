# Request admin privileges
RequestExecutionLevel admin

ManifestDPIAware true

# Define the Application Name
Name "Personal Password Manager"

# Define the output installer file
OutFile "PersonalPasswordManagerInstaller.exe"

# Define the default installation directory
InstallDir "$PROGRAMFILES\PersonalPasswordManager"

# Request user input for the installation directory
Page Directory
Page InstFiles

# Define the installation section
Section "Install"
    # Set the installation directory
    SetOutPath "$INSTDIR"
    
    # Add the main application file
    File ".\PersonalPasswordManager.exe"

    # Create the AppData directory for storing user data and logs
    # Get the user's AppData directory (Roaming)
    StrCpy $0 $APPDATA
    StrCpy $0 "$0\PersonalPasswordManager"
    CreateDirectory $0

    # Create subdirectories under AppData for Data, Data_Backups, and Logs
    CreateDirectory "$0\Data"
    CreateDirectory "$0\Data_Backups"
    CreateDirectory "$0\Logs"

    # Add the files from the Data subdirectory
    SetOutPath "$0\Data"
    File /r ".\Data\*.*"

    # Write the uninstaller executable
    WriteUninstaller "$INSTDIR\Uninstall.exe"

    # Create a Start Menu shortcut in the current user's Roaming AppData
    StrCpy $0 "$APPDATA\Microsoft\Windows\Start Menu\Programs\Personal Password Manager.lnk"
    CreateShortCut $0 "$INSTDIR\PersonalPasswordManager.exe"

    # Write registry entries to register the app in Windows Programs list
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Personal Password Manager" "DisplayName" "Personal Password Manager"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Personal Password Manager" "UninstallString" "$INSTDIR\Uninstall.exe"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Personal Password Manager" "InstallLocation" "$INSTDIR"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Personal Password Manager" "DisplayVersion" "1.0"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Personal Password Manager" "Publisher" "Peter Zong"

    # Register the app for easy launching from Run dialog or Start Menu
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\App Paths\PersonalPasswordManager.exe" "" "$INSTDIR\PersonalPasswordManager.exe"
SectionEnd

Section "Uninstall"
    ExecWait 'taskkill /f /im PersonalPasswordManager.exe'

    # Remove installed files in Program Files directory
    Delete "$INSTDIR\PersonalPasswordManager.exe"

    # Remove Data, Data_Backups, and Logs files in AppData
    StrCpy $0 $APPDATA
    StrCpy $0 "$0\PersonalPasswordManager"

    # Delete files in the subdirectories under AppData
    Delete "$0\Data\*.*"
    Delete "$0\Data_Backups\*.*"
    Delete "$0\Logs\*.*"

    # Remove the empty subdirectories in AppData
    RMDir "$0\Data"
    RMDir "$0\Data_Backups"
    RMDir "$0\Logs"

    # Remove the main PersonalPasswordManager directory in AppData
    RMDir "$0"

    # Remove the uninstaller
    Delete "$INSTDIR\Uninstall.exe"

    # Remove the registry entries
    DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Personal Password Manager"
    DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\App Paths\PersonalPasswordManager.exe"

    # Remove the Start Menu shortcut
    StrCpy $1 "$APPDATA\Microsoft\Windows\Start Menu\Programs\Personal Password Manager.lnk"
    Delete $1

    # Remove the installation directory
    RMDir "$INSTDIR"
SectionEnd

# Launch the application immediately after the installation is complete
Function .onInstSuccess
    Exec "$INSTDIR\PersonalPasswordManager.exe"
FunctionEnd