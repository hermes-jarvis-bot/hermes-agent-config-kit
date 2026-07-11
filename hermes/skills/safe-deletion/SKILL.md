---
name: safe-deletion
description: "Require explicit confirmation, scoped execution, and post-action verification for destructive operations."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/deletion-confirm-and-verify.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Safe Deletion

Source: `AnastasiyaW/claude-code-config/rules/deletion-confirm-and-verify.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# 🔴 УДАЛЕНИЕ: ЯВНОЕ ПОДТВЕРЖДЕНИЕ + ПЕРЕПРОВЕРКА, ЧТО РЕАЛЬНО СЛУЧИЛОСЬ.

Директива пользователя (2026-06-07):
> «любое удаление требует явного, понятного и однозначного подтверждения от меня. но также если
> подтверждение есть и что-то удалено — надо перепроверить, что действие удаления правда случилось.
> надо перепроверять при копировании, что скопировалось; если потом надо удалить локально — мы
> перепроверяем, что удалили локально.»

## Правило — перед удалением
- **ЛЮБОЕ удаление** (файл, папка, репо, ветка, контейнер, образ, том, облачный ресурс, запись/
  таблица БД, scheduled task, tunnel) требует **явного, понятного и однозначного подтверждения
  оператора** ДО выполнения. Никаких удалений «по предположению», «наверное не нужно», «выглядит
  мусором». Если нет уверенности — спросить с конкретным списком, что именно удаляем.
- Никаких широких/слепых удалений (`rm -rf` корней, `DROP`, `prune --volumes`, `branch -D`).

## Правило — после удаления (anti-fabrication)
- **Перепроверить, что объект РЕАЛЬНО исчез**: `Test-Path`/`ls` (файл/папка), `docker ps -a`/
  `docker images` (контейнер/образ), `git branch`/`ls-remote` (ветка), API GET → 404 (облако),
  `SELECT count(*)` (БД). Команда может вернуть успех, **ничего не удалив** (permissions, lock,
  неверный путь, no-op). Не считать удалённым, пока не подтверждено.

## Правило — копирование/перенос
- После **копирования** — перепроверить, что **скопировалось** (файл существует, count/size/хэш
  совпадают) **ДО** удаления источника. Перенос делать как «копировать → verify → потом удалить
  источник» (напр. `robocopy /MOVE` удаляет источник только после успешной копии).
- Если позже удаляем **локальный** источник — снова перепроверить, что удалили локально (и что
  копия на месте).

## Hermes adaptation — guard candidates, not active hooks
- `a reviewed guard candidate` (pre-action guard concept) — требует подтверждения для destructive intent.
- `a reviewed guard candidate` / `a reviewed guard candidate` — блок катастрофических удалений.
- `a reviewed guard candidate` — снапшот БД перед destructive SQL.
- `a reviewed guard candidate` (post-action verification concept) — проверяет, что destructive-операция реально завершилась.

Related upstream references, review before porting: AGENTS.md or project guidance «Anti-Fabrication» («Deletion = re-verification»),
`system-verification-independent.md`, `safety-hooks.md`.
