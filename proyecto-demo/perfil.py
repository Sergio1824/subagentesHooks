"""Persistencia de perfiles asociados a las cuentas del demo."""

import sqlite3


def inicializar_perfiles(connection: sqlite3.Connection) -> None:
    """Crea la tabla de perfiles si todavía no existe."""
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS user_profiles (
            username TEXT PRIMARY KEY COLLATE NOCASE,
            display_name TEXT NOT NULL,
            bio TEXT NOT NULL DEFAULT '',
            FOREIGN KEY (username) REFERENCES login_credentials(username)
        )
        """
    )
    connection.commit()


def guardar_perfil(
    connection: sqlite3.Connection, username: str, display_name: str, bio: str = ""
) -> None:
    """Crea o actualiza el nombre visible y la biografía de una cuenta existente."""
    if not isinstance(display_name, str) or not display_name.strip():
        raise ValueError("El nombre visible no puede estar vacío.")
    if not isinstance(bio, str):
        raise ValueError("La biografía debe ser texto.")
    inicializar_perfiles(connection)
    connection.execute(
        """
        INSERT INTO user_profiles (username, display_name, bio) VALUES (?, ?, ?)
        ON CONFLICT(username) DO UPDATE SET
            display_name = excluded.display_name,
            bio = excluded.bio
        """,
        (username, display_name.strip(), bio.strip()),
    )
    connection.commit()


def obtener_perfil(connection: sqlite3.Connection, username: str) -> dict[str, str] | None:
    """Devuelve el perfil de la cuenta o ``None`` si no existe."""
    inicializar_perfiles(connection)
    row = connection.execute(
        "SELECT username, display_name, bio FROM user_profiles WHERE username = ?",
        (username,),
    ).fetchone()
    if row is None:
        return None
    return {"username": row[0], "display_name": row[1], "bio": row[2]}
