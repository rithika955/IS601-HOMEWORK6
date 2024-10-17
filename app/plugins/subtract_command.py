from decimal import Decimal
from app.commands import Command

class SubtractCommand(Command):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a - b
