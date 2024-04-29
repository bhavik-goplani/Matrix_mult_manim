from manim import *
import copy

config.max_files_cached = 500

class Fox(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.A = self.createSquareMatrix(3, "A", BLUE, 0.8, 0.5)
        self.B = self.createSquareMatrix(3, "B", GREEN, 0.8, 0.5)
        self.C = self.createSquareMatrix(3, "C", ORANGE, 0.8, 0.5)
        self.grid = self.createGrid()
        self.title = Text("Fox's Algorithm", color=WHITE).to_edge(UP + LEFT).scale(0.8)
        self.text = None

    def construct(self):
        self.play(Write(self.title))
        self.A.move_to(DOWN + (0.8 * LEFT) + (0.4 * DOWN))
        self.B.move_to(DOWN + (0.8 * RIGHT) + (0.4 * DOWN))
        self.grid.move_to(DOWN)

        self.changeText(r"Algorithm works in $\sqrt{P} \text{ steps} = \sqrt{9} = 3 \text{ steps}$")
        self.play(*[FadeIn(o) for o in (self.A, self.B, self.grid)])
        self.wait(1)

        self.changeText(r"1.1 One to all broadcast of block $A_{i,i}$ within each row $i$ ; k = 0.")
        A_0 = self.broadcastMatrix(self.A)
        self.wait(1)

        self.changeText(r"1.2 Each processor $P_{i,j}$ locally updates $C_{i,j}$.")
        # create a deep copy of B
        B_0 = copy.deepcopy(self.B)
        self.parallelMultiplyMatrix(A_0, self.B, self.C)
        self.wait(1)

        self.play(*[FadeOut(o) for o in (self.A, self.grid)])
        self.wait(1)

        self.changeText(r"2.1 One to all broadcast of block $A_{i,(i+k) \mod \sqrt{P}}$ within each row $i$ ; k = 1.")
        self.play(*[FadeIn(o) for o in (self.A, B_0, self.grid)])
        A_1 = self.broadcastMatrix(self.A, 1)
        self.wait(1)

        self.changeText(r"2.2 Circular shift each column of $B$ up by one.")
        self.play(*[CyclicReplace(*column[::-1]) for column in zip(*B_0)])
        self.wait(1)

        self.changeText(r"2.3 Each processor $P_{i,j}$ locally updates $C_{i,j}$.")
        B_0 = self.shiftB(B_0)
        B_1 = copy.deepcopy(B_0)
        self.parallelMultiplyMatrix(A_1, B_0, self.C)
        self.wait(1)

        self.play(*[FadeOut(o) for o in (self.A, self.grid)])
        self.wait(1)

        self.changeText(r"3.1 One to all broadcast of block $A_{i,(i+k) \mod \sqrt{P}}$ within each row $i$ ; k = 2.")
        self.play(*[FadeIn(o) for o in (self.A, B_1, self.grid)])
        A_2 = self.broadcastMatrix(self.A, 2)
        self.wait(1)

        self.changeText(r"3.2 Circular shift each column of $B$ up by one.")
        self.play(*[CyclicReplace(*column[::-1]) for column in zip(*B_1)])
        self.wait(1)

        self.changeText(r"3.3 Each processor $P_{i,j}$ locally updates $C_{i,j}$.")
        B_1 = self.shiftB(B_1)
        self.parallelMultiplyMatrix(A_2, B_1, self.C)
        self.wait(1)

        self.play(*[FadeOut(o) for o in (self.A, self.grid, self.text)])
        self.play(FadeOut(self.title))
        self.animateEnd()

        self.wait(2)
    
    def shiftB(self, B):
        # Perform a cyclic shift on each column
        B = [[column[(i+1)%len(column)] for i in range(len(column))] for column in zip(*B)]

        # Convert each list in B_0 to a VGroup (a group of Mobjects)
        B = [VGroup(*column) for column in B]

        # Convert B_0 to a VGroup of VGroups
        B = VGroup(*B)

        # Convert B back to a 2D list of Mobjects
        B = [list(column) for column in B]

        # Perform the transpose operation
        B = list(map(list, zip(*B)))

        # Convert B back to a VGroup
        B = VGroup(*[VGroup(*column) for column in B])
        
        return B
    
    def broadcastMatrix(self, matrix, k=0):
        new_matrix = VGroup()
        elements = []
        broadcastAnimation = []
        # Populate the new matrix one by one
        for i in range(3):
            # Create a new VGroup for the row
            row = VGroup()
            for j in range(3):
                # Copy the element at the shifted position in the original matrix
                element = matrix[i][(i+k)%3].copy()
                # Position the copied element to the right of the original matrix
                broadcastAnimation.append(element.animate.move_to(matrix[i][j].get_center() + RIGHT*0.8))
                # Add the copied element to the row
                elements.append(element)
                row.add(element)
            new_matrix.add(row)
        self.wait(1)
        
        self.play(*broadcastAnimation, run_time=2)
        self.wait(1)
        # self.play(*[FadeOut(element) for element in elements], run_time=2)

        return new_matrix


    def createSquareMatrix(self, size, label, color, scale, opacity):
        matrix = VGroup()
        for x in range(size):
            row = VGroup()
            for y in range(size):
                cell = Square(side_length=0.8, fill_color=color,
                              fill_opacity=opacity, stroke_width=1)
                cell_label = MathTex(
                    label + "_{" + str(x) + str(y) + "}", color=WHITE).scale(cell.get_height())
                cell.add(cell_label)
                row.add(cell)
            matrix.add(row.arrange(RIGHT, buff=1.6))
        matrix.arrange(DOWN, buff=0.8)
        return matrix
    
    def createGrid(self):
        grid = VGroup()
        for i in range(3):
            row = VGroup()
            for j in range(3):
                cell = Rectangle(height=1.6, width=2.4, fill_color=WHITE,
                              fill_opacity=0, stroke_width=2)
                cell_label = MathTex(
                    "P_{" + str(i) + str(j) + "}", color=WHITE).scale(cell.get_height() / 2)
                cell_label.move_to(cell_label.get_center() + (0.4 * UP))
                cell.add(cell_label)
                row.add(cell)
            grid.add(row.arrange(RIGHT, buff=0))
        grid.arrange(DOWN, buff=0)
        return grid
    
    def changeText(self, text):
        self.remove(self.text)
        self.text = Tex(text, color=WHITE).scale(0.6)
        self.text.next_to(self.title, DOWN, buff=0.5).align_to(self.title, LEFT)
        self.play(Write(self.text))
    
    def parallelMultiplyMatrix(self, A, B, P):
        animationYellow = []
        animationMultiply = []
        animationFadeOut = []
        animationTransform = []
        
        for i in range(len(P)):
            for j in range(len(P[i])):
                # Highlight the elements of A and B
                animationYellow.append(A[i][j].animate.set_color(YELLOW))
                animationYellow.append(B[i][j].animate.set_color(YELLOW))

                # Show an animation of the multiplication operation
                multiply_symbol = MathTex(r"\times").move_to(A[i][j].get_center() + RIGHT*0.4)
                animationMultiply.append(Write(multiply_symbol))

                self.C[i][j].move_to(A[i][j].get_center() + RIGHT*0.4)

                # Fade in the result of the multiplication operation
                animationFadeOut.append(FadeOut(multiply_symbol))
                animationTransform.append(Transform(A[i][j], self.C[i][j]))
                animationTransform.append(Transform(B[i][j], self.C[i][j]))
                

        self.play(*animationYellow, run_time=1)
        self.wait(1)
        self.play(*animationMultiply, run_time=1)
        self.wait(1)
        self.play(*animationFadeOut, run_time=1)
        self.wait(1)
        self.play(*animationTransform, run_time=2)
        self.wait(1)
        self.play(FadeOut(self.C), FadeOut(A), FadeOut(B))
        self.wait(1)
        pass

    def circularShiftUpOnePosition(self, matrix):
        new_matrix = VGroup()

        for i in range(3):
            row = VGroup()
            for j in range(3):
                element = matrix[(j+1)%3][i].copy()
                row.add(element)
            new_matrix.add(row.arrange(RIGHT, buff=1.6))
        new_matrix.arrange(DOWN, buff=0.8)
        return new_matrix
    
    def animateEnd(self):
        # Create the shape of a heart using a Polygon
        circle_left = Circle(radius=1.5, color=RED).shift(LEFT)
        circle_right = Circle(radius=1.5, color=RED).shift(RIGHT)
        circle_left.set_fill(RED, opacity=1)
        circle_right.set_fill(RED, opacity=1)
        triangle = Polygon([-2, -1, 0], [2, -1, 0], [0, -3, 0], color=RED).set_fill(RED, opacity=1)

        # Group the shapes to form the heart
        heart = VGroup(circle_left, circle_right, triangle)

        heart.move_to(ORIGIN)
        heart.scale(0.1)
        # Animate the heart
        self.play(GrowFromCenter(heart))
        self.wait(1)

        # Display "Made with heart using Manim"
        text_left = Text("Made with").next_to(heart, LEFT)
        text_right = Text("using Manim").next_to(heart, RIGHT)
        self.play(Write(text_left), Write(text_right))
        pass