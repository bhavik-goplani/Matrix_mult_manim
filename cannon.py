from manim import *

class CannonScene(Scene):
    def construct(self):
        size = 3

        # Create a 3x3 matrix
        A = self.createSquareMatrix(size, "A", BLUE, 1)

        # position the matrices on the screen
        A.move_to(LEFT * 2)

        # show the matrices on screen
        self.play(Create(A))
        # self.play(Create(B))
        # self.play(Create(P))
        self.wait(2)

    def createSquareMatrix(self, size, label, color, scale):
        matrix = VGroup()
        for x in range(size):
            row = VGroup()
            for y in range(size):
                cell = Square(side_length=1*scale, fill_color=color, fill_opacity=0.5) 
                cell_label = MathTex(label + "_{" + str(x) + str(y) + "}", color=WHITE)
                cell.add(cell_label)
                row.add(cell)
            matrix.add(row.arrange(RIGHT, buff=0.1*scale))
        matrix.arrange(DOWN, buff=0.1*scale)  
        return matrix

