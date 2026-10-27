from pathlib import Path
from unittest.mock import patch

from automation.agent import choose_topic, main


def test_topic_available():
    slug, topic = choose_topic()
    assert slug and topic


def test_dry_run_no_write(tmp_path, capsys):
    with patch.dict('os.environ', {'AI_AGENT_ENABLED': 'false'}):
        main()
    assert 'DRY RUN' in capsys.readouterr().out
