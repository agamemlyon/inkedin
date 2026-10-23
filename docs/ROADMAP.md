# Roadmap

| Phase | Livrable | Statut |
|---|---|---|
| 0. Fondations | repo, nomenclature, config, gabarits de profil | ✅ fait |
| 1. Corpus + voix | import des posts (Treg), `voice.md` v0, interview de voix | 🟡 corpus importé, v0 à valider |
| 2. Détecteur | `tools/ink.py` FR/EN, 6 checks, tests de calibration | ✅ v1 (5 tests passent) |
| 3. Écriture | hooks (45), frameworks, skills post/interview/localize/carousel | ✅ v1, à éprouver sur 5 vrais drafts |
| 4. Planning + crons | ink-plan, `crons/crons.yaml`, validation Telegram | 🟡 définis, pas encore installés |
| 5. Publication | `tools/publish.py` (OAuth Share on LinkedIn) | ⬜ à faire |
| 6. Boucle de feedback | ink-audit, ink-reply, ink-calibrate, weights.json | 🟡 skills écrits, pas de script |
| 7. Profil | ink-profile + rubric | 🟡 skill écrit, premier audit à lancer |
| 8. Open source | README, CONTRIBUTING, démo, publication GitHub | 🟡 README fait |

## Nomenclature
- Skills : `ink-<verbe|objet>`, par exemple ink-post, ink-plan, ink-human
- Agents : un rôle en un mot (scout, interviewer, strategist, writer, editor, community, analyst)
- Crons : `inkedin-<fréquence>-<action>`
- Fichiers de données : `YYYY-MM-DD_<slug>.md` pour les posts, `YYYY-WW.md` pour les semaines
- Hooks : `id` stable + `slug` kebab-case ; ne jamais renuméroter, seulement ajouter
