import random

class NameGenerator:
    ROOTS = {
        'prefixes': ['Al', 'Bri', 'Car', 'Der', 'Eli', 'Fal', 'Gra', 'Hel', 'Ian', 'Jal', 'Kor', 'Lin', 'Mar', 'Nor', 'Ori', 'Pal', 'Que', 'Ril', 'Sal', 'Tal'],
        'middles': ['an', 'be', 'ci', 'do', 'er', 'fa', 'go', 'hu', 'in', 'jo', 'ka', 'le', 'mi', 'no', 'op', 'pe', 'qu', 'ra', 'si', 'tu'],
        'suffixes': ['a', 'en', 'is', 'on', 'us', 'ia', 'er', 'ly', 'an', 'da', 'ka', 'ma', 'na', 'ra', 'ta', 'va', 'ya', 'za', 'ie', 'io'],
        'name_roots': ['Smith', 'John', 'Will', 'Tay', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Robinson'],
        'name_endings': ['son', 'berg', 'stein', 'man', 'ton', 'field', 'wood', 'land', 'ford', 'dale', 'ley', 'ham', 'ton', 'bury', 'well', 'side', 'brook', 'way', 'gate', 'worth']
    }

    PATTERNS = {
        'first_name': [
            ['prefixes', 'suffixes'],
            ['prefixes', 'middles', 'suffixes'],
            ['prefixes', 'middles', 'middles', 'suffixes'],
            ['prefixes', 'suffixes']
        ],
        'last_name': [
            ['name_roots', 'name_endings'],
            ['name_roots'],
            ['prefixes', 'middles', 'name_endings'],
            ['name_roots', 'name_endings']
        ]
    }

    def _generate_component(self, patterns):
        pattern = random.choice(patterns)
        component = ""
        for part in pattern:
            component += random.choice(self.ROOTS[part])
        return component

    def generate(self):
        first = self._generate_component(self.PATTERNS['first_name']).capitalize()
        last = self._generate_component(self.PATTERNS['last_name']).capitalize()
        return {
            'first_name': first,
            'last_name': last,
            'full_name': f"{first} {last}"
        }

def generate_psu_email(first_name, last_name):
    digits = random.randint(100, 9999)
    return f"{first_name.lower()}.{last_name.lower()}{digits}@psu.edu"

def generate_birth_date():
    year = 2000 + random.randint(0, 5)
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 28)).zfill(2)
    return f"{year}-{month}-{day}"

def generate_psu_id():
    suffix = "".join([str(random.randint(0, 9)) for _ in range(8)])
    return f"9{suffix}"
