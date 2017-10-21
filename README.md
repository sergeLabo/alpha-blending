## Alpha Blending

#### Composition, déformation, trituration, motion, diminution, augmentation d'images avec un canal alpha en temps réel à 60 fps.

### C'est typiquement le job de la carte graphique

Ce bout de brousse est tiré de https://stackoverflow.com/questions/25182421/overlay-two-numpy-arrays-treating-fourth-plane-as-alpha-level

Wikipedia EN [Alpha Compositing](https://en.wikipedia.org/wiki/Alpha_compositing)

Wikipedia FR [Alpha blending](https://fr.wikipedia.org/wiki/Alpha_blending)

Je cite:

En infographie, la simulation de transparence ou alpha blending est une technique graphique consistant à ajouter de la transparence à des images en deux dimensions ou à des objets tridimensionnels. Les deux cas sont semblables étant donné qu'un objet 3D donné est souvent modélisé par des surfaces avec une image servant de texture. (Application d'une texture dans blender)

La technique de simulation de transparence consiste à ajouter à chaque pixel une valeur, par exemple un octet (nombre de 0 à 255), définissant le caractère translucide de la surface et appelée canal alpha. Un objet est totalement opaque si la valeur alpha est au maximum (255 dans le cas d'un octet). Au contraire, il est invisible si cette valeur est à 0.*** Cette technique nécessite une forte puissance de calcul ou des fonctions spécifiques mises en œuvre par les processeurs des cartes graphiques modernes. Les jeux l'utilisent intensivement depuis quelques années.***

Donc bien sûr, *le logiciel de Graphisme 3D libre Blender fait cela depuis toujours* !!!

### Et je faisait de la prose sans le savoir

### Le jeu alpha-blending de ce projet montre des exemples
#### Rotation
Le logo de La Labomedia tourne.

#### Scale
Une image avec des ondes blanches est grossie puis rapetissée.

#### Une image sur un cube défini comme une balle animée par le moteur physique
Le logo est sur un cube défini comme une balle, et il est enfermé dans un autre cube.

#### Déformation d'un plan par une armature et des actions
TODO
c'est en cours
pour les actions

### Installation
Il faut installer:
* labtools
https://wiki.labomedia.org/index.php/Cr%C3%A9er_son_propre_package_python
