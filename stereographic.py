from manim import *


class StereographicProjection(ThreeDScene):
    def construct(self):
        resolution_fa = 1
        n = 7
        theta = np.pi/n
        beta = PI/3
        rep = 3
        self.set_camera_orientation(phi=120 * DEGREES, theta=-160 * DEGREES)
        axes = ThreeDAxes(x_range=(-3, 3, 1), y_range=(-3, 3, 1), z_range=(-3, 3, 0.5))
        R_sphere = 1
        r = R_sphere * (1 - np.sin(theta))/(1 + np.sin(theta))
        mini_circles = VGroup()
        p = r * np.sin(theta) / (1 - np.sin(theta))

        for i in range(n):
            posy = (r+p) * np.sin(i*2*theta)
            posx = (r+p) * np.cos(i*2*theta)

            c = Circle(radius=p, color=GOLD)
            c.move_to([posx, posy, 0])
            mini_circles.add(c)

        def stereographic_projection(point):
            x, y, z = point
            xp = R_sphere * x / (R_sphere - z + 1e-6)
            yp = R_sphere * y / (R_sphere - z + 1e-6)
            return np.array([xp, yp, 0])

        def inverse_stereographic_projection(point):
            xp, yp, zp = point
            x = (2 * xp) / (R_sphere ** 2 + xp ** 2 + yp ** 2)
            y = (2 * yp) / (R_sphere ** 2 + xp ** 2 + yp ** 2)
            z = (xp ** 2 + yp ** 2 - 1) / (xp ** 2 + yp ** 2 + 1)
            return np.array([x, y, z])

        surface_plane = Surface(
            lambda u, v: axes.c2p(u, v, 0),
            resolution=(resolution_fa, resolution_fa),
            v_range=[-5, 5],
            u_range=[-5, 5],
        ).set_color(BLACK)

        surface_plane.set_style(fill_opacity=0.5)
        # sphere = Sphere(center=[0, 0, 0], radius=R_sphere, resolution=(50, 50), fill_opacity=0.1).set_color(GRAY)

        sphere = Sphere(radius=R_sphere, color=YELLOW, fill_opacity=0.3)
        s_p = sphere.copy()
        self.add(axes, surface_plane)
        self.play(Create(sphere))
        self.wait(1)
        circle = Circle(radius=R_sphere, color=RED)
        c1 = circle.copy()
        self.play(Create(circle))
        self.wait(1)
        m_circle = Circle(radius=r, color=GREEN)
        m_c = m_circle.copy()
        min_c = mini_circles.copy()
        self.play(Create(m_circle))
        self.wait(1)
        self.play(Create(mini_circles))
        self.wait(1)
        self.begin_ambient_camera_rotation(about="phi", rate=-0.2)
        self.play(mini_circles.animate.apply_function(inverse_stereographic_projection),
                  m_circle.animate.apply_function(inverse_stereographic_projection), run_time=2)

        self.play(Rotate(VGroup(sphere, m_circle, mini_circles, circle), axis=np.array([1, 0, 0]), angle=beta), run_time=2)

        self.play(mini_circles.animate.apply_function(stereographic_projection),
                  m_circle.animate.apply_function(stereographic_projection),
                  circle.animate.apply_function(stereographic_projection),
                  run_time=2)

        # for i in range(rep):
        #     self.play(Rotate(VGroup(min_c, m_c, c1), axis=np.array([0, 0, 1]), angle=2 * PI / rep))
        #     m3 = min_c.copy()
        #     m2 = m_c.copy()
        #     m1 = c1.copy()
        #     m2 = m2.apply_function(inverse_stereographic_projection)
        #     m3 = m3.apply_function(inverse_stereographic_projection)
        #
        #     Rotate(VGroup(s_p, m1, m2, m3), axis=np.array([1, 0, 0]), angle=beta)
        #     m3 = m3.apply_function(stereographic_projection)
        #     m2 = m2.apply_function(stereographic_projection)
        #     m1 = m1.apply_function(stereographic_projection)
        #     if i == 0:
        #         self.remove(mini_circles, m_circle, circle)
        #     self.add(m1, m2, m3)
        #     self.wait(1)

        self.stop_ambient_camera_rotation()
