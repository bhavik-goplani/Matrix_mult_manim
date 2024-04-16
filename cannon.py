from manim import *

class CannonScene(Scene):
    def __init__ (self, **kwargs):
        super().__init__(**kwargs)
        self.A = self.createSquareMatrix(3, "A", BLUE, 0.8)
        self.B = self.createSquareMatrix(3, "B", GREEN, 0.8)
        self.P = self.createSquareMatrix(3, "P", RED, 0.8)

    def construct(self):
        title = Text("Cannon's Algorithm", color=WHITE).to_edge(UP + LEFT).scale(0.8)
        step_0 = Text("Step 0: Circular shift i-th row of matrix A's blocks i positions to the left", color=WHITE).scale(0.6)
        step_0.next_to(title, DOWN, buff=0.5).align_to(title, LEFT)
        
        self.play(Write(title))
        self.animateInitial()
        self.play(Write(step_0))
        self.animateStep0()

        self.wait(2)

    def createSquareMatrix(self, size, label, color, scale):
        matrix = VGroup()
        for x in range(size):
            row = VGroup()
            for y in range(size):
                cell = Square(side_length=1*scale, fill_color=color, fill_opacity=0.5) 
                cell_label = MathTex(label + "_{" + str(x) + str(y) + "}", color=WHITE).scale(cell.get_height())
                cell.add(cell_label)
                row.add(cell)
            matrix.add(row.arrange(RIGHT, buff=0.1*scale))
        matrix.arrange(DOWN, buff=0.1*scale)  
        return matrix
    
    def animateInitial(self):
        A = self.A
        B = self.B
        P = self.P
        # position the matrices on the screen
        A.move_to(LEFT * 4)
        B.move_to(ORIGIN)
        P.move_to(RIGHT * 4)

        A_text = Text("A (3x3)", color=WHITE).next_to(A, UP).scale(0.5)
        B_text = Text("B (3x3)", color=WHITE).next_to(B, UP).scale(0.5)
        P_text = Text("P (3x3)", color=WHITE).next_to(P, UP).scale(0.5)

        steps_text = MathTex(r"\text{Algorithm works in } \sqrt{P} \text{ steps} = \sqrt{9} = 3 \text{ steps}", color=WHITE).next_to(B, DOWN, buff=1).scale(0.8)

        self.play(Create(A), Create(B), Create(P))
        self.play(Write(A_text), Write(B_text), Write(P_text))
        self.play(Write(steps_text))
        self.wait(2)

        self.play(FadeOut(A, B, P))
        self.play(FadeOut(A_text, B_text, P_text, steps_text))
        self.wait(1)
        pass

    def animateStep0(self):
        A = self.A
        B = self.B
        P = self.P

        self.play(Create(A))
        self.wait(1)

        for i in range(3):
            # Create a left pointing arrow
            arrow = Arrow(A[i].get_center()+ RIGHT*4, A[i].get_center() + RIGHT*2, buff=0)
            # Create the text
            text = Text(f'Shift by {i}').scale(0.6)
            text.next_to(arrow, RIGHT, buff=0.5)

            # Add the arrow and the text to the scene
            self.play(Create(arrow), Write(text))
            self.wait(1)

        # Circular shift each element of row A to the left by the row number
        self.circularShiftLeft1(A)
    pass

    def circularShiftLeft(self, matrix):
        matrix_copy = [[m.copy() for m in row] for row in matrix]

        # Move each element in the copy to the location of the next element in the original matrix
        for i in range(3):
            for j in range(3):
                self.play(matrix_copy[i][j].animate.move_to(matrix[i][(j-i)%3].get_center()), run_time=2)

        self.wait(1)

        # Move each element in the original matrix to the location of the corresponding element in the copy
        for i in range(3):
            for j in range(3):
                self.play(matrix[i][j].animate.move_to(matrix_copy[i][j].get_center()), run_time=2)

        self.wait(1)
        pass

    def circularShiftLeft1(self, matrix):
        # Create a new VGroup to hold the new matrix
        scale = 0.8
        new_matrix = VGroup()

        # Populate the new matrix one by one
        for i in range(3):
            # Create a new VGroup for the row
            row = VGroup()
            for j in range(3):
                # Copy the element at the shifted position in the original matrix
                element = matrix[i][(j+i)%3].copy()
                # Position the copied element to the right of the original matrix
                self.play(element.animate.move_to(matrix[i][j].get_center() + RIGHT*8), run_time=2)
                # Add the copied element to the row
                row.add(element)
            new_matrix.arrange(DOWN, buff=0.1*scale)
        self.wait(1)

        pass
        

