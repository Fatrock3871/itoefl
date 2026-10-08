"""Testes do validador e da migração do banco de questões.

    python -m unittest bank/tools/test_bank.py

Só stdlib. Os testes do validador montam itens na memória; o teste da
migração roda migrate.py numa pasta temporária e confere que a segunda
rodada não muda nenhum byte.
"""

import copy
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

import validate  # noqa: E402


def mcq(**over):
    item = {
        "id": "test-mcq.1",
        "section": "reading",
        "task_type": "Read in Daily Life",
        "exam_format": True,
        "format": "mcq",
        "skill": None,
        "cefr_min": "B1",
        "cefr_max": "B2",
        "stimulus": None,
        "prompt": "What is the main purpose of the notice?",
        "text_format": "plain",
        "options": {"A": "one", "B": "two", "C": "three", "D": "four"},
        "answer": "B",
        "explanation": "O aviso diz isso. (A) inverte o sentido.",
        "hint": None,
        "trap_codes": [],
        "tags": [],
        "status": "rascunho",
        "source": {"kind": "migrado", "file": "app/drills_data.py", "ref": "x", "live_on_site": True,
                   "answer_letter": "origem", "build_map": None},
    }
    item.update(over)
    return item


class SchemaTests(unittest.TestCase):
    def setUp(self):
        self.schema = validate.load_schema()

    def test_valid_item_has_no_schema_errors(self):
        self.assertEqual(validate.check_schema(mcq(), self.schema), [])

    def test_missing_required_field_is_reported(self):
        it = mcq()
        del it["answer"]
        errs = validate.check_schema(it, self.schema)
        self.assertTrue(any("answer" in e for e in errs), errs)

    def test_bad_enum_is_reported(self):
        errs = validate.check_schema(mcq(section="math"), self.schema)
        self.assertTrue(any("section" in e for e in errs), errs)

    def test_bad_id_pattern_is_reported(self):
        errs = validate.check_schema(mcq(id="Bad Id"), self.schema)
        self.assertTrue(any("id" in e for e in errs), errs)

    def test_unknown_field_is_reported(self):
        errs = validate.check_schema(mcq(foo=1), self.schema)
        self.assertTrue(any("foo" in e for e in errs), errs)


class RuleTests(unittest.TestCase):
    def run_rules(self, items):
        errors, warnings, _ = validate.validate_items([("t.json", it) for it in items])
        return errors, warnings

    def test_valid_items_pass(self):
        errors, _ = self.run_rules([mcq(), mcq(id="test-mcq.2")])
        self.assertEqual(errors, [])

    def test_duplicate_ids_fail(self):
        errors, _ = self.run_rules([mcq(), mcq()])
        self.assertTrue(any("duplicado" in e for e in errors), errors)

    def test_answer_not_among_options_fails(self):
        errors, _ = self.run_rules([mcq(answer="E")])
        self.assertTrue(any("resposta" in e for e in errors), errors)

    def test_multi_select_answers_must_exist_and_match_count(self):
        it = mcq(format="multi_select", answer=["A", "E"], select_count=2)
        errors, _ = self.run_rules([it])
        self.assertTrue(any("resposta" in e for e in errors), errors)

    def test_task_type_must_belong_to_section(self):
        errors, _ = self.run_rules([mcq(section="listening")])
        self.assertTrue(any("task_type" in e for e in errors), errors)

    def test_cefr_min_cannot_exceed_max(self):
        errors, _ = self.run_rules([mcq(cefr_min="C1", cefr_max="B1")])
        self.assertTrue(any("cefr" in e for e in errors), errors)

    def test_fill_words_answers_must_match_gaps(self):
        it = mcq(task_type="Complete the Words", format="fill_words", options=None,
                 stimulus={"kind": "text", "format": "plain", "title": None, "audio_ref": None,
                           "content": "Each [[bee]] has a [[job]]."},
                 answer=["bee", "job", "extra"])
        errors, _ = self.run_rules([it])
        self.assertTrue(any("lacuna" in e for e in errors), errors)

    def test_build_sentence_answer_chunks_must_be_in_bank(self):
        it = mcq(section="writing", task_type="Build a Sentence", format="build_sentence",
                 prompt="{1} {2}?", options=["Can", "you"], answer=["Can", "she"])
        errors, _ = self.run_rules([it])
        self.assertTrue(any("resposta" in e for e in errors), errors)

    def test_explanation_citing_missing_letter_warns(self):
        it = mcq(options={"A": "x", "B": "y", "C": "z"}, explanation="(D) está errada.")
        errors, warnings = self.run_rules([it])
        self.assertEqual(errors, [])
        self.assertTrue(any("(D)" in w for w in warnings), warnings)


class MigrationTests(unittest.TestCase):
    def test_migration_is_idempotent_and_valid(self):
        import migrate
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            report1 = migrate.run(out)
            first = {p.name: p.read_bytes() for p in sorted(out.rglob("*.json"))}
            report2 = migrate.run(out)
            second = {p.name: p.read_bytes() for p in sorted(out.rglob("*.json"))}
            self.assertEqual(first, second)
            self.assertEqual(report1, report2)
            for src in report1:
                self.assertEqual(src["origem"], src["destino"], src)
            errors, _, _ = validate.validate_items(validate.load_items(out))
            self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
