import os
import pkgutil
import importlib
import sys
from app.commands import CommandHandler, Command
from dotenv import load_dotenv
import logging
import logging.config

class App:
    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'TESTING')
        self.command_handler = CommandHandler()

    def configure_logging(self):
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging configured.")

    def load_environment_variables(self):
        settings = {key: value for key, value in os.environ.items()}
        logging.info("Environment variables loaded.")
        return settings

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        return self.settings.get(env_var, None)

    def load_plugins(self):
        plugins_package = 'app.plugins'
        plugins_path = plugins_package.replace('.', '/')
        if not os.path.exists(plugins_path):
            logging.warning(f"Plugins directory '{plugins_path}' not found.")
            return
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_path]):
            if is_pkg:
                try:
                    plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                    self.register_plugin_commands(plugin_module, plugin_name)
                except ImportError as e:
                    logging.error(f"Error importing plugin {plugin_name}: {e}")

    def register_plugin_commands(self, plugin_module, plugin_name):
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                # Command names are now explicitly set to the plugin's folder name
                self.command_handler.register_command(plugin_name, item())
                logging.info(f"Command '{plugin_name}' from plugin '{plugin_name}' registered.")

    def start(self):
        self.load_plugins()
        logging.info("Application started. Type 'exit' to exit.")
        try:
            while True:
                cmd_input = input(">>> ").strip()
                if cmd_input.lower() == 'exit':
                    logging.info("Application exit.")
                    sys.exit(0)  # Use sys.exit(0) for a clean exit, indicating success.
                try:
                    self.command_handler.execute_command(cmd_input)
                except KeyError:  # Assuming execute_command raises KeyError for unknown commands
                    logging.error(f"Unknown command: {cmd_input}")
                    sys.exit(1)  # Use a non-zero exit code to indicate failure or incorrect command.
        except KeyboardInterrupt:
            logging.info("Application interrupted and exiting gracefully.")
            sys.exit(0)  # Assuming a KeyboardInterrupt should also result in a clean exit.
        finally:
            logging.info("Application shutdown.")


if __name__ == "__main__":
    app = App()
    app.start()


"""
Calculator Module

The addition, subtraction, multiplication, and division of fundamental arithmetic operations are 
supported by this module's simple calculator implementation. For precise numerical calculations, 
it makes use of the Decimal class and saves each result for probable future use.

"""

from calculator.operations import add, subtract, divide, multiply
from calculator.calculation import Calculation
from calculator.calculations import calculations
from decimal import Decimal
from typing import Callable

class Calculator:
    """
    A class that encapsulates basic arithmetic operations.

    Methods:
        perform(a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]) -> Decimal:
            Performs the given operation on two Decimal numbers and logs the calculation.
        
        add(a: Decimal, b: Decimal) -> Decimal:
            Returns the sum of two Decimal numbers.
        
        subtract(a: Decimal, b: Decimal) -> Decimal:
            Returns the difference between two Decimal numbers.
        
        multiply(a: Decimal, b: Decimal) -> Decimal:
            Returns the product of two Decimal numbers.
        
        divide(a: Decimal, b: Decimal) -> Decimal:
            Returns the quotient of two Decimal numbers.
    """

    @staticmethod
    def perform(a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]) -> Decimal:
        """
        Perform a calculation with the specified operation and stores history.

        Args:
            a (Decimal): The first operand.
            b (Decimal): The second operand.
            operation (Callable[[Decimal, Decimal], Decimal]): The arithmetic operation to perform.

        Returns:
            Decimal: The result of the operation.
        """
        # Create a Calculation object and log it
        calculation = Calculation.create(a, b, operation)
        calculations.add_calculation(calculation)
        # Execute the operation and return the result
        return calculation.operate()
    
    @staticmethod
    def add(a: Decimal, b: Decimal) -> Decimal:
        """
        Add two Decimal numbers.

        Args:
            a (Decimal): The first operand.
            b (Decimal): The second operand.

        Returns:
            Decimal: The sum of a and b.
        """
        return Calculator.perform(a, b, add)
    
    @staticmethod
    def subtract(a: Decimal, b: Decimal) -> Decimal:
        """
        Subtract one Decimal number from another.

        Args:
            a (Decimal): The minuend.
            b (Decimal): The subtrahend.

        Returns:
            Decimal: The result of a - b.
        """
        return Calculator.perform(a, b, subtract)

    @staticmethod
    def multiply(a: Decimal, b: Decimal) -> Decimal:
        """
        Multiply two Decimal numbers.

        Args:
            a (Decimal): The first operand.
            b (Decimal): The second operand.

        Returns:
            Decimal: The product of a and b.
        """
        return Calculator.perform(a, b, multiply)
    
    @staticmethod
    def divide(a: Decimal, b: Decimal) -> Decimal:
        """
        Divide one Decimal number by another.

        Args:
            a (Decimal): The dividend.
            b (Decimal): The divisor.

        Returns:
            Decimal: The result of a / b.
        
        Raises:
            ZeroDivisionError: If b is zero.
        """
        return Calculator.perform(a, b, divide)

