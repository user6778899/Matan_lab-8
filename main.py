import numpy as np
import matplotlib.pyplot as plt

# Функция f(x) = cos^2(x)
def f(x):
    return np.cos(x)**2

# Аналитическое значение интеграла
true_integral = np.pi / 2  # int_0^pi cos^2(x) dx = pi/2

# Методы интегрирования
def rectangle_left(a, b, n):
    dx = (b - a) / n
    x = np.linspace(a, b, n+1)[:-1]  # Левые точки
    return np.sum(f(x) * dx)

def rectangle_right(a, b, n):
    dx = (b - a) / n
    x = np.linspace(a, b, n+1)[1:]  # Правые точки
    return np.sum(f(x) * dx)

def rectangle_mid(a, b, n):
    dx = (b - a) / n
    x = np.linspace(a + dx/2, b - dx/2, n)  # Средние точки
    return np.sum(f(x) * dx)

def rectangle_random(a, b, n):
    dx = (b - a) / n
    x = np.linspace(a, b, n+1)
    xi = np.random.uniform(x[:-1], x[1:])  # Случайные точки
    return np.sum(f(xi) * dx)

def trapezoid(a, b, n):
    dx = (b - a) / n
    x = np.linspace(a, b, n+1)
    y = f(x)
    return np.sum((y[:-1] + y[1:]) * dx / 2)

def simpson(a, b, n):
    dx = (b - a) / n
    x = np.linspace(a, b, n+1)
    y = f(x)
    mid_x = (x[:-1] + x[1:]) / 2
    mid_y = f(mid_x)
    return np.sum((y[:-1] + 4*mid_y + y[1:]) * dx / 6)

# Построение графиков для n = 4, 8, 16 (метод прямоугольников, средняя точка)
def plot_rectangles(a, b, n, filename):
    dx = (b - a) / n
    x = np.linspace(a, b, n+1)
    x_mid = (x[:-1] + x[1:]) / 2
    y_mid = f(x_mid)
    
    # График функции
    x_fine = np.linspace(a, b, 1000)
    plt.plot(x_fine, f(x_fine), 'b-', label='f(x) = cos²(x)')
    
    # Закрашенные прямоугольники
    for i in range(n):
        plt.bar(x_mid[i], y_mid[i], width=dx, alpha=0.3, align='center', color='orange')
    
    plt.title(f'Интеграл, n = {n}')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

# Вычисления и анализ ошибок
a, b = 0, np.pi
n_values = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
results = {}

# Вычисляем ошибки для всех n
for n in n_values:
    left = rectangle_left(a, b, n)
    right = rectangle_right(a, b, n)
    mid = rectangle_mid(a, b, n)
    random = rectangle_random(a, b, n)
    trap = trapezoid(a, b, n)
    simp = simpson(a, b, n)
    
    results[n] = {
        'left': (left, abs(left - true_integral), (left - true_integral)**2),
        'right': (right, abs(right - true_integral), (right - true_integral)**2),
        'mid': (mid, abs(mid - true_integral), (mid - true_integral)**2),
        'random': (random, abs(random - true_integral), (random - true_integral)**2),
        'trap': (trap, abs(trap - true_integral), (trap - true_integral)**2),
        'simp': (simp, abs(simp - true_integral), (simp - true_integral)**2)
    }

# Вывод результатов только для n = 1024 в виде таблицы
print("Результаты для n = 1024:")
print("Метод\t\t\tЗначение\tMAE\t\tMSE")
print("-" * 50)
for method, (value, mae, mse) in results[1024].items():
    method_name = {
        'left': 'Прямоугольники (левая)',
        'right': 'Прямоугольники (правая)',
        'mid': 'Прямоугольники (середина)',
        'random': 'Прямоугольники (случайная)',
        'trap': 'Трапеции',
        'simp': 'Симпсон'
    }[method]
    print(f"{method_name:<20}\t{value:.12f}\t{mae:.2e}\t{mse:.2e}")

# Подготовка данных для графиков MAE и MSE
mae_data = {method: [results[n][method][1] for n in n_values] for method in results[1024].keys()}
mse_data = {method: [results[n][method][2] for n in n_values] for method in results[1024].keys()}

# Стили для линий
styles = {
    'left': '-o',    # синяя линия с кругами
    'right': '--s',  # оранжевая пунктирная с квадратами
    'mid': '-.^',    # зелёная штрих-пунктирная с треугольниками
    'random': ':d',  # красная точечная с ромбами
    'trap': '-*',    # фиолетовая с звёздами
    'simp': '--x'    # коричневая пунктирная с крестиками
}

# График зависимости MAE от n
plt.figure(figsize=(8, 6))
for method, mae in mae_data.items():
    label = {
        'left': 'Прямоугольники (левая)',
        'right': 'Прямоугольники (правая)',
        'mid': 'Прямоугольники (середина)',
        'random': 'Прямоугольники (случайная)',
        'trap': 'Трапеции',
        'simp': 'Симпсон'
    }[method]
    plt.plot(n_values, mae, styles[method], label=label, linewidth=2, markersize=8)
plt.xscale('log')
plt.yscale('log')
plt.ylim(1e-20, 1e-1)  # Устанавливаем пределы для y, чтобы видеть все линии
plt.xlabel('Число разбиений n')
plt.ylabel('MAE')
plt.title('Зависимость MAE от n')
plt.legend()
plt.grid(True)
plt.savefig('mae_plot.png')
plt.close()

# График зависимости MSE от n
plt.figure(figsize=(8, 6))
for method, mse in mse_data.items():
    label = {
        'left': 'Прямоугольники (левая)',
        'right': 'Прямоугольники (правая)',
        'mid': 'Прямоугольники (середина)',
        'random': 'Прямоугольники (случайная)',
        'trap': 'Трапеции',
        'simp': 'Симпсон'
    }[method]
    plt.plot(n_values, mse, styles[method], label=label, linewidth=2, markersize=8)
plt.xscale('log')
plt.yscale('log')
plt.ylim(1e-40, 1e-1)  # Устанавливаем пределы для y, чтобы видеть все линии
plt.xlabel('Число разбиений n')
plt.ylabel('MSE')
plt.title('Зависимость MSE от n')
plt.legend()
plt.grid(True)
plt.savefig('mse_plot.png')
plt.close()

# Построение графиков для n = 4, 8, 16
for n in [4, 8, 16]:
    plot_rectangles(a, b, n, f'plot_n{n}.png')

# Сообщение о сохранённых графиках
print("\nГрафики сохранены:")
print("- plot_n4.png, plot_n8.png, plot_n16.png: графики интегральных сумм")
print("- mae_plot.png: зависимость MAE от n")
print("- mse_plot.png: зависимость MSE от n")
