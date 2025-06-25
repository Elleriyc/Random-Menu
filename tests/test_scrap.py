import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from bs4 import BeautifulSoup
import sys
import os

# Ajouter le répertoire parent au path pour importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.scrap import Plat, Entree, Dessert, entree, plat, dessert


class TestPlat:
    """Tests pour la classe Plat."""
    
    def test_plat_init(self):
        """Test l'initialisation d'un objet Plat."""
        plat_obj = Plat("Pasta Bolognaise", "/recette/pasta", "4.5/5", "125 avis")
        
        assert plat_obj.titre == "Pasta Bolognaise"
        assert plat_obj.lien == "/recette/pasta"
        assert plat_obj.note == "4.5/5"
        assert plat_obj.avis == "125 avis"
    
    def test_plat_init_plat(self):
        """Test la méthode init_plat."""
        plat_obj = Plat("Pasta Bolognaise", "/recette/pasta", "4.5/5", "125 avis")
        result = plat_obj.init_plat()
        
        expected = "Pasta Bolognaise - 4.5/5 - 125 avis"
        assert result == expected


class TestEntree:
    """Tests pour la classe Entree."""
    
    def test_entree_init(self):
        """Test l'initialisation d'un objet Entree."""
        entree_obj = Entree("Salade César", "/recette/salade", "4.2/5", "89 avis")
        
        assert entree_obj.titre == "Salade César"
        assert entree_obj.lien == "/recette/salade"
        assert entree_obj.note == "4.2/5"
        assert entree_obj.avis == "89 avis"
    
    def test_entree_init_entree(self):
        """Test la méthode init_entree."""
        entree_obj = Entree("Salade César", "/recette/salade", "4.2/5", "89 avis")
        result = entree_obj.init_entree()
        
        expected = "Salade César - 4.2/5 - 89 avis"
        assert result == expected


class TestDessert:
    """Tests pour la classe Dessert."""
    
    def test_dessert_init(self):
        """Test l'initialisation d'un objet Dessert."""
        dessert_obj = Dessert("Tiramisu", "/recette/tiramisu", "4.8/5", "203 avis")
        
        assert dessert_obj.titre == "Tiramisu"
        assert dessert_obj.lien == "/recette/tiramisu"
        assert dessert_obj.note == "4.8/5"
        assert dessert_obj.avis == "203 avis"
    
    def test_dessert_init_dessert(self):
        """Test la méthode init_dessert."""
        dessert_obj = Dessert("Tiramisu", "/recette/tiramisu", "4.8/5", "203 avis")
        result = dessert_obj.init_dessert()
        
        expected = "Tiramisu - 4.8/5 - 203 avis"
        assert result == expected


