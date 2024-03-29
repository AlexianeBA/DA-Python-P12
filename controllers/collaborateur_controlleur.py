import hashlib
import secrets
import atexit
from models.collaborateur import Collaborateur
from database.db_config import Session
from database.db_config import get_session
from models.client import Client
from typing import Dict, Optional, Tuple


def hash_password(password: str) -> Tuple[str, str]:
    """
    Hash le mot de passe avec un sel aléatoire.

    Args:
        password (str): Le mot de passe à hacher.

    Returns:
        tuple: Un tuple contenant le mot de passe haché et le sel utilisé.
    """
    salt = secrets.token_hex(8)
    hashed_password = hashlib.sha3_256((password + salt).encode()).hexdigest()
    return hashed_password, salt


def create_collaborateur(
    nom_utilisateur: str, mot_de_passe: str, role: str
) -> Collaborateur:
    """
    Crée un nouveau collaborateur dans la base de données.

    Args:
        nom_utilisateur (str): Le nom d'utilisateur du collaborateur.
        mot_de_passe (str): Le mot de passe du collaborateur.
        role (str): Le rôle du collaborateur.

    Returns:
        Collaborateur: Le collaborateur créé.
    """
    session = Session()
    hashed_password, salt = hash_password(mot_de_passe)
    collaborateur = Collaborateur(
        nom_utilisateur=nom_utilisateur,
        mot_de_passe=hashed_password,
        salt=salt,
        role=role,
    )
    session.add(collaborateur)
    session.commit()
    session.close()
    return collaborateur


def get_support_name(collaborateur_id: int) -> str:
    """
    Récupère le nom du support à partir de l'identifiant du collaborateur.

    Args:
        collaborateur_id (int): L'identifiant du collaborateur.

    Returns:
        str: Le nom du support associé au collaborateur.
    """
    session = Session()
    collaborateur = session.query(Collaborateur).filter_by(id=collaborateur_id).first()

    if collaborateur:
        support_name = collaborateur.nom_utilisateur
        session.close()
        if support_name:
            return support_name

    return "Support introuvable"


def authenticate_collaborateur(
    nom_utilisateur: str, mot_de_passe: str
) -> Collaborateur:
    """
    Authentifie un collaborateur.

    Args:
        nom_utilisateur (str): Le nom d'utilisateur du collaborateur.
        mot_de_passe (str): Le mot de passe du collaborateur.

    Returns:
        int: L'identifiant du collaborateur si l'authentification réussit, sinon None.
    """
    session = get_session()
    collaborateur = (
        session.query(Collaborateur).filter_by(nom_utilisateur=nom_utilisateur).first()
    )
    collaborateur_id = None
    if collaborateur:
        hashed_password_input = hashlib.sha3_256(
            (mot_de_passe + collaborateur.salt).encode()
        ).hexdigest()
        if hashed_password_input == collaborateur.mot_de_passe:
            collaborateur.is_connected = True
            session.commit()
            collaborateur_id = collaborateur.id
    else:
        print("User not found!")

    session.close()
    return collaborateur_id


def get_collaborateur_by_id(collaborateur_id: int) -> Collaborateur:
    """
    Récupère un collaborateur à partir de son identifiant.

    Args:
        collaborateur_id (int): L'identifiant du collaborateur à récupérer.

    Returns:
        Collaborateur: Le collaborateur correspondant à l'identifiant donné.
    """
    session = Session()
    collaborateur = session.query(Collaborateur).filter_by(id=collaborateur_id).first()
    session.close()
    return collaborateur


def get_collaborateur_id_connected(nom_utilisateur):
    """
    Récupère l'identifiant et le rôle du collaborateur connecté.

    Returns:
        tuple: Un tuple contenant l'identifiant et le rôle du collaborateur connecté,
               ou (None, None) s'il n'y a aucun collaborateur connecté.
    """
    session = get_session()
    collaborateur = (
        session.query(Collaborateur).filter_by(nom_utilisateur=nom_utilisateur).first()
    )
    session.close()
    if collaborateur:
        return collaborateur.id, collaborateur.role
    print("aucun collaborateur connecté")
    return None, None


