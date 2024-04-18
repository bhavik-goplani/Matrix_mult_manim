from manim import *

class CannonScene(Scene):
    def __init__ (self, **kwargs):
        super().__init__(**kwargs)
        self.A = self.createSquareMatrix(3, "A", BLUE, 0.8, 0.5)
        self.B = self.createSquareMatrix(3, "B", GREEN, 0.8, 0.5)
        self.P = self.createSquareMatrix(3, "P", RED, 0.8, 0.2)
        self.C = self.createSquareMatrix(3, "C", ORANGE, 0.8, 0.5)
        self.title = Text("Cannon's Algorithm", color=WHITE).to_edge(UP + LEFT).scale(0.8)
        self.A_0 = None

    def construct(self):
        
        self.play(Write(self.title))
        self.animateInitial()
        self.animateStep0()

        self.play(FadeOut(self.title))
        self.animateEnd()

        self.wait(2)

    def createSquareMatrix(self, size, label, color, scale, opacity):
        matrix = VGroup()
        for x in range(size):
            row = VGroup()
            for y in range(size):
                cell = Square(side_length=1*scale, fill_color=color, fill_opacity=opacity, stroke_width=1*scale) 
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
        arrows = VGroup()
        texts = VGroup()
        step_0 = Text("Step 0: Circular shift i-th row of matrix A's blocks i positions to the left", color=WHITE).scale(0.6)
        step_0.next_to(self.title, DOWN, buff=0.5).align_to(self.title, LEFT)

        self.play(Write(step_0))
        self.play(Create(A))
        self.wait(1)

        for i in range(3):
            # Create a left pointing arrow
            arrow = Arrow(A[i].get_center()+ RIGHT*2, A[i].get_center() + RIGHT*1.5, buff=0)
            # Append the arrow to the list of arrows
            arrows.add(arrow)
            # Create the text
            text = Text(f'Shift by {i}').scale(0.3)
            # Append the text to the list of texts
            texts.add(text)
            text.next_to(arrow, RIGHT, buff=0.5)

            # Add the arrow and the text to the scene
            self.play(Create(arrow), Write(text))
            self.wait(1)

        # Circular shift each element of row A to the left by the row number
        self.A_0 = self.circularShiftLeft(A)
        self.play(FadeOut(A), FadeOut(arrows), FadeOut(texts), FadeOut(step_0))
        arrows = VGroup()
        texts = VGroup()

        step_0 = Text("Step 0: Circular shift j-th column of matrix B's blocks j positions up", color=WHITE).scale(0.6)
        step_0.next_to(self.title, DOWN, buff=0.5).align_to(self.title, LEFT)

        B.move_to(LEFT * 4)
        
        self.play(Write(step_0))
        self.play(Create(B))
        self.wait(1)

        for i in range(3):
            arrow = Arrow(B[1][i].get_center() + DOWN*2, B[1][i].get_center() + DOWN*1.5, buff=0)
            arrows.add(arrow)
            text = Text(f'Shift by {i}').scale(0.3)
            texts.add(text)
            text.next_to(arrow, DOWN, buff=0.5)
            self.play(Create(arrow), Write(text))
            self.wait(1)

        self.B_0 = self.circularShiftUp(B)
        self.play(FadeOut(B), FadeOut(arrows), FadeOut(texts), FadeOut(step_0))
        self.wait(1)

        self.A_0.move_to(LEFT * 4).scale(0.6)
        self.B_0.move_to(RIGHT * 4).scale(0.6)
        P.move_to(ORIGIN).scale(1.2)

        self.play(Create(self.A_0), Create(self.B_0), Create(P))
        self.wait(1)
        self.parallelDistributeMatrix(self.A_0, self.B_0, P)

        self.play(FadeOut(self.A_0), FadeOut(self.B_0), FadeOut(P))

        pass

    def circularShiftLeft(self, matrix):
        # Create a new VGroup to hold the new matrix
        new_matrix = VGroup()
        elements = []

        # Populate the new matrix one by one
        for i in range(3):
            # Create a new VGroup for the row
            row = VGroup()
            for j in range(3):
                # Copy the element at the shifted position in the original matrix
                element = matrix[i][(j+i)%3].copy()
                # Position the copied element to the right of the original matrix
                self.play(element.animate.move_to(matrix[i][j].get_center() + RIGHT*6), run_time=2)
                # Add the copied element to the row
                elements.append(element)
                row.add(element)
            new_matrix.add(row)
        self.wait(1)
        
        self.play(*[FadeOut(element) for element in elements], run_time=2)
        return new_matrix
    
    def circularShiftUp(self, matrix):
        new_matrix = VGroup()
        elements = []

        for i in range(3):
            col = VGroup()
            for j in range(3):
                element = matrix[(j+i)%3][i].copy()
                self.play(element.animate.move_to(matrix[j][i].get_center() + RIGHT*6), run_time=2)
                elements.append(element)
                col.add(element)
            new_matrix.add(col)
        self.wait(1)

        self.play(*[FadeOut(element) for element in elements], run_time=2)
        return new_matrix

    def parallelDistributeMatrix(self, A, B, P):
        # Distribute each element in A and B to P in parallel to compute the product
        animations = [
            ApplyMethod(A[i][j].move_to, P[i][j].get_center() + UP*0.25 + LEFT*0.25)
            for i in range(len(A))
            for j in range(len(A[i]))
        ] + [
            ApplyMethod(B[j][i].move_to, P[i][j].get_center() + UP*0.25 + RIGHT*0.25)
            for i in range(len(B))
            for j in range(len(B[i]))
        ]

        self.play(*animations, run_time=3)
        self.wait(2)

        self.C.scale(0.6)

        animationYellow = []
        animationMultiply = []
        animationFadeOut = []
        animationTransform = []
        
        for i in range(len(P)):
            for j in range(len(P[i])):
                # Highlight the elements of A and B
                animationYellow.append(A[i][j].animate.set_color(YELLOW))
                animationYellow.append(B[j][i].animate.set_color(YELLOW))

                # Show an animation of the multiplication operation
                multiply_symbol = MathTex(r"\times").move_to(P[i][j].get_center() + UP*0.25)
                animationMultiply.append(Write(multiply_symbol))

                self.C[i][j].move_to(P[i][j].get_center() + UP*0.25)

                # Fade in the result of the multiplication operation
                animationFadeOut.append(FadeOut(multiply_symbol))
                animationTransform.append(Transform(A[i][j], self.C[i][j]))
                animationTransform.append(Transform(B[j][i], self.C[i][j]))
                

        self.play(*animationYellow, run_time=1)
        self.wait(1)
        self.play(*animationMultiply, run_time=1)
        self.wait(1)
        self.play(*animationFadeOut, run_time=1)
        self.wait(1)
        self.play(*animationTransform, run_time=2)
        self.wait(2)
        pass

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