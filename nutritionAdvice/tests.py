from django.test import TestCase, Client
from django.urls import reverse

class MealRecommendationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('meal_recommendation')

    def test_get_meal_recommendation_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meal_recommendation.html')
        self.assertContains(response, '<form')

    def test_post_meal_recommendation_view(self):
        data = {
            'calorie_goal': '500',
            'meal_type': 'breakfast'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meal_recommendation.html')
        self.assertIn('meal_recommendations', response.context)
        self.assertGreater(len(response.context['meal_recommendations']), 0)
