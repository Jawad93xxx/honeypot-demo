# honeypot-demo

Honeypot HTTP minimal et portable — capture et journalisation structurée des requêtes HTTP pour démonstration technique, analyse et apprentissage.

Auteur : Jawad93xxx  
Licence : MIT

Résumé
-------
honeypot-demo est une application Flask containerisée qui accepte toutes les requêtes HTTP, les enregistre en JSON (une ligne par requête) et permet une analyse simple. Conçu pour une démonstration pratique (entretien / portfolio) : démarrage rapide, logs structurés et script d’analyse léger.

Principales caractéristiques
----------------------------
- Application "catch‑all" (Flask) qui répond à toutes les routes et méthodes HTTP.
- Log JSON par requête : timestamp, adresse source, méthode, chemin, headers, body.
- Conteneur Docker + docker‑compose pour déploiement local reproductible.
- Bind‑mount local ./logs pour accès direct au fichier `requests.log`.
- Script Python d’analyse (anonymisation IP, top IPs, top chemins, répartition méthodes).

Arborescence
-----------
- README.md
- LICENSE
- .gitignore
- docker-compose.yml
- analyze.py
- logs/               (dossier local, contient requests.log)
- honeypot/
  - Dockerfile
  - requirements.txt
  - app.py

Prérequis
---------
- Docker Desktop (WSL2 recommandé sous Windows) ou Docker Engine sur Linux/macOS
- Python 3.8+ (pour exécuter le script d’analyse localement)
- Git si vous souhaitez versionner/pousser vers GitHub

Installation et exécution (rapide)
---------------------------------
1. Cloner ou copier le dépôt dans un répertoire local, par exemple :
   cd C:\Users\<vous>\Desktop\honeypot-demo

2. Créer le dossier de logs (si absent) :
   PowerShell:
   ```
   New-Item -ItemType Directory -Path .\logs -Force
   ```

3. Lancer la stack :
   ```
   docker compose up --build
   ```
   Le service écoute par défaut sur le port 8080. Attendre l’affichage indiquant que Flask fonctionne (ex. "Running on http://0.0.0.0:8080").

4. Tester rapidement (dans une nouvelle fenêtre) :
   ```
   curl.exe http://localhost:8080/test
   curl.exe -X POST -d "payload=hello" http://localhost:8080/api/test
   ```

5. Consulter les logs (fichier local) :
   - Ouvrir dans l’éditeur :
     ```
     notepad .\logs\requests.log
     ```
   - Suivre en temps réel :
     ```
     Get-Content .\logs\requests.log -Tail 50 -Wait
     ```

Format des logs
---------------
Chaque ligne de `requests.log` est un objet JSON avec au minimum :
- timestamp — UTC ISO8601 (ex. 2025-10-30T15:51:35.209015Z)
- remote_addr — adresse source (IP)
- method — méthode HTTP (GET, POST, ...)
- path — chemin demandé
- args — paramètres de requête (dict)
- headers — dictionnaire des en‑têtes HTTP
- body — corps de la requête (texte)

Analyse
-------
Un script d’analyse minimal est fourni (`analyze.py`) :
```
python analyze.py .\logs\requests.log
```
Fonctions :
- compte total de requêtes,
- top IPs (anonymisées par hachage),
- top chemins,
- répartition par méthode.

Usage recommandé pour une démo
-----------------------------
1. Ouvrir le dépôt et lire le README (contexte).
2. Lancer `docker compose up --build`.
3. Dans une nouvelle fenêtre, exécuter quelques requêtes `curl` (GET + POST).
4. Ouvrir `./logs/requests.log` pour montrer le format JSON.
5. Lancer `python analyze.py ./logs/requests.log` et présenter le résumé obtenu.

Considérations de sécurité & éthique
-----------------------------------
- Ce projet est uniquement destiné à un usage éducatif et de démonstration.
- Ne jamais exécuter ce honeypot directement exposé sur Internet sans mise en place de protections (pare‑feu, isolation réseau, surveillance).
- Les logs peuvent contenir des données sensibles (payloads). Traitez les avec précaution et anonymisez les adresses IP si vous partagez des exemples publiquement.
- Ne pas utiliser ce code pour collecter des données personnelles sans consentement ni en violation des lois locales.

Conseils pour production / suite possible
----------------------------------------
- Isoler le container dans un réseau dédié et limiter les sorties réseau.
- Enrichir les logs (geoIP, user‑agent parsing) et stocker dans une base/temporaire (sqlite, ELK).
- Ajouter un pipeline d’ingestion ou un collector (push vers API ou transformer en CSV).
- Mettre en place des tests automatisés et un workflow CI qui build l’image et exécute un smoke test.

Contribuer
----------
Contributions bienvenues : issues (bug / amélioration), PRs (petites fonctionnalités, tests).  
Avant une PR : ouvrir une issue pour discussion si le changement est significatif.

Licence
-------
MIT — voir le fichier LICENSE dans le dépôt.

Contact
-------
Profil GitHub : https://github.com/Jawad93xxx  
