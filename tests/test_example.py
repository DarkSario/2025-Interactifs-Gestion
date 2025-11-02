from interactifs_gestion import greet


def test_greet():
    assert greet("Monde") == "Bonjour, Monde!"
