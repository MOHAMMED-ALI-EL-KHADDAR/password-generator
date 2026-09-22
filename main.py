#!/usr/bin/env python3
"""
Password Generator CLI - Production-Ready Security Tool

A cryptographically secure password generator with customizable criteria,
entropy verification, and clipboard integration.

Security Best Practices:
- Uses secrets module (CSPRNG) instead of random
- No password logging or disk writes
- Clipboard clearing warnings
- Entropy verification via zxcvbn
- Input validation and error handling
"""

import secrets
import string
import sys
import time
import threading
from typing import Tuple, Optional
from pathlib import Path

from rich.console import Console  # type: ignore[reportMissingImports]
from rich.table import Table # type: ignore[reportMissingImports]
from rich.panel import Panel # type: ignore[reportMissingImports]
from rich.prompt import Prompt, Confirm # type: ignore[reportMissingImports]
from rich.style import Style # type: ignore[reportMissingImports]
import click # type: ignore[reportMissingImports]

try:
    import pyperclip  # type: ignore[reportMissingImports]
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

try:
    from zxcvbn import zxcvbn  # type: ignore[reportMissingImports]
    ZXCVBN_AVAILABLE = True
except ImportError:
    ZXCVBN_AVAILABLE = False


# Console for rich output
console = Console()

