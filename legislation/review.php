<?php
/**
 * One-click review endpoint for the ALIM legislation library.
 *
 * A reviewer opens a scenario page with their personal token in the URL:
 *     https://alim.my/legislation/doing/dj-club-night/?r=<token>
 * The page asks this script who they are, shows two buttons, and posts the
 * verdict back here. One click is the whole interaction.
 *
 * Nothing secret lives under the web root. The token map and the full record,
 * including anything a reviewer flags, sit in ../../private/. The only file
 * this writes into public space is data/reviews.json, which carries a name, a
 * page and a date so the pages can show who reviewed them. Tokens and notes
 * never go in there.
 */

declare(strict_types=1);

const PRIVATE_DIR = __DIR__ . '/../../private';
const PUBLIC_JSON = __DIR__ . '/data/reviews.json';
const MIN_SECONDS_BETWEEN = 2;

/* How a reviewer wants to be credited on the public page. Nobody is named
   until they have chosen, because a practising lawyer's name on a public
   statement of law is their professional exposure, not ours to spend. */
const CREDIT_MODES = ['name', 'role', 'none'];

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

function fail(string $msg, int $code = 400): never {
    http_response_code($code);
    echo json_encode(['ok' => false, 'error' => $msg]);
    exit;
}

$configPath = PRIVATE_DIR . '/reviewers.php';
if (!is_file($configPath)) {
    fail('review is not configured', 503);
}
/** @var array{reviewers: array<string, array>, pages: array<string,string>, admin_key: string} $CONFIG */
$CONFIG = require $configPath;

function store_path(): string { return PRIVATE_DIR . '/reviews.json'; }

function read_store(): array {
    $p = store_path();
    if (!is_file($p)) return [];
    $raw = file_get_contents($p);
    $data = json_decode($raw ?: '[]', true);
    return is_array($data) ? $data : [];
}

/** Write the private record, then the trimmed public one, both atomically. */
function write_store(array $store, array $config): void {
    $tmp = store_path() . '.tmp';
    file_put_contents($tmp, json_encode($store, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES), LOCK_EX);
    rename($tmp, store_path());

    // Public file is grouped by page, then by track. A plain-English check is
    // never allowed to read as a legal sign-off, so the two never merge.
    // Credit is honoured here: unchosen or declined means nothing is published,
    // though the record is kept privately either way.
    $prefs = $store['_credit'] ?? [];
    $public = [];
    foreach ($store as $key => $rec) {
        if ($key === '_credit') continue;
        if (($rec['verdict'] ?? '') !== 'clear') continue;
        [$page, $track] = array_pad(explode('|', $key, 2), 2, 'legal');
        $mode = $prefs[$rec['by']] ?? null;
        if ($mode === null || $mode === 'none') continue;
        $shown = $mode === 'role'
            ? ($track === 'legal' ? 'a practising lawyer on the ALIM board' : 'an ALIM director')
            : $rec['by'];
        $public[$page][$track] = ['by' => $shown, 'on' => substr($rec['at'], 0, 10)];
    }
    $tmp2 = PUBLIC_JSON . '.tmp';
    file_put_contents($tmp2, json_encode($public, JSON_UNESCAPED_SLASHES | JSON_FORCE_OBJECT), LOCK_EX);
    rename($tmp2, PUBLIC_JSON);
}

function reviewer_for(string $token, array $config): ?array {
    foreach ($config['reviewers'] as $tok => $r) {
        if (hash_equals((string)$tok, $token)) return $r;
    }
    return null;
}

$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';

/* ---- admin: who has done what -------------------------------------- */
if ($method === 'GET' && isset($_GET['admin'])) {
    if (!hash_equals($CONFIG['admin_key'], (string)$_GET['admin'])) fail('no', 403);
    $store = read_store();
    $out = [];
    foreach ($CONFIG['reviewers'] as $r) {
        $done = [];
        $outstanding = [];
        foreach ($r['pages'] as $pg) {
            $k = $pg . '|' . ($r['track'] ?? 'legal');
            if (isset($store[$k]) && $store[$k]['by'] === $r['name']) {
                $done[] = ['page' => $pg, 'verdict' => $store[$k]['verdict'],
                           'at' => $store[$k]['at'], 'note' => $store[$k]['note'] ?? ''];
            } else {
                $outstanding[] = $pg;
            }
        }
        $out[] = ['name' => $r['name'], 'bundle' => $r['bundle'],
                  'track' => $r['track'] ?? 'legal',
                  'credit' => ($store['_credit'][$r['name']] ?? 'not chosen yet'),
                  'done' => count($done), 'of' => count($r['pages']),
                  'outstanding' => $outstanding, 'records' => $done];
    }
    echo json_encode(['ok' => true, 'reviewers' => $out], JSON_PRETTY_PRINT);
    exit;
}

