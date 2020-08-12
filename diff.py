import sympy
from sympy import *
class Expr:
    def __init__(self):

        pass

    def differentiate(self):

        return None

    def is_zero(self):

        return isinstance(self, ConstExpr) and self._const == 0



class ConstExpr(Expr):

    def __init__(self, const):

        self._const = const

    def differentiate(self):

        return ConstExpr(0)

    def pretty(self):

        return str(self._const)

    def simplify(self):

        return self

       

class AddExpr(Expr):

    def __init__(self, lhs_expr, rhs_expr):

        self._lhs_expr = lhs_expr

        self._rhs_expr = rhs_expr

    def differentiate(self):

        return AddExpr(

            self._lhs_expr.differentiate(),

            self._rhs_expr.differentiate()

        )


    def simplify(self):

        self._lhs_expr = self._lhs_expr.simplify()

        self._rhs_expr = self._rhs_expr.simplify()

        if self._lhs_expr.is_zero():

            return self._rhs_expr

        if self._rhs_expr.is_zero():

            return self._lhs_expr

        return self

    def pretty(self):

        return '(' + self._lhs_expr.pretty() + ') + (' +  self._rhs_expr.pretty() + ')'

class Subtract(Expr):

    def __init__(self, lhs_expr, rhs_expr):

        self._lhs_expr = lhs_expr

        self._rhs_expr = rhs_expr

    def Subtract(self):

        return SubtractExpr(

            self._lhs_expr.differentiate(),


            self._rhs_expr.differentiate()

        )


    def simplify(self):

        self._lhs_expr = self._lhs_expr.simplify()

        self._rhs_expr = self._rhs_expr.simplify()

        if self._lhs_expr.is_zero():

            return self._rhs_expr

        if self._rhs_expr.is_zero():

            return self._lhs_expr

        return self

    def pretty(self):

        return '(' + self._lhs_expr.pretty() + ')-(' +  self._rhs_expr.pretty() + ')'


class MulExpr(Expr):

    def __init__(self, lhs_expr, rhs_expr):

        self._lhs_expr = lhs_expr

        self._rhs_expr = rhs_expr

    def differentiate(self):

        return AddExpr(

            MulExpr(self._lhs_expr.differentiate(), self._rhs_expr),

            MulExpr(self._rhs_expr.differentiate(), self._lhs_expr)

        )

    def simplify(self):

        self._lhs_expr = self._lhs_expr.simplify()

        self._rhs_expr = self._rhs_expr.simplify()

        if self._lhs_expr.is_zero():

            return ConstExpr(0)

        if self._rhs_expr.is_zero():

            return ConstExpr(0)

        return self

    def pretty(self):

        return '(' + self._lhs_expr.pretty() + ') * (' +  self._rhs_expr.pretty() + ')'
    
class DivExpr(Expr):
    def __init__(self,numExpr,denoExpr):
        self.numExpr=numExpr
        self.denoExpr=denoExpr
    def differentiate(self):
        return(
            DivExpr((Subtract(MulExpr(self.denoExpr,self.numExpr.differentiate()),(MulExpr((self.numExpr),self.denoExpr.differentiate())))),MulExpr(self.denoExpr,self.denoExpr)))
    def pretty(self):
        return '(' + self.numExpr.pretty() + ') / (' + self.denoExpr.pretty() + ')' 
class PowerExpr(Expr):

    def __init__(self, power):

        self._power = power

       

    def differentiate(self):

        return MulExpr(ConstExpr(self._power), PowerExpr(self._power-1))

       

    def simplify(self):

        if self._power == 0:

            return ConstExpr(1)

        return self

       

    def pretty(self):

      return 'x^' + str(self._power)
'''class sqExpr(Expr):
    def __init__(self,baseExpr):
        self.baseExpr=baseExpr
    def differentiate(self):
        return '''
    

class comp(Expr):
    def __init__(self,outerExpr,innerExpr):
        self.innerExpr=innerExpr
        self.outerExpr=outerExpr
    def differentiate(self):
        return MulExpr(comp(self.outerExpr.differentiate(),self.innerExpr),self.innerExpr.differentiate())
    def pretty(self):
        return "(" + self.outerExpr.pretty() + "(" + self.innerExpr.pretty() + "))"
    def simplify(self):
        return self

class log(Expr):
    def __init__(self,expr):
        self.expr=expr
    def differentiate(self):
        return MulExpr(self.expr.differentiate(),DivExpr(MulExpr(ConstExpr(1),PowerExpr(0)),self.expr))
    def pretty(self):
        return 'log()'+self.expr.pretty()+')'
class exp(Expr):
    def __init__(self,expr):
        self.expr=expr
    def differentiate(self):
        return MulExpr(self.expr.differentiate(),exp(self.expr))
    def pretty(self):
        return 'exp('+self.expr.pretty()+')'
class sin(Expr):
    def __init__(self):
        pass
    def differentiate(self):
        return cos()
    def pretty(self):
        return "sin"
class cos(Expr):
    def __init__(self):
        pass
    def differentiate(self):
        return MulExpr(ConstExpr(-1),sin())
    def pretty(self):
        return "cos"
    def simplify(self):
        return self
'''class tan(Expr):
    def __init__(self):
        pass
    def differentiate(self):
        return MulExpr(sec(),sec())
    def pretty(self):
        return "tan"
class sec(Expr):
    def __init__(self):
        pass
    def differentiate(self):
        return MulExpr(sec(),tan())
    def pretty(self):
        return "sec"
    def simplify(self):
        pass
class cosec(Expr):
    def __init__(self):
        pass
    def differentiate(self):
        return MulExpr(ConstExpr(-1),MulExpr(cosec(),cot()))
    def pretty(self):
        return "cosec"
    def simplify(self):
        pass
class cot(Expr):
    def __init__(self):
        pass
    def differentiate(self):
        return MulExpr(ConstExpr(-1),MulExpr(cosec(),cosec()))
    def pretty(self):
        return "cot"
    def simplify(self):
        pass'''
def diff(expr):
    print(simplify(differentiate(expr).pretty()))
def differentiate(Expr):
    return Expr.differentiate()



