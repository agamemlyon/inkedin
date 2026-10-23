# Publier sur LinkedIn : ce qui est permis

| Action | API officielle ? | InkedIn |
|---|---|---|
| Publier sur **ton propre** profil | Oui : produit self-serve *Share on LinkedIn*, scope `w_member_social`, `POST /rest/posts` | optionnel (`publishing.mode: api`), seulement après validation |
| Lire tes stats d'impressions | Non pour un membre (API Community Management réservée aux partenaires) | à coller à la main ou en export CSV |
| Lire des posts / commentaires publics | Pas via l'API officielle | Treg (fournisseurs tiers, lecture seule, sans tes cookies) |
| Liker, commenter, inviter, envoyer des DM automatiquement | Interdit (CGU LinkedIn) | jamais : l'agent rédige, tu envoies |
| Extensions qui pilotent linkedin.com, pods d'engagement | Interdit | jamais |

## Mise en place du mode `api` (environ 15 min)
1. https://developer.linkedin.com → *Create app* (une Company Page est requise, une page « perso » vide suffit).
2. Products → ajouter **Sign In with LinkedIn using OpenID Connect** et **Share on LinkedIn**.
3. Auth → redirect URL `http://localhost:8765/callback`.
4. Stocker `LINKEDIN_CLIENT_ID` / `LINKEDIN_CLIENT_SECRET` dans un coffre (Hermes : browser_vault ou fichier `.env`
   gitignoré). Ne les colle jamais dans un chat.
5. `tools/publish.py auth` → le navigateur s'ouvre, tu acceptes, et le token (valable 60 jours) est stocké localement.
6. `tools/publish.py post data/queue/<fichier>.md` refuse tout fichier qui n'a pas `status: approved`.

> Le scheduling natif n'existe pas pour les membres dans l'API. C'est le cron `inkedin-publish` qui publie au créneau prévu.
> La planification depuis l'interface LinkedIn reste une bonne alternative en mode `copy`.
