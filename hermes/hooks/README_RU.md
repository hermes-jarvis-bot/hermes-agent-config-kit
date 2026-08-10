# Хуки hermes-agent-config-kit

Reviewed-hook lane (см. `SECURITY.md`). Это Hermes-native реимплементации выбранных
апстримных Claude-Code/Codex guard-хуков — никогда не copy-paste апстримного файла,
потому что I/O-контракт отличается (имена тулов, форма block-JSON и, критически:
**Hermes никогда не блокирует по exit-коду, только по JSON-решению на stdout**).

`scripts/install_hermes.py --apply` копирует файлы этой директории в
`<hermes-home>/hooks/config-kit/`. **Он ничего не регистрирует в `~/.hermes/config.yaml` и
не активирует ни один хук.** Подключение скопированного хука в свой профиль — осознанный,
ручной, выполняемый оператором шаг — этот адаптер никогда не авто-исполняет и не
авто-активирует исполняемый контент.

Три вида, по событию — не у каждого события Claude Code есть Hermes-эквивалент, который
реально доходит до модели, поэтому смотри, в какую корзину попадает конкретный хук, а не
предполагай по аналогии с апстримом:

- **`pre_tool_call`-гварды** (`destructive-command-guard.py`, `git-destructive-guard.py`,
  `self-harm-guard.py`, `command-injection-guard.py`) реально могут блокировать вызов — Hermes
  парсит их stdout JSON и не даёт выполниться тул-коллу.
- **`post_tool_call`-гварды** (`verify-deleted-guard.py`, `over-engineering-advisor.py`) —
  **только аудит-лог**. `post_tool_call` в Hermes — fire-and-forget observer-событие:
  `_emit_post_tool_call_hook()` в `model_tools.py` отбрасывает всё, что вернёт
  `invoke_hook()`, поэтому ничто, что печатает post_tool_call-хук, не попадает в контекст
  модели ни в текущем, ни в следующем ходе (проверено 2026-08-08 по живому исходнику; детали —
  в `mappings/reviewed-hooks.yaml`). Эти два хука вместо этого пишут durable-вердикт в общий
  safety-лог — полезно как аудит-след для оператора, но не живой фидбек агенту в моменте, в
  отличие от поведения апстрима в Claude Code. Пересмотреть, если будущая версия Hermes
  добавит путь инъекции контекста для `post_tool_call`.
- **`pre_llm_call`/`pre_verify`/`on_session_end`-хуки** (`session-handoff-check.py`,
  `session-handoff-reminder.py`, `docs-staleness-guard.py`, `kb-validate-gate.py`) —
  смешанная корзина, каждый проверен индивидуально, а не по аналогии: `pre_llm_call` (с
  фильтром `extra.is_first_turn`) реально инъектирует контекст в первое сообщение модели, как
  рабочий `pre_tool_call`-блок; `pre_verify` реально подталкивает живого агента, но только на
  ходах с правкой файлов, максимум 3 nudge *на сессию, общих для всех хуков, зарегистрированных
  на это событие* (`session-handoff-reminder.py`, `kb-validate-gate.py` и Stop-часть
  `transfer-contract-guard.py` все его используют — см. секцию `kb-validate-gate.py` про
  трейд-офф отсюда); `on_session_end` — только аудит-лог, как `post_tool_call`. См. секцию
  каждого хука ниже.
- **`transfer-contract-guard.py` покрывает все три корзины одновременно** — один хук,
  зарегистрированный на `pre_tool_call` (реальный блок), `post_tool_call` (только аудит-лог) и
  оба `pre_verify`/`on_session_end` (двойная регистрация). См. его собственную секцию ниже.

**Заметка про multi-session (добавлена 2026-08-10):** `session-handoff-check.py`,
`session-handoff-reminder.py` и `transfer-contract-guard.py` делят общий heartbeat-механизм
(`hermes_hook_common.touch_session_heartbeat()`/`session_is_live()`,
`.hermes/sessions/<session_id>/heartbeat`, TTL 30 минут, override
`HERMES_SESSION_HEARTBEAT_TTL`). Именно он позволяет `transfer-contract-guard.py` отличить
чужую, но всё ещё живую сессию от заброшенной, и именно поэтому
`session-handoff-check.py`/`session-handoff-reminder.py` теперь scoped свои маркеры на сессию
(`.hermes/sessions/<session_id>/{session-start,handoff-reminded}`), а не на проект — две
параллельные Hermes-сессии в одном проекте больше не топчут состояние друг друга. Портировано
из апстримного фикса конкретно для `transfer-contract-guard.py`; эквивалентный фикс для
остальных двух хуков — собственное добавление этого адаптера (апстрим эту пару пока не
исправил).

