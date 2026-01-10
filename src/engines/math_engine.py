import random
from src.constants import CHAR_DAUGHTER

class MathEngine:
    def __init__(self, data_manager):
        self.dm = data_manager

    def generate_question(self, char_id):
        settings = self.dm.get_settings()
        weights = settings["math_weights"]

        # Determine active weights based on character
        if char_id == CHAR_DAUGHTER:
            active_weights = weights["daughter"]
            max_range = settings["math_ranges"]["daughter"]["max"]
        else:
            active_weights = weights["son_dad"]
            max_range = 100 # Default/ignored for advanced logic usually

        # Select operation based on weights
        ops = list(active_weights.keys())
        probs = list(active_weights.values())

        # Normalize weights if they don't sum to 100 (basic safety)
        total = sum(probs)
        if total == 0:
             # Fallback
             op = "add"
        else:
             op = random.choices(ops, weights=probs, k=1)[0]

        return self._create_problem(op, char_id, max_range)

    def _create_problem(self, op, char_id, max_range):
        if op == "add":
            # Basic addition
            a = random.randint(1, max_range)
            b = random.randint(1, max_range)
            return f"{a} + {b} = ?", str(a + b)

        elif op == "sub":
            # Basic subtraction (no negatives for now)
            a = random.randint(1, max_range)
            b = random.randint(1, a)
            return f"{a} - {b} = ?", str(a - b)

        elif op == "add_2d":
            a = random.randint(10, 99)
            b = random.randint(10, 99)
            return f"{a} + {b} = ?", str(a + b)

        elif op == "sub_2d":
            a = random.randint(10, 99)
            b = random.randint(10, a) # Ensure positive result
            return f"{a} - {b} = ?", str(a - b)

        elif op == "add_3d":
            a = random.randint(100, 999)
            b = random.randint(100, 999)
            return f"{a} + {b} = ?", str(a + b)

        elif op == "sub_3d":
            a = random.randint(100, 999)
            b = random.randint(100, a)
            return f"{a} - {b} = ?", str(a - b)

        elif op == "mult_2x1":
            a = random.randint(10, 99)
            b = random.randint(2, 9)
            return f"{a} x {b} = ?", str(a * b)

        elif op == "mult_2x2":
            a = random.randint(10, 99)
            b = random.randint(10, 99)
            return f"{a} x {b} = ?", str(a * b)

        elif op == "div":
            # Division with remainder or exact
            # We want simple division within 9x9 scope or slightly larger?
            # Prompt: "Division: Exact division, Division with Remainders (within 9x9 table scope)"
            # This implies divisor and quotient are likely within 9x9 scope?
            divisor = random.randint(2, 9)
            quotient = random.randint(1, 9)
            remainder = random.randint(0, divisor - 1)
            dividend = divisor * quotient + remainder

            if remainder == 0:
                return f"{dividend} ÷ {divisor} = ?", str(quotient)
            else:
                # Format: "Q...R" or just ask for quotient and remainder?
                # For simplicity in answering, maybe just Exact division for now unless input supports complex string
                # Or prompts says "Division with Remainders".
                # Let's format answer as "Q R" e.g. "3 1" for 3 remainder 1.
                return f"{dividend} ÷ {divisor} = ? (Q R)", f"{quotient} {remainder}"

        return "1 + 1 = ?", "2" # Fallback
