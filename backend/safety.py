"""
Safety Module
Screens user messages for medical emergencies and high-risk situations
BEFORE they reach the LLM, returning safe, hard-coded guidance instead of
a generated answer. This is a critical guardrail for a production medical tool.
"""

import re
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


# Generic emergency-number guidance shown in every emergency response.
# The app serves multiple regions, so we list the common ones rather than assume.
_EMERGENCY_NUMBERS_EN = (
    "call your local emergency number immediately "
    "(for example: 911 in the US, 1122 or 115 in Pakistan, 112 across the EU/UK, 999 in the UK)"
)
_EMERGENCY_NUMBERS_UR = (
    "foran apne ilaqe ke emergency number par call karein "
    "(misaal ke taur par: Pakistan mein 1122 ya 115, US mein 911, EU/UK mein 112)"
)


def _emergency_response(advice_en: str, advice_ur: str, language: str) -> str:
    """Wrap condition-specific advice with a consistent emergency header/footer."""
    if language == 'ur':
        return (
            "⚠️ YE AIK EMERGENCY HO SAKTI HAI ⚠️\n\n"
            f"{advice_ur}\n\n"
            f"Bar-e-meharbani {_EMERGENCY_NUMBERS_UR}. "
            "Main aik AI tool hoon aur emergency medical care ki jagah nahi le sakta. "
            "Kisi qareebi shakhs ki madad lein aur waqt zaya na karein."
        )
    return (
        "⚠️ THIS MAY BE A MEDICAL EMERGENCY ⚠️\n\n"
        f"{advice_en}\n\n"
        f"Please {_EMERGENCY_NUMBERS_EN}. "
        "I am an AI tool and cannot replace emergency medical care. "
        "Do not delay — get help from someone nearby right now."
    )


def _self_harm_response(language: str) -> str:
    """Crisis response for self-harm / suicidal ideation. Highest priority."""
    if language == 'ur':
        return (
            "Mujhe aap ki fikr hai, aur main chahta hoon ke aap mehfooz rahein.\n\n"
            "Agar aap khud ko nuqsan pohnchane ka soch rahe hain, to bar-e-meharbani abhi kisi "
            "se baat karein — kisi bharose mand dost, ghar wale, ya kisi mental health helpline par. "
            f"{_EMERGENCY_NUMBERS_UR}.\n\n"
            "Aap akele nahi hain aur madad mojood hai. Pakistan mein aap Umang helpline "
            "(0311-7786264) par rabta kar sakte hain. Main aik AI tool hoon — bar-e-meharbani "
            "kisi insaan se zaroor baat karein jo abhi aap ki madad kar sake."
        )
    return (
        "I'm really concerned about your safety, and I want you to know you're not alone.\n\n"
        "If you're thinking about harming yourself, please reach out right now to someone you "
        "trust — a friend, a family member, or a mental health crisis line. In the US you can call "
        "or text 988 (Suicide & Crisis Lifeline). In the UK, call 116 123 (Samaritans). "
        f"Otherwise, {_EMERGENCY_NUMBERS_EN}.\n\n"
        "I'm only an AI tool and can't provide crisis care, but a trained person can help you "
        "right now. Please talk to someone."
    )


# Each rule: (compiled regex, handler). Order matters — first match wins,
# so self-harm is checked first as the most sensitive case.
def _compile(*phrases: str) -> "re.Pattern":
    # Match whole words/phrases, case-insensitive, tolerant of extra spaces.
    parts = [r"\b" + r"\s+".join(map(re.escape, p.split())) + r"\b" for p in phrases]
    return re.compile("|".join(parts), re.IGNORECASE)


_SELF_HARM = _compile(
    "kill myself", "killing myself", "end my life", "ending my life",
    "want to die", "suicide", "suicidal", "self harm", "self-harm",
    "harm myself", "hurt myself", "no reason to live", "overdose on purpose",
    "khudkushi", "apni jaan", "marna chahta", "marna chahti",
)

_CARDIAC = _compile(
    "chest pain", "chest pressure", "chest tightness", "crushing chest",
    "pain in my left arm", "heart attack", "seene mein dard",
)

_STROKE = _compile(
    "face drooping", "slurred speech", "can't speak", "cant speak",
    "sudden numbness", "one side of my body", "having a stroke", "stroke symptoms",
)

