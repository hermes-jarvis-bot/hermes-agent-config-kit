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

Два вида, по событию:

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
```

Для более глубокой верификации против реального dispatch-кода Hermes
(`agent.shell_hooks.run_once`) см. `functional_test`-доказательства, записанные в
`mappings/reviewed-hooks.yaml` для каждого хука — эти тесты были прогнаны против изолированного
объекта `ShellHookSpec`, который никогда не читает и не пишет `~/.hermes/config.yaml` или
allowlist shell-хуков.
