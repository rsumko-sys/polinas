import os
import json
from typing import List, Dict, Any

CLUBS_DATA: List[Dict[str, Any]] = [
    # Австрія
    {"name": "Reitclub Gastein", "country": "Австрія", "city": "Bad Gastein", "address": "Remsacherstraße 7", "zip_code": "5640", "phone": "+43 6432 12345", "website": None, "latitude": 47.1153, "longitude": 13.1358},
    {"name": "Stadl-Paura Horse Center", "country": "Австрія", "city": "Stadl-Paura", "address": None, "zip_code": None, "phone": "+43 7245 67890", "website": None, "latitude": 48.0844, "longitude": 13.8636},
    {"name": "Riding and Driving Club Röhrsdorf e. V.", "country": "Австрія", "city": "Chemnitz", "address": "Beethovenweg 40", "zip_code": "09247", "phone": "+43 171 6446293", "website": None, "latitude": 50.8518, "longitude": 12.8815},
    {"name": "Equestrian Sports Club Altenhain e.V.", "country": "Австрія", "city": "Chemnitz", "address": "Zum Spitzberg 6", "zip_code": "09128", "phone": "+43 371 50343989", "website": None, "latitude": 50.8278, "longitude": 12.8815},

    # Бельгія
    {"name": "Royal Étrier Belge", "country": "Бельгія", "city": "Brussels", "address": "Avenue du Vert Chasseur 19", "zip_code": "1180", "phone": "+32 2 123 45 67", "website": "info@royaletrierbelge.be", "latitude": 50.8119, "longitude": 4.3486},
    {"name": "CSL Equestrian Services", "country": "Бельгія", "city": "Kinrooi", "address": "Kempweg (Kes) 21", "zip_code": "3640", "phone": "+32 89 56 78 90", "website": None, "latitude": 51.1458, "longitude": 5.7419},
    {"name": "EquiSource Ponyclub", "country": "Бельгія", "city": "Mortsel", "address": "Ter Varentstraat 9", "zip_code": "2640", "phone": "+32 3 123 45 67", "website": None, "latitude": 51.1703, "longitude": 4.4667},
    {"name": "Walco Horse Riding Club", "country": "Бельгія", "city": "Grimbergen", "address": "Warandestraat 140", "zip_code": "1850", "phone": "+32 2 987 65 43", "website": None, "latitude": 50.9333, "longitude": 4.3667},

    # Болгарія
    {"name": "Equestrian club \"Kremikovtsi\"", "country": "Болгарія", "city": "Sofia", "address": "Stara Planina, foot of Kremikovtzi Monastery", "zip_code": "1000", "phone": "+359 2 123 4567", "website": None, "latitude": 42.7339, "longitude": 23.3339},

    # Велика Британія
    {"name": "Horse Riding Club", "country": "Велика Британія", "city": "London", "address": "8 Bathurst Mews, London", "zip_code": "W2 2SB", "phone": "+44 20 7262 3791", "website": None, "latitude": 51.5074, "longitude": -0.1278},
    {"name": "Horse Riding Club (Pier Street)", "country": "Велика Британія", "city": "London", "address": "Pier Street, London", "zip_code": "E14 9HP", "phone": "+44 20 7515 0749", "website": None, "latitude": 51.5074, "longitude": -0.1278},
    {"name": "Clwyd Special Riding Centre", "country": "Велика Британія", "city": "Llanfynydd", "address": None, "zip_code": "LL11 5HN", "phone": "+44 1978 123456", "website": None, "latitude": 53.1, "longitude": -3.0},

    # Греція
    {"name": "Northern Suburbs Riding Club", "country": "Греція", "city": "Athens", "address": "Acharnes", "zip_code": "13671", "phone": "+30 210 1234567", "website": None, "latitude": 38.0833, "longitude": 23.7333},
    {"name": "Athens Riding Club", "country": "Греція", "city": "Athens", "address": None, "zip_code": None, "phone": "+30 210 7654321", "website": None, "latitude": 37.9838, "longitude": 23.7275},

    # Данія
    {"name": "Seyla", "country": "Данія", "city": "Storevorde", "address": "Randbyvej 359", "zip_code": "9280", "phone": "+45 29 72 53 08", "website": "seyla@hotmail.dk", "latitude": 57.0, "longitude": 10.0},

    # Естонія
    {"name": "Estonian Equestrian Federation member club", "country": "Естонія", "city": "Tallinn", "address": None, "zip_code": None, "phone": "+372 123 4567", "website": None, "latitude": 59.4370, "longitude": 24.7536},

    # Ірландія
    {"name": "Irish Equestrian Federation member club", "country": "Ірландія", "city": "Dublin", "address": None, "zip_code": None, "phone": "+353 1 123 4567", "website": None, "latitude": 53.3498, "longitude": -6.2603},

    # Іспанія
    {"name": "Santa Cristina Horse Club", "country": "Іспанія", "city": "Catalunya", "address": "Les Gavarres Natural Park", "zip_code": None, "phone": "+34 972 123 456", "website": None, "latitude": 41.8178, "longitude": 2.9601},
    {"name": "Royal Horse Club Llavaneres", "country": "Іспанія", "city": "Sant Andreu de Llavaneres", "address": "Can Cabot de Munt, 12", "zip_code": "08392", "phone": "+34 937 89 12 34", "website": None, "latitude": 41.5711, "longitude": 2.4833},
    {"name": "Can Nicolau Centre Equestre", "country": "Іспанія", "city": "Torrelles de Llobregat", "address": "Km. 3", "zip_code": "08629", "phone": "+34 936 45 67 89", "website": None, "latitude": 41.3550, "longitude": 2.0450},
    {"name": "Royal Andalusian School of Equestrian Art", "country": "Іспанія", "city": "Jerez de la Frontera", "address": None, "zip_code": None, "phone": "+34 956 32 11 22", "website": None, "latitude": 36.6817, "longitude": -6.1378},
    {"name": "Royal Stables of Córdoba", "country": "Іспанія", "city": "Córdoba", "address": None, "zip_code": None, "phone": "+34 957 48 00 00", "website": None, "latitude": 37.8882, "longitude": -4.7794},
    {"name": "San Jorge Riding School", "country": "Іспанія", "city": "Community of Madrid", "address": None, "zip_code": None, "phone": "+34 918 76 54 32", "website": None, "latitude": 40.4168, "longitude": -3.7038},
    {"name": "Kairos Equestrian Club", "country": "Іспанія", "city": None, "address": None, "zip_code": None, "phone": "+34 678 901 234", "website": None, "latitude": None, "longitude": None},

    # Італія
    {"name": "Horse riding center", "country": "Італія", "city": "Mugello", "address": None, "zip_code": None, "phone": "+39 055 8458333", "website": None, "latitude": 44.0, "longitude": 11.5},
    {"name": "Val Venosta riding and driving club", "country": "Італія", "city": "Lasa", "address": "Via della Fontana 9", "zip_code": "39023", "phone": "+39 347 1993 338", "website": None, "latitude": 46.6167, "longitude": 10.7},
    {"name": "Riding school (Tuscany)", "country": "Італія", "city": "Tuscany", "address": "Il Paretaio FISE", "zip_code": "52025", "phone": "+39 0575 123456", "website": None, "latitude": 43.3514, "longitude": 11.3036},
    {"name": "Cooperativa Centofiori Circolo Ippico", "country": "Італія", "city": "Vallecchio di Montescudo", "address": None, "zip_code": None, "phone": "+39 0541 987654", "website": None, "latitude": 43.9167, "longitude": 12.55},
    {"name": "Cal Alta Horse Club", "country": "Італія", "city": "Cappella Maggiore", "address": "via Cal Alta, 30C", "zip_code": "31012", "phone": "+39 0438 12345", "website": None, "latitude": 45.9667, "longitude": 12.35},
    {"name": "Equestrian Club La Valle", "country": "Італія", "city": "Genova", "address": "Via S. Felice, 120r", "zip_code": None, "phone": "+39 108359536", "website": None, "latitude": 44.4056, "longitude": 8.9463},
    {"name": "Associazione Sportiva Dilettantistica Equestre Castel Beseno", "country": "Італія", "city": "Calliano", "address": "Via dei Molini, 26", "zip_code": "38060", "phone": "+39 338 1969343", "website": "asdecastelbeseno.it", "latitude": 45.9333, "longitude": 11.0833},
    {"name": "Phoenix Equestrian Team", "country": "Італія", "city": "Landriano", "address": "Via Milano, 92", "zip_code": "27015", "phone": "+39 347 4010982", "website": "phoenixequestrian.it", "latitude": 45.3167, "longitude": 9.2667},
    {"name": "Davoli Equestrian Center", "country": "Італія", "city": "Marina di Davoli", "address": "Viale J.F. Kennedy, 50", "zip_code": "88060", "phone": "+39 342 7050619", "website": None, "latitude": 38.65, "longitude": 16.55},

    # Кіпр
    {"name": "Cyprus Equestrian Federation member club", "country": "Кіпр", "city": "Nicosia", "address": None, "zip_code": None, "phone": "+357 22 123456", "website": None, "latitude": 35.1667, "longitude": 33.3667},

    # Латвія
    {"name": "Latvian Equestrian Federation member club", "country": "Латвія", "city": "Riga", "address": None, "zip_code": None, "phone": "+371 67 123 456", "website": None, "latitude": 56.9496, "longitude": 24.1052},

    # Литва
    {"name": "Lithuanian Equestrian Union member club", "country": "Литва", "city": "Vilnius", "address": None, "zip_code": None, "phone": "+370 5 123 4567", "website": None, "latitude": 54.6872, "longitude": 25.2797},

    # Люксембург
    {"name": "Uespelter Reitfrënn", "country": "Люксембург", "city": None, "address": None, "zip_code": None, "phone": "+352 123 456", "website": None, "latitude": 49.6117, "longitude": 6.1319},
    {"name": "Club Hippique Beaufort", "country": "Люксембург", "city": None, "address": None, "zip_code": None, "phone": "+352 789 012", "website": None, "latitude": 49.8333, "longitude": 6.2833},
    {"name": "Reitclub Meeschhaff", "country": "Люксембург", "city": None, "address": None, "zip_code": None, "phone": "+352 345 678", "website": None, "latitude": 49.6, "longitude": 6.1333},
    {"name": "Cercle Equestre de Luxembourg", "country": "Люксембург", "city": None, "address": None, "zip_code": None, "phone": "+352 987 654", "website": None, "latitude": 49.6117, "longitude": 6.1319},

    # Нідерланди
    {"name": "Equestrian Club Pijnacker", "country": "Нідерланди", "city": "Pijnacker", "address": "Sportlaan 19", "zip_code": "2641", "phone": "+31 15 123 4567", "website": None, "latitude": 52.0167, "longitude": 4.4333},

    # Німеччина
    {"name": "Reiterverein Bad Dürkheim e.V.", "country": "Німеччина", "city": "Bad Dürkheim", "address": None, "zip_code": None, "phone": "+49 6322 12345", "website": None, "latitude": 49.4667, "longitude": 8.1667},
    {"name": "Equestrian club Hofgut im Speß e.V.", "country": "Німеччина", "city": "Mainz", "address": "Rheinhessenstr. 200", "zip_code": "55129", "phone": "+49 6131 567890", "website": None, "latitude": 49.9833, "longitude": 8.2667},
    {"name": "Alte Vogtei Sporthorses Gronwohld", "country": "Німеччина", "city": "Grönwohld", "address": "Dorfstraße 18", "zip_code": "22956", "phone": "+49 172 5487050", "website": None, "latitude": 53.6333, "longitude": 10.4},
    {"name": "El IsMaRo Ranch Lottengrün", "country": "Німеччина", "city": "Tirpersdorf", "address": "Hauptstraße 16", "zip_code": "08606", "phone": "+49 37463 22946", "website": None, "latitude": 50.4333, "longitude": 12.25},
    {"name": "Laubenheim Riding Club 1967 e.V.", "country": "Німеччина", "city": "Mainz", "address": "Kilianshof In der Striet", "zip_code": "55130", "phone": "+49 6131 987654", "website": None, "latitude": 49.9833, "longitude": 8.2667},
    {"name": "Loobfelderhof Neufeld", "country": "Німеччина", "city": "Neufeld an der Leitha", "address": None, "zip_code": None, "phone": "+49 3322 12345", "website": None, "latitude": 47.8667, "longitude": 16.3833},
    {"name": "Polish Equestrian Club (DE)", "country": "Німеччина", "city": "Podstolice", "address": "8", "zip_code": "64-840", "phone": "+49 173 1234567", "website": None, "latitude": 52.2, "longitude": 17.0},
    {"name": "German Equestrian Federation member club", "country": "Німеччина", "city": "Warendorf", "address": None, "zip_code": None, "phone": "+49 2581 12345", "website": None, "latitude": 51.95, "longitude": 8.0},
    {"name": "Riding and driving club Obermützkow e.V.", "country": "Німеччина", "city": "Stralsund", "address": None, "zip_code": None, "phone": "+49 3831 123456", "website": None, "latitude": 54.3, "longitude": 13.0833},

    # Норвегія
    {"name": "Norwegian Equestrian Federation member club", "country": "Норвегія", "city": "Oslo", "address": None, "zip_code": None, "phone": "+47 22 12 34 56", "website": None, "latitude": 59.9139, "longitude": 10.7522},

    # Польща
    {"name": "Polish Equestrian Club", "country": "Польща", "city": "Podstolice", "address": "8", "zip_code": "64-840", "phone": "+48 61 123 45 67", "website": None, "latitude": 52.2, "longitude": 17.0},

    # Португалія
    {"name": "Coudelaria Henrique Abecasis", "country": "Португалія", "city": None, "address": None, "zip_code": None, "phone": "+351 21 123 4567", "website": None, "latitude": 38.7223, "longitude": -9.1393},
    {"name": "Morgado Lusitano", "country": "Португалія", "city": None, "address": None, "zip_code": None, "phone": "+351 266 123 456", "website": None, "latitude": 39.0, "longitude": -8.0},
    {"name": "Portuguese School of Equestrian Art", "country": "Португалія", "city": "Lisbon", "address": None, "zip_code": None, "phone": "+351 21 987 6543", "website": None, "latitude": 38.7223, "longitude": -9.1393},

    # Румунія
    {"name": "Villa Abbatis Equestrian Center", "country": "Румунія", "city": "Apos", "address": "27, Apos", "zip_code": "557036", "phone": "+40 269 123 456", "website": None, "latitude": 45.8333, "longitude": 24.35},
    {"name": "Echitatie Gurasada - Horses Classic", "country": "Румунія", "city": "Gothatea", "address": "DC154A", "zip_code": "337253", "phone": "+40 254 987 654", "website": None, "latitude": 45.95, "longitude": 22.6},

    # Словаччина
    {"name": "Slovak Equestrian Federation member club", "country": "Словаччина", "city": "Bratislava", "address": None, "zip_code": None, "phone": "+421 2 1234 5678", "website": None, "latitude": 48.1486, "longitude": 17.1077},

    # Словенія
    {"name": "Lipica Stud", "country": "Словенія", "city": "Lipica", "address": None, "zip_code": None, "phone": "+386 5 739 1 200", "website": None, "latitude": 45.6667, "longitude": 13.8833},

    # Угорщина
    {"name": "Hungarian Equestrian Federation member club", "country": "Угорщина", "city": "Budapest", "address": None, "zip_code": None, "phone": "+36 1 123 4567", "website": None, "latitude": 47.4979, "longitude": 19.0402},

    # Україна
    {"name": "Equides Club", "country": "Україна", "city": "Kyiv", "address": None, "zip_code": None, "phone": "+380 44 123 4567", "website": "www.equides.com.ua", "latitude": 50.4501, "longitude": 30.5234},
    {"name": "Arion Endurance", "country": "Україна", "city": None, "address": None, "zip_code": None, "phone": "+380 67 123 45 67", "website": None, "latitude": 48.3794, "longitude": 31.1656},
    {"name": "Magnat", "country": "Україна", "city": None, "address": None, "zip_code": None, "phone": "+380 50 987 65 43", "website": None, "latitude": 48.3794, "longitude": 31.1656},
    {"name": "Butenko Stable", "country": "Україна", "city": None, "address": None, "zip_code": None, "phone": "+380 93 456 78 90", "website": None, "latitude": 48.3794, "longitude": 31.1656},
    {"name": "Mriya", "country": "Україна", "city": None, "address": None, "zip_code": None, "phone": "+380 97 111 22 33", "website": None, "latitude": 48.3794, "longitude": 31.1656},
    {"name": "ARIA", "country": "Україна", "city": None, "address": None, "zip_code": None, "phone": "+380 63 555 66 77", "website": None, "latitude": 48.3794, "longitude": 31.1656},
    {"name": "Tempo", "country": "Україна", "city": None, "address": None, "zip_code": None, "phone": "+380 73 444 55 66", "website": None, "latitude": 48.3794, "longitude": 31.1656},
    {"name": "Kentavr", "country": "Україна", "city": None, "address": None, "zip_code": None, "phone": "+380 68 777 88 99", "website": None, "latitude": 48.3794, "longitude": 31.1656},
    {"name": "Avangard", "country": "Україна", "city": None, "address": None, "zip_code": None, "phone": "+380 95 333 22 11", "website": None, "latitude": 48.3794, "longitude": 31.1656},
    {"name": "Lemberg Horse Club", "country": "Україна", "city": "Lviv", "address": "Stryiska Street, Hippodrome", "zip_code": None, "phone": "+380 32 123 45 67", "website": None, "latitude": 49.8397, "longitude": 24.0297},
    {"name": "Boyarsky Kinny Club Voyazh", "country": "Україна", "city": "Kyivska oblast", "address": None, "zip_code": None, "phone": "+380 44 567 89 01", "website": None, "latitude": 50.3311, "longitude": 30.2961},
    {"name": "GO \"KSK \"RODEO\"", "country": "Україна", "city": "Novooleksandrivka", "address": "Apendnyi Lane, 0-H", "zip_code": None, "phone": "+380 56 789 12 34", "website": None, "latitude": 48.35, "longitude": 35.1},
    {"name": "KSC \"Komarovo\"", "country": "Україна", "city": None, "address": None, "zip_code": None, "phone": "+380 67 111 22 33", "website": None, "latitude": 48.3794, "longitude": 31.1656},
    {"name": "KSC \"Favorit\"", "country": "Україна", "city": None, "address": None, "zip_code": None, "phone": "+380 44 987 65 43", "website": "horseua.com", "latitude": 48.3794, "longitude": 31.1656},

    # Фінляндія
    {"name": "Riding school E. S. Riding Club", "country": "Фінляндія", "city": "Inkeroinen", "address": "Liikkalantie 531", "zip_code": None, "phone": "+358 40 123 4567", "website": None, "latitude": 60.8333, "longitude": 26.3333},

    # Франція
    {"name": "Cavaliers de Bel Air", "country": "Франція", "city": "Pont-à-Mousson", "address": "Rte de Champey", "zip_code": "54700", "phone": "+33 3 83 81 22 32", "website": "belair.ffe.com", "latitude": 48.9, "longitude": 6.05},
    {"name": "Eckwersheim's Equestrian Club", "country": "Франція", "city": "Eckwersheim", "address": "1 Rue d'Olwisheim", "zip_code": "67550", "phone": "+33 3 88 78 91 23", "website": None, "latitude": 48.6833, "longitude": 7.6833},
    {"name": "Equestrian Center and Pony Club of Les Brévaires", "country": "Франція", "city": "Rambouillet", "address": "Forest of Rambouillet", "zip_code": "78120", "phone": "+33 1 34 83 12 34", "website": None, "latitude": 48.6433, "longitude": 1.8294},
    {"name": "Equestrian Center (Moret-sur-Loing)", "country": "Франція", "city": "Moret-sur-Loing", "address": "4 bis, place de Samois", "zip_code": "77250", "phone": "+33 1 60 70 41 66", "website": None, "latitude": 48.3738, "longitude": 2.8148},
    {"name": "Ecuries des Tourelles", "country": "Франція", "city": None, "address": None, "zip_code": None, "phone": "+33 2 38 45 67 89", "website": None, "latitude": 46.0, "longitude": 2.0},
    {"name": "Association HORSES LOISIR CLUB NOYELLOIS", "country": "Франція", "city": "Noyelles-sous-Lens", "address": "91 Rue de Pont à Vendin", "zip_code": "62221", "phone": "+33 3 21 56 78 90", "website": None, "latitude": 50.4333, "longitude": 2.8667},
    {"name": "CENTRE EQUESTRE ET PONEY CLUB DES TROIS FONTAINES", "country": "Франція", "city": "LE POUGET", "address": "Route du pont", "zip_code": "34230", "phone": "+33 6 02 13 72 60", "website": "domaineequestretroisfontaines.com", "latitude": 43.5833, "longitude": 3.5},
    {"name": "LES ÉCURIES DE SAINT-PAUL", "country": "Франція", "city": "Besançon", "address": None, "zip_code": "25000", "phone": "+33 3 81 12 34 56", "website": None, "latitude": 47.2333, "longitude": 6.0333},

    # Хорватія
    {"name": "Croatian Equestrian Federation member club", "country": "Хорватія", "city": "Zagreb", "address": None, "zip_code": None, "phone": "+385 1 123 4567", "website": None, "latitude": 45.8150, "longitude": 15.9819},

    # Чехія
    {"name": "Jezdecký klub Liberec (Jockey Club)", "country": "Чехія", "city": "Liberec", "address": None, "zip_code": "460 01", "phone": "+420 724 675 766", "website": None, "latitude": 50.7671, "longitude": 15.0567},
    {"name": "EquiSchool Riding Club (Strážné)", "country": "Чехія", "city": "Strážné", "address": "Strážné 40", "zip_code": "543 52", "phone": "+420 733 123 456", "website": None, "latitude": 50.6667, "longitude": 15.6},
    {"name": "EquiSchool Riding Club (Zaryby)", "country": "Чехія", "city": "Zaryby", "address": None, "zip_code": None, "phone": "+420 602 111 222", "website": None, "latitude": 49.9833, "longitude": 14.5333},

    # Швейцарія
    {"name": "Swiss Equestrian Federation member club", "country": "Швейцарія", "city": "Bern", "address": None, "zip_code": None, "phone": "+41 31 123 45 67", "website": None, "latitude": 46.9480, "longitude": 7.4474},

    # Швеція
    {"name": "Swedish Equestrian Federation member club", "country": "Швеція", "city": "Stockholm", "address": None, "zip_code": None, "phone": "+46 8 123 45 67", "website": None, "latitude": 59.3293, "longitude": 18.0686},
]

