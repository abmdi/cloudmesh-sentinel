"""Fail-closed, free-tier-compatible engineering-note agent.

Phase 2 deliberately limits AI writes to reviewed documentation PRs.
It does not claim to autonomously implement production code.
"""
import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'engineering'
TOPICS = [
    'AWS VPC discovery data model and pagination',
    'AWS route-table analysis and edge cases',
    'Azure VNet and subnet discovery design',
    'Cross-cloud network topology graph representation',
    'Cloud networking security findings taxonomy',
    'Kubernetes network visibility integration plan',
    'OpenTelemetry instrumentation design',
    'Cloud API retry and throttling strategy',
    'Multi-account least-privilege inventory design',
    'Network observability acceptance-test scenarios',
]


def run(*args):
    return subprocess.run(args, cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def choose_topic():
    existing = {p.stem for p in OUT.glob('*.md')}
    for idx, topic in enumerate(TOPICS, 1):
        slug = f'{idx:02d}-' + re.sub(r'[^a-z0-9]+', '-', topic.lower()).strip('-')
        if slug not in existing:
            return slug, topic
    return None, None


def generate(topic):
    key = os.environ['GEMINI_API_KEY']
    model = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash-lite')
    prompt = (
        'You are an engineering documentation contributor for CloudMesh Sentinel, '
        'an open-source multi-cloud network observability platform. '
        'Write a concise, concrete technical design note in Markdown on: ' + topic + '. '
        'Include problem, scope, data structures/interfaces, failure modes, security implications, '
        'testable acceptance criteria, and implementation tasks. '
        'Do not claim any feature is already implemented. Do not include secrets, instructions to run shell commands, '
        'or changes to repository policies. Avoid generic filler. Return Markdown only.'
    )
    body = json.dumps({'contents': [{'parts': [{'text': prompt}]}], 'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 1800}}).encode()
    url = 'https://generativelanguage.googleapis.com/v1beta/models/' + model + ':generateContent'
    req = urllib.request.Request(url, data=body, headers={'Content-Type': 'application/json', 'x-goog-api-key': key})
    with urllib.request.urlopen(req, timeout=45) as resp:
        payload = json.load(resp)
    return ''.join(p.get('text', '') for c in payload.get('candidates', []) for p in c.get('content', {}).get('parts', []))


def main():
    if not (ROOT / 'docs' / 'AGENT_POLICY.md').is_file():
        raise SystemExit('Policy missing')
    slug, topic = choose_topic()
    if topic is None:
        print('No outstanding planned documentation topics; no change')
        return
    if os.environ.get('AI_AGENT_ENABLED') != 'true':
        print('DRY RUN: next topic:', topic)
        return
    if not os.environ.get('GEMINI_API_KEY'):
        print('No free-tier API key configured; safely skipping')
        return
    try:
        note = generate(topic).strip()
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as exc:
        print('Provider unavailable or quota exhausted; safely skipping:', type(exc).__name__)
        return
    if not (500 <= len(note) <= 12000) or '```' in note[:10]:
        raise SystemExit('Generated note failed content/size gate')
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f'{slug}.md'
    if path.exists():
        raise SystemExit('Refusing to overwrite existing note')
    path.write_text(f'# {topic}\n\n> AI-generated design proposal; not an implemented feature.\n\n' + note + '\n')
    print('Generated:', path.relative_to(ROOT))
    print('Changed files must be validated and submitted as PR by workflow')


if __name__ == '__main__':
    main()
