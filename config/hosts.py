from django_hosts import patterns, host


host_patterns = patterns(
    '',
    host('', 'config.urls.api', name='api'),
    host('admin', 'config.urls.admin', name='admin'),
)
