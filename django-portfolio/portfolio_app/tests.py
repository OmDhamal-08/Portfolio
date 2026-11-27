from django.test import SimpleTestCase as TestCase  # no database in this project
from django.conf import settings
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


class ResumeLinkTests(TestCase):
    def test_resume_buttons_link_straight_to_the_pdf(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'href="/static/resume.pdf" download="Om_Dhamal_Resume.pdf"')

    def test_old_download_url_redirects_to_the_pdf(self):
        response = self.client.get(reverse('download_resume'))
        self.assertRedirects(response, '/static/resume.pdf', status_code=301, fetch_redirect_response=False)


class ContactFormTests(TestCase):
    data = {'name': 'Test User', 'email': 'test@example.com', 'subject': 'Hello there',
            'message': 'This is a test message from the contact form.'}

    def setUp(self):
        from django.core.cache import cache
        cache.clear()  # reset the per-IP rate limit

    def test_message_is_emailed_to_me_with_a_copy_to_the_visitor(self):
        from django.core import mail

        response = self.client.post(reverse('contact'), self.data)
        self.assertRedirects(response, reverse('contact'))
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])
        self.assertEqual(mail.outbox[0].reply_to, ['test@example.com'])
        self.assertEqual(mail.outbox[1].to, ['test@example.com'])

    def test_failed_send_keeps_the_text_and_offers_a_mailto_fallback(self):
        from unittest import mock

        with mock.patch('portfolio_app.views.EmailMessage.send', side_effect=OSError('SMTP down')):
            response = self.client.post(reverse('contact'), self.data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "couldn't be sent")
        self.assertContains(response, 'This is a test message from the contact form.')
        self.assertContains(response, 'mailto:dhamalomm@gmail.com?subject=Hello%20there')

    def test_contact_page_offers_gmail_compose_and_mailto(self):
        response = self.client.get(reverse('contact'))
        self.assertContains(response, 'https://mail.google.com/mail/?view=cm&amp;fs=1&amp;to=dhamalomm@gmail.com')
        self.assertContains(response, 'mailto:dhamalomm@gmail.com')


class SeoAndPreviewTests(TestCase):
    def test_pages_have_link_preview_tags(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, '<meta property="og:image" content="http://testserver/static/images/og-card.png" />')
        self.assertContains(response, 'name="twitter:card" content="summary_large_image"')
        self.assertContains(response, '<link rel="canonical" href="http://testserver/" />')

    def test_project_preview_uses_project_summary(self):
        response = self.client.get(reverse('project_detail', args=['shopmind-ai']))
        self.assertContains(response, 'property="og:title" content="ShopMind AI - Agentic Commerce Assistant - Case Study"')


class ExperienceTests(TestCase):
    def test_experience_loads_newest_first(self):
        items = content.load_experience()
        self.assertTrue(items)
        self.assertEqual(items[0].company, 'EduSkills')
        self.assertEqual(items[0].employment_type_label, 'Internship')

    def test_home_and_about_show_experience(self):
        for name in ('home', 'about'):
            response = self.client.get(reverse(name))
            self.assertContains(response, 'AI &amp; Machine Learning Virtual Intern')
            self.assertContains(response, 'Oct 2025')


class CodingStatsTests(TestCase):
    def setUp(self):
        from django.core.cache import cache
        cache.clear()

    def test_stats_partial_renders_live_numbers_and_caches_them(self):
        from unittest import mock
        from . import coding_stats

        with mock.patch.object(coding_stats, 'FETCHERS', {
            'leetcode': lambda: {'solved': 300, 'easy': 200, 'medium': 95, 'hard': 5},
            'github': lambda: {'contributions': 250, 'repos': 24},
            'codeforces': lambda: {'rating': 900, 'max_rating': 910},
        }):
            response = self.client.get(reverse('coding_stats'))
        self.assertContains(response, '300')
        self.assertContains(response, '250')
        self.assertContains(response, 'max 910')
        self.assertIn('s-maxage=86400', response['Cache-Control'])
        # Second request is served from the cache, without calling the APIs
        with mock.patch.object(coding_stats, 'FETCHERS', {}):
            self.assertContains(self.client.get(reverse('coding_stats')), '300')

    def test_failed_service_falls_back_to_known_numbers(self):
        from unittest import mock
        from . import coding_stats

        def broken():
            raise OSError('LeetCode is down')

        with mock.patch.object(coding_stats, 'FETCHERS', {
            'leetcode': broken,
            'github': lambda: {'contributions': 250, 'repos': 24},
            'codeforces': lambda: {'rating': 900, 'max_rating': 910},
        }):
            stats = coding_stats.get_coding_stats()
        self.assertEqual(stats['leetcode'], coding_stats.FALLBACK['leetcode'])
        self.assertEqual(stats['github']['contributions'], 250)

    def test_home_page_loads_stats_lazily(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'hx-get="/coding-stats/"')


class SitemapRobotsAndStructuredDataTests(TestCase):
    def test_sitemap_lists_pages_and_projects(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<loc>http://testserver/</loc>')
        self.assertContains(response, '<loc>http://testserver/projects/shopmind-ai/</loc>')

    def test_robots_points_to_sitemap(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertContains(response, 'Sitemap: http://testserver/sitemap.xml')

    def test_home_has_person_structured_data(self):
        import json as _json
        import re

        html = self.client.get(reverse('home')).content.decode()
        block = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1)
        data = _json.loads(block)
        self.assertEqual(data[0]['@type'], 'Person')
        self.assertEqual(data[0]['name'], 'Om Dhamal')
        self.assertIn('https://github.com/OmDhamal-08', data[0]['sameAs'])