## Доступные хуки

### `destructive-command-guard.py`

Блокирует катастрофически разрушительные shell-команды, запущенные через тул `terminal`:
`rm -rf` на root/home/wildcards, `DROP`/`TRUNCATE` без `WHERE`, `kubectl delete --all`,
`docker system prune --volumes`, `mkfs`/`dd` на блочное устройство, fork bomb.

```yaml
hooks:
  pre_tool_call:
    - matcher: "terminal"
      command: "python3 ~/.hermes/hooks/config-kit/destructive-command-guard.py"
      timeout: 10
```

Обход: `HERMES_ALLOW_DESTRUCTIVE=1` или маркер `# hermes-bypass: destructive` в команде.

### `git-destructive-guard.py`

Блокирует разрушительные git-операции: `reset --hard`, `push --force`, `branch -D`
(регистро-зависимо — `-d` разрешён), `clean -fdx`, `checkout -- .`,
`filter-branch`/`filter-repo`, удаление main/master/production ref, интерактивный rebase
HEAD, агрессивная чистка reflog/gc.

```yaml
hooks:
  pre_tool_call:
    - matcher: "terminal"
      command: "python3 ~/.hermes/hooks/config-kit/git-destructive-guard.py"
      timeout: 10
```

Обход: `HERMES_ALLOW_GIT_DESTRUCTIVE=1` или маркер `# hermes-bypass: git-destructive`.

### `self-harm-guard.py`

Блокирует команды, которые могут отрезать агента от собственного хоста: правка/рестарт/kill
sshd, убийство собственного runtime-процесса (`hermes`/`hermes_cli`/`node`/`bun`/`python` через
`killall`/`pkill -f`), правила iptables/ufw, рвущие собственную связность, reboot без handoff.

```yaml
hooks:
  pre_tool_call:
    - matcher: "terminal"
      command: "python3 ~/.hermes/hooks/config-kit/self-harm-guard.py"
      timeout: 10
```

Обход: `HERMES_ALLOW_SELF_HARM=1` или маркер `# hermes-bypass: self-harm`.

### `command-injection-guard.py`

Ловит shell-substitution injection: текст, задуманный как данные, который выполняется как
команда через `$(...)`/backticks раньше, чем внешняя команда его увидит (например, `dropdb`,
протащенный в `gh issue create --body "$(...)"`). Тривиальные, без побочных эффектов подстановки
(`pwd`, `date`, `git rev-parse` и т.п.) проходят; всё с деструктивным глаголом — hard block;
всё промежуточное — advisory-блок до подтверждения.

```yaml
hooks:
  pre_tool_call:
    - matcher: "terminal"
      command: "python3 ~/.hermes/hooks/config-kit/command-injection-guard.py"
      timeout: 10
```

Обход: `HERMES_ALLOW_INJECTION=1` или маркер `# hermes-bypass: injection`.

### `verify-deleted-guard.py` (только аудит-лог — см. заметку выше)

После выполнения деструктивной команды (`rm`/`rmdir`, `docker rm`/`rmi`/`volume rm`/
`network rm`, `kubectl delete`, `curl -X DELETE`) проверяет, действительно ли цель исчезла, и
логирует `verified-deleted` / `still-present` / `could-not-verify`. "Exit-код 0" ≠ "вещь
исчезла".

```yaml
hooks:
  post_tool_call:
    - matcher: "terminal"
      command: "python3 ~/.hermes/hooks/config-kit/verify-deleted-guard.py"
      timeout: 15
```

Без обхода — он никогда не блокирует, только логирует.

### `over-engineering-advisor.py` (только аудит-лог — см. заметку выше)

После вызова `write_file` или `patch` логирует совет, если изменение большое (нетто-строк
больше настраиваемого порога) или трогает манифест зависимостей (`package.json`,
`requirements.txt` и т.п.) — механически усиливает quality-code / YAGNI-лестницу, никогда не
блокируя.

```yaml
hooks:
  post_tool_call:
    - matcher: "write_file|patch"
      command: "python3 ~/.hermes/hooks/config-kit/over-engineering-advisor.py"
      timeout: 15
```

Настройки: `HERMES_BLOAT_EDIT_LINES` (по умолчанию 150), `HERMES_BLOAT_NEWFILE_LINES`
(по умолчанию 300). Обход: `HERMES_ALLOW_BLOAT=1` или маркер `# hermes-bypass: bloat` в
изменённом контенте.

