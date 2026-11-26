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
        self.assertContains(response, 'ShopMind AI')

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
        self.assertContains(response, 'AWS Certified Cloud Practitioner')
        self.assertNotContains(response, 'Oracle')
        # Filter chips only list types that are actually used
        self.assertContains(response, 'Foundational Certification')
        self.assertNotContains(response, 'Professional Certification')

    def test_achievements_page_renders(self):
        response = self.client.get(reverse('achievements'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fusion 2025 National Level Hackathon')

    def test_education_page_renders(self):
        response = self.client.get(reverse('education'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'B.Tech in Computer Engineering')

    def test_skills_page_renders(self):
        response = self.client.get(reverse('skills'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python')

    def test_contact_page_renders(self):
        response = self.client.get(reverse('contact'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your Full Name')


class CaseStudyAndNowTests(TestCase):
    def test_projects_have_case_study_fields(self):
        project = content.get_project('portfolio-website')

        self.assertTrue(project.has_case_study())
        self.assertTrue(project.problem)
        self.assertTrue(all(item.challenge for item in project.challenges))

    def test_project_detail_shows_case_study_sections(self):
        response = self.client.get(reverse('project_detail', kwargs={'slug': 'portfolio-website'}))

        self.assertContains(response, 'The problem')
        self.assertContains(response, 'how I solved them')

    def test_invalid_challenge_entry_is_rejected(self):
        with self.assertRaises(content.ContentValidationError):
            content._challenges([{'fix': 'missing challenge text'}], 'demo')

    def test_now_content_loads_and_renders(self):
        now = content.load_now()

        self.assertIsNotNone(now)
        self.assertTrue(now.learning)
        response = self.client.get(reverse('now'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, now.learning[0].name)

    def test_home_shows_currently_learning(self):
        response = self.client.get(reverse('home'))

        self.assertContains(response, 'Currently')


class ProjectSearchTests(TestCase):
    def test_search_matches_title_description_and_tech(self):
        self.assertTrue(any(p.slug == 'expense-tracker' for p in content.list_projects(query='expense')))
        self.assertTrue(all('FastAPI' in p.technologies for p in content.list_projects(tech='fastapi')))
        self.assertEqual(content.list_projects(query='zzzz-no-such-project'), [])

    def test_full_page_request_returns_whole_page(self):
        response = self.client.get(reverse('projects'), {'q': 'sanskrit'})

        self.assertContains(response, '<html', html=False)
        self.assertContains(response, 'Sanskrit Character Recognition')
        self.assertNotContains(response, 'Expense Tracker</a>')

    def test_htmx_request_returns_only_results_partial(self):
        response = self.client.get(reverse('projects'), {'tech': 'Django'}, HTTP_HX_REQUEST='true')

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '<html', html=False)
        self.assertContains(response, 'Portfolio Website')
        self.assertIn('HX-Request', response['Vary'])

    def test_empty_search_shows_message(self):
        response = self.client.get(reverse('projects'), {'q': 'zzzz-no-such-project'}, HTTP_HX_REQUEST='true')

        self.assertContains(response, 'No projects match that search')


class ContentCacheTests(TestCase):
    def setUp(self):
        from django.core.cache import cache
        cache.clear()

    def test_content_files_are_cached(self):
        from unittest import mock

        content.load_projects()
        with mock.patch('pathlib.Path.read_text', side_effect=AssertionError('file was re-read')):
            # Second load must come from the cache, not the disk.
            self.assertTrue(content.load_projects())

    def test_cache_key_changes_when_file_changes(self):
        import os

        path = content._content_root() / 'now.json'
        content.load_now()
        stat = path.stat()
        try:
            os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000_000))
            from unittest import mock
            with mock.patch('pathlib.Path.read_text', wraps=path.read_text) as reader:
                content.load_now()
            self.assertTrue(reader.called)
        finally:
            os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns))


class ResumeDownloadTests(TestCase):
    def test_downloads_static_pdf(self):
        response = self.client.get(reverse('download_resume'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_database_error_falls_back_to_static_pdf(self):
        from unittest import mock
        from django.db import DatabaseError

        with mock.patch('portfolio_app.views.Resume.objects.filter', side_effect=DatabaseError('no such table')):
            response = self.client.get(reverse('download_resume'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
