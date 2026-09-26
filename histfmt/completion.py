"""Shell completion scripts for histfmt's own options.

Generated as plain strings rather than shelling out to argcomplete or
similar, since the option list is small and stable enough that keeping it
in sync by hand is less trouble than a dependency.
"""

_BASH = """\
_histfmt() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="--format --json --no-dedupe --time-format --filter --regex --completion --help"

    case "$prev" in
        --format)
            COMPREPLY=( $(compgen -W "zsh-extended plain fish" -- "$cur") )
            return 0
            ;;
        --completion)
            COMPREPLY=( $(compgen -W "bash zsh fish" -- "$cur") )
            return 0
            ;;
        --time-format|--filter)
            return 0
            ;;
    esac

    if [[ "$cur" == -* ]]; then
        COMPREPLY=( $(compgen -W "$opts" -- "$cur") )
        return 0
    fi

    COMPREPLY=( $(compgen -f -- "$cur") )
    return 0
}
complete -F _histfmt histfmt
"""

_ZSH = """\
#compdef histfmt

_histfmt() {
    _arguments \\
        '--format[force a source format instead of auto-detecting it]:format:(zsh-extended plain fish)' \\
        '--json[emit a JSON array instead of the human-readable listing]' \\
        '--no-dedupe[keep consecutive duplicate commands instead of collapsing them]' \\
        '--time-format[strftime pattern for timestamps in the human-readable listing]:strftime pattern:' \\
        '--filter[only show commands containing PATTERN]:pattern:' \\
        '--regex[treat --filter PATTERN as a regular expression]' \\
        '--completion[print a shell completion script and exit]:shell:(bash zsh fish)' \\
        '--help[show the help message and exit]' \\
        '*:history file:_files'
}

_histfmt "$@"
"""

_FISH = """\
complete -c histfmt -l format -x -a "zsh-extended plain fish" -d "force a source format instead of auto-detecting it"
complete -c histfmt -l json -d "emit a JSON array instead of the human-readable listing"
complete -c histfmt -l no-dedupe -d "keep consecutive duplicate commands instead of collapsing them"
complete -c histfmt -l time-format -x -d "strftime pattern for timestamps in the human-readable listing"
complete -c histfmt -l filter -x -d "only show commands containing PATTERN"
complete -c histfmt -l regex -d "treat --filter's PATTERN as a regular expression"
complete -c histfmt -l completion -x -a "bash zsh fish" -d "print a shell completion script and exit"
complete -c histfmt -l help -d "show the help message and exit"
complete -c histfmt -F
"""

_SCRIPTS = {"bash": _BASH, "zsh": _ZSH, "fish": _FISH}


def get_completion(shell: str) -> str:
    """Return the completion script for `shell`.

    Raises ValueError for anything not in `_SCRIPTS`; the CLI only ever
    calls this with a value argparse already restricted to that set, so
    this is a safety net rather than user-facing validation.
    """
    try:
        return _SCRIPTS[shell]
    except KeyError:
        raise ValueError(f"no completion script for shell {shell!r}") from None