### `session-handoff-check.py`

На первом LLM-вызове новой сессии сканирует `.hermes/handoffs/` (проект) и
`~/.hermes/handoffs/` (глобально) на предмет свежих handoff'ов и инъектирует список в
контекст модели, чтобы она могла предложить продолжить. В отличие от двух `post_tool_call`
гвардов выше, здесь контекст реально доходит до модели — возврат `{"context": ...}` у
`pre_llm_call` добавляется в первое сообщение пользователя (проверено по живому исходнику, не
предположено).

```yaml
hooks:
  pre_llm_call:
    - command: "python3 ~/.hermes/hooks/config-kit/session-handoff-check.py"
      timeout: 10
```

Переопределение директории handoff'ов: `HERMES_HANDOFF_DIR` (по умолчанию
`.hermes/handoffs/` в проекте). Без обхода — никогда не блокирует, только инъектирует
контекст или молчит.

### `session-handoff-reminder.py` (двойная регистрация — см. заметку ниже)

Напоминает написать handoff, когда сессия идёт долго (`SESSION_MIN_MINUTES`, по умолчанию
15) без свежего handoff на диске (`HANDOFF_STALE_MINUTES`, по умолчанию 30). Регистрировать
на **оба** события — каждое закрывает пробел другого:

```yaml
hooks:
  pre_verify:
    - command: "python3 ~/.hermes/hooks/config-kit/session-handoff-reminder.py"
      timeout: 10
  on_session_end:
    - command: "python3 ~/.hermes/hooks/config-kit/session-handoff-reminder.py"
      timeout: 10
```

- `pre_verify` реально подталкивает живого агента написать handoff перед завершением хода,
  но Hermes проверяет его только когда агент правил файл *в этом самом ходе*, и не больше 3
  раз за сессию (бюджет общий с любым другим потребителем `pre_verify`).
- `on_session_end` стреляет на каждом ходе независимо от правок — широкий, надёжный
  fallback — но только аудит-лог (см. заметку в начале файла).

Оба используют одни и те же маркер-файлы `.hermes/.handoff-reminded`/`.hermes/.session-start`,
так что какое бы событие ни сработало первым в ходе, оно подавляет второе до конца сессии.
Переопределение директории handoff'ов — тот же `HERMES_HANDOFF_DIR`. Без обхода — никогда не
блокирует.

### `docs-staleness-guard.py`

На первом LLM-вызове сессии флагает, если `openwiki/` или `docs/layers/` отстали от `HEAD`
больше чем на `HERMES_DOCS_STALE_COMMITS` (по умолчанию 20) коммитов, или если `openwiki/`
существует, но ни `AGENTS.md`, ни `CLAUDE.md` на него не указывает. Git-based, cooldown 7 дней
между напоминаниями для одного проекта.

```yaml
hooks:
  pre_llm_call:
    - command: "python3 ~/.hermes/hooks/config-kit/docs-staleness-guard.py"
      timeout: 10
```

Дополнительные якоря: список repo-относительных путей в `.hermes/.docs-anchors` (по одному на
строку, `#` — комментарий). Отключить для проекта: тронуть `.hermes/.skip-docs-staleness`.
Несёт свой собственный `--self-test` (чистая git/filesystem-логика — запускается прямо, без
установки Hermes): `python3 hermes/hooks/docs-staleness-guard.py --self-test`.

### `kb-validate-gate.py` (двойная регистрация — см. заметку выше)

Блокирует/логирует, пока собственный `scripts/validate_kb.py` репозитория (см. шаблон
`kb-skeleton`) сообщает, что база знаний рассинхронизирована с кодом, или пока `[LONG-RUN]`-
проект (`feature_list.json` присутствует) не имеет вообще никакой agent-документации.

```yaml
hooks:
  pre_verify:
    - command: "python3 ~/.hermes/hooks/config-kit/kb-validate-gate.py"
      timeout: 30
  on_session_end:
    - command: "python3 ~/.hermes/hooks/config-kit/kb-validate-gate.py"
      timeout: 30
```

В отличие от `session-handoff-reminder.py`, этот хук готов блокировать на *каждом* подходящем
ходе, пока KB остаётся сломанной — он не подавляет себя после одного nudge. Значит, он сильнее
конкурирует за общий бюджет `pre_verify` (3 nudge/сессия): в редком случае, когда KB реально
сломана *и* сессия при этом долгая без свежего handoff, этот хук может выжрать весь бюджет и
оставить `session-handoff-reminder.py` без живого nudge до конца сессии (его запись в
audit-лог через `on_session_end` всё равно сработает — ничего не теряется совсем, просто может
не дойти живьём). Если хочешь ограничить этот хук одним nudge за сессию — добавь свою проверку
маркер-файла перед регистрацией, или зарегистрируй только `on_session_end`, пропустив
`pre_verify`.

