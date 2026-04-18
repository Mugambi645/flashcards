from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from django.utils import timezone
from cards.models import Card, NUM_BOXES, BOXES
from cards.views import CardListView, CardCreateView, CardUpdateView

# Model Tests
class CardModelTest(TestCase):
    """Test suite for the Card model"""
    
    def setUp(self):
        """Create a sample card for testing"""
        self.card = Card.objects.create(
            question="What is Django?",
            answer="A Python web framework",
            box=1
        )
    
    def test_card_creation(self):
        """Test that a card is created correctly"""
        self.assertEqual(self.card.question, "What is Django?")
        self.assertEqual(self.card.answer, "A Python web framework")
        self.assertEqual(self.card.box, 1)
        self.assertIsNotNone(self.card.date_created)
    
    def test_string_representation(self):
        """Test that the string representation returns the question"""
        self.assertEqual(str(self.card), "What is Django?")
    
    def test_default_box_value(self):
        """Test that new cards default to box 1"""
        new_card = Card.objects.create(
            question="Test question",
            answer="Test answer"
        )
        self.assertEqual(new_card.box, 1)
    
    def test_box_choices(self):
        """Test that box field only accepts valid choices"""
        valid_boxes = [1, 2, 3, 4, 5]
        for box_num in valid_boxes:
            card = Card.objects.create(
                question=f"Question {box_num}",
                answer=f"Answer {box_num}",
                box=box_num
            )
            self.assertEqual(card.box, box_num)
    
    def test_question_max_length(self):
        """Test that question field respects max_length"""
        max_length = Card._meta.get_field('question').max_length
        self.assertEqual(max_length, 100)
    
    def test_answer_max_length(self):
        """Test that answer field respects max_length"""
        max_length = Card._meta.get_field('answer').max_length
        self.assertEqual(max_length, 100)
    
    def test_auto_now_add_date_created(self):
        """Test that date_created is automatically set on creation"""
        before_creation = timezone.now()
        card = Card.objects.create(
            question="Timing test",
            answer="Test answer"
        )
        after_creation = timezone.now()
        
        self.assertGreaterEqual(card.date_created, before_creation)
        self.assertLessEqual(card.date_created, after_creation)
    
    def test_box_range_constants(self):
        """Test that NUM_BOXES and BOXES constants are correct"""
        self.assertEqual(NUM_BOXES, 5)
        self.assertEqual(list(BOXES), [1, 2, 3, 4, 5])

# View Tests
class CardListViewTest(TestCase):
    """Test suite for CardListView"""
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')
        
        # Create test cards
        self.card1 = Card.objects.create(
            question="Question 1",
            answer="Answer 1",
            box=2
        )
        self.card2 = Card.objects.create(
            question="Question 2",
            answer="Answer 2",
            box=1
        )
        self.card3 = Card.objects.create(
            question="Question 3",
            answer="Answer 3",
            box=2
        )
    
    def test_view_url_accessible_by_name(self):
        """Test that the home view is accessible by its URL name"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        """Test that the view uses the card_list.html template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "cards/card_list.html")
    
    def test_view_displays_all_cards(self):
        """Test that the view displays all cards"""
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['card_list']), 3)
    
    def test_cards_ordered_correctly(self):
        """Test that cards are ordered by box first"""
        response = self.client.get(self.url)
        cards = response.context['card_list']
        self.assertEqual(cards[0].box, 1)
        self.assertEqual(cards[1].box, 2)
        self.assertEqual(cards[2].box, 2)
    
    def test_empty_card_list(self):
        """Test that the view handles empty card list gracefully"""
        Card.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['card_list']), 0)
        self.assertEqual(response.status_code, 200)

class CardCreateViewTest(TestCase):
    """Test suite for CardCreateView"""
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('card-create')
        self.valid_data = {
            'question': 'New Question',
            'answer': 'New Answer',
            'box': 3
        }
    
    def test_view_url_accessible(self):
        """Test that the create view is accessible"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        """Test that the view uses card_form.html template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "cards/card_form.html")
    
    def test_create_valid_card(self):
        """Test creating a new card with valid data"""
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check that card was created
        self.assertEqual(Card.objects.count(), 1)
        card = Card.objects.first()
        self.assertEqual(card.question, 'New Question')
        self.assertEqual(card.answer, 'New Answer')
        self.assertEqual(card.box, 3)
    
    def test_create_card_without_question(self):
        """Test that creating a card without question fails"""
        invalid_data = self.valid_data.copy()
        invalid_data['question'] = ''
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)  # Returns to form with errors
        self.assertEqual(Card.objects.count(), 0)
    
    def test_create_card_without_answer(self):
        """Test that creating a card without answer fails"""
        invalid_data = self.valid_data.copy()
        invalid_data['answer'] = ''
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Card.objects.count(), 0)
    
    def test_create_card_with_invalid_box(self):
        """Test that creating a card with invalid box number fails"""
        invalid_data = self.valid_data.copy()
        invalid_data['box'] = 10  # Box only goes up to 5
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Card.objects.count(), 0)
    
    def test_success_redirect_url(self):
        """Test that successful creation redirects to card-create"""
        response = self.client.post(self.url, self.valid_data)
        self.assertRedirects(response, reverse('card-create'))

