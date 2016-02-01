import ast
import operator as op

import servant.fields

from servant.exceptions import ActionError
from servant.exceptions import ServantException
from servant.service.actions import Action


class AddAction(Action):
    number1 = servant.fields.IntField(
            required=True,
    )
    number2 = servant.fields.IntField(
            required=True,
    )
    result = servant.fields.IntField(
            in_response=True,
    )

    def run(self, **kwargs):
        self.result = self.number1 + self.number2


class SubtractAction(AddAction):
    def run(self, **kwargs):
        self.result = self.number1 - self.number2


class BackwardSubtractAction(SubtractAction):
    def run(self, **kwargs):
        self.result = self.number2 - self.number1


class MultiplyAction(AddAction):
    def run(self, **kwargs):
        self.result = self.number1 * self.number2


class DivideAction(Action):
    numerator = servant.fields.DecimalField(
            required=True,
            in_response=True,
    )
    denominator = servant.fields.DecimalField(
            required=True,
            in_response=True,
    )
    quotient = servant.fields.DecimalField(
            in_response=True,
    )

    def run(self, **kwargs):
        if self.denominator == 0:
            raise ActionError('Cannot divide by zero')
        self.quotient = self.numerator / self.denominator


class CalculateAction(Action):
    expression = servant.fields.StringField(
            required=True,
    )
    result = servant.fields.IntField(
            in_response=True,
    )

    def __eval(self, node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            client = self.get_internal_client(do_begin_response=False)

            # <left> <operator> <right>
            left = self.__eval(node.left)
            operator = type(node.op)
            right = self.__eval(node.right)

            if operator == ast.Add:
                response = client.add(number1=left, number2=right)
                #print '%s + %s = %s' % (left, right, response.result)
                return response.result
            elif operator == ast.Sub:
                response = client.subtract(number1=left, number2=right)
                #print '%s - %s = %s' % (left, right, response.result)
                return response.result
            elif operator == ast.Mult:
                response = client.multiply(number1=left, number2=right)
                #print '%s * %s = %s' % (left, right, response.result)
                return response.result
            elif operator == ast.Div:
                response = client.divide(numerator=left, denominator=right)
                #print '%s / %s = %s' % (left, right, response.quotient)
                if not response.is_error():
                    return response.quotient
                else:
                    raise ActionError('Error multiplying')
        else:
            raise TypeError(node)

    def eval_expr(self, expr):
        return self.__eval(ast.parse(expr, mode='eval').body)

    def run(self, **kwargs):
        self.result = self.eval_expr(self.expression)

