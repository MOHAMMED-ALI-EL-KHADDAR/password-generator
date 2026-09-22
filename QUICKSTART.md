# Quick Start Guide

## Installation (1 minute)

```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
python main.py info
```

## 5 Essential Commands

### 1. Generate a Simple 16-Character Password
```bash
python main.py password
```
**Output**: A 16-character password with uppercase, lowercase, numbers, and special characters

### 2. Generate a Stronger 24-Character Password
```bash
python main.py password --length 24 --copy
```
**Output**: 24-character password copied to your clipboard

### 3. Generate a Memorable Master Password (Passphrase)
```bash
python main.py passphrase --words 6 --copy
```
**Output**: A 6-word passphrase like `correct-horse-battery-staple-example-zone`

### 4. Interactive Mode (Guided Setup)
```bash
python main.py password --interactive
```
**Output**: Step-by-step prompts for your preferences, then generates password

### 5. Learn About Password Security
```bash
python main.py info
```
**Output**: Security recommendations and entropy thresholds

---

## Common Scenarios

### Scenario: Password for Email Account
```bash
python main.py password --length 16 --copy
# Standard secure password, copied to clipboard
```

### Scenario: Master Password for Password Manager
```bash
python main.py passphrase --words 6 --copy
# Memorable yet extremely secure (66 bits entropy)
```

### Scenario: Maximum Security (Encryption Key)
```bash
python main.py password --length 48 --copy
# 48-character password with all character types
```

### Scenario: Simple Account (Low Security)
```bash
python main.py password --length 12 --no-special --copy
# Alphanumeric only for simple accounts
```

---

## Understanding the Output

### Example Password Output
```
┌────────────────────────────┐
│   Generated Password       │
├────────────────────────────┤
│ Password  │ aB7#mK9$xL2@qW │
│ Strength  │ Strong ●●●● │
│ Entropy   │ 105 bits       │
│ Recommend │ Excellent!     │
└────────────────────────────┘

✓ Password copied to clipboard
```

**What it means:**
- **Strength**: Strong (●●●●) = 80-128 bits = Excellent for most accounts
- **Entropy**: 105 bits = ~2.85 × 10³¹ possible combinations
- **Recommendation**: Safe for regular accounts

### Entropy Quick Reference
| Bits | Strength | Use Case |
|------|----------|----------|
| 40-50 | Weak | Temporary accounts only |
| 50-80 | Fair | Regular accounts |
| 80-128 | Strong | **Sensitive accounts** |
| 128+ | Very Strong | **Master passwords** |

---

## Pro Tips

### ✅ Do

1. **Use a password manager** to store generated passwords
   - Recommended: 1Password, Bitwarden, KeePass

2. **Generate strong passwords** for sensitive accounts
   ```bash
   python main.py password --length 24 --copy
   ```

3. **Use passphrases** for master passwords
   ```bash
   python main.py passphrase --words 7 --copy
   ```

4. **Enable 2FA/MFA** on important accounts
   - Email, banking, social media

5. **Close your terminal** after generating passwords
   - Clears terminal history

### ❌ Don't

1. ❌ Reuse passwords across different services
2. ❌ Store passwords in plain text files
3. ❌ Share passwords via email or chat
4. ❌ Trust browser password managers alone
5. ❌ Use predictable passwords (birthdate, pet names, etc.)

---

## Troubleshooting

### "Command not found: python"
Use `python3` instead:
```bash
python3 main.py password
```

### "No module named 'click'" or similar
Reinstall dependencies:
```bash
pip install -r requirements.txt
```

### Clipboard not working
**Linux users**: Install xclip
```bash
sudo apt-get install xclip  # Ubuntu/Debian
sudo dnf install xclip      # Fedora/RHEL
```

### Want to change password length?
```bash
python main.py password --length 32  # 32 characters instead of 16
```

---

## Next Steps

1. **Read the full README** for detailed documentation
   ```bash
   cat README.md
   ```

2. **Explore all options**
   ```bash
   python main.py password --help
   python main.py passphrase --help
   ```

3. **Integrate with password manager**
   - Set up 1Password, Bitwarden, or KeePass
   - Use this tool to generate strong passwords
   - Import into password manager

4. **Understand entropy** for informed decisions
   ```bash
   python main.py info
   ```

---

## Security Checklist

- [ ] Changed default passwords on critical accounts
- [ ] Generated strong passwords for each service
- [ ] Enabled 2FA/MFA on email, banking, social media
- [ ] Set up password manager (1Password, Bitwarden, KeePass)
- [ ] Closed terminal window after use
- [ ] Securely stored master password (memorized or encrypted)
- [ ] Reviewed `python main.py info` security recommendations

---

**Questions?** Refer to README.md for comprehensive documentation.
