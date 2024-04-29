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

    def construct(self):
        self.play(Write(self.title))
        self.add(self.A, self.B, self.grid)
        self.A.move_to(DOWN + (0.8 * LEFT) + (0.4 * DOWN))
        self.B.move_to(DOWN + (0.8 * RIGHT) + (0.4 * DOWN))
        self.grid.move_to(DOWN)

        self.play(*[FadeIn(o) for o in (self.A, self.B, self.grid)])
        self.wait(1)



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
    
    def parallelDistributeMatrix(self, A, B, P):
        # Distribute each element in A and B to P in parallel to compute the product
        text = MathTex(r"\text{Each processor } P_{i,j} \text{ locally updates matrix block } C_{i,j} \text{ in parallel.}").scale(0.6)
        text.next_to(self.title, DOWN, buff=0.5).align_to(self.title, LEFT)
        self.play(Write(text))
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
        self.wait(1)
        self.play(FadeOut(self.C), FadeOut(A), FadeOut(B), FadeOut(text))
        self.wait(1)
        pass