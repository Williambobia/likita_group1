"""
Commande Django pour créer des données de test
Usage: python manage.py create_test_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

from apps.core.models import Membre, MessageDirectrice, VisionMission
from apps.media_app.models import Emission, ArticleEmission
from apps.events.models import Evenement, GalerieEvenement, Inscription
from apps.academia.models import Formation, InscriptionFormation, Certificat
from apps.blog.models import Categorie, Article, Commentaire
from apps.users.models import ProfilUtilisateur


class Command(BaseCommand):
    help = 'Crée des données de test pour LIKITA Group'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Création des données de test...'))
        
        # 1. Créer des utilisateurs de test
        self.create_users()
        
        # 2. Créer des membres de l'équipe
        self.create_membres()
        
        # 3. Créer message de la directrice
        self.create_message_directrice()
        
        # 4. Créer Vision/Mission/Valeurs
        self.create_vision_mission()
        
        # 5. Créer des émissions
        self.create_emissions()
        
        # 6. Créer des événements
        self.create_evenements()
        
        # 7. Créer des formations
        self.create_formations()
        
        # 8. Créer des articles de blog
        self.create_articles()
        
        # 9. Créer des inscriptions de test
        self.create_inscriptions()
        
        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] Donnees de test creees avec succes!'))
        self.stdout.write(self.style.SUCCESS('Vous pouvez maintenant vous connecter avec:'))
        self.stdout.write(self.style.SUCCESS('Username: testuser1 / Password: testpass123'))

    def create_users(self):
        """Créer 3 utilisateurs de test"""
        self.stdout.write('Création des utilisateurs...')
        users_data = [
            {'username': 'testuser1', 'email': 'test1@likita.com', 'first_name': 'Marie', 'last_name': 'Dubois'},
            {'username': 'testuser2', 'email': 'test2@likita.com', 'first_name': 'Sophie', 'last_name': 'Martin'},
            {'username': 'testuser3', 'email': 'test3@likita.com', 'first_name': 'Julie', 'last_name': 'Bernard'},
        ]
        
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
                ProfilUtilisateur.objects.get_or_create(user=user)
                self.stdout.write(f'  + Utilisateur cree: {user.username}')

    def create_membres(self):
        """Créer 5 membres de l'équipe"""
        self.stdout.write('Création des membres de l\'équipe...')
        membres_data = [
            {'nom': 'Pulumba', 'prenom': 'Nadine', 'fonction': 'Directrice Générale', 'biographie': 'Fondatrice et Directrice Générale de LIKITA Group, passionnée par l\'autonomisation des femmes.'},
            {'nom': 'Kabila', 'prenom': 'Sarah', 'fonction': 'Responsable Communication', 'biographie': 'Experte en communication et marketing digital.'},
            {'nom': 'Mwamba', 'prenom': 'Grace', 'fonction': 'Responsable Événements', 'biographie': 'Spécialiste en organisation d\'événements et gestion de projets.'},
            {'nom': 'Tshisekedi', 'prenom': 'Aline', 'fonction': 'Responsable Formations', 'biographie': 'Formatrice certifiée en développement personnel et professionnel.'},
            {'nom': 'Lumumba', 'prenom': 'Patience', 'fonction': 'Responsable Médias', 'biographie': 'Productrice et animatrice d\'émissions télévisées.'},
        ]
        
        for i, membre_data in enumerate(membres_data):
            Membre.objects.get_or_create(
                nom=membre_data['nom'],
                prenom=membre_data['prenom'],
                defaults={
                    'fonction': membre_data['fonction'],
                    'biographie': membre_data['biographie'],
                    'ordre_affichage': i + 1,
                    'actif': True,
                }
            )
            self.stdout.write(f'  + Membre cree: {membre_data["prenom"]} {membre_data["nom"]}')

    def create_message_directrice(self):
        """Créer le message de la directrice"""
        self.stdout.write('Création du message de la directrice...')
        MessageDirectrice.objects.get_or_create(
            titre='Mot de la Directrice Générale',
            defaults={
                'contenu': '''Chers visiteurs,

C'est avec une immense joie que je vous accueille sur le site de LIKITA Group. Notre organisation est née d'une vision simple mais puissante : autonomiser les femmes à travers les médias, les événements et l'éducation.

Depuis notre création, nous avons accompagné des centaines de femmes dans leur développement personnel et professionnel. Chaque émission, chaque événement, chaque formation est une opportunité de créer un impact positif dans nos communautés.

Ensemble, construisons un avenir meilleur où chaque femme peut réaliser son plein potentiel.

Bienvenue dans la famille LIKITA !''',
                'signature': 'Nadine Pulumba',
                'fonction': 'Directrice Générale',
                'actif': True,
            }
        )
        self.stdout.write('  + Message de la directrice cree')

    def create_vision_mission(self):
        """Créer Vision, Mission et Valeurs"""
        self.stdout.write('Création de la Vision, Mission et Valeurs...')
        
        # Vision
        VisionMission.objects.get_or_create(
            type='vision',
            defaults={
                'titre': 'Notre Vision',
                'description': 'Être la référence en matière d\'autonomisation des femmes en RDC et en Afrique, à travers des médias inspirants, des événements transformateurs et des formations de qualité.',
                'ordre_affichage': 1,
                'actif': True,
            }
        )
        
        # Mission
        VisionMission.objects.get_or_create(
            type='mission',
            defaults={
                'titre': 'Notre Mission',
                'description': 'Autonomiser les femmes en leur offrant des plateformes médiatiques, des opportunités de formation et des espaces de networking pour leur développement personnel et professionnel.',
                'ordre_affichage': 1,
                'actif': True,
            }
        )
        
        # Valeurs
        valeurs_data = [
            {'titre': 'Excellence', 'description': 'Nous visons l\'excellence dans tout ce que nous entreprenons.', 'icone': 'fas fa-star', 'ordre': 1},
            {'titre': 'Intégrité', 'description': 'Nous agissons avec honnêteté et transparence.', 'icone': 'fas fa-shield-alt', 'ordre': 2},
            {'titre': 'Solidarité', 'description': 'Nous croyons en la force du collectif et de l\'entraide.', 'icone': 'fas fa-hands-helping', 'ordre': 3},
            {'titre': 'Innovation', 'description': 'Nous innovons constamment pour mieux servir notre communauté.', 'icone': 'fas fa-lightbulb', 'ordre': 4},
        ]
        
        for valeur_data in valeurs_data:
            VisionMission.objects.get_or_create(
                type='valeur',
                titre=valeur_data['titre'],
                defaults={
                    'description': valeur_data['description'],
                    'icone': valeur_data['icone'],
                    'ordre_affichage': valeur_data['ordre'],
                    'actif': True,
                }
            )
        
        self.stdout.write('  + Vision, Mission et Valeurs creees')

    def create_emissions(self):
        """Créer 4 émissions"""
        self.stdout.write('Création des émissions...')
        emissions_data = [
            {
                'titre': 'Femmes Entrepreneures : Histoires de Succès',
                'description': 'Découvrez les parcours inspirants de femmes entrepreneures qui ont réussi à créer leur entreprise.',
                'date_diffusion': timezone.now().date() - timedelta(days=30),
                'invite': 'Marie Kabila, Entrepreneure',
                'duree': '45 min',
                'tags': 'entrepreneuriat, femmes, succès, inspiration',
            },
            {
                'titre': 'Leadership Féminin en Afrique',
                'description': 'Une discussion approfondie sur le leadership féminin et les défis à relever.',
                'date_diffusion': timezone.now().date() - timedelta(days=20),
                'invite': 'Dr. Sarah Mwamba, Consultante',
                'duree': '50 min',
                'tags': 'leadership, femmes, afrique, développement',
            },
            {
                'titre': 'Éducation et Formation des Femmes',
                'description': 'L\'importance de l\'éducation et de la formation continue pour l\'autonomisation des femmes.',
                'date_diffusion': timezone.now().date() - timedelta(days=10),
                'invite': 'Prof. Grace Tshisekedi',
                'duree': '40 min',
                'tags': 'éducation, formation, femmes, développement',
            },
            {
                'titre': 'Santé et Bien-être des Femmes',
                'description': 'Un épisode dédié à la santé physique et mentale des femmes.',
                'date_diffusion': timezone.now().date() - timedelta(days=5),
                'invite': 'Dr. Aline Lumumba, Médecin',
                'duree': '35 min',
                'tags': 'santé, bien-être, femmes, médecine',
            },
        ]
        
        for emission_data in emissions_data:
            emission, created = Emission.objects.get_or_create(
                titre=emission_data['titre'],
                defaults={
                    'description': emission_data['description'],
                    'date_diffusion': emission_data['date_diffusion'],
                    'invite': emission_data['invite'],
                    'duree': emission_data['duree'],
                    'tags': emission_data['tags'],
                    'publie': True,
                }
            )
            if created:
                self.stdout.write(f'  + Emission creee: {emission.titre}')

    def create_evenements(self):
        """Créer 4 événements"""
        self.stdout.write('Création des événements...')
        evenements_data = [
            {
                'titre': 'Forum Mwasi Mwinda 2024',
                'type_evenement': 'forum',
                'description': 'Le grand forum annuel qui célèbre les réalisations féminines et encourage le dialogue.',
                'date_debut': timezone.now() + timedelta(days=30),
                'date_fin': timezone.now() + timedelta(days=30, hours=8),
                'lieu': 'Kinshasa, RDC',
                'prix': 0,
                'places_disponibles': 200,
            },
            {
                'titre': 'Conférence sur l\'Entrepreneuriat Féminin',
                'type_evenement': 'conference',
                'description': 'Une conférence pour encourager et soutenir les femmes entrepreneures.',
                'date_debut': timezone.now() + timedelta(days=45),
                'date_fin': timezone.now() + timedelta(days=45, hours=4),
                'lieu': 'Lubumbashi, RDC',
                'prix': 5000,
                'places_disponibles': 100,
            },
            {
                'titre': 'Atelier de Développement Personnel',
                'type_evenement': 'atelier',
                'description': 'Un atelier pratique pour développer vos compétences personnelles.',
                'date_debut': timezone.now() + timedelta(days=60),
                'date_fin': timezone.now() + timedelta(days=60, hours=6),
                'lieu': 'Kinshasa, RDC',
                'prix': 10000,
                'places_disponibles': 50,
            },
            {
                'titre': 'Séminaire Leadership Féminin',
                'type_evenement': 'seminaire',
                'description': 'Un séminaire intensif sur le leadership et la prise de décision.',
                'date_debut': timezone.now() + timedelta(days=75),
                'date_fin': timezone.now() + timedelta(days=77),
                'lieu': 'Kinshasa, RDC',
                'prix': 25000,
                'places_disponibles': 30,
            },
        ]
        
        for event_data in evenements_data:
            evenement, created = Evenement.objects.get_or_create(
                titre=event_data['titre'],
                defaults={
                    'type_evenement': event_data['type_evenement'],
                    'description': event_data['description'],
                    'description_courte': event_data['description'][:200],
                    'date_debut': event_data['date_debut'],
                    'date_fin': event_data['date_fin'],
                    'lieu': event_data['lieu'],
                    'prix': event_data['prix'],
                    'places_disponibles': event_data['places_disponibles'],
                    'statut': 'a_venir',
                    'publie': True,
                }
            )
            if created:
                self.stdout.write(f'  + Evenement cree: {evenement.titre}')

    def create_formations(self):
        """Créer 4 formations"""
        self.stdout.write('Création des formations...')
        formations_data = [
            {
                'titre': 'Formation en Leadership Féminin',
                'theme': 'Leadership et Management',
                'description': 'Une formation complète pour développer vos compétences en leadership.',
                'type_formation': 'formation',
                'niveau': 'intermediaire',
                'duree': '3 jours',
                'prix': 50000,
                'certificat': True,
                'formateur': 'Dr. Sarah Mwamba',
            },
            {
                'titre': 'Webinaire : Communication Efficace',
                'theme': 'Communication',
                'description': 'Apprenez les techniques de communication efficace en ligne.',
                'type_formation': 'webinaire',
                'niveau': 'tous',
                'duree': '2 heures',
                'prix': 0,
                'certificat': False,
                'formateur': 'Marie Kabila',
            },
            {
                'titre': 'Cours en Ligne : Gestion Financière',
                'theme': 'Finance',
                'description': 'Maîtrisez les bases de la gestion financière personnelle et professionnelle.',
                'type_formation': 'cours',
                'niveau': 'debutant',
                'duree': '4 semaines',
                'prix': 30000,
                'certificat': True,
                'formateur': 'Grace Tshisekedi',
            },
            {
                'titre': 'Atelier : Création d\'Entreprise',
                'theme': 'Entrepreneuriat',
                'description': 'Un atelier pratique pour créer et lancer votre entreprise.',
                'type_formation': 'atelier',
                'niveau': 'tous',
                'duree': '1 jour',
                'prix': 20000,
                'certificat': True,
                'formateur': 'Aline Lumumba',
            },
        ]
        
        for formation_data in formations_data:
            formation, created = Formation.objects.get_or_create(
                titre=formation_data['titre'],
                defaults={
                    'theme': formation_data['theme'],
                    'description': formation_data['description'],
                    'description_courte': formation_data['description'][:200],
                    'type_formation': formation_data['type_formation'],
                    'niveau': formation_data['niveau'],
                    'duree': formation_data['duree'],
                    'prix': formation_data['prix'],
                    'certificat': formation_data['certificat'],
                    'formateur': formation_data['formateur'],
                    'publie': True,
                }
            )
            if created:
                self.stdout.write(f'  + Formation creee: {formation.titre}')

    def create_articles(self):
        """Créer 5 articles de blog"""
        self.stdout.write('Création des articles de blog...')
        
        # Créer des catégories
        categories_data = [
            {'nom': 'Actualités', 'couleur': '#F2B705'},
            {'nom': 'Événements', 'couleur': '#3A2A1A'},
            {'nom': 'Formations', 'couleur': '#F8E6B0'},
            {'nom': 'Témoignages', 'couleur': '#28a745'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            categorie, created = Categorie.objects.get_or_create(
                nom=cat_data['nom'],
                defaults={'couleur': cat_data['couleur']}
            )
            categories[cat_data['nom']] = categorie
        
        # Créer des articles
        user = User.objects.first()
        articles_data = [
            {
                'titre': 'Lancement de LIKITA Group : Un Nouveau Départ',
                'categorie': 'Actualités',
                'description_courte': 'Découvrez l\'histoire du lancement de LIKITA Group et nos objectifs pour l\'avenir.',
                'contenu': 'LIKITA Group a été lancé avec une vision claire : autonomiser les femmes à travers les médias, les événements et l\'éducation. Cet article retrace notre parcours depuis le début.',
                'tags': 'lancement, likita, femmes, autonomisation',
            },
            {
                'titre': 'Forum Mwasi Mwinda 2024 : Un Succès Retentissant',
                'categorie': 'Événements',
                'description_courte': 'Retour sur le Forum Mwasi Mwinda 2024 qui a rassemblé plus de 200 participantes.',
                'contenu': 'Le Forum Mwasi Mwinda 2024 a été un véritable succès avec plus de 200 participantes venues de toute la RDC. Des conférences inspirantes, des ateliers pratiques et des moments de networking inoubliables.',
                'tags': 'forum, événement, succès, femmes',
            },
            {
                'titre': '5 Conseils pour Développer Votre Leadership',
                'categorie': 'Formations',
                'description_courte': 'Découvrez 5 conseils pratiques pour développer vos compétences en leadership.',
                'contenu': 'Le leadership est une compétence qui se développe. Voici 5 conseils pratiques pour renforcer votre capacité à diriger et inspirer votre équipe.',
                'tags': 'leadership, conseils, développement, compétences',
            },
            {
                'titre': 'Témoignage : Comment j\'ai Créé Mon Entreprise',
                'categorie': 'Témoignages',
                'description_courte': 'Le témoignage inspirant d\'une entrepreneure qui a réussi à créer son entreprise.',
                'contenu': 'Découvrez le parcours inspirant d\'une entrepreneure qui a surmonté les obstacles pour créer son entreprise et réaliser ses rêves.',
                'tags': 'témoignage, entrepreneuriat, succès, inspiration',
            },
            {
                'titre': 'L\'Importance de la Formation Continue',
                'categorie': 'Formations',
                'description_courte': 'Pourquoi la formation continue est essentielle pour votre développement professionnel.',
                'contenu': 'Dans un monde en constante évolution, la formation continue est devenue essentielle. Découvrez pourquoi et comment continuer à apprendre tout au long de votre carrière.',
                'tags': 'formation, développement, carrière, apprentissage',
            },
        ]
        
        for article_data in articles_data:
            article, created = Article.objects.get_or_create(
                titre=article_data['titre'],
                defaults={
                    'auteur': user,
                    'categorie': categories.get(article_data['categorie']),
                    'description_courte': article_data['description_courte'],
                    'contenu': article_data['contenu'],
                    'tags': article_data['tags'],
                    'statut': 'publie',
                    'date_publication': timezone.now() - timedelta(days=random.randint(1, 30)),
                }
            )
            if created:
                self.stdout.write(f'  + Article cree: {article.titre}')

    def create_inscriptions(self):
        """Créer des inscriptions de test"""
        self.stdout.write('Creation des inscriptions de test...')
        
        # Inscriptions aux événements
        users = User.objects.filter(username__startswith='testuser')[:2]
        evenements = Evenement.objects.filter(publie=True)[:2]
        
        for user in users:
            for evenement in evenements:
                inscription, created = Inscription.objects.get_or_create(
                    utilisateur=user,
                    evenement=evenement,
                    defaults={
                        'statut': 'confirme' if random.choice([True, False]) else 'en_attente',
                    }
                )
                if created:
                    self.stdout.write(f'  + Inscription evenement: {user.username} -> {evenement.titre}')
        
        # Inscriptions aux formations
        formations = Formation.objects.filter(publie=True)[:2]
        for user in users:
            for formation in formations:
                inscription, created = InscriptionFormation.objects.get_or_create(
                    utilisateur=user,
                    formation=formation,
                    defaults={
                        'statut': 'confirme' if random.choice([True, False]) else 'en_attente',
                    }
                )
                if created:
                    self.stdout.write(f'  + Inscription formation: {user.username} -> {formation.titre}')
                    
                    # Créer un certificat si la formation en délivre un et que l'inscription est confirmée
                    if formation.certificat and inscription.statut == 'confirme':
                        Certificat.objects.get_or_create(
                            inscription=inscription,
                            defaults={'verifie': True}
                        )
                        self.stdout.write(f'  + Certificat cree pour: {user.username} -> {formation.titre}')

