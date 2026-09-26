import unittest

from histfmt.completion import get_completion


class GetCompletionTests(unittest.TestCase):
    def test_bash_script_registers_the_completion_function(self):
        script = get_completion("bash")
        self.assertIn("complete -F _histfmt histfmt", script)

    def test_zsh_script_has_compdef_header(self):
        script = get_completion("zsh")
        self.assertTrue(script.startswith("#compdef histfmt"))

    def test_fish_script_completes_the_histfmt_command(self):
        script = get_completion("fish")
        self.assertIn("complete -c histfmt", script)

    def test_each_script_mentions_every_long_option(self):
        options = ["--format", "--json", "--no-dedupe", "--time-format", "--filter", "--regex"]
        for shell in ("bash", "zsh", "fish"):
            script = get_completion(shell)
            for option in options:
                self.assertIn(option, script, f"{option} missing from {shell} completion")

    def test_unknown_shell_raises(self):
        with self.assertRaises(ValueError):
            get_completion("powershell")


if __name__ == "__main__":
    unittest.main()
