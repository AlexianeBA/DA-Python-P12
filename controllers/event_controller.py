from datetime import datetime
from typing import Dict
from models.collaborateur import Collaborateur
from models.event import Events
from database.db_config import Session
from controllers.collaborateur_controlleur import get_collaborateur_by_id

session = Session()


def create_event(
    contract_id: int,
    client_name: str,
    date_debut: datetime,
    date_fin: datetime,
    contact_support: str,
    lieu: str,
    participants: int,
    notes: str,
    collaborateur_id: int,
) -> Events:
    """
    Crée un nouvel événement dans la base de données.

    Args:
        contract_id (int): L'identifiant du contrat associé à l'événement.
        client_name (str): Le nom du client associé à l'événement.
        collaborateur_id (int): L'identifiant du collaborateur associé à l'événement.
        date_debut (datetime): La date de début de l'événement.
        date_fin (datetime): La date de fin de l'événement.
        contact_support (str): Le contact de support pour l'événement.
        lieu (str): Le lieu de l'événement.
        participants (int): Les participants à l'événement.
        notes (str): Les notes de l'événement.

    Returns:
        Events: L'événement créé.
    """
    session = Session()

    event = Events(
        contract_id=contract_id,
        client_name=client_name,
        date_debut=date_debut,
        date_fin=date_fin,
        contact_support=contact_support,
        lieu=lieu,
        participants=participants,
        notes=notes,
        collaborateur_id=collaborateur_id,
    )
    session.add(event)
    session.commit()
    session.close()
    return event


def get_event_by_id(event_id: int) -> Events:
    """
    Récupère un événement à partir de son identifiant.

    Args:
        event_id (int): L'identifiant de l'événement à récupérer.

    Returns:
        Events: L'événement correspondant à l'identifiant donné.
    """
    event = session.query(Events).filter_by(id=event_id).first()
    session.close()
    return event


def update_event(event_id: int, new_values: Dict[str, str]) -> None:
    """
    Met à jour les informations d'un événement.

    Args:
        event_id (int): L'identifiant de l'événement à mettre à jour.
        new_values (dict): Un dictionnaire contenant les nouvelles valeurs à attribuer
                           aux attributs de l'événement.

    Returns:
        None
    """
    event = session.query(Events).filter_by(id=event_id).first()
    if event:
        for attr in new_values:
            setattr(event, attr, new_values[attr])
        session.commit()
    session.close()


def delete_event(event_id: int) -> None:
    """
    Supprime un événement de la base de données.

    Args:
        event_id (int): L'identifiant de l'événement à supprimer.

    Returns:
        None
    """
    event = session.query(Events).filter_by(id=event_id).first()
    if event:
        session.delete(event)
        session.commit()
    session.close()


def get_events_filter_by_collaborateur(collaborateur_id: int) -> Events:
    """
    Récupère tous les événements associés à un collaborateur donné.

    Args:
        collaborateur_id (int): L'identifiant du collaborateur.

    Returns:
        list: Une liste des événements associés au collaborateur.
    """
    events = session.query(Events).filter_by(collaborateur_id=collaborateur_id[0]).all()
    return events


def get_all_events() -> Events:
    """
    Récupère tous les événements de la base de données.

    Returns:
        list: Une liste de tous les événements.
    """
    events = session.query(Events).all()
    return events


def get_events_filter_by_date(date_debut: int = None) -> Events:
    """
    Récupère tous les événements filtrés par date de début.

    Args:
        date_debut (datetime, optional): La date de début à filtrer. Par défaut, None.

    Returns:
        list: Une liste des événements filtrés par date de début.
    """
    query = session.query(Events)

    if date_debut:
        query = query.filter(Events.date_debut == date_debut)
    query = query.order_by(Events.date_debut)
    event = query.all()
    return event


def get_events_filter_by_date_passed() -> Events:
    """
    Récupère tous les événements passés.

    Returns:
        list: Une liste des événements passés.
    """
    current_date = datetime.now()
    past_events = (
        session.query(Events)
        .filter(Events.date_debut < current_date)
        .order_by(Events.date_debut)
        .all()
    )
    return past_events


def get_events_filter_by_date_future() -> Events:
    """
    Récupère tous les événements futurs.

    Returns:
        list: Une liste des événements futurs.
    """
    current_date = datetime.now()
    future_events = (
        session.query(Events)
        .filter(Events.date_debut >= current_date)
        .order_by(Events.date_debut)
        .all()
    )
    return future_events
