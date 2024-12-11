import math
import random
import time

def polar_to_cartesian(r, theta):
    """Перетворення полярних координат в декартові"""
    theta_rad = math.radians(theta)
    x = r * math.cos(theta_rad)
    y = r * math.sin(theta_rad)
    return x, y

def cartesian_to_polar(x, y):
    """Перетворення декартових координат в полярні"""
    r = math.sqrt(x*x + y*y)
    theta = math.degrees(math.atan2(y, x))
    if theta < 0:
        theta += 360
    return r, theta

def spherical_to_cartesian(r, theta, phi):
    """Перетворення сферичних координат в декартові"""
    theta_rad = math.radians(theta)
    phi_rad = math.radians(phi)
    x = r * math.sin(phi_rad) * math.cos(theta_rad)
    y = r * math.sin(phi_rad) * math.sin(theta_rad)
    z = r * math.cos(phi_rad)
    return x, y, z

def cartesian_to_spherical(x, y, z):
    """Перетворення декартових координат в сферичні"""
    r = math.sqrt(x*x + y*y + z*z)
    theta = math.degrees(math.atan2(y, x))
    if theta < 0:
        theta += 360
    phi = math.degrees(math.acos(z/r))
    return r, theta, phi

def distance_cartesian_2d(x1, y1, x2, y2):
    """Відстань у декартових координатах 2D"""
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def distance_cartesian_3d(x1, y1, z1, x2, y2, z2):
    """Відстань у декартових координатах 3D"""
    return math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

def distance_polar(r1, theta1, r2, theta2):
    """Відстань у полярних координатах"""
    theta1_rad = math.radians(theta1)
    theta2_rad = math.radians(theta2)
    return math.sqrt(r1**2 + r2**2 - 2*r1*r2*math.cos(theta2_rad - theta1_rad))

def distance_spherical_direct(r1, theta1, phi1, r2, theta2, phi2):
    """Пряма відстань у сферичних координатах"""
    x1, y1, z1 = spherical_to_cartesian(r1, theta1, phi1)
    x2, y2, z2 = spherical_to_cartesian(r2, theta2, phi2)
    return distance_cartesian_3d(x1, y1, z1, x2, y2, z2)

def distance_spherical_arc(r1, theta1, phi1, r2, theta2, phi2):
    """Дугова відстань у сферичних координатах"""
    theta1_rad = math.radians(theta1)
    theta2_rad = math.radians(theta2)
    phi1_rad = math.radians(phi1)
    phi2_rad = math.radians(phi2)
    
    return r1 * math.acos(
        math.sin(phi1_rad) * math.sin(phi2_rad) + 
        math.cos(phi1_rad) * math.cos(phi2_rad) * 
        math.cos(theta1_rad - theta2_rad)
    )

def generate_point_2d():
    """Генерація випадкової точки 2D"""
    return (random.uniform(0, 10), random.uniform(0, 360))

def generate_point_3d():
    """Генерація випадкової точки 3D"""
    return (random.uniform(0, 10), random.uniform(0, 360), random.uniform(0, 180))

def test_conversion():
    """Перехід між системами координат"""
    print("\n=== Перехід між системами координат ===")
    n = int(input("Введіть кількість точок: "))
    
    for i in range(n):
        r, theta = generate_point_2d()
        print(f"\nТочка {i+1}:")
        print(f"Полярні: r = {r:.2f}, θ = {theta:.2f}°")
        
        x, y = polar_to_cartesian(r, theta)
        print(f"Декартові: x = {x:.2f}, y = {y:.2f}")
        
        r2, theta2 = cartesian_to_polar(x, y)
        print(f"Знову полярні: r = {r2:.2f}, θ = {theta2:.2f}°")

