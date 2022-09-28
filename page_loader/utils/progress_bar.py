from progress.bar import IncrementalBar


def get_progress_bar():
    return IncrementalBar(bar_prefix='Downloading: |',
                          suffix='%(percent).1f%% - (eta: %(eta)s)',
                          )