def get_only_id_collaborateur():
    session = get_session()
    collaborateur = session.query(Collaborateur).filter_by(is_connected=True).first()
    session.close()
    if collaborateur:
        return collaborateur.id
    return None


def update_collaborateur(collaborateur_id: int, new_values: Dict[str, str]) -> None:
    """
    Met à jour les informations d'un collaborateur.

    Args:
        collaborateur_id (int): L'identifiant du collaborateur à mettre à jour.
        new_values (dict): Un dictionnaire contenant les nouvelles valeurs à attribuer
                           aux attributs du collaborateur.

    Returns:
        None
    """

    session = Session()
    collaborateur = session.query(Collaborateur).filter_by(id=collaborateur_id).first()
    if collaborateur:
        for attr in new_values:
            setattr(collaborateur, attr, new_values[attr])
        session.commit()
    session.close()


def get_collaborateur_name_by_id(collaborateur_id: int) -> str:
    """
    Récupère le nom du collaborateur à partir de son ID.

    Args:
        collaborateur_id (int): L'identifiant du collaborateur.

    Returns:
        str: Le nom d'utilisateur du collaborateur.
    """
    session = Session()
    collaborateur = session.query(Collaborateur).filter_by(id=collaborateur_id).first()
    session.close()

    if collaborateur:
        return collaborateur.nom_utilisateur
    else:
        return "Inconnu"


def get_all_commercial():
    """
    Affiche la liste de tous les commerciaux disponibles.
    """
    session = Session()
    collaborateur = session.query(Collaborateur).filter_by(role="commercial").all()
    session.close()
    if collaborateur:
        return collaborateur


def delete_collaborateur(nom_utilisateur: int) -> None:
    """
    Supprime un collaborateur de la base de données.

    Args:
        collaborateur_id (int): L'identifiant du collaborateur à supprimer.

    Returns:
        None
    """
    session = Session()
    collaborateur = (
        session.query(Collaborateur).filter_by(nom_utilisateur=nom_utilisateur).first()
    )
    if collaborateur:
        session.delete(collaborateur)
        session.commit()
    session.close()


def get_all_collaborateurs(nom_utilisateur: Optional[str] = None) -> Collaborateur:
    """
    Récupère une liste de tous les collaborateurs ou filtrée par nom d'utilisateur.

    Args:
        nom_utilisateur (str, optional): Le nom d'utilisateur à filtrer. Par défaut, None.

    Returns:
        list: Une liste des collaborateurs récupérés.
    """
    session = Session()
    query = session.query(Collaborateur)
    if nom_utilisateur:
        query = query.filter(Collaborateur.nom_utilisateur == nom_utilisateur)
    query = query.order_by(Collaborateur.nom_utilisateur)
    collaborateurs = query.all()
    return collaborateurs


def get_collaborateurs_filtered(nom_utilisateur: Optional[str] = None) -> Collaborateur:
    """
    Récupère une liste de collaborateurs filtrés par nom d'utilisateur.

    Args:
        nom_utilisateur (str, optional): Le nom d'utilisateur à filtrer. Par défaut, None.

    Returns:
        list: Une liste des collaborateurs filtrés par nom d'utilisateur.
    """
    session = Session()
    query = session.query(Collaborateur)

    if nom_utilisateur:
        query = query.filter(Collaborateur.nom_utilisateur == nom_utilisateur)
    query = query.order_by(Collaborateur.nom_utilisateur)
    collaborateur = query.all()
    return collaborateur


def disconnection_collaborateur():
    """
    Déconnecte le collaborateur connecté.

    Returns:
        None
    """
    session = get_session()
    collaborateur = session.query(Collaborateur).filter_by(is_connected=True).first()
    if collaborateur:
        collaborateur.is_connected = False
        session.commit()
        session.close()


atexit.register(disconnection_collaborateur)