class CardUpdateViewTest(TestCase):
    """Test suite for CardUpdateView"""
    
    def setUp(self):
        self.client = Client()
        self.card = Card.objects.create(
            question='Original Question',
            answer='Original Answer',
            box=1
        )
        self.url = reverse('card-update', args=[self.card.id])
        self.valid_data = {
            'question': 'Updated Question',
            'answer': 'Updated Answer',
            'box': 4
        }
    
    def test_view_url_accessible(self):
        """Test that the update view is accessible"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        """Test that the view uses card_form.html template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "cards/card_form.html")
    
    def test_update_valid_card(self):
        """Test updating a card with valid data"""
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Refresh card from database
        self.card.refresh_from_db()
        self.assertEqual(self.card.question, 'Updated Question')
        self.assertEqual(self.card.answer, 'Updated Answer')
        self.assertEqual(self.card.box, 4)
    
    def test_update_nonexistent_card(self):
        """Test updating a card that doesn't exist"""
        url = reverse('card-update', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_update_card_with_invalid_data(self):
        """Test updating with invalid data"""
        invalid_data = self.valid_data.copy()
        invalid_data['question'] = ''
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        
        # Card should remain unchanged
        self.card.refresh_from_db()
        self.assertEqual(self.card.question, 'Original Question')
    
    def test_success_redirect_url(self):
        """Test that successful update redirects to home"""
        response = self.client.post(self.url, self.valid_data)
        self.assertRedirects(response, reverse('home'))

# URL Tests
class UrlsTest(SimpleTestCase):
    """Test suite for URL patterns"""
    
    def test_home_url_resolves(self):
        """Test that home URL resolves to CardListView"""
        url = reverse('home')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CardListView)
    
    def test_card_create_url_resolves(self):
        """Test that card-create URL resolves to CardCreateView"""
        url = reverse('card-create')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CardCreateView)
    
    def test_card_update_url_resolves(self):
        """Test that card-update URL resolves to CardUpdateView"""
        url = reverse('card-update', args=[1])
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CardUpdateView)
    
    def test_home_url_pattern(self):
        """Test the exact URL pattern for home"""
        self.assertEqual(reverse('home'), '/')
    
    def test_card_create_url_pattern(self):
        """Test the exact URL pattern for card-create"""
        self.assertEqual(reverse('card-create'), '/new')
    
    def test_card_update_url_pattern(self):
        """Test the exact URL pattern for card-update"""
        self.assertEqual(reverse('card-update', args=[42]), '/edit/42')

# Integration Tests
class IntegrationTest(TestCase):
    """End-to-end integration tests for the flashcard app"""
    
    def setUp(self):
        self.client = Client()
    
    def test_full_card_lifecycle(self):
        """Test creating, viewing, and editing a card"""
        # 1. Create a card
        create_url = reverse('card-create')
        create_data = {
            'question': 'Integration Test Question',
            'answer': 'Integration Test Answer',
            'box': 2
        }
        response = self.client.post(create_url, create_data)
        self.assertEqual(response.status_code, 302)
        
        # 2. Verify card appears in list
        home_url = reverse('home')
        response = self.client.get(home_url)
        self.assertContains(response, 'Integration Test Question')
        self.assertContains(response, 'Integration Test Answer')
        
        # 3. Get the card ID
        card = Card.objects.get(question='Integration Test Question')
        
        # 4. Edit the card
        update_url = reverse('card-update', args=[card.id])
        update_data = {
            'question': 'Updated Integration Question',
            'answer': 'Updated Integration Answer',
            'box': 4
        }
        response = self.client.post(update_url, update_data)
        self.assertEqual(response.status_code, 302)
        
        # 5. Verify updated content appears
        response = self.client.get(home_url)
        self.assertContains(response, 'Updated Integration Question')
        self.assertContains(response, 'Updated Integration Answer')
        self.assertNotContains(response, 'Integration Test Question')
    
    def test_multiple_cards_display(self):
        """Test that multiple cards are displayed correctly"""
        # Create multiple cards
        cards_data = [
            ('Card A', 'Answer A', 1),
            ('Card B', 'Answer B', 2),
            ('Card C', 'Answer C', 3),
        ]
        
        for question, answer, box in cards_data:
            self.client.post(reverse('card-create'), {
                'question': question,
                'answer': answer,
                'box': box
            })
        
        # Check that all cards are displayed
        response = self.client.get(reverse('home'))
        for question, answer, _ in cards_data:
            self.assertContains(response, question)
            self.assertContains(response, answer)
        
        # Check total count
        self.assertEqual(Card.objects.count(), 3)
    
    def test_form_validation_errors(self):
        """Test that form validation errors are displayed correctly"""
        # Submit empty form
        response = self.client.post(reverse('card-create'), {})
        self.assertEqual(response.status_code, 200)
        
        # Should show error messages
        self.assertContains(response, 'This field is required')
    
    def test_navigation_between_pages(self):
        """Test navigation links work correctly"""
        # Start at home page
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Click create new card link
        response = self.client.get(reverse('card-create'))
        self.assertEqual(response.status_code, 200)
        
        # Create a card
        self.client.post(reverse('card-create'), {
            'question': 'Nav Test',
            'answer': 'Nav Answer',
            'box': 1
        })
        
        # Navigate back to home
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Nav Test')