_BREATHING = _compile(
    "can't breathe", "cant breathe", "cannot breathe", "trouble breathing",
    "difficulty breathing", "struggling to breathe", "choking", "anaphylaxis",
    "throat closing", "saans nahi", "saans lene mein",
)

_BLEEDING = _compile(
    "severe bleeding", "won't stop bleeding", "wont stop bleeding",
    "bleeding heavily", "coughing up blood", "vomiting blood", "lots of blood",
)

_POISON = _compile(
    "overdose", "took too many pills", "poisoned", "poisoning",
    "swallowed", "drank bleach", "zeher",
)

_SEIZURE_UNCONSCIOUS = _compile(
    "having a seizure", "unconscious", "passed out", "not waking up",
    "not responding", "behosh",
)

# (rule, english advice, roman-urdu advice)
_EMERGENCY_RULES = [
    (
        _CARDIAC,
        "Chest pain can be a sign of a heart attack and needs urgent assessment. "
        "Sit down, stay calm, and if advised by emergency services and not allergic, "
        "chew an aspirin while you wait for help.",
        "Seene mein dard heart attack ki nishani ho sakti hai aur foran tawajju chahta hai. "
        "Baith jayein, pursukoon rahein, aur madad ka intezar karein.",
    ),
    (
        _STROKE,
        "These can be signs of a stroke. Acting fast is critical — note the time symptoms "
        "started, as it affects treatment.",
        "Ye stroke (falij) ki alamaat ho sakti hain. Jaldi amal karna bohat zaroori hai — "
        "yaad rakhein alamaat kab shuru hui thin.",
    ),
    (
        _BREATHING,
        "Difficulty breathing or a closing throat can be life-threatening, especially if it "
        "came on suddenly or after an allergen. If you have a prescribed epinephrine "
        "auto-injector (EpiPen), use it.",
        "Saans lene mein dushwari jaan-leva ho sakti hai, khaaskar agar achanak shuru hui ho. "
        "Agar aap ke paas EpiPen mojood hai to use karein.",
    ),
    (
        _BLEEDING,
        "Heavy bleeding or coughing/vomiting blood needs urgent care. Apply firm pressure to "
        "any external bleeding with a clean cloth while you get help.",
        "Zyada khoon behna foran ilaj chahta hai. Bahari khoon par saaf kapre se dabaao dalein "
        "aur madad hasil karein.",
    ),
    (
        _POISON,
        "A possible overdose or poisoning is an emergency. If you can, find the container or "
        "substance involved so responders know what was taken.",
        "Overdose ya zeher khana aik emergency hai. Agar mumkin ho to woh cheez ya dabba sath "
        "rakhein taake madadgaar jaan saken kya liya gaya.",
    ),
    (
        _SEIZURE_UNCONSCIOUS,
        "Someone who is unconscious, unresponsive, or having a seizure needs emergency help. "
        "If they are not breathing normally and you are trained, begin CPR.",
        "Behoshi ya doray ki soorat mein foran emergency madad chahiye. Agar woh saans theek se "
        "nahi le raha aur aap ko training hai to CPR shuru karein.",
    ),
]


def screen_message(message: str, language: str = 'en') -> Optional[Dict[str, Any]]:
    """
    Check a user message for emergency / high-risk content.

    Returns None if the message is safe to pass to the normal RAG pipeline.
    Otherwise returns a dict with a hard-coded safe 'response' and a 'safety_flag'
    describing why it was intercepted (useful for logging/audit).
    """
    if not message:
        return None

    # Self-harm is checked first and always takes priority.
    if _SELF_HARM.search(message):
        logger.warning("Safety guardrail triggered: self_harm")
        return {
            'response': _self_harm_response(language),
            'safety_flag': 'self_harm',
            'sources': [],
        }

    for rule, advice_en, advice_ur in _EMERGENCY_RULES:
        if rule.search(message):
            flag = rule.pattern[:30]
            logger.warning(f"Safety guardrail triggered: emergency ({flag}...)")
            return {
                'response': _emergency_response(advice_en, advice_ur, language),
                'safety_flag': 'emergency',
                'sources': [],
            }

    return None
