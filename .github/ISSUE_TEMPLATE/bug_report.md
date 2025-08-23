name: Bug report
description: Report a problem to help us improve
title: "[bug] "
labels: ["bug"]
body:
  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
      description: Also tell us what you expected to happen
      placeholder: Tell us what you see!
    validations:
      required: true
  - type: textarea
    id: repro
    attributes:
      label: Reproduction steps
      description: Minimal steps to reproduce
      placeholder: |
        1. Run '...'
        2. Click '...'
        3. See error
  - type: input
    id: version
    attributes:
      label: Version
      placeholder: 0.1.0
  - type: dropdown
    id: area
    attributes:
      label: Area
      options:
        - API
        - CLI
        - Tools
        - Dashboard
        - Docs
        - CI