Обход: `HERMES_SKIP_KB_GATE=1` или `.hermes/.skip-kb-gate`. Несёт свой `--self-test`:
`python3 hermes/hooks/kb-validate-gate.py --self-test`.

### `transfer-contract-guard.py` (покрывает все три корзины — см. заметку выше)

Требует durable JSON-контракт под `.hermes/transfers/<id>.json` для команд
clone/copy/move/sync (`git clone`, `robocopy`, `rclone`, `rsync`, `scp`, `sftp`, `xcopy`,
`cp`/`copy`/`Copy-Item`, `mv`/`move`/`Move-Item`) — см. форму в
`templates/transfer-contract.json`. Регистрируется на все три события:

```yaml
hooks:
  pre_tool_call:
    - matcher: "terminal"
      command: "python3 ~/.hermes/hooks/config-kit/transfer-contract-guard.py"
      timeout: 10
  post_tool_call:
    - matcher: "terminal"
      command: "python3 ~/.hermes/hooks/config-kit/transfer-contract-guard.py"
      timeout: 10
  pre_verify:
    - command: "python3 ~/.hermes/hooks/config-kit/transfer-contract-guard.py"
      timeout: 10
  on_session_end:
    - command: "python3 ~/.hermes/hooks/config-kit/transfer-contract-guard.py"
      timeout: 10
```

- `pre_verify`/`on_session_end` блокируют/логируют, пока хоть один контракт открыт
  (`planned`/`running`/`verification_pending`) или закрыт-но-невалиден — гейт против
  «осиротевшего» переноса. Это **третий** потребитель общего бюджета `pre_verify` (3
  nudge/сессия), вместе с `session-handoff-reminder.py` и `kb-validate-gate.py` — см. секцию
  `kb-validate-gate.py` выше про этот трейд-офф.

Распознаёт `.hermes/transfers/`, `.claude/transfers/`, `.agent/transfers/` и
`.codex/transfers/` (cross-harness: контракт, написанный другим harness в том же репо, всё
равно исполняется). Без обхода — этот хук блокирует только на реально отсутствующем или
невалидном контракте; напиши контракт вместо поиска лазейки.

## Активация любого хука

Добавь соответствующий блок выше в свой `~/.hermes/config.yaml`, затем подтверди на запросе
согласия при первом использовании (или установи `hooks_auto_accept: true` /
`HERMES_ACCEPT_HOOKS=1`, если уже доверяешь). Проверь через:

```bash
hermes hooks list
hermes hooks test pre_tool_call --for-tool terminal
hermes hooks doctor
```

Лог: `~/.hermes/logs/config-kit-safety.log` (JSONL, одна строка на каждое оценённое событие,
общий для всех хуков выше).

## Тестирование без касания живого профиля

У каждого хука есть stdlib-only тест в `tests/`, который подаёт синтетический JSON прямо на
stdin скрипта и проверяет его stdout/stderr — тот же wire-формат, что использует Hermes, без
какой-либо зависимости от живой установки Hermes или `~/.hermes/config.yaml`:

```bash
python3 hermes/hooks/tests/test_destructive_command_guard.py
python3 hermes/hooks/tests/test_git_destructive_guard.py
python3 hermes/hooks/tests/test_self_harm_guard.py
python3 hermes/hooks/tests/test_command_injection_guard.py
python3 hermes/hooks/tests/test_verify_deleted_guard.py
python3 hermes/hooks/tests/test_over_engineering_advisor.py
python3 hermes/hooks/tests/test_session_handoff_check.py
python3 hermes/hooks/tests/test_session_handoff_reminder.py
python3 hermes/hooks/tests/test_docs_staleness_guard.py
python3 hermes/hooks/tests/test_kb_validate_gate.py
python3 hermes/hooks/tests/test_transfer_contract_guard.py
```

Для более глубокой верификации против реального dispatch-кода Hermes
(`agent.shell_hooks.run_once`) см. `functional_test`-доказательства, записанные в
`mappings/reviewed-hooks.yaml` для каждого хука — эти тесты были прогнаны против изолированного
объекта `ShellHookSpec`, который никогда не читает и не пишет `~/.hermes/config.yaml` или
allowlist shell-хуков.