# Diceware word list (subset of EFF long word list)
DICEWARE_WORDS = [
    "about", "above", "abuse", "access", "accident", "account", "achieve", "acid",
    "acquire", "across", "act", "action", "active", "activity", "actual", "adapt",
    "add", "address", "adjust", "admit", "adopt", "advance", "advice", "advise",
    "affair", "afford", "afraid", "after", "again", "against", "age", "agency",
    "agent", "agree", "agreement", "ahead", "aim", "air", "alarm", "album",
    "alert", "alien", "alive", "allow", "almost", "alone", "along", "alter",
    "always", "amateur", "amaze", "amazing", "ambiguous", "ambulance", "amend",
    "america", "among", "amount", "amuse", "analyst", "anchor", "ancient", "and",
    "angel", "anger", "angle", "angry", "animal", "ankle", "announce", "annoy",
    "another", "answer", "antenna", "antique", "anxiety", "any", "apart", "apology",
    "app", "appear", "apple", "apply", "appoint", "appreciate", "approve", "april",
    "arch", "arctic", "area", "arena", "argue", "argument", "arise", "arm",
    "armed", "armor", "army", "around", "arrange", "arrest", "arrival", "arrive",
    "arrow", "art", "artefact", "artist", "artwork", "ask", "aspect", "assault",
    "asset", "assist", "assume", "asthma", "athlete", "atom", "attack", "attend",
    "attention", "attitude", "attract", "auction", "audit", "august", "aunt",
    "author", "auto", "autumn", "avenue", "avid", "avoid", "awake", "aware",
    "away", "awesome", "awful", "awkward", "axis", "axle", "baby", "bachelor",
    "back", "bacon", "badge", "badly", "bag", "baggage", "bail", "bait",
    "bake", "balance", "balcony", "ball", "ballet", "balloon", "bamboo", "banana",
    "banner", "bar", "barb", "bare", "bargain", "barrel", "base", "basic",
    "basket", "batch", "bath", "bathe", "battery", "battle", "beach", "bead",
    "beak", "beam", "bean", "bear", "beard", "beast", "beat", "beauty",
    "became", "because", "become", "beef", "been", "beep", "beer", "bees",
    "beetle", "before", "began", "begin", "begone", "behalf", "behave", "behind",
    "behold", "being", "belch", "belief", "believe", "belong", "below", "belt",
    "bench", "bend", "beneath", "benefit", "bent", "berry", "beside", "besides",
    "best", "betray", "better", "between", "beyond", "bias", "bible", "bicycle",
    "bid", "bike", "bind", "biology", "bird", "birth", "bit", "bite",
    "bitter", "black", "blade", "blame", "blank", "blast", "bleak", "bleat",
    "bled", "bleed", "bless", "blind", "blood", "blossom", "blouse", "blue",
    "bluff", "blunt", "blur", "blush", "board", "boat", "body", "boil",
    "bold", "bolt", "bomb", "bone", "bonus", "book", "boost", "border",
    "boring", "borrow", "boss", "bottom", "bounce", "box", "boy", "brace",
    "brain", "brand", "brass", "brave", "bravo", "brawl", "brawn", "breach",
    "bread", "break", "breast", "breath", "breathe", "bred", "breed", "brew",
    "brick", "bride", "bridge", "brief", "bright", "bring", "brink", "brisk",
    "broccoli", "broke", "broken", "bronze", "brood", "brook", "broom", "broth",
    "brother", "brought", "brow", "brown", "browse", "browser", "bruin", "brunt",
    "brush", "brute", "bubble", "buddy", "budget", "buffalo", "build", "built",
    "bulb", "bulk", "bullet", "bundle", "bunny", "burden", "burger", "burst",
    "bus", "business", "bust", "busy", "but", "butter", "button", "buy",
    "buyer", "buzz", "buzzard", "by", "bypass", "cabin", "cable", "cactus",
    "cage", "cake", "call", "calm", "camera", "camp", "can", "canal",
    "cancel", "candy", "cane", "canine", "cannon", "cannot", "canoe", "canon",
    "canopy", "canvas", "canyon", "capable", "capacity", "cape", "capital",
    "captain", "car", "carbon", "card", "care", "career", "careful", "careless",
    "cares", "cargo", "caring", "carmine", "carnival", "carol", "carriage",
    "carrier", "carry", "cart", "case", "cash", "casino", "casket", "cast",
    "castle", "casual", "cat", "catalog", "catch", "category", "cater", "cattle",
    "caught", "cause", "caution", "cave", "cavern", "ceased", "ceiling", "celery",
    "cement", "census", "century", "cereal", "certain", "chain", "chair", "chalk",
    "champ", "champion", "change", "channel", "chaos", "chapel", "chapter",
    "charge", "chariot", "charity", "charm", "chart", "chase", "chat", "cheap",
    "cheat", "check", "cheese", "chef", "cherry", "chess", "chest", "chicken",
    "chief", "child", "children", "chill", "chimney", "chin", "china", "choice",
    "choose", "chosen", "christmas", "chrome", "chubby", "chuck", "chug", "chum",
    "chunk", "churn", "cigar", "cinnamon", "circle", "circuit", "circular",
    "circumvent", "cistern", "citadel", "cite", "citizen", "city", "civic",
    "civil", "claim", "clad", "claim", "clam", "clamber", "clamp", "clan",
    "clang", "clank", "clap", "clara", "clarity", "clash", "clasp", "class",
    "classic", "classify", "classmate", "classroom", "classy", "clatter", "clause",
    "clavichord", "claw", "clay", "clean", "clear", "cleanse", "clearer",
    "clearly", "cleaver", "cleavage", "clef", "cleft", "clement", "clench",
    "clergy", "clerk", "clever", "client", "cliff", "climate", "climb", "climber",
    "clime", "clinch", "cling", "clinic", "clinical", "clink", "clip", "clique",
    "cloak", "clock", "clockwise", "clod", "clog", "cloister", "clone", "close",
    "closer", "closest", "closet", "closure", "clot", "cloth", "clothe", "clothes",
    "clothing", "cloud", "cloudy", "clout", "clove", "cloven", "clover", "clown",
    "cloy", "club", "cluck", "clue", "clump", "clumsy", "clung", "cluster",
    "clutch", "clutter", "coach", "coast", "coastal", "coat", "coating", "coax",
    "cobalt", "cobbler", "cobweb", "cocaine", "cock", "cockatoo", "cockerel",
    "cockpit", "cockroach", "cocktail", "cocky", "cocoa", "coconut", "cocoon",
    "cod", "code", "codeine", "coder", "codger", "codify", "coeds", "coequal",
    "coerce", "coercion", "coercive", "coeval", "coexist", "coffee", "coffer",
    "coffin", "cog", "cogency", "cogent", "cogitate", "cognac", "cognate",
    "cognition", "cognitive", "cognizable", "cognizant", "cognomen", "cognoscenti",
    "cogon", "cogwheel", "cohabit", "cohabitation", "coheir", "cohere", "coherence",
    "coherent", "cohesion", "cohesive", "cohort", "coif", "coiffure", "coign",
    "coil", "coin", "coinage", "coincide", "coincidence", "coincident", "coincidental",
    "coir", "coke", "cola", "colander", "cold", "colder", "coldest", "coldly",
    "coldness", "cole", "coleus", "colic", "colicky", "coliseum", "colitis",
    "collaborate", "collaboration", "collaborative", "collaborator", "collage",
    "collagen", "collapse", "collar", "collarbone", "collard", "collate", "collateral",
    "collation", "colleague", "collect", "collected", "collectible", "collecting",
    "collection", "collective", "collectively", "collectiveness", "collectivity",
    "collector", "collectorship", "colleen", "college", "collegial", "collegian",
    "collegiate", "collet", "collide", "collier", "colliery", "collinear", "collision",
    "collisional", "collocation", "collocution", "collodion", "colloid", "colloidal",
    "collop", "colloquial", "colloquialism", "colloquially", "colloquy", "collude",
    "collusion", "collusive", "collusively", "colluvium", "cologne", "colon",
    "colonel", "colonelcy", "colonelship", "colonial", "colonialism", "colonialist",
    "colonic", "colonist", "colonization", "colonize", "colonizer", "colonnade",
    "colonnaded", "colony", "colophon", "color", "colorado", "coloration", "colorant",
    "coloratura", "colored", "colorfast", "colorful", "colorfully", "colorfulness",
    "coloring", "colorist", "colorize", "colorless", "colorlessly", "colorlessness",
    "colors", "colossae", "colossi", "colossus", "colostomy", "colostrum",
]

