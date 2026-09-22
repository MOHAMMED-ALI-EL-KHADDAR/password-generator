# Password Generator CLI

A **production-ready, cryptographically secure command-line password generator** with customizable criteria, entropy verification, clipboard integration, and comprehensive security best practices.

## 🔐 Security Guarantees

### Cryptographic Randomness

This tool uses **Python's `secrets` module** (not `random`), which provides cryptographically secure pseudo-random number generation (CSPRNG).

#### Why `secrets` > `random`

| Aspect | `random` | `secrets` |
|--------|----------|----------|
| **Algorithm** | Mersenne Twister (deterministic) | OS-level CSPRNG |
| **Seed-Safe** | Predictable if seeded | Unseeded & unpredictable |
| **Cryptographic Use** | ❌ Not suitable | ✅ Designed for cryptography |
| **Entropy Source** | Pseudo-random | True randomness (OS entropy) |

**Practical Implication**: With `random`, an attacker knowing the seed can predict all future passwords. With `secrets`, this is mathematically infeasible.

### Security Best Practices Implemented

✅ **No Password Logging**: Generated passwords are never written to disk or logs  
✅ **Clipboard Auto-Clear**: Clipboard is automatically cleared after 30 seconds  
✅ **Entropy Verification**: Every password is evaluated using `zxcvbn` strength checker  
✅ **Ambiguous Character Exclusion**: Removes l/1/I/O/0 to prevent typos  
✅ **Input Validation**: Strict bounds checking (4-256 character length)  
✅ **Thread-Safe Clipboard**: Daemon thread handles clipboard clearing safely  
✅ **No Dependencies on Insecure Libraries**: Explicit exclusion of `random`-based solutions  

## 📋 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Setup

```bash
# Clone or download the project
cd password-generator

# Install dependencies
pip install -r requirements.txt

# Make executable (Linux/macOS)
chmod +x main.py
```

## 🚀 Usage

### Basic Password Generation

```bash
# Generate a default 16-character password
python main.py password

# Generate a 24-character password
python main.py password --length 24

# Generate without special characters
python main.py password --no-special

# Copy to clipboard automatically
python main.py password --copy
```

### Interactive Mode

```bash
# Guided password configuration
python main.py password --interactive

# Guided passphrase generation
python main.py passphrase --interactive
```

### Passphrase Generation

```bash
# Generate a 4-word diceware passphrase
python main.py passphrase

# Generate a 6-word passphrase for higher entropy
python main.py passphrase --words 6

# Generate and copy to clipboard
python main.py passphrase --words 5 --copy
```

### Information & Education

```bash
# Display security information
python main.py info
```

## 📊 Command Reference

### `password` Command

Generate cryptographically secure random passwords.

**Options:**
```
--length, -l INTEGER          Length of password (4-256) [default: 16]
--uppercase / --no-uppercase  Include uppercase letters [default: True]
--lowercase / --no-lowercase  Include lowercase letters [default: True]
--numbers / --no-numbers      Include digits [default: True]
--special / --no-special      Include special characters [default: True]
--no-ambiguous / --allow-ambiguous
                              Exclude l,1,I,O,0 [default: True]
--copy / --no-copy            Copy to clipboard [default: False]
--interactive / --no-interactive
                              Interactive configuration [default: False]
```

**Examples:**
```bash
# Ultra-secure 32-character password with all character types
python main.py password --length 32

# Alphanumeric only (no special characters)
python main.py password --no-special

# Simple 12-character password for low-security accounts
python main.py password --length 12 --no-special

# Maximum security password (numbers + special + uppercase + lowercase)
python main.py password --length 24 --copy
```

### `passphrase` Command

Generate memorable diceware-style passphrases for master passwords.

**Options:**
```
--words, -w INTEGER           Number of words (3-10) [default: 4]
--copy / --no-copy            Copy to clipboard [default: False]
--interactive / --no-interactive
                              Interactive mode [default: False]
```

**Examples:**
```bash
# Standard 4-word passphrase (~44 bits of entropy)
python main.py passphrase

# 6-word passphrase for master password (~66 bits of entropy)
python main.py passphrase --words 6 --copy

# 5-word passphrase, copy to clipboard
python main.py passphrase --words 5 --copy
```

### `info` Command

Display comprehensive security information.

```bash
python main.py info
```

## 📈 Entropy & Security Levels

### Understanding Password Entropy

Entropy (measured in **bits**) quantifies password randomness:
- Each bit doubles computational effort to crack via brute force
- 64 bits = ~18.4 quintillion combinations

### Recommended Entropy by Use Case

| Use Case | Recommended Bits | Example Length |
|----------|------------------|-----------------|
| Temporary account | 40 bits | 8-char alphanumeric |
| Low-security account | 50 bits | 10-char alphanumeric |
| Regular account | 80 bits | 16-char (all types) |
| **Master password** | **128+ bits** | **6-word passphrase** |
| Encryption key | **256 bits** | **48-char password** |

### Calculating Entropy

```
Entropy (bits) = log₂(pool_size) × password_length

Example: 16-char password with 94 possible characters
Entropy = log₂(94) × 16 ≈ 105 bits
```

This tool automatically calculates entropy for each generated password.

## 🛡️ Clipboard Security

### Auto-Clear Behavior

```
Timeline:
0s:  Password copied to clipboard
5s:  Password remains in clipboard
20s: Password still in clipboard
30s: ✓ Clipboard automatically cleared
31s: Clipboard is empty
```

### Limitations

- **X11/Wayland (Linux)**: Clipboard managers may retain history
- **macOS**: System clipboard is secure; no retention after clear
- **Windows**: Clipboard history feature may bypass clearing

