import datetime
from controllers.client_controller import create_client
from controllers.user_controller import authenticate_user

from db_config import Session


def main():
    print("Veuillez vous connecter:")
    nom_utilisateur = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")

    user = authenticate_user(nom_utilisateur, password)
    if user:
        print("Connexion réussie! Bienvenue,")
        action = input(
            "Que souhaitez-vous faire ? Tapez 1 pour créer un client: ",
        )
        if action == "1":
            nom_complet = input("Entrez le nom complet du client : ")
            email = input("Entrez l'email du client : ")
            telephone = input("Entrez le numéro de téléphone du client : ")
            nom_entreprise = input("Entrez le nom de l'entreprise du client : ")
            date_de_creation = datetime.date.today()
            dernière_maj_contact = datetime.date.today()
            contact_commercial_chez_epic_events = input(
                "Entrez le nom du contact commercial chez Epic Events : "
            )
        nouveau_client = create_client(
            nom_complet=nom_complet,
            email=email,
            telephone=telephone,
            nom_entreprise=nom_entreprise,
            date_de_creation=date_de_creation,
            dernière_maj_contact=dernière_maj_contact,
            contact_commercial_chez_epic_events=contact_commercial_chez_epic_events,
        )
        with Session() as session:
            try:
                session.add(nouveau_client)
                session.commit()
                print("Client ajouté avec succès !")
            except Exception as e:
                session.rollback()
                print(f"Erreur lors de l'ajout du client : {e}")
    else:
        print("Adresse e-mail ou mot de passe incorrect.")


if __name__ == "__main__":
    main()