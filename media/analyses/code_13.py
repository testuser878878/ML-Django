
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import solve

def solve_boundary_value_problem_shooting_newton(a, b, A, B, C, D, f, N, epsilon, K, alpha0, beta0):
    """
    Решает краевую задачу для уравнения 3-го порядка методом стрельбы с использованием метода Ньютона.

    Args:
        a (float): Левая граница интервала.
        b (float): Правая граница интервала.
        A (float): Значение U(a).
        B (float): Значение U(b).
        C (float): Значение U'(b).
        D (float): Значение U''(b)
        f (function): Правая часть дифференциального уравнения (функция от u, u', u'', x).
                     Функция должна возвращать u'''
        N (int): Количество шагов сетки.
        epsilon (float): Точность решения системы нелинейных уравнений.
        K (int): Предельное число итераций.
        alpha0 (float): Начальное значение пристрелочного параметра U'(a).
        beta0 (float): Начальное значение пристрелочного параметра U''(a).

    Returns:
        tuple: Кортеж, содержащий:
            - x (numpy.ndarray): Массив координат сетки.
            - u (numpy.ndarray): Массив значений решения u(x).
            - alpha (float): Конечное значение пристрелочного параметра U'(a).
            - beta (float): Конечное значение пристрелочного параметра U''(a)
            - L (int): Число итераций.
            - IER (int): Код завершения (0: нет ошибок, 1: превышено число итераций, 2: ошибка входных данных).
            - results_table (numpy.ndarray): Таблица результатов для каждой точки сетки.
                                             Возвращает None, если решение не найдено.
    """

    def shooting_method(alpha, beta):
        """
        Решает задачу Коши для уравнения 3-го порядка с начальными условиями:
        U(a) = A, U'(a) = alpha, U''(a) = beta.

        Args:
            alpha (float): Начальное условие для U'(a).
            beta (float):  Начальное условие для U''(a).

        Returns:
            tuple: Кортеж, содержащий:
                - x (numpy.ndarray): Массив координат сетки.
                - u (numpy.ndarray): Массив значений решения u(x).
                - udash (numpy.ndarray): Массив значений производной u'(x).
                - udouble_dash (numpy.ndarray): Массив значений второй производной u''(x).
        """
        h = (b - a) / N
        x = np.linspace(a, b, N + 1)
        u = np.zeros(N + 1)
        udash = np.zeros(N + 1)
        udouble_dash = np.zeros(N + 1)

        u[0] = A
        udash[0] = alpha
        udouble_dash[0] = beta

        # Метод Рунге-Кутты 4-го порядка для системы 3-х ОДУ первого порядка.
        for i in range(N):
            k1_u = udash[i]
            k1_udash = udouble_dash[i]
            k1_udouble_dash = f(u[i], udash[i], udouble_dash[i], x[i])

            k2_u = udash[i] + h/2 * k1_udash
            k2_udash = udouble_dash[i] + h/2 * k1_udouble_dash
            k2_udouble_dash = f(u[i] + h/2 * k1_u, udash[i] + h/2 * k1_udash, udouble_dash[i] + h/2 * k1_udouble_dash, x[i] + h/2)

            k3_u = udash[i] + h/2 * k2_udash
            k3_udash = udouble_dash[i] + h/2 * k2_udouble_dash
            k3_udouble_dash = f(u[i] + h/2 * k2_u, udash[i] + h/2 * k2_udash, udouble_dash[i] + h/2 * k2_udouble_dash, x[i] + h/2)

            k4_u = udash[i] + h * k3_udash
            k4_udash = udouble_dash[i] + h * k3_udouble_dash
            k4_udouble_dash = f(u[i] + h * k3_u, udash[i] + h * k3_udash, udouble_dash[i] + h * k3_udouble_dash, x[i] + h)

            u[i+1] = u[i] + h/6 * (k1_u + 2*k2_u + 2*k3_u + k4_u)
            udash[i+1] = udash[i] + h/6 * (k1_udash + 2*k2_udash + 2*k3_udash + k4_udash)
            udouble_dash[i+1] = udouble_dash[i] + h/6 * (k1_udouble_dash + 2*k2_udouble_dash + 2*k3_udouble_dash + k4_udouble_dash)

        return x, u, udash, udouble_dash


    def calculate_residuals(alpha, beta):
        """
        Вычисляет невязки для заданных alpha и beta.
        """
        x, u, udash, udouble_dash = shooting_method(alpha, beta)
        F = udash[-1] - C  # U'(b) - C
        G = udouble_dash[-1] - D  # U''(b) - D
        return F, G

    def calculate_jacobian(alpha, beta, delta=1e-6):
        """
        Вычисляет якобиан системы уравнений численно.
        """
        F, G = calculate_residuals(alpha, beta)

        # Вычисляем частные производные по alpha
        F_alpha, G_alpha = calculate_residuals(alpha + delta, beta)
        dF_dalpha = (F_alpha - F) / delta
        dG_dalpha = (G_alpha - G) / delta

        # Вычисляем частные производные по beta
        F, G = calculate_residuals(alpha, beta) #Recalculate for accurate derivatives
        F_beta, G_beta = calculate_residuals(alpha, beta + delta)
        dF_dbeta = (F_beta - F) / delta
        dG_dbeta = (G_beta - G) / delta

        jacobian = np.array([[dF_dalpha, dF_dbeta],
                             [dG_dalpha, dG_dbeta]])
        return jacobian


    # Проверка входных данных
    if N <= 0 or epsilon <= 0 or K <= 0:
        print("Ошибка: Некорректные входные данные.")
        return None, None, None, None, None, 2, None

    IER = 1  # Изначально предполагаем, что превышено число итераций
    L = 0  # счетчик итераций

    alpha = alpha0  # Начальное приближение для alpha
    beta = beta0  # Начальное приближение для beta

    for i in range(K):
        L = i + 1

        # 1. Вычисляем невязки
        F, G = calculate_residuals(alpha, beta)

        # 2. Проверяем сходимость
        if abs(F) < epsilon and abs(G) < epsilon:
            IER = 0
            x, u, udash, udouble_dash = shooting_method(alpha, beta)
            break

        # 3. Вычисляем якобиан
        jacobian = calculate_jacobian(alpha, beta)

        # 4. Решаем систему линейных уравнений для коррекции
        try:
            delta_alpha, delta_beta = solve(jacobian, -np.array([F, G]))
        except np.linalg.LinAlgError:
            print("Якобиан вырожден. Метод Ньютона не сходится.")
            IER = 1 # or other appropriate error code
            break # Exit the iteration loop
        # 5. Обновляем alpha и beta
        alpha += delta_alpha
        beta += delta_beta
        #  Add damping or line search if Newton is diverging (Optional)


    if IER == 1:
        print("Превышено максимальное число итераций.")
        x, u, udash, udouble_dash = shooting_method(alpha, beta)

    # Создание таблицы результатов
    if IER == 0 or IER == 1:  # решение найдено или превышено число итераций
        results_table = np.zeros((N + 1, 7))
        results_table[:, 0] = x
        results_table[:, 1] = u

        # Предполагаем, что есть точное решение u_exact(x) (нужно реализовать)
        def u_exact(x_val):
             #TODO: Replace with the analytical solution
            return np.cos(x_val)  # Example
        def udash_exact(x_val):
             #TODO: Replace with analytical solution
            return -np.sin(x_val)

        def udouble_dash_exact(x_val):
             #TODO: Replace with analytical solution
             return -np.cos(x_val)

        delta_u = np.abs(u - u_exact(x))
        delta_udash = np.abs(udash - udash_exact(x))
        delta_udouble_dash = np.abs(udouble_dash - udouble_dash_exact(x))

        results_table[:, 2] = delta_u
        results_table[:, 3] = udash
        results_table[:, 4] = delta_udash
        results_table[:, 5] = udouble_dash
        results_table[:, 6] = delta_udouble_dash

        return x, u, alpha, beta, L, IER, results_table

    else:
        return None, None, None, None, None, IER, None