/* ---- the public attribution map, served through PHP -----------------
   The same data is written to data/reviews.json, but that file sits behind
   the host's CDN and was observed serving a stale copy for minutes after a
   write. Anything that has to be live is read from here instead, where
   Cache-Control: no-store is set on the response itself. */
if ($method === 'GET' && isset($_GET['state'])) {
    $store = read_store();
    $prefs = $store['_credit'] ?? [];
    $out = [];
    foreach ($store as $key => $rec) {
        if ($key === '_credit' || ($rec['verdict'] ?? '') !== 'clear') continue;
        [$page, $track] = array_pad(explode('|', $key, 2), 2, 'legal');
        $mode = $prefs[$rec['by']] ?? null;
        if ($mode === null || $mode === 'none') continue;
        $out[$page][$track] = [
            'by' => $mode === 'role'
                ? ($track === 'legal' ? 'a practising lawyer on the ALIM board' : 'an ALIM director')
                : $rec['by'],
            'on' => substr($rec['at'], 0, 10),
        ];
    }
    echo json_encode($out, JSON_FORCE_OBJECT);
    exit;
}

/* ---- who am I, so the page can greet by name ------------------------ */
if ($method === 'GET') {
    $token = (string)($_GET['whoami'] ?? '');
    if ($token === '') fail('missing token');
    $r = reviewer_for($token, $CONFIG);
    if (!$r) fail('not a valid review link', 403);
    $store = read_store();
    $track = $r['track'] ?? 'legal';
    $pages = [];
    foreach ($r['pages'] as $pg) {
        $k = $pg . '|' . $track;
        $done = isset($store[$k]) && $store[$k]['by'] === $r['name'];
        $pages[] = ['id' => $pg, 'title' => $CONFIG['pages'][$pg] ?? $pg, 'done' => $done,
                    'verdict' => $done ? $store[$k]['verdict'] : null];
    }
    echo json_encode(['ok' => true, 'name' => $r['name'], 'bundle' => $r['bundle'],
                      'track' => $track, 'bundle_name' => $r['bundle_name'] ?? '',
                      'credit' => ($store['_credit'][$r['name']] ?? null),
                      'pages' => $pages]);
    exit;
}

/* ---- record a verdict ----------------------------------------------- */
if ($method !== 'POST') fail('method not allowed', 405);

$body = json_decode(file_get_contents('php://input') ?: '[]', true);
if (!is_array($body)) fail('bad body');

$token   = (string)($body['token'] ?? '');
$page    = (string)($body['page'] ?? '');
$verdict = (string)($body['verdict'] ?? '');
$note    = trim((string)($body['note'] ?? ''));

$r = reviewer_for($token, $CONFIG);
if (!$r) fail('not a valid review link', 403);

/* setting how you are credited is not about any one page */
if ($verdict === 'credit') {
    $mode = (string)($body['credit'] ?? '');
    if (!in_array($mode, CREDIT_MODES, true)) fail('bad credit mode');
    $store = read_store();
    $store['_credit'][$r['name']] = $mode;
    write_store($store, $CONFIG);
    echo json_encode(['ok' => true, 'name' => $r['name'], 'credit' => $mode]);
    exit;
}

if (!isset($CONFIG['pages'][$page])) fail('unknown page');
if (!in_array($page, $r['pages'], true)) fail('that page is not in your bundle', 403);
if (!in_array($verdict, ['clear', 'flag', 'undo', 'credit'], true)) fail('bad verdict');
if ($verdict === 'flag' && $note === '') fail('say what is wrong');
if (mb_strlen($note) > 4000) fail('note too long');

$track = $r['track'] ?? 'legal';
$key   = $page . '|' . $track;

$store = read_store();
$existing = $store[$key] ?? null;
if ($existing && ($existing['by'] ?? '') !== $r['name']) {
    fail('someone else has already recorded this page', 409);
}
if ($existing && (time() - strtotime($existing['at'])) < MIN_SECONDS_BETWEEN) {
    fail('too fast', 429);
}

if ($verdict === 'undo') {
    unset($store[$key]);
} else {
    $store[$key] = [
        'by'      => $r['name'],
        'verdict' => $verdict,
        'note'    => $verdict === 'flag' ? $note : '',
        'at'      => gmdate('c'),
    ];
}
write_store($store, $CONFIG);

/* hand back the next unreviewed page so they never go back to WhatsApp */
$next = null;
foreach ($r['pages'] as $pg) {
    if (!isset($store[$pg . '|' . $track])) {
        $next = ['id' => $pg, 'title' => $CONFIG['pages'][$pg] ?? $pg]; break;
    }
}
$doneCount = 0;
foreach ($r['pages'] as $pg) if (isset($store[$pg . '|' . $track])) $doneCount++;

echo json_encode(['ok' => true, 'name' => $r['name'], 'track' => $track, 'verdict' => $verdict,
                  'done' => $doneCount, 'of' => count($r['pages']), 'next' => $next]);
