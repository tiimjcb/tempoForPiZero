from PIL import Image, ImageDraw, ImageFont
import datetime
import requests
from textwrap import wrap

# Dimensions de l'écran
EPD_WIDTH = 296
EPD_HEIGHT = 160

# Couleurs spécifiques pour l'écran e-ink
WHITE = 0  # Blanc
BLACK = 1   # Noir
YELLOW = 2   # Jaune
RED = 3     # Rouge




# Classe pour stocker les données de l'API du tarif Tempo
class TempoData:
    def __init__(self, date: datetime, code: int):
        self.date = date
        self.code = code



# Fonction pour récupérer les données de l'API du tarif Tempo
# 0 : inconnu, 1 : bleu, 2 : blanc, 3 : rouge
def get_data(string):

    match string:
        case 'today':
            url = "https://www.api-couleur-tempo.fr/api/jourTempo/today"
        case 'tomorrow':
            url = "https://www.api-couleur-tempo.fr/api/jourTempo/tomorrow"
        case _:
            raise ValueError("Invalid input: string must be 'today' or 'tomorrow'")

    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Error: {response.status_code}")
    periode = response.json().get('periode')
    today_year = datetime.datetime.now().year
    if str(today_year) not in periode:
       raise ValueError(f"Error: {today_year} not in {periode} -> there must be a problem with the API (or you're stuck in a time loop)")

    code = response.json().get('codeJour')
    date_str = response.json().get('dateJour')
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    return TempoData(date, code)