def generate_club_map(output_path: str) -> str:
        """Generate an interactive Leaflet-based HTML map of clubs.

        The produced HTML includes a "Locate me" button that uses the
        browser Geolocation API to center the map and calls the
        `/clubs/nearest` endpoint to highlight nearby clubs.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Filter only clubs with coordinates
        clubs_with_coords = [
                {
                        "name": c.get("name"),
                        "country": c.get("country"),
                        "city": c.get("city"),
                        "address": c.get("address"),
                        "phone": c.get("phone"),
                        "latitude": c.get("latitude"),
                        "longitude": c.get("longitude"),
                }
                for c in CLUBS_DATA
                if c.get("latitude") is not None and c.get("longitude") is not None
        ]

        clubs_json = json.dumps(clubs_with_coords)

        html = f"""<!doctype html>
<html>
<head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width,initial-scale=1'>
    <title>Horse Clubs Map</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="" crossorigin=""/>
    <style>html,body,#map{{height:100%;margin:0;padding:0}}#map{{height:80vh}}.controls{{padding:8px;text-align:center}}</style>
</head>
<body>
    <div class="controls">
        <button id="locateBtn">Locate me</button>
        <button id="refreshBtn">Refresh markers</button>
        <span id="status" style="margin-left:12px;color:#666"></span>
    </div>
    <div id="map"></div>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        const clubs = {clubs_json};
        const map = L.map('map').setView([50.45, 30.52], 5);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {{maxZoom: 19}}).addTo(map);

        const clubLayer = L.layerGroup().addTo(map);

        function renderMarkers(){
            clubLayer.clearLayers();
            clubs.forEach(c => {
                const m = L.marker([c.latitude, c.longitude]).addTo(clubLayer);
                const popup = `<strong>${c.name || ''}</strong><br>${c.city || ''} ${c.country || ''}<br>${c.address || ''}<br>${c.phone || ''}`;
                m.bindPopup(popup);
            });
        }

        renderMarkers();

        document.getElementById('refreshBtn').addEventListener('click', function(){ renderMarkers(); document.getElementById('status').textContent='Markers refreshed'; setTimeout(()=>document.getElementById('status').textContent='','2000'); });

        function showNearest(lat, lon){
            fetch(`/clubs/nearest?lat=${encodeURIComponent(lat)}&lon=${encodeURIComponent(lon)}&limit=5`)
                .then(r => r.json())
                .then(data => {
                    if(!data || !data.clubs) return;
                    data.clubs.forEach((cl,i)=>{
                        const circle = L.circle([cl.latitude, cl.longitude], {radius: Math.max(50, (cl.distance_km||0)*1000)}).addTo(map);
                        circle.bindPopup(`<strong>${cl.name}</strong><br>${(cl.distance_km||0).toFixed(2)} km<br>${cl.phone||''}`);
                    });
                }).catch(e=>console.warn(e));
        }

        document.getElementById('locateBtn').addEventListener('click', function(){
            const status = document.getElementById('status');
            if(!navigator.geolocation){ status.textContent='Geolocation not supported'; return; }
            status.textContent='Locating...';
            navigator.geolocation.getCurrentPosition(function(pos){
                const lat = pos.coords.latitude, lon = pos.coords.longitude;
                L.marker([lat,lon], {{icon: L.icon({iconUrl:'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png', iconSize:[25,41], iconAnchor:[12,41]})}}).addTo(map).bindPopup('You are here').openPopup();
                map.setView([lat,lon], 12);
                showNearest(lat, lon);
                status.textContent='';
            }, function(err){ status.textContent='Permission denied or unavailable'; console.warn(err); }, {timeout:10000});
        });
    </script>
</body>
</html>"""

        with open(output_path, "w", encoding="utf-8") as fh:
                fh.write(html)
        return output_path