# --- Пример использования ---
if __name__ == '__main__':
    # 1. Определение задачи
    a = 0.0
    b = 1.0
    A = 1.0
    B = 0.54030  # Пример граничного условия U(b)
    C = -0.84147  # Пример граничного условия U'(b)
    D = -0.54030  # Пример граничного условия U''(b)

    # Пример ДУ 3-го порядка: u''' + u'' + u' + u = 0
    def f(u, udash, udouble_dash, x):
        return -udouble_dash - udash - u

    N = 100  # Количество шагов сетки
    epsilon = 1e-6  # Точность
    K = 100  # Предельное число итераций
    alpha0 = 0.0  # Начальное значение alpha (U'(a))
    beta0 = 0.0  # Начальное значение beta (U''(a))

    # 2. Решение задачи
    x, u, alpha, beta, L, IER, results_table = solve_boundary_value_problem_shooting_newton(a, b, A, B, C, D, f, N, epsilon, K, alpha0, beta0)

    # 3. Вывод результатов
    if IER == 0 or IER == 1:
        print("Конечное значение alpha (U'(a)):", alpha)
        print("Конечное значение beta (U''(a)):", beta)
        print("Число итераций:", L)
        print("Код завершения (IER):", IER)
        print("Таблица результатов:")
        print("-------------------------------------------------------------------------------------------------------------------------")
        print("|     x     |     y     |    Delta U    |      y'      |   Delta U'  |     y''     |   Delta U'' |")
        print("-------------------------------------------------------------------------------------------------------------------------")

        for row in results_table:
            print(f"| {row[0]:9.5f} | {row[1]:9.5f} | {row[2]:11.5e} | {row[3]:9.5f} | {row[4]:11.5e} | {row[5]:9.5f} | {row[6]:11.5e} |")

        print("-------------------------------------------------------------------------------------------------------------------------")

        # 4. Визуализация результатов
        plt.plot(x, u)
        plt.xlabel("x")
        plt.ylabel("u(x)")
        plt.title("Решение краевой задачи 3-го порядка методом Ньютона")
        plt.grid(True)
        plt.show()

    else:
        print("Решение не было найдено. Код завершения (IER):", IER)