def update_screen():
    image = Image.new('P', (EPD_WIDTH, EPD_HEIGHT), WHITE)
    draw = ImageDraw.Draw(image)

    palette = [255, 255, 255, 0, 0, 0, 255, 255, 0, 255, 0, 0]  # Blanc, Noir, Jaune, Rouge
    image.putpalette(palette)

    try:
        # Récupération des données pour 'today' et 'tomorrow'
        today_data = get_data("today")
        tomorrow_data = get_data("tomorrow")

        # Barre de séparation verticale
        middle_x = EPD_WIDTH // 2
        draw.line((middle_x + 5, 10, middle_x + 5, int(EPD_HEIGHT * 0.8)), fill=BLACK)

        # Polices
        font_title = ImageFont.truetype("SFUIDisplay-Bold.ttf", 24)  # Grande police pour les titres
        font_text = ImageFont.truetype("SFUIDisplay-Bold.ttf", 16)  # Police pour le texte couleur

        # Titre "aujourd'hui"
        title_left = "Aujourd'hui"
        title_left_x = (middle_x - draw.textbbox((0, 0), title_left, font=font_title)[2]) // 2
        draw.text((title_left_x, 10), title_left, font=font_title, fill=BLACK)

        # Texte pour aujourd'hui
        today_color_text = ("Données\ninconnues" if today_data.code == 0 else
                            f"Jour\n{'bleu' if today_data.code == 1 else 'blanc' if today_data.code == 2 else 'rouge'}")
        today_text_x = (middle_x - draw.textbbox((0, 0), today_color_text, font=font_text)[2]) // 2
        draw.multiline_text((today_text_x, 60), today_color_text, font=font_text,
                            fill=RED if today_data.code == 3 else BLACK, spacing=4, align="center")

        # Titre "demain"
        title_right = "Demain"
        title_right_x = middle_x + (middle_x - draw.textbbox((0, 0), title_right, font=font_title)[2]) // 2
        draw.text((title_right_x, 10), title_right, font=font_title, fill=BLACK)

        # Texte demain
        tomorrow_color_text = ("Données\ninconnues" if tomorrow_data.code == 0 else
                               f"Jour\n{'bleu' if tomorrow_data.code == 1 else 'blanc' if tomorrow_data.code == 2 else 'rouge'}")
        tomorrow_text_x = middle_x + (middle_x - draw.textbbox((0, 0), tomorrow_color_text, font=font_text)[2]) // 2
        draw.multiline_text((tomorrow_text_x, 60), tomorrow_color_text, font=font_text,
                            fill=RED if tomorrow_data.code == 3 else BLACK, spacing=4, align="center")

        # Bas de l'écran -- ligne avec la date et heure de dernière MAJ
        last_update = datetime.datetime.now().strftime("Dernière MAJ : %d/%m/%y - %H:%M")
        date_text_bbox = draw.textbbox((0, 0), last_update, font=font_text)
        date_text_width = date_text_bbox[2] - date_text_bbox[0]
        date_text_height = date_text_bbox[3] - date_text_bbox[1]
        draw.text(((EPD_WIDTH - date_text_width) // 2,
                   EPD_HEIGHT - int(EPD_HEIGHT * 0.2) + (int(EPD_HEIGHT * 0.2) - date_text_height) // 2),
                  last_update, font=font_text, fill=BLACK)

    # On catch si il y a une exception
    except Exception as e:
        middle_x = EPD_WIDTH // 2

        # Symbole attention
        triangle_height = int(EPD_HEIGHT * 0.8)
        triangle_half_width = int(middle_x * 0.4)  # Réduit la largeur du triangle
        triangle_points = [
            (middle_x // 2, (EPD_HEIGHT - triangle_height) // 2),  # Sommet en haut
            (middle_x // 2 - triangle_half_width, (EPD_HEIGHT + triangle_height) // 2),  # Bas gauche
            (middle_x // 2 + triangle_half_width, (EPD_HEIGHT + triangle_height) // 2)  # Bas droite
        ]
        draw.polygon(triangle_points, fill=RED)
        warning_symbol = "!"
        font_warning = ImageFont.truetype("SFUIDisplay-Bold.ttf", 60)  # Taille réduite pour s'adapter au triangle
        warning_bbox = draw.textbbox((0, 0), warning_symbol, font=font_warning)
        warning_x = (middle_x // 2) - (warning_bbox[2] - warning_bbox[0]) // 2
        warning_y = (EPD_HEIGHT - warning_bbox[3]) // 2
        draw.text((warning_x, warning_y), warning_symbol, font=font_warning, fill=WHITE)

        # Divisions des lignes dans la colonne de droite
        right_top_section_height = int(EPD_HEIGHT * 0.3)
        right_bottom_section_start = right_top_section_height

        # Titre "ERREUR"
        error_title = "ERREUR"
        font_title = ImageFont.truetype("SFUIDisplay-Bold.ttf", 24)
        title_bbox = draw.textbbox((0, 0), error_title, font=font_title)
        title_x = middle_x + (middle_x - title_bbox[2]) // 2
        title_y = (right_top_section_height - title_bbox[3]) // 2
        draw.text((title_x, title_y), error_title, font=font_title, fill=BLACK)

        # On determine la nature de l'erreur et on ajuste le message en conséquence
        if isinstance(e, ValueError) and "Error:" in str(e):
            if "status code" in str(e):
                error_message = "Erreur avec l'API : Code statut"
            elif "time loop" in str(e):
                error_message = "Erreur avec l'API : Problème d'année"
            else:
                error_message = "Erreur inconnue avec l'API"
        elif "Connection" in str(e):
            error_message = "Erreur de connexion : vérifier le réseau"
        else:
            error_message = "Erreur inconnue"

        # Message d'erreur
        font_text = ImageFont.truetype("SFUIDisplay-Bold.ttf", 16)
        max_text_width = middle_x - 30  # Limite de largeur encore réduite pour le texte dans la colonne droite

        wrapped_text = "\n".join(wrap(error_message, width=15))  # Ajusté pour réduire davantage la largeur
        message_y = right_bottom_section_start + 10  # Décalage sous la ligne supérieure
        draw.multiline_text((middle_x + 10, message_y), wrapped_text, font=font_text, fill=BLACK, spacing=4)

    # Sauvegarder l'image
    image.save('simulation_e_paper_test.png')
    print("L'image a été sauvegardée sous 'simulation_e_paper_test.png'.")

# Main
update_screen()
