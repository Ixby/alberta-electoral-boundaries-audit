import re

backup_text = open("report_public_backup.md", encoding="utf-8").read()


def get_section(title, skip_header=True):
    title_regex = re.escape(title).replace(r"\ ", r"\s+").replace(r"\-", r".")
    pattern = r"^#{2,3}\s+" + title_regex + r".*?(?=^#{2,3}\s+|\Z)"
    match = re.search(pattern, backup_text, re.MULTILINE | re.DOTALL)
    if match:
        content = match.group(0).strip()
        if skip_header:
            lines = content.split("\n")[1:]
            return "\n".join(lines).strip()
        return content
    return ""


part1 = (
    "# Two Maps, Then None: Inside Alberta's 2026 Boundary Audit\n\n*A plain-language look at the 2025–26 Electoral Boundary Commission, the math behind the minority map, and what comes next.*\n\n## Part I: How the Commission Broke\n\n"
    + get_section("The short version")
)

part2 = "## Part II: The 250,000-Map Litmus Test {.new-page}\n\n" + get_section(
    "What the audit found across seven measures"
)

part3 = "## Part III: Cracking, Packing, and Draining\n\n" + get_section(
    "Three things the minority map does differently {: .new-page }"
)

part4 = "## Part IV: The Impact on the Ground {.new-page}\n\n" + get_section(
    "Lane 2 — the structural pattern"
)

part5 = '## Part V: How "Clean Gerrymanders" Work {.new-page}\n\n' + get_section(
    "The 50/50 test: surgical fortification vs. blunt force"
)

part6 = "## Part VI: What Happens in November\n\n" + get_section("Verdict {.new-page}")

full_text = "\n\n---\n\n".join([part1, part2, part3, part4, part5, part6])

words = len(full_text.split())
print(f"Constructed text word count: {words}")

with open("report_public.md", "w", encoding="utf-8") as f:
    f.write(full_text)
