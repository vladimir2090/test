import subprocess

def get_wifi_passwords():
    # Execute command to get list of Wi-Fi profiles
    try:
        profiles_data = subprocess.check_output(['netsh', 'wlan', 'how', 'profiles']).decode('utf-8', errors="backslashreplace")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return {}

    print("Profiles data:")
    print(profiles_data)

    profiles = [line.split(":")[1].strip() for line in profiles_data.split('\n') if "All User Profile" in line]

    wifi_passwords = {}

    for profile in profiles:
        # Execute command to get information about Wi-Fi profile
        try:
            profile_info = subprocess.check_output(['netsh', 'wlan', 'how', 'profile', profile, 'key=clear']).decode('utf-8', errors="backslashreplace")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command for profile {profile}: {e}")
            continue

        print(f"Profile info for {profile}:")
        print(profile_info)

        # Find line with password
        password_line = [line for line in profile_info.split('\n') if "Key Content" in line]

        if password_line:
            password = password_line[0].split(":")[1].strip()
            wifi_passwords[profile] = password
        else:
            wifi_passwords[profile] = None

    return wifi_passwords

if __name__ == "__main__":
    passwords = get_wifi_passwords()
    for profile, password in passwords.items():
        print(f"SSID: {profile}, Password: {'*' * len(password) if password else 'No password'}")