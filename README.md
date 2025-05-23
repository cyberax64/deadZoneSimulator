# Dead Zone Simulator

Ce projet propose un simulateur 2D d'un système planétaire et d'une supernova. Il permet d'explorer la théorie selon laquelle les planètes extérieures, suite à l'explosion d'une étoile et l'éjection de matière, perdent de la vitesse en rencontrant le flux de matière, entraînant un rétrécissement de leur orbite et l'accrétion de gaz, ce qui pourrait expliquer l'origine de planètes géantes gazeuses près de naines bleues.

## Théorie

Lorsqu'une étoile explose en supernova, une quantité considérable de matière (gaz léger, poussières) est projetée à grande vitesse. Cette onde de choc peut rencontrer les planètes externes qui, en traversant ce flux, subissent un freinage (drag) dû à l'interaction avec le milieu, provoquant :

1. Une diminution de leur vitesse orbitale.
2. Un déplacement vers l'intérieur du système (réduction du demi-grand axe).
3. L'accrétion d'une partie du matériau supernova sur la planète, augmentant sa masse et sa taille, pouvant la transformer en planète géante gazeuse.

Ce mécanisme pourrait expliquer comment des planètes géantes gazeuses se retrouvent dans des zones « interdites » proches de naines bleues.

## Caractéristiques du simulateur

- Simulation 2D d'un système planétaire (8 planètes de notre système solaire) avec Pygame.
- Modélisation d'une supernova via une onde de choc circulaire.
- Paramétrage de la force de drag et de la vitesse de propagation.
- Transition animée réduisant les orbites et augmentant la taille des planètes.
- Affichage du nombre de particules (virtuel) associé à chaque planète.

## Installation

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/cyberax64/deadZoneSimulator.git
   cd deadZoneSimulator
   ```
2. Installer Pygame :
   ```bash
   pip install pygame
   ```

## Usage

```bash
python simulator.py
```

- Cliquer sur le bouton « Supernova » pour déclencher l'explosion et la propagation de l'onde de choc.
- Observer la réduction d'orbite et l'accroissement des planètes au passage de l'onde.
- Appuyer sur `Échap` ou fermer la fenêtre pour quitter.

## Licence

Ce projet est distribué sous la licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