def test_distance():
    """Розрахунок відстаней у сферичній системі координат"""
    print("\n=== Розрахунок відстаней у сферичній системі координат ===")
    n = int(input("Введіть кількість пар точок: "))
    
    for i in range(n):
        r1, theta1 = generate_point_2d()
        r2, theta2 = generate_point_2d()
        
        print(f"\nПара {i+1}:")
        print(f"Точка 1: r = {r1:.2f}, θ = {theta1:.2f}°")
        print(f"Точка 2: r = {r2:.2f}, θ = {theta2:.2f}°")
        
        x1, y1 = polar_to_cartesian(r1, theta1)
        x2, y2 = polar_to_cartesian(r2, theta2)
        
        dist_cart = distance_cartesian_2d(x1, y1, x2, y2)
        dist_polar = distance_polar(r1, theta1, r2, theta2)
        
        print(f"Відстань (декартова): {dist_cart:.2f}")
        print(f"Відстань (полярна): {dist_polar:.2f}")

def test_performance():
    """Бенчмарки продуктивності"""
    print("\n=== Бенчмарки продуктивності ===")
    n = int(input("Введіть розмір вибірки: "))
    
    # Генерація точок
    points_2d = [generate_point_2d() for _ in range(n)]
    points_3d = [generate_point_3d() for _ in range(n)]
    
    results = []
    
    # 1. Декартові 2D
    start_time = time.time()
    for i in range(len(points_2d)-1):
        x1, y1 = polar_to_cartesian(points_2d[i][0], points_2d[i][1])
        x2, y2 = polar_to_cartesian(points_2d[i+1][0], points_2d[i+1][1])
        distance_cartesian_2d(x1, y1, x2, y2)
    cart_2d_time = (time.time() - start_time) * 1000
    
    # 2. Декартові 3D
    start_time = time.time()
    for i in range(len(points_3d)-1):
        x1, y1, z1 = spherical_to_cartesian(points_3d[i][0], points_3d[i][1], points_3d[i][2])
        x2, y2, z2 = spherical_to_cartesian(points_3d[i+1][0], points_3d[i+1][1], points_3d[i+1][2])
        distance_cartesian_3d(x1, y1, z1, x2, y2, z2)
    cart_3d_time = (time.time() - start_time) * 1000
    
    # 3. Полярні
    start_time = time.time()
    for i in range(len(points_2d)-1):
        distance_polar(points_2d[i][0], points_2d[i][1],
                      points_2d[i+1][0], points_2d[i+1][1])
    polar_time = (time.time() - start_time) * 1000
    
    # 4. Сферичні (пряма відстань)
    start_time = time.time()
    for i in range(len(points_3d)-1):
        distance_spherical_direct(points_3d[i][0], points_3d[i][1], points_3d[i][2],
                                points_3d[i+1][0], points_3d[i+1][1], points_3d[i+1][2])
    spherical_direct_time = (time.time() - start_time) * 1000
    
    # 5. Сферичні (дугова відстань)
    start_time = time.time()
    for i in range(len(points_3d)-1):
        distance_spherical_arc(points_3d[i][0], points_3d[i][1], points_3d[i][2],
                             points_3d[i+1][0], points_3d[i+1][1], points_3d[i+1][2])
    spherical_arc_time = (time.time() - start_time) * 1000
    
    print(f"\nРезультати для {n} точок:")
    print(f"1. Декартові 2D: {cart_2d_time:.2f} мс")
    print(f"2. Декартові 3D: {cart_3d_time:.2f} мс")
    print(f"3. Полярні: {polar_time:.2f} мс")
    print(f"4. Сферичні (пряма): {spherical_direct_time:.2f} мс")
    print(f"5. Сферичні (дугова): {spherical_arc_time:.2f} мс")

def main():
    while True:
        print("\n=== Перетворення між системами координат ===")
        print("1. Перехід між системами координат")
        print("2. Розрахунок відстаней у сферичній системі координат")
        print("3. Бенчмарки продуктивності")
        print("4. Вихід")
        
        choice = input("\nОберіть опцію: ")
        
        if choice == '1':
            test_conversion()
        elif choice == '2':
            test_distance()
        elif choice == '3':
            test_performance()
        elif choice == '4':
            break
        else:
            print("Невірна опція! Спробуйте ще раз.")

if __name__ == "__main__":
    main()
