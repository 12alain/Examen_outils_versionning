import os
import subprocess
import requests


# Récupérons le token d'accès personnel à partir de la variable d'environnement
def get_personal_access_token():
    personal_access_token = os.getenv("GITHUB_ACCESS_TOKEN")
    if not personal_access_token:
        raise ValueError(
            "Veuillez définir la variable d'environnement GITHUB_ACCESS_TOKEN."
        )
    return personal_access_token


# Vérifions si le dépôt existe déjà sur GitHub
def check_if_repo_exists(headers, username, repo_name):
    repo_url = f"https://api.github.com/repos/{username}/{repo_name}"
    response = requests.get(repo_url, headers=headers)
    return response.status_code == 200


# Créons le répertoire local sur le bureau de l'utilisateur
def create_local_directory(directory_name):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    target_directory = os.path.join(desktop_path, directory_name)
    os.makedirs(target_directory, exist_ok=True)
    return target_directory


# Créons le fichier README.md
def create_readme_file(target_directory):
    readme_path = os.path.join(target_directory, "README.md")
    if not os.path.exists(readme_path):
        with open(readme_path, "w") as readme_file:
            readme_file.write(
                "# Mon Projet d'Analyse de Données\n\n"
                "Remplissez ici la description de votre projet."
            )


# Créons le fichier LICENSE
def create_license_file(target_directory):
    license_path = os.path.join(target_directory, "LICENSE")
    if not os.path.exists(license_path):
        with open(license_path, "w") as license_file:
            license_file.write("Conditions de licence à définir ici.")


# Initialisons un dépôt Git local et faisons le premier commit
def initialize_git_repo(target_directory):
    subprocess.run(["git", "init"], cwd=target_directory)
    subprocess.run(["git", "add", "."], cwd=target_directory)
    subprocess.run(
        ["git", "commit", "-m", "Premier commit avec README.md et LICENSE"],
        cwd=target_directory,
    )


# Créons un dépôt sur GitHub
def create_github_repo(headers, repo_data):
    response = requests.post(
        "https://api.github.com/user/repos", json=repo_data, headers=headers
    )
    if response.status_code == 201:
        print(f"Dépôt '{repo_data['name']}' créé avec succès sur GitHub.")
        return response.json()["clone_url"]
    else:
        print(
            f"Échec de la création du dépôt sur GitHub. Code de statut : "
            f"{response.status_code}, Réponse : {response.text}"
        )
        return None


# Ajoutons le dépôt GitHub en tant que remote et poussons le code
def push_code_to_github(repo_url, target_directory):
    subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=target_directory)
    subprocess.run(["git", "push", "-u", "origin", "master"], cwd=target_directory)


# Ajoutons deux tickets au dépôt GitHub
def create_github_issues(headers, username, repo_name):
    issues = [
        {
            "title": "Ticket 1 : Configuration initiale",
            "body": "Ce ticket suit la configuration initiale du dépôt.",
        },
        {
            "title": "Ticket 2 : Ajouter un module de nettoyage des données",
            "body": "Implémenter le module de nettoyage des données pour le projet.",
        },
    ]

    for issue in issues:
        issue_response = requests.post(
            f"https://api.github.com/repos/{username}/{repo_name}/issues",
            json=issue,
            headers=headers,
        )
        if issue_response.status_code == 201:
            print(f"Ticket '{issue['title']}' créé avec succès.")
        else:
            print(
                f"Échec de la création du ticket '{issue['title']}'. Code de statut : "
                f"{issue_response.status_code}, Réponse : {issue_response.text}"
            )


# Fonction principale pour exécuter tout le processus
def main():
    # Nom d'utilisateur GitHub
    USERNAME = "12alain"

    # Récupérons le token d'accès personnel
    personal_access_token = get_personal_access_token()

    # En-têtes de l'API GitHub
    headers = {
        "Authorization": f"token {personal_access_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Saisir le nom du dépôt
    repo_name = input("Entrez le nom du dépôt GitHub : ")

    # Vérifions si le dépôt existe déjà
    if check_if_repo_exists(headers, USERNAME, repo_name):
        print(f"Le dépôt '{repo_name}' existe déjà sur GitHub.")
        return

    # Créons le répertoire local
    target_directory = create_local_directory(repo_name)

    # Créons les fichiers README.md et LICENSE
    create_readme_file(target_directory)
    create_license_file(target_directory)

    # Initialisons le dépôt Git local et faisons un commit
    initialize_git_repo(target_directory)

    # Définissons les données du dépôt
    repo_data = {
        "name": repo_name,
        "description": "Ceci est mon nouveau dépôt",
        "private": False,
    }

    # Créons le dépôt sur GitHub
    repo_url = create_github_repo(headers, repo_data)

    # Si le dépôt a été créé avec succès, poussons le code
    if repo_url:
        push_code_to_github(repo_url, target_directory)
        # Ajoutons des tickets GitHub
        create_github_issues(headers, USERNAME, repo_name)


# Exécutez la fonction principale
if __name__ == "__main__":
    main()