**Recommendation**: Close your terminal window after use to clear history.

## 🔍 Output Interpretation

### Strength Ratings

```
Very Weak (●)
├─ Score: 0
├─ Bits: < 40
└─ Action: Use longer password or more character types

Weak (●●)
├─ Score: 1
├─ Bits: 40-60
└─ Action: Increase length or complexity

Fair (●●●)
├─ Score: 2
├─ Bits: 60-80
└─ Action: Good for most accounts

Strong (●●●●)
├─ Score: 3
├─ Bits: 80-128
└─ Action: Excellent for sensitive accounts

Very Strong (●●●●●)
├─ Score: 4
├─ Bits: 128+
└─ Action: Maximum security (master passwords)
```

## 🏗️ Architecture & Design

### Core Components

```
main.py
├── PasswordGenerator
│   ├── generate_password()    → Cryptographically secure random password
│   ├── generate_passphrase()  → Diceware-style memorable passphrase
│   └── check_strength()       → zxcvbn strength evaluation
├── ClipboardManager
│   ├── copy_to_clipboard()    → Secure clipboard copy
│   └── _schedule_clipboard_clear()  → Timeout clearing
└── CLI Commands
    ├── password               → Password generation
    ├── passphrase             → Passphrase generation
    └── info                   → Security information
```

### Cryptographic Flow

```python
# 1. Define character pool
char_pool = string.ascii_letters + string.digits + string.punctuation

# 2. Remove ambiguous characters
char_pool = [c for c in char_pool if c not in AMBIGUOUS_CHARS]

# 3. Generate using CSPRNG (secrets module)
password = "".join(secrets.choice(char_pool) for _ in range(length))
         # ^ cryptographically secure random choice

# 4. Evaluate strength (zxcvbn)
result = zxcvbn(password)

# 5. Display with entropy calculation
entropy = log₂(len(char_pool)) × length
```

## 🧪 Testing & Validation

### Recommended Tests

```bash
# Test password generation
python main.py password --length 16 --copy

# Test passphrase generation
python main.py passphrase --words 4 --copy

# Test without special characters
python main.py password --length 12 --no-special

# Test without ambiguous characters
python main.py password --no-ambiguous

# Test maximum length
python main.py password --length 256

# Test interactive mode
python main.py password --interactive
```

## 📚 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `click` | 8.1.7+ | CLI framework |
| `rich` | 13.7.0+ | Rich terminal output (tables, panels) |
| `zxcvbn` | 4.4.28+ | Password strength evaluation |
| `pyperclip` | 1.8.2+ | Cross-platform clipboard access |

### Why These Dependencies?

- **click**: Industry-standard CLI creation with minimal boilerplate
- **rich**: Professional terminal UI (tables, panels, colors)
- **zxcvbn**: Dropbox's battle-tested password strength library
- **pyperclip**: Reliable clipboard access on Windows/macOS/Linux

## ⚠️ Security Warnings

### Never

❌ Store passwords in plain text files  
❌ Commit passwords to version control  
❌ Share passwords via email or chat  
❌ Use the same password across multiple services  
❌ Trust browser password managers alone (use dedicated managers)  

### Do

✅ Use a password manager (1Password, Bitwarden, KeePass, Dashlane)  
✅ Enable 2FA/MFA on all critical accounts  
✅ Rotate passwords for sensitive accounts annually  
✅ Use unique passwords for each service  
✅ Keep this tool in a secure location  
✅ Close terminal window after use (clears history)  

## 🔧 Advanced Configuration

### Custom Diceware Word List

To use a custom word list, modify the `DICEWARE_WORDS` constant in `main.py`:

```python
DICEWARE_WORDS = [
    "custom", "word", "list", "here", ...
]
```

**Requirement**: List must contain 1000+ words (≥10 bits per word)

### Adjusting Clipboard Timeout

Modify `ClipboardManager` initialization in `main.py`:

```python
# 60-second clipboard timeout instead of 30
clipboard = ClipboardManager(timeout_seconds=60)
```

## 📖 Further Reading

### Educational Resources

- **NIST Password Guidelines**: https://pages.nist.gov/800-63-3/sp800-63b.html
- **zxcvbn Library**: https://github.com/dropbox/zxcvbn
- **Python secrets Module**: https://docs.python.org/3/library/secrets.html
- **EFF Diceware**: https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases

### Password Managers (Recommended)

- [1Password](https://1password.com/) — Commercial, excellent UX
- [Bitwarden](https://bitwarden.com/) — Open-source, self-hostable
- [KeePass](https://keepass.info/) — Desktop-only, offline
- [Dashlane](https://www.dashlane.com/) — Feature-rich, mobile-friendly

## 🐛 Troubleshooting

### Issue: "zxcvbn not installed" warning

**Solution**: Install zxcvbn
```bash
pip install zxcvbn
```

### Issue: Clipboard not working on Linux

**Requirement**: Ensure `xclip` or `xsel` is installed
```bash
# Ubuntu/Debian
sudo apt-get install xclip

# Fedora/RHEL
sudo dnf install xclip

# Arch
sudo pacman -S xclip
```

### Issue: "No valid characters available" error

**Cause**: All character types excluded or ambiguous characters removed
**Solution**: Disable `--no-ambiguous` or enable more character types

```bash
python main.py password --allow-ambiguous
```

## 📄 License

This project is provided as-is for educational and personal security purposes.

## 🤝 Contributing

For security issues, do **not** open public issues. Security matters should be reported privately.

---

**Last Updated**: 2024  
**Python Version**: 3.10+  
**Cryptographic Standard**: CSPRNG (secrets module)
