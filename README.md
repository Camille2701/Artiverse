# Artiverse

> Une plateforme communautaire pour partager et découvrir des médias (livres, films, séries, jeux).

## Aperçu

Artiverse est un projet full-stack composé d'une application front-end (Nuxt) et d'un back-end API. L'objectif est de permettre aux utilisateurs de créer des profils, publier des médias et interagir via un fil d'activité.

## Points forts
- Interface responsive construite avec Nuxt.js
- API REST organisée en version `v1` pour scalabilité
- Modèles et services côté serveur pour logique métier séparée

## Stack technique
- Front-end : Nuxt (TypeScript), Tailwind CSS
- Back-end : Node/TypeScript (architecture modulaire dans `back-end/app`)
- Base de données : (déclarer la DB utilisée dans vos variables d'environnement)

## Structure du dépôt (extraits)
- `front-end/` : application Nuxt (pages, composants, composables)
- `back-end/` : serveur API (app, core, models, services, schemas)
- `server/` : endpoints server / api pour le front-end (utilisés en dev)
- `package.json` : scripts et dépendances monorepo

## Prérequis
- Node.js (16+ recommandé)
- Yarn ou npm
- Base de données (ex : Postgres) si utilisée par le back-end

## Installation (locale)

1. Cloner le dépôt

```bash
git clone <repo-url>
cd Artiverse
```

2. Installer les dépendances

```bash
# pour le projet racine (si nécessaire)
npm install

# front-end
cd front-end
npm install

# ouvrir un autre terminal pour le back-end
cd ../back-end
npm install
```

## Variables d'environnement (exemple)
- `DATABASE_URL` — chaîne de connexion à la base de données
- `JWT_SECRET` — clé secrète pour les tokens
- `PORT` — port du serveur API

Créez un fichier `.env` à la racine (ou dans `back-end/`) et ajoutez les variables nécessaires.

## Lancer en développement

Pour le front-end (Nuxt) :

```bash
cd front-end
npm run dev
```

Pour le back-end (API) :

```bash
cd back-end
npm run dev
```

Notes : certains endpoints de développement sont aussi disponibles dans `server/api/` pour mocker rapidement des appels depuis le front-end.

## Tests
Vérifiez dans chaque dossier (`front-end`, `back-end`) s'il existe des scripts `test`. Exemple :

```bash
cd front-end
npm run test
```

## Contribution
- Ouvrir une issue pour discuter d'une fonctionnalité
- Créer une branche feature/description
- PRs doivent inclure une description et, si possible, des tests

## Déploiement
- Préparez les variables d'environnement sur l'hôte
- Construisez le front-end (`npm run build` dans `front-end`)
- Démarrez le back-end en mode production

## Ressources utiles
- Front-end : `front-end/nuxt.config.ts`
- Endpoints serveur : `server/api/`
- Typages partagés : `server/types/`

## Licence
Choisissez une licence et ajoutez-la ici (ex : MIT).

## Contact
Pour des questions ou contribuer, ouvrez une issue ou contactez les mainteneurs du projet.
