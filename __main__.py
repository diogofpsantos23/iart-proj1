import random
import pandas as pd


class Package:
    def __init__(self, package_type, coordinates):
        self.package_type = package_type
        self.coordinates_x = coordinates[0]
        self.coordinates_y = coordinates[1]

        if package_type == 'fragile':
            self.breaking_chance = random.uniform(0.0001, 0.01)  # 0.01-1% chance of breaking per km
            self.breaking_cost = random.uniform(3, 10)  # Extra cost in case of breaking

        elif package_type == 'urgent':
            self.delivery_time = random.uniform(100, 240)  # Delivery time in minutes (100 minutes to 4 hours)


def generate_package_stream(num_packages, map_size):
    package_types = ['fragile', 'normal', 'urgent']
    package_stream = [Package(random.choice(package_types), (random.uniform(0, map_size), random.uniform(0, map_size)))
                      for _ in range(num_packages)]
    return package_stream


# Example: Generate a stream of 15 packages in a map of size 60x60
num_packages = 15
map_size = 60
package_stream = generate_package_stream(num_packages, map_size)

df = pd.DataFrame([(i, package.package_type, package.coordinates_x,
                    package.coordinates_y, package.breaking_chance if package.package_type ==
                                                                      'fragile' else None,
                    package.breaking_cost if package.package_type ==
                                             'fragile' else None, package.delivery_time if package.package_type ==
                                                                                           'urgent' else None) for
                   i, package in enumerate(package_stream, start=1)],
                  columns=["Package", "Type", "CoordinatesX", "CoordinatesY", "Breaking Chance", "Breaking Cost",
                           "Delivery Time"])

print(df)