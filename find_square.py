import sys
from functools import reduce


class Board:
    """L'objet board représente la surface à analyser dans le but d'y découvrir
    le carré couvrant maximal.

    La surface est celle d'un plateau `n * m` cellules. Chaque cellule peut être:

    - vide,
    - occupée par un obstacle,
    - remplie.

    Board grâce à sa méthode `draw` donne une nouvelle représentation de la
    surface sur laquelle un des plus grand carrés possibles (celui le plus en
    haut à gauche) ne contenant pas d'obstacle a été rempli du caractère prévu
    à cet effet.

    Pour déterminer le plus grand carré possible (donné par la property
    `biggest_square`), l'algorithme parcours la surface en essayant de déterminer
    depuis chaque cellule en commençant par le coin en haut à gauche le plus grand
    carré possible en utilisant la méthode `get_biggest_square_from`.
    Le parcours s'arrête quand un carré satisfaisant a été trouvé. C'est à dire
    quand on trouve un carré dont le côté est plus long que la longueur maximale
    des côtés des carrés potentiellement découvrables. Cette longueur potentielle
    diminue en effet au fur et à mesure du parcours.

    :param area: la représentation du plateau sous la forme d'une chaîne de caractères.
      Chaque ligne représentant une ligne du plateau, chaque emplacement sur
      une ligne une cellule du plateau. L'état de chaque cellule(vide, occupé, plein)
      est représenté à l'aide du caractère approprié.
    :param obstacle_repr: le caractère utilisé pour représenté un obstacle. defaut: "o".
    :param plain_repr: le caractère utilisé pour représenté le plein. defaut: "x".
    :param empty_repr: le caractère utilisé pour représenté le vide. defaut: ".".
    """

    def __init__(self, area, obstacle_repr='o',
                 plain_repr='x', empty_repr='.'):
        self.raw_area = area
        self.area = [
            [cell for cell in row]
            for row in (
                self.raw_area
                .strip('\n')
                .strip()
                .split('\n')
            )
        ]
        self.obstacle_repr = obstacle_repr
        self.plain_repr = plain_repr
        self.empty_repr = empty_repr
        self._biggest_square = None
        self._is_valid = None

    def get_cell(self, x, y):
        """Méthode permettant l'accès aléatoire au cellules du plateau.

        :param x: index de la ligne sur le plateau,
        :param y: index de la colonne dans la ligne.

        :returns: le contenu à `(x, y)` sur le plateau.
        """
        return self.area[x][y]

    def get_square_sides(self, x, y, side):
        """Récupère dans une liste le contenu des côtés opposés à la position
        donnée par `x` et `y` sur le carré de coté `side`.

        *Par exemple*:
        Demander `get_square_sides(0, 0, 2)` renverra le contenu des cellules:
        (0,2), (1, 2), (2, 0), (2, 1) et (2, 2).

        Si `side` est irréaliste au regard de la taille du plateau la méthode
        renvoie `None`.
        """
        if x + side >= len(self.area) or y + side >= len(self.area[0]):
            return None
        return (
            tuple(row[y + side] for row in (self.area[x : x + side + 1]))
            + tuple(self.area[x + side][y : y + side])
        )

    @property
    def is_valid(self):
        """Indique si le plateau est valide. Pour que celui-ci soit valide il
        doit remplir les conditions suivantes:

        * Toutes les lignes doivent avoir la même longueur.
        * Il y a au moins une ligne d’au moins une case.
        * À la fin de chaque ligne il y a un retour à la ligne.
        * Les caractères présents dans la carte doivent être uniquement ceux
          présentés à la première ligne.
        """
        if self._is_valid is None:
            lines = self.area
            self._is_valid = (
                lines
                and len(lines[0]) >= 1
                and reduce(
                    lambda prev, new: (prev[0] and prev[1] == len(new), prev[1]),
                    lines[1:],
                    (True, len(lines[0]))
                )[0]
                and all(c in [self.plain_repr, self.empty_repr, self.obstacle_repr, '\n']
                        for c in self.raw_area)
            )
        return self._is_valid

    def get_biggest_square_from(self, x, y):
        """Renvoie la longueur maximale du côté d'un carré positionné en `x`, `y`
        sur son coin le plus en haut à gauche ne rencontrant pas d'obstacle.

        La méthode itère sur chaque longueur possible en commençant par la plus
        petite et cesse dès qu'un obstacle est trouvé en renvoyant la longueur obtenue.
        """
        cell = self.get_cell(x, y)
        if cell == self.obstacle_repr:
            return 0
        side = 1
        while True:
            new_friends = self.get_square_sides(x, y, side)
            if not new_friends or self.obstacle_repr in set(new_friends):
                break
            side += 1
        return side

    @property
    def biggest_square(self):
        """La position et la longueur d'un plus grand carré possible ne
        contenant pas d'obstacle sur ce plateau.
        La position est toujours donnée par rapport au coin supérieur gauche
        du carré.

        :returns : Le triplet (côté, x, y).
        """
        if self.is_valid and self._biggest_square is None:
            side_length = len(self.area[0])
            for x in range(0, len(self.area)):
                if self._biggest_square and self._biggest_square[2] >= side_length:
                    break
                for y in range(0, len(self.area[0])):
                    side = self.get_biggest_square_from(x, y)
                    if self._biggest_square is None or side > self._biggest_square[0]:
                        self._biggest_square = side, x, y
                    if y == 0:
                        side_length -= 1
        return self._biggest_square

    def draw(self):
        """Renvoie la représentation du plateau sur lequel le plus grand carré ne
        rencontrant pas d'obstacle et le plus en haut à gauche est représenté
        avec le caractère donné pas `self.plain_repr`.
        """
        if self.biggest_square is None:
            return self.raw_area
        biggest_side, biggest_sq_x, biggest_sq_y = self.biggest_square
        lines = []
        for x in range(0, len(self.area)):
            line = []
            for y in range(0, len(self.area[0])):
                cell = self.get_cell(x, y)
                if (
                        cell == self.empty_repr
                        and biggest_sq_x <= x < biggest_sq_x + biggest_side
                        and biggest_sq_y <= y < biggest_sq_y + biggest_side
                ):
                    line.append(self.plain_repr)
                else:
                    line.append(cell)
            lines.append(''.join(line))
        return '\n'.join(lines)


if __name__ == "__main__":

    for filename in sys.argv[1:]:
        print("===")
        print(filename)
        with open(filename) as f:
            header = f.readline().strip()
            empty_repr = header[-3]
            obstacle_repr = header[-2]
            plain_repr = header[-1]
            b = Board(
                f.read(),
                empty_repr=empty_repr,
                plain_repr=plain_repr,
                obstacle_repr=obstacle_repr
            )
        if not b.is_valid:
            sys.stderr.write("map error\n")
            continue
        print(f"Biggest square with {b.biggest_square[0]} units side "
              f"at ({b.biggest_square[1]}, {b.biggest_square[2]})")
        print(b.draw())
