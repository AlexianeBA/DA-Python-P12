from typing import Any, Dict, List, Tuple
from controllers.client_controller import (
    get_clients_filter_by_collaborateur,
    get_client_by_id,
)
from datetime import datetime
from rich.table import Table
from controllers.collaborateur_controlleur import (
    get_collaborateur_id_connected,
    get_collaborateur_name_by_id,
)
from models.client import Client
from models.collaborateur import Collaborateur
from views.main_view import console
import datetime


def get_client_details(
    nom_utilisateur,
) -> Tuple[str, str, str, str, datetime.date, datetime.date, int]:
    nom_complet = input("Entrez le nom complet du client : ")
    email = input("Entrez l'email du client : ")
    telephone = input("Entrez le numéro de téléphone du client : ")
    nom_entreprise = input("Entrez le nom de l'entreprise du client : ")
    date_de_creation = datetime.date.today()
    derniere_maj_contact = datetime.date.today()
    collaborateur_id = get_collaborateur_id_connected(nom_utilisateur)
    return (
        nom_complet,
        email,
        telephone,
        nom_entreprise,
        date_de_creation,
        derniere_maj_contact,
        collaborateur_id,
    )


def update_client_view(client_id: int, current_values: Any) -> Dict[str, str]:
    """
    Affiche la vue de mise à jour du client.

    Args:
        client_id (int): L'identifiant du client à mettre à jour.
        current_values (Client): Les valeurs actuelles du client.

    Returns:
        dict: Les nouvelles valeurs saisies pour le client.
    """
    new_values = {}

    print(
        "Entrez les nouvelles valeurs pour le client (laissez vide pour conserver les valeurs actuelles) :"
    )

    new_values["nom_complet"] = (
        input(f"Nouveau nom complet du client ({current_values.nom_complet}): ")
        or current_values.nom_complet
    )
    new_values["email"] = (
        input(f"Nouvel email du client ({current_values.email}): ")
        or current_values.email
    )
    new_values["telephone"] = (
        input(f"Nouveau numéro de téléphone du client ({current_values.telephone}): ")
        or current_values.telephone
    )
    new_values["nom_entreprise"] = (
        input(
            f"Nouveau nom de l'entreprise du client ({current_values.nom_entreprise}): "
        )
        or current_values.nom_entreprise
    )

    return new_values


def display_list_of_clients(clients: List[Client]) -> None:
    """
    Affiche la liste des clients.

    Args:
        clients (list): La liste des clients à afficher.
    """
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("ID")
    table.add_column("Nom complet")
    table.add_column("Email")
    table.add_column("Téléphone")
    table.add_column("Nom de l'entreprise")
    table.add_column("Date de création")
    table.add_column("Dernière mise à jour du contact")
    table.add_column("Nom du commercial")
    table.add_column("ID du commercial")

    for client in clients:
        nom_utilisateur_commercial = get_collaborateur_name_by_id(
            client.collaborateur_id
        )
        table.add_row(
            str(client.id),
            client.nom_complet,
            client.email,
            client.telephone,
            client.nom_entreprise,
            str(client.date_de_creation),
            str(client.derniere_maj_contact),
            nom_utilisateur_commercial,
            str(client.collaborateur_id),
        )
    print("Voici la liste des clients chez Epicevents: ")
    console.print(table)


def display_clients_of_collaborateur_connected(nom_utilisateur) -> None:
    """
    Affiche les clients du collaborateur connecté.
    """
    collaborateur_id, collaborateur_role = get_collaborateur_id_connected(
        nom_utilisateur
    )
    if collaborateur_id:
        clients = get_clients_filter_by_collaborateur(collaborateur_id)
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("ID du client")
        table.add_column("Nom complet du client")
        table.add_column("Adresse email du client")
        table.add_column("Numéro de téléphone du client")
        table.add_column("Nom de l'entreprise du client")
        table.add_column("Date de création de la fiche client")
        table.add_column("Dernière mise à jour de la fiche client")
        table.add_column("Nom du contact commercial chez Epicevents")
        table.add_column("ID du commercial")
        for client in clients:
            nom_utilisateur_commercial = get_collaborateur_name_by_id(
                client.collaborateur_id
            )
            table.add_row(
                str(client.id),
                client.nom_complet,
                client.email,
                str(client.telephone),
                client.nom_entreprise,
                client.date_de_creation.strftime("%Y-%m-%d"),
                client.derniere_maj_contact.strftime("%Y-%m-%d"),
                nom_utilisateur_commercial,
                str(client.collaborateur_id),
            )
        print("Liste de vos clients: ")
        console.print(table)
    else:
        print("aucun collaborateur connecté")
