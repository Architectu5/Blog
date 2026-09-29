from django.test import TestCase
from django.urls import reverse

from .models import Post


class PostViewsTests(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title="Тест", content="Текст поста")

    def test_list_page_shows_post(self):
        response = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тест")

    def test_detail_page(self):
        response = self.client.get(reverse("post_detail", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)

    def test_detail_404_for_missing_post(self):
        response = self.client.get(reverse("post_detail", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_create_post(self):
        response = self.client.post(
            reverse("post_create"),
            {"title": "Новый", "content": "Содержимое"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title="Новый").exists())

    def test_delete_post(self):
        self.client.post(reverse("post_delete", args=[self.post.id]))
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())


class PostApiTests(TestCase):
    def test_api_list(self):
        Post.objects.create(title="API", content="Текст")
        response = self.client.get("/api/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)