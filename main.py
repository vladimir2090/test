import subprocess

def get_wifi_passwords():
    # Выполняем команду для получения списка профилей Wi-Fi
    try:
        profiles_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return {}

    print("Profiles data:")
    print(profiles_data)

    profiles = [line.split(":")[1].strip() for line in profiles_data.split('\n') if "All User Profile" in line]

    wifi_passwords = {}

    for profile in profiles:
        # Выполняем команду для получения информации о профиле Wi-Fi
        try:
            profile_info = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors="backslashreplace")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command for profile {profile}: {e}")
            continue

        print(f"Profile info for {profile}:")
        print(profile_info)

        # Ищем строку с паролем
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
        print(f"SSID: {profile}, Password: {password}")