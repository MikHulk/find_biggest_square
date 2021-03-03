import unittest
from find_square import Board


class TestBoard(unittest.TestCase):

    def test_simple(self):
        src_area = (
            ".o..\n"
            ".o..\n"
            "....\n"
            "o...\n"
        )
        board = Board(src_area)
        self.assertTrue(board.is_valid)
        self.assertEqual(board.get_cell(0, 0), '.')
        self.assertEqual(board.get_cell(0, 3), '.')
        self.assertEqual(board.get_cell(0, 1), 'o')
        self.assertEqual(board.get_cell(3, 0), 'o')
        self.assertEqual(board.get_cell(3, 3), '.')
        self.assertEqual(board.get_cell(3, 1), '.')
        self.assertIsNone(board.get_square_sides(0, 0, 4))
        self.assertIsNotNone(board.get_square_sides(0, 0, 3))
        self.assertEqual(
            board.get_square_sides(0, 0, 3),
            ('.', ) * 4 + ('o', ) + ('.', ) * 2
        )
        self.assertEqual(
            board.draw(),
            (
                ".oxx\n"
                ".oxx\n"
                "....\n"
                "o..."
            )
        )
        self.assertEqual(
            board.biggest_square,
            (2, 0, 2)
        )

    def test_large_dense(self):
        src_area = (
            ".o....o....o..o..o.o\n"
            "..........o.o.......\n"
            "..........oo......o.\n"
            "...............oo...\n"
            "...oo.....o........o\n"
            ".......oo...........\n"
            "....o...............\n"
            "o...................\n"
            ".o...........o..o...\n"
            "o...o..o.o......o...\n"
            ".............oo.o.o.\n"
            ".................o..\n"
            ".........o..........\n"
            ".o......o........o..\n"
            "o...o...o.......o...\n"
            "..o..o.......oo.....\n"
            "........o...oo......\n"
            "............o.......\n"
            ".oo...........oo....\n"
            ".o.o..o........o...."
        )
        board = Board(src_area)
        self.assertTrue(board.is_valid)
        expected = (
            ".oxxxxo....o..o..o.o\n"
            "..xxxx....o.o.......\n"
            "..xxxx....oo......o.\n"
            "..xxxx.........oo...\n"
            "...oo.....o........o\n"
            ".......oo...........\n"
            "....o...............\n"
            "o...................\n"
            ".o...........o..o...\n"
            "o...o..o.o......o...\n"
            ".............oo.o.o.\n"
            ".................o..\n"
            ".........o..........\n"
            ".o......o........o..\n"
            "o...o...o.......o...\n"
            "..o..o.......oo.....\n"
            "........o...oo......\n"
            "............o.......\n"
            ".oo...........oo....\n"
            ".o.o..o........o...."
        )
        self.assertEqual(
            board.draw(),
            expected
        )
        self.assertEqual(
            board.biggest_square,
            (4, 0, 2)
        )

    def test_full(self):
        src_area = (
            "xxxxxxxxxxxxxxxxxxxx\n" * 20
        )
        board = Board(src_area)
        self.assertTrue(board.is_valid)
        self.assertEqual(
            board.draw() + "\n",
            src_area
        )
        self.assertEqual(
            board.biggest_square,
            (20, 0, 0)
        )

    def test_empty(self):
        src_area = (
            "....................\n" * 20
        )
        board = Board(src_area)
        self.assertTrue(board.is_valid)
        self.assertEqual(
            board.draw() + "\n",
            src_area.replace('.', 'x')
        )
        self.assertEqual(
            board.biggest_square,
            (20, 0, 0)
        )

    def test_one_obstacle_at_begin(self):
        src_area = (
            ".........o.........\n"
            + "...................\n" * 19
        )
        board = Board(src_area)
        self.assertTrue(board.is_valid)
        expected = (
            ".........o.........\n"
            + "xxxxxxxxxxxxxxxxxxx\n" * 19
        )
        self.assertEqual(
            board.draw() + "\n",
            expected
        )
        self.assertEqual(
            board.biggest_square,
            (19, 1, 0)
        )

    def test_one_obstacle_middle(self):
        src_area = (
            "...................\n" * 9
            + ".........o.........\n"
            + "...................\n" * 9
        )
        board = Board(src_area)
        self.assertTrue(board.is_valid)
        expected = (
            "xxxxxxxxx..........\n" * 9
            + ".........o.........\n"
            + "...................\n" * 9
        )
        self.assertEqual(
            board.draw() + "\n",
            expected
        )
        self.assertEqual(
            board.biggest_square,
            (9, 0, 0)
        )

    def test_one_obstacle_on_the_left(self):
        src_area = (
            "...................\n" * 9
            + "........o..........\n"
            + "...................\n" * 9
        )
        board = Board(src_area)
        self.assertTrue(board.is_valid)
        expected = (
            ".........xxxxxxxxxx\n" * 9
            + "........oxxxxxxxxxx\n"
            + "...................\n" * 9
        )
        self.assertEqual(
            board.draw() + "\n",
            expected
        )
        self.assertEqual(
            board.biggest_square,
            (10, 0, 9)
        )

    def test_uniform_area(self):
        src_area = (
            (".o.o.o.o.o.o.o.o.o.\n"
             + "o.o.o.o.o.o.o.o.o.o\n") * 10
        )
        board = Board(src_area)
        self.assertTrue(board.is_valid)
        expected = (
            ("xo.o.o.o.o.o.o.o.o.\n"
             + "o.o.o.o.o.o.o.o.o.o\n")
            + (".o.o.o.o.o.o.o.o.o.\n"
               + "o.o.o.o.o.o.o.o.o.o\n") * 9
        )
        self.assertEqual(
            board.draw() + "\n",
            expected
        )
        self.assertEqual(
            board.biggest_square,
            (1, 0, 0)
        )

    def test_one_row(self):
        src_area = "..o"
        board = Board(src_area)
        self.assertTrue(board.is_valid)
        expected = "x.o"
        self.assertEqual(
            board.draw(),
            expected
        )
        self.assertEqual(
            board.biggest_square,
            (1, 0, 0)
        )

    def test_one_col(self):
        src_area = ".\n.\no"
        board = Board(src_area)
        self.assertTrue(board.is_valid)
        expected = "x\n.\no"
        self.assertEqual(
            board.draw(),
            expected
        )
        self.assertEqual(
            board.biggest_square,
            (1, 0, 0)
        )

    def test_no_area(self):
        src_area = ""
        board = Board(src_area)
        self.assertFalse(board.is_valid)
        expected = ""
        self.assertEqual(
            board.draw(),
            expected
        )
        self.assertIsNone(board.biggest_square)

    def test_large_square_at_the_end_of_rectangle(self):
        src_area = "\n".join((
            "oo........",
            "o.........",
            ".....o....",
            "..o.......",
            ".....o...o",
            "..........",
            "..........",
            "o.....o...",
            "........o.",
            "..........",
        ))
        board = Board(src_area)
        self.assertTrue(board.is_valid)
        expected = "\n".join((
            "oo........",
            "o.........",
            ".....o....",
            "..o.......",
            ".....o...o",
            ".xxxxx....",
            ".xxxxx....",
            "oxxxxxo...",
            ".xxxxx..o.",
            ".xxxxx....",
        ))
        self.assertEqual(
            board.draw(),
            expected
        )
        self.assertEqual(
            board.biggest_square,
            (5, 5, 1)
        )


if __name__ == '__main__':
    unittest.main()