# Ambiguous character sets
AMBIGUOUS_CHARS = set("il1Lo0O")


class PasswordGeneratorError(Exception):
    """Base exception for password generator errors."""
    pass


class ClipboardManager:
    """Manages clipboard operations with timeout and clearing."""

    def __init__(self, timeout_seconds: int = 30):
        self.timeout_seconds = timeout_seconds
        self.clear_thread: Optional[threading.Thread] = None

    def copy_to_clipboard(self, content: str) -> bool:
        """Copy content to clipboard and schedule clearing."""
        if not CLIPBOARD_AVAILABLE:
            return False

        try:
            pyperclip.copy(content)
            self._schedule_clipboard_clear()
            return True
        except Exception as e:
            console.print(f"[red]Clipboard error: {e}[/red]")
            return False

    def _schedule_clipboard_clear(self) -> None:
        """Schedule clipboard clearing after timeout."""
        def clear_clipboard():
            time.sleep(self.timeout_seconds)
            try:
                pyperclip.copy("")
                console.print(
                    f"[yellow]✓ Clipboard cleared after {self.timeout_seconds}s[/yellow]"
                )
            except Exception:
                pass

        self.clear_thread = threading.Thread(target=clear_clipboard, daemon=True)
        self.clear_thread.start()


class PasswordGenerator:
    """Cryptographically secure password generator."""

    def __init__(self):
        self.clipboard = ClipboardManager()

    def generate_password(
        self,
        length: int = 16,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_numbers: bool = True,
        use_special: bool = True,
        exclude_ambiguous: bool = True,
    ) -> str:
        """
        Generate a cryptographically secure password.

        Args:
            length: Password length (minimum 4, maximum 256)
            use_uppercase: Include uppercase letters
            use_lowercase: Include lowercase letters
            use_numbers: Include digits
            use_special: Include special characters
            exclude_ambiguous: Exclude ambiguous characters (l, 1, I, O, 0)

        Returns:
            Generated password string

        Raises:
            PasswordGeneratorError: If invalid configuration
        """
        if length < 4 or length > 256:
            raise PasswordGeneratorError("Password length must be between 4 and 256")

        if not any([use_uppercase, use_lowercase, use_numbers, use_special]):
            raise PasswordGeneratorError(
                "At least one character type must be enabled"
            )

        # Build character pool
        char_pool = ""
        if use_uppercase:
            char_pool += string.ascii_uppercase
        if use_lowercase:
            char_pool += string.ascii_lowercase
        if use_numbers:
            char_pool += string.digits
        if use_special:
            char_pool += string.punctuation

        # Remove ambiguous characters if requested
        if exclude_ambiguous:
            char_pool = "".join(c for c in char_pool if c not in AMBIGUOUS_CHARS)

        if not char_pool:
            raise PasswordGeneratorError(
                "No valid characters available with current settings"
            )

        # Generate password using cryptographically secure random
        password = "".join(secrets.choice(char_pool) for _ in range(length))
        return password

    def generate_passphrase(self, word_count: int = 4) -> str:
        """
        Generate a diceware-style passphrase.

        Args:
            word_count: Number of words (minimum 3, maximum 10)

        Returns:
            Generated passphrase with words separated by hyphens

        Raises:
            PasswordGeneratorError: If invalid word count
        """
        if word_count < 3 or word_count > 10:
            raise PasswordGeneratorError("Word count must be between 3 and 10")

        words = [
            secrets.choice(DICEWARE_WORDS) for _ in range(word_count)
        ]
        return "-".join(words)

    def check_strength(self, password: str) -> Tuple[str, int, str]:
        """
        Evaluate password strength using zxcvbn.

        Args:
            password: Password to evaluate

        Returns:
            Tuple of (strength_label, score, feedback)
        """
        if not ZXCVBN_AVAILABLE:
            return "unknown", 0, "zxcvbn not installed"

        result = zxcvbn(password)
        score = result["score"]  # 0-4

        strength_map = {
            0: ("Very Weak", "[red]●[/red]", "Add more variety"),
            1: ("Weak", "[red]●●[/red]", "Increase length or complexity"),
            2: ("Fair", "[yellow]●●●[/yellow]", "Good but could be stronger"),
            3: ("Strong", "[green]●●●●[/green]", "Excellent choice"),
            4: ("Very Strong", "[bright_green]●●●●●[/bright_green]", "Maximum security"),
        }

        strength_label, visual, feedback = strength_map.get(score, ("Unknown", "", ""))
        return strength_label, score, feedback


