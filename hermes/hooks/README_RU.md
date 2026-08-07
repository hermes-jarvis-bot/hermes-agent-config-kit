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

## Доступные хуки

### `destructive-command-guard.py`

Блокирует катастрофически разрушительные shell-команды, запущенные через тул `terminal`:
`rm -rf` на root/home/wildcards, `DROP`/`TRUNCATE` без `WHERE`, `kubectl delete --all`,
`docker system prune --volumes`, `mkfs`/`dd` на блочное устройство, fork bomb.

Для активации добавь это в свой собственный `~/.hermes/config.yaml`:

```yaml
hooks:
  pre_tool_call:
    - matcher: "terminal"
      command: "python3 ~/.hermes/hooks/config-kit/destructive-command-guard.py"
      timeout: 10
```

Затем подтверди на запросе согласия при первом использовании (или установи
`hooks_auto_accept: true` / `HERMES_ACCEPT_HOOKS=1`, если уже доверяешь). Проверь через:

```bash
hermes hooks list
hermes hooks test pre_tool_call --for-tool terminal
hermes hooks doctor
```

Обойти для одного вызова можно через `HERMES_ALLOW_DESTRUCTIVE=1` в сессии, или маркер
`# hermes-bypass: destructive` прямо в тексте команды (полезно, когда env-переменная не
видна субпроцессу хука).

Лог: `~/.hermes/logs/config-kit-safety.log` (JSONL, одна строка на каждое оценённое событие).

## Тестирование без касания живого профиля

`tests/test_destructive_command_guard.py` подаёт синтетический JSON прямо на stdin скрипта
и проверяет его stdout — тот же wire-формат, что использует Hermes, без какой-либо
зависимости от живой установки Hermes или `~/.hermes/config.yaml`:

```bash
python3 hermes/hooks/tests/test_destructive_command_guard.py
```

Для более глубокой верификации против реального dispatch-кода Hermes
(`agent.shell_hooks.run_once`) см. доказательства ревью, записанные в
`mappings/reviewed-hooks.yaml` — этот тест был прогнан против изолированного объекта
`ShellHookSpec`, который никогда не читает и не пишет `~/.hermes/config.yaml` или
allowlist shell-хуков.
