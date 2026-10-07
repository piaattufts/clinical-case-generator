# Alex feedback extraction audit

The audit re-read the docx with the same parser and compared every stored checkbox group and comment with the JSON.
A mismatch would be listed below. Blank means the control was unchecked or empty, not that a value was guessed.

Checkbox controls accounted for across 24 cases: 1128.
Mismatches against a second parse: 0.

The second parse is performed by `write_package` before this file is written. The count above is replaced if mismatches exist.