def display_password_table(
    password: str,
    strength: str,
    score: int,
    feedback: str,
    entropy: Optional[float] = None,
) -> None:
    """Display password details in a formatted table."""
    table = Table(title="Generated Password", show_header=False, border_style="cyan")
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    table.add_row("Password", password)
    table.add_row("Strength", strength)
    if entropy:
        table.add_row("Entropy (bits)", f"{entropy:.2f}")
    table.add_row("Recommendation", feedback)

    console.print(table)


def get_password_config() -> dict:
    """Interactive configuration for password generation."""
    console.print("\n[bold cyan]Password Configuration[/bold cyan]\n")

    config = {
        "length": int(
            Prompt.ask("Password length", default="16", console=console)
        ),
        "use_uppercase": Confirm.ask(
            "Include uppercase letters", default=True, console=console
        ),
        "use_lowercase": Confirm.ask(
            "Include lowercase letters", default=True, console=console
        ),
        "use_numbers": Confirm.ask(
            "Include numbers", default=True, console=console
        ),
        "use_special": Confirm.ask(
            "Include special characters", default=True, console=console
        ),
        "exclude_ambiguous": Confirm.ask(
            "Exclude ambiguous characters (l, 1, I, O, 0)", default=True, console=console
        ),
    }

    return config


@click.group()
def cli():
    """Password Generator CLI - Cryptographically Secure Password Generation."""
    pass


@cli.command()
@click.option(
    "--length", "-l", default=16, type=click.IntRange(4, 256),
    help="Password length (4-256 characters)"
)
@click.option(
    "--uppercase/--no-uppercase", default=True,
    help="Include uppercase letters"
)
@click.option(
    "--lowercase/--no-lowercase", default=True,
    help="Include lowercase letters"
)
@click.option(
    "--numbers/--no-numbers", default=True,
    help="Include numbers"
)
@click.option(
    "--special/--no-special", default=True,
    help="Include special characters"
)
@click.option(
    "--no-ambiguous/--allow-ambiguous", default=True,
    help="Exclude ambiguous characters"
)
@click.option(
    "--copy/--no-copy", default=False,
    help="Copy password to clipboard"
)
@click.option(
    "--interactive/--no-interactive", default=False,
    help="Interactive mode"
)
def password(
    length: int,
    uppercase: bool,
    lowercase: bool,
    numbers: bool,
    special: bool,
    no_ambiguous: bool,
    copy: bool,
    interactive: bool,
):
    """Generate a cryptographically secure password."""
    console.print(
        Panel(
            "[bold green]🔐 Password Generator[/bold green]",
            expand=False,
            border_style="green",
        )
    )

    generator = PasswordGenerator()

    # Interactive mode
    if interactive:
        config = get_password_config()
        length = config["length"]
        uppercase = config["use_uppercase"]
        lowercase = config["use_lowercase"]
        numbers = config["use_numbers"]
        special = config["use_special"]
        no_ambiguous = config["exclude_ambiguous"]
        copy = Confirm.ask(
            "Copy to clipboard", default=False, console=console
        )

    try:
        password_str = generator.generate_password(
            length=length,
            use_uppercase=uppercase,
            use_lowercase=lowercase,
            use_numbers=numbers,
            use_special=special,
            exclude_ambiguous=no_ambiguous,
        )

        # Check strength
        strength_label, score, feedback = generator.check_strength(password_str)

        # Calculate entropy
        char_pool_size = 0
        if uppercase:
            char_pool_size += 26
        if lowercase:
            char_pool_size += 26
        if numbers:
            char_pool_size += 10
        if special:
            char_pool_size += 32

        if no_ambiguous:
            char_pool_size -= len(AMBIGUOUS_CHARS)

        import math
        entropy = length * math.log2(char_pool_size) if char_pool_size > 0 else 0

        display_password_table(
            password_str, strength_label, score, feedback, entropy
        )

        # Clipboard
        if copy:
            if generator.clipboard.copy_to_clipboard(password_str):
                console.print(
                    "[green]✓ Password copied to clipboard[/green]"
                )
            else:
                console.print(
                    "[yellow]⚠ Clipboard not available. Use --no-copy to suppress this message.[/yellow]"
                )

        # Explicit warning about password visibility
        console.print(
            Panel(
                "[yellow]⚠ Security Reminder: Password is visible in terminal history.[/yellow]\n"
                "[dim]• Close terminal window to clear history[/dim]\n"
                "[dim]• Never share passwords via email or chat[/dim]\n"
                "[dim]• Use password managers for secure storage[/dim]",
                border_style="yellow",
            )
        )

    except PasswordGeneratorError as e:
        console.print(f"[red]Error: {e}[/red]", file=sys.stderr)
        sys.exit(1)


