from lexical_parser import Token, Types
from typing import Self

class Node_Prog:
    def __init__(self, type = None, expr = None) -> None:
        self.expr = expr
        self.type = type
    
    def get_type(self):
        return self.type
    
    def set_type(self, type):
        self.type = type
    
    def get_expression(self):
        return self.expr
    
    def set_expression(self, expr):
        self.expr = expr

class Leaf:
    def __init__(self, token: Token) -> None:
        self.token = token
    
    def get_value(self):
        return self.token.value
    
    def get_type(self):
        return self.token.type

class Leaf_Factor(Leaf):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

class Leaf_Operator(Leaf):
    def __init__(self, token: Token) -> None:
        super().__init__(token)
        
class Node_Expr:
    def __init__(self, left = None, right = None, operator = None) -> None:
        self.left: Self | Leaf = left
        self.right: Self | Leaf = right
        self.operator: Leaf = operator
    
    def get_left(self) -> Self | Leaf:
        return self.left

    def get_right(self) -> Self | Leaf:
        return self.right
        
    def get_operator(self) -> Leaf:
        return self.operator
        
    def set_right(self, right) -> None:
        self.right = right
    
    def set_left(self, left) -> None:
        self.left = left
    
    def set_operator(self, operator) -> None:
        self.operator = operator
        
class Node_Term(Node_Expr):
    def __init__(self, left=None, right=None, operator=None) -> None:
        super().__init__(left, right, operator)
        
class Token_Parse:
    def __init__(self, tokens: list[Token]) -> None:
        self.types = Types()
        self.index = -1
        self.tokens = tokens
        self.current_token = None
        self.__advance()

    def __advance(self) -> None:
        self.index += 1
        if self.index == len(self.tokens):
            self.current_token = None
        else:
            self.current_token = self.tokens[self.index]

    def __parse_expr(self, head: Node_Prog) -> None:
        if not head.get_type():
            head.set_expression(Node_Expr())
            head.set_type(self.current_token.type)
        self.__advance()
        current_node: Node_Expr | Node_Term = head.get_expression()
        if self.current_token.type == self.types._OPARAN:
            self.__advance()
            while self.current_token and self.current_token.type not in self.types.get_key_types():
                if not current_node.get_left():
                    if self.current_token.type == self.types._INT:
                        current_node.set_left(Leaf_Factor(self.current_token))
                        self.__advance()
                    elif self.current_token.type == self.types._OPARAN:
                        current_node.set_left(Node_Expr())
                        self.__parse_expr(current_node.left())
                    elif self.current_token.type == self.types._CPARAN:
                        break
                elif not current_node.get_right():
                    if self.current_token.type == self.types._INT:
                        current_node.set_right(Leaf_Factor(self.current_token))
                        self.__advance()
                    elif self.current_token.type == self.types._OPARAN:
                        current_node.set_right(Node_Expr())
                        self.__parse_expr(current_node.right())
                    elif self.current_token.type == self.types._CPARAN:
                        break
            

    def parse(self) -> list[Node_Prog]:
        programs = [] 
        while self.current_token:
            head = Node_Prog()
            current_node = head
            if(self.current_token.type in self.types.get_key_types()):
                self.__parse_expr(current_node)
                programs.append(head)
            self.__advance()
        return programs
    
