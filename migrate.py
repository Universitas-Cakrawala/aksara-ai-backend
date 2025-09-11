#!/usr/bin/env python3
"""
Migration management script untuk Aksara AI Backend
"""
import os
import sys
import subprocess
from pathlib import Path

# Tambahkan root project ke sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def run_alembic_command(command_args):
    """Run alembic command dengan proper environment"""
    try:
        cmd = ["python", "-m", "alembic"] + command_args
        result = subprocess.run(
            cmd, cwd=project_root, check=True, capture_output=True, text=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running alembic command: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False


def create_migration(message):
    """Buat migration baru dengan autogenerate"""
    print(f"Creating migration: {message}")
    return run_alembic_command(["revision", "--autogenerate", "-m", message])


def upgrade_database(revision="head"):
    """Upgrade database ke revision tertentu"""
    print(f"Upgrading database to {revision}")
    return run_alembic_command(["upgrade", revision])


def downgrade_database(revision):
    """Downgrade database ke revision tertentu"""
    print(f"Downgrading database to {revision}")
    return run_alembic_command(["downgrade", revision])


def show_current_revision():
    """Tampilkan current revision"""
    print("Current database revision:")
    return run_alembic_command(["current"])


def show_history():
    """Tampilkan history migrations"""
    print("Migration history:")
    return run_alembic_command(["history"])


def show_heads():
    """Tampilkan head revisions"""
    print("Head revisions:")
    return run_alembic_command(["heads"])


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python migrate.py create <message>     # Buat migration baru")
        print("  python migrate.py upgrade [revision]   # Upgrade database")
        print("  python migrate.py downgrade <revision> # Downgrade database")
        print("  python migrate.py current              # Tampilkan current revision")
        print("  python migrate.py history              # Tampilkan history")
        print("  python migrate.py heads                # Tampilkan heads")
        sys.exit(1)

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 3:
            print("Error: Migration message is required")
            sys.exit(1)
        message = " ".join(sys.argv[2:])
        create_migration(message)

    elif command == "upgrade":
        revision = sys.argv[2] if len(sys.argv) > 2 else "head"
        upgrade_database(revision)

    elif command == "downgrade":
        if len(sys.argv) < 3:
            print("Error: Target revision is required for downgrade")
            sys.exit(1)
        revision = sys.argv[2]
        downgrade_database(revision)

    elif command == "current":
        show_current_revision()

    elif command == "history":
        show_history()

    elif command == "heads":
        show_heads()

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
