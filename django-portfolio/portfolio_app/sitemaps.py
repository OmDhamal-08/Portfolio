"""sitemap.xml: every public page plus one entry per project case study."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from . import content_loader as content


class PageSitemap(Sitemap):
    changefreq = 'weekly'

    PRIORITIES = {'home': 1.0, 'projects': 0.9, 'about': 0.8, 'contact': 0.7}

    def items(self):
        return ['home', 'about', 'projects', 'skills', 'now', 'education', 'certifications', 'achievements', 'contact']

    def location(self, name):
        return reverse(name)

    def priority(self, name):
        return self.PRIORITIES.get(name, 0.6)


class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return content.list_projects()

    def location(self, project):
        return reverse('project_detail', args=[project.slug])

    def lastmod(self, project):
        return project.end_date or project.start_date


SITEMAPS = {'pages': PageSitemap, 'projects': ProjectSitemap}