class TestEntreeFunction:
    """Tests pour la fonction entree()."""
    
    @patch('src.scrap.requests.get')
    def test_entree_success(self, mock_get):
        """Test la fonction entree avec une réponse réussie."""
        # Mock HTML response
        mock_html = """
        <html>
            <div class="mrtn-card-vertical-detailed">
                <div class="mrtn-card__title">
                    <a href="/recette/salade-cesar">Salade César</a>
                </div>
                <div class="mrtn-home-rating__rating">4.2/5</div>
                <div class="mrtn-home-rating__nbreviews">89 avis</div>
            </div>
            <div class="mrtn-card-vertical-detailed">
                <div class="mrtn-card__title">
                    <a href="/recette/soupe-tomate">Soupe de tomate</a>
                </div>
                <div class="mrtn-home-rating__rating">4.0/5</div>
                <div class="mrtn-home-rating__nbreviews">156 avis</div>
            </div>
        </html>
        """
        
        mock_response = Mock()
        mock_response.ok = True
        mock_response.text = mock_html
        mock_get.return_value = mock_response
        
        result = entree()
        
        assert len(result) == 2
        assert isinstance(result[0], Entree)
        assert result[0].titre == "Salade César"
        assert result[0].lien == "/recette/salade-cesar"
        assert result[0].note == "4.2/5"
        assert result[0].avis == "89 avis"
    
    @patch('src.scrap.requests.get')
    def test_entree_empty_response(self, mock_get):
        """Test la fonction entree avec une réponse vide."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response
        
        result = entree()
        
        assert result == []
    
    @patch('src.scrap.requests.get')
    def test_entree_request_failure(self, mock_get):
        """Test la fonction entree avec un échec de requête."""
        mock_response = Mock()
        mock_response.ok = False
        mock_get.return_value = mock_response
        
        result = entree()
        
        assert result == []
    
    @patch('src.scrap.requests.get')
    def test_entree_missing_elements(self, mock_get):
        """Test la fonction entree avec des éléments manquants."""
        mock_html = """
        <html>
            <div class="mrtn-card-vertical-detailed">
                <!-- Aucun élément de recette -->
            </div>
        </html>
        """
        
        mock_response = Mock()
        mock_response.ok = True
        mock_response.text = mock_html
        mock_get.return_value = mock_response
        
        result = entree()
        
        assert len(result) == 1
        assert result[0].titre == "Titre non trouvé"
        assert result[0].lien == "Lien non trouvé"
        assert result[0].note == "Note non trouvée"
        assert result[0].avis == "Avis non trouvés"


class TestPlatFunction:
    """Tests pour la fonction plat()."""
    
    @patch('src.scrap.requests.get')
    @patch('builtins.print')  # Mock print pour éviter l'output pendant les tests
    def test_plat_success(self, mock_print, mock_get):
        """Test la fonction plat avec une réponse réussie."""
        mock_html = """
        <html>
            <div class="mrtn-card-vertical-detailed">
                <div class="mrtn-card__title">
                    <a href="/recette/pasta-bolognaise">Pasta Bolognaise</a>
                </div>
                <div class="mrtn-home-rating__rating">4.5/5</div>
                <div class="mrtn-home-rating__nbreviews">125 avis</div>
            </div>
        </html>
        """
        
        mock_response = Mock()
        mock_response.ok = True
        mock_response.text = mock_html
        mock_get.return_value = mock_response
        
        result = plat()
        
        assert len(result) == 1
        assert isinstance(result[0], Plat)
        assert result[0].titre == "Pasta Bolognaise"
        assert result[0].lien == "/recette/pasta-bolognaise"
        assert result[0].note == "4.5/5"
        assert result[0].avis == "125 avis"
    
    @patch('src.scrap.requests.get')
    @patch('builtins.print')
    def test_plat_request_failure(self, mock_print, mock_get):
        """Test la fonction plat avec un échec de requête."""
        mock_response = Mock()
        mock_response.ok = False
        mock_get.return_value = mock_response
        
        result = plat()
        
        # La fonction retourne une liste vide en cas d'échec
        assert result == []


class TestDessertFunction:
    """Tests pour la fonction dessert()."""
    
    @patch('src.scrap.requests.get')
    def test_dessert_success(self, mock_get):
        """Test la fonction dessert avec une réponse réussie."""
        mock_html = """
        <html>
            <div class="mrtn-card-vertical-detailed">
                <div class="mrtn-card__title">
                    <a href="/recette/tiramisu">Tiramisu</a>
                </div>
                <div class="mrtn-home-rating__rating">4.8/5</div>
                <div class="mrtn-home-rating__nbreviews">203 avis</div>
            </div>
            <div class="mrtn-card-vertical-detailed">
                <div class="mrtn-card__title">
                    <a href="/recette/tarte-pommes">Tarte aux pommes</a>
                </div>
                <div class="mrtn-home-rating__rating">4.3/5</div>
                <div class="mrtn-home-rating__nbreviews">167 avis</div>
            </div>
        </html>
        """
        
        mock_response = Mock()
        mock_response.ok = True
        mock_response.text = mock_html
        mock_get.return_value = mock_response
        
        result = dessert()
        
        assert len(result) == 2
        assert isinstance(result[0], Dessert)
        assert result[0].titre == "Tiramisu"
        assert result[0].lien == "/recette/tiramisu"
        assert result[0].note == "4.8/5"
        assert result[0].avis == "203 avis"
    
    @patch('src.scrap.requests.get')
    def test_dessert_request_failure(self, mock_get):
        """Test la fonction dessert avec un échec de requête."""
        mock_response = Mock()
        mock_response.ok = False
        mock_get.return_value = mock_response
        
        result = dessert()
        
        assert result == []
    
    @patch('src.scrap.requests.get')
    def test_dessert_empty_response(self, mock_get):
        """Test la fonction dessert avec une réponse vide."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response
        
        result = dessert()
        
        assert result == []


class TestIntegration:
    """Tests d'intégration pour vérifier que les fonctions fonctionnent ensemble."""
    
    @patch('src.scrap.requests.get')
    def test_all_functions_return_correct_types(self, mock_get):
        """Test que toutes les fonctions retournent les bons types."""
        mock_html = """
        <html>
            <div class="mrtn-card-vertical-detailed">
                <div class="mrtn-card__title">
                    <a href="/recette/test">Test Recipe</a>
                </div>
                <div class="mrtn-home-rating__rating">4.0/5</div>
                <div class="mrtn-home-rating__nbreviews">100 avis</div>
            </div>
        </html>
        """
        
        mock_response = Mock()
        mock_response.ok = True
        mock_response.text = mock_html
        mock_get.return_value = mock_response
        
        with patch('builtins.print'):  # Mock print pour la fonction plat
            entrees = entree()
            plats = plat()
            desserts = dessert()
        
        # Vérifier les types de retour
        assert isinstance(entrees, list)
        assert isinstance(desserts, list)
        
        if entrees:
            assert all(isinstance(e, Entree) for e in entrees)
        if plats:
            assert all(isinstance(p, Plat) for p in plats)
        if desserts:
            assert all(isinstance(d, Dessert) for d in desserts)


if __name__ == "__main__":
    pytest.main([__file__])