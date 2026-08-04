"""
Deterministic emergency-symptom screening, independent of the LLM.

The LLM can be inconsistent about safety-critical calls, so any of these
keyword patterns force an "go to the ER now" banner regardless of what the
model says. This is a coarse net, not a diagnostic tool.
"""
import re

# Each entry: (regex pattern matched against lowercased text, reason shown to the user)
_RED_FLAG_PATTERNS = [
    (r"chest pain|shortness of breath|can'?t breathe|difficulty breathing", "possible heart / lung emergency"),
    (r"ألم في الصدر|ضيق في التنفس|صعوبة في التنفس|مش قادر اتنفس", "احتمال طوارئ في القلب أو الرئة"),

    (r"face droop|slurred speech|one side.*weak|sudden numbness|can'?t move (my )?(arm|leg|face)", "possible stroke"),
    (r"تعليق في الوش|ثقل في اللسان|تنميل مفاجئ|ضعف مفاجئ في (نص الجسم|اليد|الرجل)|صعوبة في الكلام", "احتمال جلطة دماغية"),

    (r"severe bleeding|won'?t stop bleeding|coughing up blood|vomiting blood|blood in (stool|urine)", "severe bleeding"),
    (r"نزيف شديد|النزيف مش بيقف|بصق دم|قيء دم|دم في (البراز|البول)", "نزيف شديد"),

    (r"suicidal|want to die|kill myself|hurt myself", "mental health emergency"),
    (r"عايز اموت|هقتل نفسي|فكرة الانتحار|هأذي نفسي", "أزمة نفسية طارئة"),

    (r"anaphyla|throat (is )?closing|swelling of (the )?(face|throat|tongue)|severe allergic", "possible anaphylaxis"),
    (r"تورم في (الوش|الحلق|اللسان)|حساسية شديدة", "احتمال صدمة تحسسية"),

    (r"severe abdominal pain|rigid (abdomen|stomach)|worst (headache|pain) of (my|his|her) life", "possible surgical emergency"),
    (r"ألم شديد جدا في البطن|بطن متيبس|أسوأ صداع في حياتي", "احتمال حالة جراحية طارئة"),

    (r"high fever.*(stiff neck|confusion)|stiff neck.*fever", "possible meningitis"),
    (r"حمى شديدة.*(تيبس في الرقبة|تشوش)|تيبس في الرقبة.*حمى", "احتمال التهاب سحائي"),

    (r"seizure|convulsion|passed out|lost consciousness|unconscious", "possible neurological emergency"),
    (r"تشنج|نوبة صرع|غاب عن الوعي|فقدان الوعي", "احتمال طارئة عصبية"),
]

_COMPILED = [(re.compile(p, re.IGNORECASE), reason) for p, reason in _RED_FLAG_PATTERNS]


def screen(text: str) -> list[str]:
    """Return a list of matched emergency reasons (empty if none)."""
    hits = []
    for pattern, reason in _COMPILED:
        if pattern.search(text):
            hits.append(reason)
    return hits
