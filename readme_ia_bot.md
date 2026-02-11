# 🤖 Documentation IA du Bot – Jeu de Combat 2D

## 📌 Vue d’ensemble

Cette intelligence artificielle contrôle un adversaire dans un jeu de combat 2D en temps réel.

Elle repose sur une architecture hybride combinant :

- Machine à états finis (Finite State Machine)
- Système probabiliste
- Adaptation comportementale périodique
- Humanisation contrôlée

L’IA hérite intégralement de la classe `Player`, ce qui signifie que :

- Toute la logique de combat est partagée
- Les animations, dégâts, knockback et collisions sont gérés par `Player`
- L’IA ne gère que la prise de décision

---

# 🧠 Architecture Générale

Cycle global d’exécution :

```
Observation du joueur
→ Analyse périodique
→ Adaptation du style
→ Choix d’état
→ Exécution comportementale
→ Répétition
```

L’IA fonctionne en boucle à chaque frame.

---

# 🔍 1. Système d’Observation

Méthode principale : `observe_player()`

L’IA enregistre en continu :

- Nombre d’attaques récentes
- Nombre de sauts
- Nombre d’attaques aériennes

Ces statistiques sont accumulées sur une fenêtre temporelle.

---

# ⏱ 2. Fenêtre d’Analyse

```python
self.analysis_window = 4.0
```

Toutes les 4 secondes :

1. Analyse des comportements récents
2. Adaptation du style
3. Réinitialisation des compteurs

Ce mécanisme évite une réaction instantanée trop parfaite et simule une lecture progressive du joueur.

---

# 🎭 3. Styles Comportementaux

L’IA possède plusieurs styles dynamiques :

## Balanced
Comportement neutre par défaut.

## Aggressive
Déclenché si :
- Vie < 30%
- Avantage > 20 HP

Effet : décisions plus rapides et plus d’attaques.

## Punisher
Déclenché si le joueur spamme les attaques.

Effet : augmentation de la probabilité d’attaque.

## Anti-Air
Déclenché si le joueur saute fréquemment.

Effet : priorité aux attaques contre cible aérienne.

---

# ⚡ 4. Tempo Dynamique

Chaque style modifie :

```python
self.tempo_multiplier
```

Il influence la fréquence des décisions.

Plus il est bas, plus l’IA prend des décisions rapidement.

---

# 🧩 5. Machine à États (FSM)

États possibles :

- `idle`
- `approach`
- `reposition`
- `jump`
- `attack`
- `kick`

Chaque état correspond à une intention comportementale.

---

# 📏 6. Analyse Spatiale

L’IA divise l’espace en zones :

| Zone | Condition |
|------|-----------|
| Loin | abs_dx > far_distance |
| Moyenne | entre far_distance et too_close_distance |
| Trop proche | abs_dx < too_close_distance |

Ces zones influencent les décisions.

---

# 🎲 7. Système Probabiliste

Les décisions ne sont pas déterministes.

Exemples :

- Probabilité d’attaque variable selon le style
- Probabilité de kick
- Probabilité de saut
- Probabilité d’attaque aérienne

Cela rend l’IA imprévisible.

---

# 🧍 8. Humanisation

```python
self.error_chance = 0.05
```

5% de chance de prendre une décision sous-optimale.

Objectif :
- Éviter la perfection artificielle
- Simuler un comportement humain

---

# ⏳ 9. Système de Cooldown

L’IA respecte :

- Cooldown global d’attaque
- Cooldown de kick

Cela empêche le spam irréaliste.

---

# 🛫 10. Gestion Aérienne

Le bot peut :

- Sauter volontairement
- Attaquer en l’air
- Reculer si le joueur saute vers lui

Cela crée un comportement semi-stratégique.

---

# 🔄 11. Cycle par Frame

À chaque frame :

1. `handle_movement()`
2. `update()`
3. `observe_player()`
4. Décrément des timers
5. Analyse périodique si nécessaire

---

# 🏗 Nature de l’IA

Ce système n’est pas :

- Du machine learning
- Un réseau neuronal
- Un behavior tree complexe

C’est :

> Une Machine à États Finis probabiliste adaptative

Adaptée aux jeux de combat 2D en 1v1.

---

# ✅ Forces

- Adaptative
- Non robotique
- Stable
- Extensible
- Facile à maintenir

---

# ⚠ Limites Actuelles

- Pas de prédiction avancée
- Pas de gestion du coin (corner)
- Pas de système de garde
- Pas de planification long terme

---

# 🚀 Extensions Possibles

- Ajout d’un système de block
- Gestion du corner
- Prédiction de trajectoire
- Lecture d’animation
- Multiples niveaux de difficulté
- Mode Boss

---

# 📌 Conclusion

L’IA du bot est une base solide pour un jeu de combat indépendant.

Elle combine :

- FSM simple
- Adaptation comportementale
- Probabilités dynamiques
- Humanisation contrôlée

Elle est conçue pour être facilement extensible vers des comportements plus avancés.

