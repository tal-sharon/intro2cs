import copy
from typing import List, Tuple, Optional

Coordinate = Tuple[int, int]


class Bomb:
    """
    A class which represents a Bomb.
    A Bomb has a color and location, a blast radius and a timer which determines when it explodes.
    A Bomb can change and expand it's coordinates and color when it explodes into a 'blast'.
    A Bomb can 'move forward' in it's sequence and explode.
    A bomb can give you it's full sequence and it's current 'frame' coordinates.
    """

    def __init__(self, x: int, y: int, radius: int, time: int, bomb_color: str, blast_color: str) -> None:
        """
        Initiates a Bomb object
        :param x: The column index of the coordinate
        :param y: The row index of the coordinate
        :param radius: The radius of the Bomb's blast
        :param time: The time before to the Bomb blasts
        :param bomb_color: The Bomb's initiate color
        :param blast_color: The Bomb's color after explosion
        """
        self.__location = x, y
        self.__time = time
        self.__radius = radius
        self.__cur_color = bomb_color
        self.__blast_color = blast_color

        # the Bomb's sequence (seq) is a list of all the 'frames' from the birth of a Bomb
        # and through it's blast until it's death. A sequence moves by a frame each move and iteration.
        self.__seq: List[List[Coordinate]] = self.get_bomb_seq()

        # the Bomb's index is the stage of the Bomb's life. 0 when born, and each iteration index increases by 1.
        self.__ind: int = 0

        # the coordinates of the bombs is a list containing the current frame of the Bomb in it's sequence by the index
        self.__coordinates = self.__seq[self.__ind]

    def get_bomb_seq(self) -> List[List[Coordinate]]:
        """
        Gets the Bomb's full sequence of frames
        the Bomb's sequence (seq) is a list of all the 'frames' from the birth of a Bomb
        and through it's blast until it's death.
        Each frame contains a list of the bombs coordinates in that stage
        :return: The Bomb's full sequence
        """
        bomb_seq = []
        for frame in range(self.__time):
            bomb_seq.append([self.__location])
        blast = self.__create_blast_seq()
        for frame in blast:
            bomb_seq.append(frame)
        copy_seq = copy.deepcopy(bomb_seq)
        return copy_seq

    def __create_blast_seq(self) -> List[List[Coordinate]]:
        """
        Creates the sequence of the blast stages of a Bomb
        :return: The Bomb's blast sequence of coordinates
        """
        blast = []
        for frame in range(self.__radius+1):
            cells = self.__create_blast_cells(frame)
            blast.append(cells)
        return blast

    def __create_blast_cells(self, r) -> List[Coordinate]:
        """
        Creates a frame of a blast and gets all the cells and coordinates
        :param r: The frame's blast radius
        :return: A list of all the coordinates in the frame
        """
        x, y = self.__location
        frame = []
        for i in range(x - r, x + r + 1):
            for j in range(y - r, y + r + 1):
                if abs(x - i) + abs(y - j) == r:
                    frame.append((i, j))
        return frame

    def get_color(self) -> str:
        """
        Gets the current color of the Bomb (which might change after explosion when blasts)
        :return:
        """
        return self.__cur_color

    def get_coordinates(self) -> List[Coordinate]:
        """
        Gets the current list of coordinates of the Bomb
        :return: A list of Bomb's all current coordinates
        """
        coords = copy.deepcopy(self.__coordinates)
        return coords

    def target_cells(self) -> Optional[List[Coordinate]]:
        """
        Gets all coordinates of the Bomb's next frame
        :return: A list of coordinates
        """
        if self.__ind + 1 >= len(self.__seq):
            return None
        return self.__seq[self.__ind + 1]

    def move(self) -> Optional[List[Coordinate]]:
        """
        'Moves' the Bomb forward in it's sequence to the next frame
        :return: A list of coordinates of the next frame in the sequence
        """
        self.__ind += 1

        # check if index is out of bomb's sequence length, if so, return None.
        if self.__ind >= len(self.__seq):
            return None

        # set coordinates to the updated frame in the sequence
        self.__coordinates = self.__seq[self.__ind]

        # check if bomb timer is out of time. if so, bomb exploded, therefore, change it's color accordingly.
        if self.__ind >= self.__time:
            self.__cur_color = self.__blast_color

        return copy.deepcopy(self.__coordinates)