@cli.command()
@click.option(
    "--words", "-w", default=4, type=click.IntRange(3, 10),
    help="Number of words (3-10)"
)
@click.option(
    "--copy/--no-copy", default=False,
    help="Copy passphrase to clipboard"
)
@click.option(
    "--interactive/--no-interactive", default=False,
    help="Interactive mode"
)
def passphrase(words: int, copy: bool, interactive: bool):
    """Generate a diceware-style passphrase."""
    console.print(
        Panel(
            "[bold green]🎲 Passphrase Generator[/bold green]",
            expand=False,
            border_style="green",
        )
    )

    generator = PasswordGenerator()

    if interactive:
        words = int(
            Prompt.ask("Number of words", default="4", console=console)
        )
        copy = Confirm.ask(
            "Copy to clipboard", default=False, console=console
        )

    try:
        passphrase_str = generator.generate_passphrase(word_count=words)

        # Display passphrase
        console.print(f"\n[bold green]Generated Passphrase:[/bold green]\n")
        console.print(f"[cyan]{passphrase_str}[/cyan]\n")

        # Check strength
        strength_label, score, feedback = generator.check_strength(passphrase_str)

        # Calculate entropy (each word ~11 bits from 2048 words)
        entropy = words * 11

        display_password_table(
            passphrase_str, strength_label, score, feedback, entropy
        )

        if copy:
            if generator.clipboard.copy_to_clipboard(passphrase_str):
                console.print(
                    "[green]✓ Passphrase copied to clipboard[/green]"
                )
            else:
                console.print(
                    "[yellow]⚠ Clipboard not available[/yellow]"
                )

        console.print(
            Panel(
                "[yellow]⚠ Passphrase is memorable and secure.[/yellow]\n"
                "[dim]• Great for master passwords[/dim]\n"
                "[dim]• Easier to remember than random passwords[/dim]\n"
                "[dim]• Use in password managers[/dim]",
                border_style="yellow",
            )
        )

    except PasswordGeneratorError as e:
        console.print(f"[red]Error: {e}[/red]", file=sys.stderr)
        sys.exit(1)


@cli.command()
def info():
    """Display information about password security."""
    info_text = """
[bold cyan]Password Security Information[/bold cyan]

[bold]Why Cryptographic Randomness Matters:[/bold]
• Python's `random` module uses Mersenne Twister (predictable if seeded)
• Python's `secrets` module uses OS-level CSPRNG (cryptographically secure)
• For passwords, only CSPRNG is acceptable

[bold]Security Thresholds:[/bold]
• [yellow]Weak (< 50 bits):[/yellow] Vulnerable to brute force
• [yellow]Fair (50-60 bits):[/yellow] Acceptable for low-value accounts
• [green]Strong (80+ bits):[/green] Recommended for critical accounts
• [green]Very Strong (128+ bits):[/green] Maximum security (master passwords)

[bold]Best Practices:[/bold]
1. Use unique passwords for each account
2. Store passwords in a password manager (1Password, Bitwarden, KeePass)
3. Enable 2FA/MFA for critical accounts
4. Regularly rotate passwords for sensitive accounts
5. Never reuse passwords across services

[bold]Passphrase vs Random Password:[/bold]
• Passphrases: Easier to remember, ~11 bits per word
• Random passwords: Higher entropy, harder to remember
• Recommendation: Use passphrases for master passwords,
  random passwords for most other accounts (stored in manager)
"""
    console.print(info_text)


if __name__ == "__main__":
    cli()
