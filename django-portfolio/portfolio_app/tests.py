from django.test import TestCase
from django.urls import reverse

from . import content_loader as content


class ContentLoaderTests(TestCase):
    def test_content_files_validate(self):
        self.assertEqual(content.validate_content(), [])

    def test_projects_load_from_files(self):
        projects = content.list_projects()

        self.assertGreaterEqual(len(projects), 1)
        self.assertTrue(any(project.slug == 'portfolio-website' for project in projects))

    def test_project_filtering_works_without_database_models(self):
        projects = content.list_projects(project_type='ml', status='completed')

        self.assertTrue(projects)
        self.assertTrue(all(project.project_type == 'ml' for project in projects))
        self.assertTrue(all(project.status == 'completed' for project in projects))

    def test_project_detail_lookup_uses_slug(self):
        project = content.get_project('portfolio-website')

        self.assertEqual(project.title, 'Portfolio Website')


class PortfolioPageTests(TestCase):
    def test_home_page_renders_file_backed_content(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Portfolio Website')

    def test_projects_page_renders_and_filters(self):
        response = self.client.get(reverse('projects'), {'type': 'ml', 'status': 'completed'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Heart Disease Prediction')

    def test_project_detail_page_renders(self):
        response = self.client.get(reverse('project_detail', kwargs={'slug': 'portfolio-website'}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Project Overview')

    def test_certifications_page_renders(self):
        response = self.client.get(reverse('certifications'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'OCI AI Foundations')

    def test_achievements_page_renders(self):
        response = self.client.get(reverse('achievements'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fusion 2025 National Level Hackathon')

    def test_education_page_renders(self):
        response = self.client.get(reverse('education'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bachelor of Technology in Computer Science')

    def test_skills_page_renders(self):
        response = self.client.get(reverse('skills'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python')

    def test_contact_page_renders(self):
        response = self.client.get(reverse('contact'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your Full Name')
